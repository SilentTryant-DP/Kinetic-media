const fs = require('fs');
const path = require('path');
const { createRequire } = require('module');

let mysql, dotenv;
try {
  const backendRequire = createRequire(path.join(__dirname, '../backend/package.json'));
  mysql = backendRequire('mysql2/promise');
  dotenv = backendRequire('dotenv');
} catch (e) {
  try {
    mysql = require(path.join(__dirname, '../backend/node_modules/mysql2/promise'));
    dotenv = require(path.join(__dirname, '../backend/node_modules/dotenv'));
  } catch (e2) {
    mysql = require('mysql2/promise');
    dotenv = require('dotenv');
  }
}

dotenv.config({ path: path.join(__dirname, '../backend/.env') });

const password = process.argv[2] !== undefined ? process.argv[2] : (process.env.DB_PASSWORD || '');
const host = process.env.DB_HOST || 'localhost';
const port = parseInt(process.env.DB_PORT || '3306', 10);
const user = process.env.DB_USER || 'root';
const databaseName = process.env.DB_NAME || 'social_media_dbms';

async function runSetup() {
  console.log(`Connecting to MySQL at ${host}:${port} as user '${user}'...`);

  let rootConn;
  try {
    rootConn = await mysql.createConnection({
      host,
      port,
      user,
      password,
      multipleStatements: true
    });
    console.log('✓ Successfully connected to MySQL server.');
  } catch (err) {
    console.error(`✗ Connection failed: ${err.message}`);
    process.exit(1);
  }

  try {
    console.log(`[1/5] Creating database '${databaseName}' if it doesn't exist...`);
    await rootConn.query(`CREATE DATABASE IF NOT EXISTS \`${databaseName}\` CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;`);
    await rootConn.end();

    const dbConn = await mysql.createConnection({
      host,
      port,
      user,
      password,
      database: databaseName,
      multipleStatements: true
    });

    console.log('[2/5] Creating schema tables (database/schema.sql)...');
    const schemaSql = fs.readFileSync(path.join(__dirname, 'schema.sql'), 'utf-8');
    await dbConn.query(schemaSql);
    console.log('✓ Schema tables created.');

    console.log('[3/5] Creating triggers, views, and procedures...');
    // Drop existing before creating to avoid ER_TRG_ALREADY_EXISTS / ER_SP_ALREADY_EXISTS
    await dbConn.query('DROP TRIGGER IF EXISTS trg_like_insert;');
    await dbConn.query('DROP TRIGGER IF EXISTS trg_like_delete;');
    await dbConn.query('DROP TRIGGER IF EXISTS trg_notify_on_like;');
    await dbConn.query('DROP PROCEDURE IF EXISTS get_mutual_followers;');

    // Trigger 1: sync like count on insert
    await dbConn.query(`
      CREATE TRIGGER trg_like_insert
      AFTER INSERT ON Likes
      FOR EACH ROW
      BEGIN
          UPDATE Posts SET like_count = like_count + 1
          WHERE post_id = NEW.post_id;
      END
    `);

    // Trigger 2: sync like count on delete
    await dbConn.query(`
      CREATE TRIGGER trg_like_delete
      AFTER DELETE ON Likes
      FOR EACH ROW
      BEGIN
          UPDATE Posts SET like_count = like_count - 1
          WHERE post_id = OLD.post_id;
      END
    `);

    // Trigger 3: notification on like
    await dbConn.query(`
      CREATE TRIGGER trg_notify_on_like
      AFTER INSERT ON Likes
      FOR EACH ROW
      BEGIN
          INSERT INTO Notifications (user_id, type, reference_id)
          SELECT p.user_id, 'like', NEW.post_id
          FROM Posts p
          WHERE p.post_id = NEW.post_id
            AND p.user_id <> NEW.user_id;
      END
    `);

    // View: user_feed
    await dbConn.query(`
      CREATE OR REPLACE VIEW user_feed AS
      SELECT f.follower_id AS viewer_id,
             p.post_id, p.user_id, p.content, p.media_url, p.like_count, p.language, p.tone, p.created_at,
             u.username AS author,
             u.username AS username
      FROM Follows f
      JOIN Posts p ON p.user_id = f.following_id
      JOIN Users u ON u.user_id = p.user_id
      WHERE p.is_deleted = FALSE;
    `);

    // Stored Procedure: get_mutual_followers
    await dbConn.query(`
      CREATE PROCEDURE get_mutual_followers(IN user_a INT, IN user_b INT)
      BEGIN
          SELECT u.user_id, u.username
          FROM Follows f1
          JOIN Follows f2 ON f1.follower_id = f2.follower_id
          JOIN Users u    ON u.user_id = f1.follower_id
          WHERE f1.following_id = user_a
            AND f2.following_id = user_b;
      END
    `);
    console.log('✓ Triggers, views, and procedures created.');

    console.log('[4/5] Creating performance indexes (database/indexes.sql)...');
    const indexStatements = [
      'CREATE INDEX idx_posts_user_created ON Posts(user_id, created_at);',
      'CREATE INDEX idx_follows_following ON Follows(following_id);',
      'CREATE INDEX idx_follows_follower ON Follows(follower_id);',
      'CREATE INDEX idx_likes_post ON Likes(post_id);',
      'CREATE INDEX idx_comments_post ON Comments(post_id);',
      'CREATE INDEX idx_notifications_user_read ON Notifications(user_id, is_read);'
    ];

    for (const stmt of indexStatements) {
      try {
        await dbConn.query(stmt);
      } catch (idxErr) {
        // Ignore duplicate index errors
        if (!idxErr.message.includes('Duplicate key name')) {
          console.warn(`Index warning: ${idxErr.message}`);
        }
      }
    }
    console.log('✓ Indexes verified.');

    console.log('[5/5] Seeding demo users, posts, and relationships (database/seed_data.sql)...');
    const seedSql = fs.readFileSync(path.join(__dirname, 'seed_data.sql'), 'utf-8');
    await dbConn.query(seedSql);
    console.log('✓ Seed data populated.');

    // Print summary counts
    const [[{ userCount }]] = await dbConn.query('SELECT COUNT(*) AS userCount FROM Users;');
    const [[{ postCount }]] = await dbConn.query('SELECT COUNT(*) AS postCount FROM Posts;');
    const [[{ followCount }]] = await dbConn.query('SELECT COUNT(*) AS followCount FROM Follows;');
    console.log('\n======================================================');
    console.log('  Database setup completed successfully!');
    console.log(`  Users: ${userCount} | Posts: ${postCount} | Follows: ${followCount}`);
    console.log('======================================================');

    // Update backend/.env DB_PASSWORD if it changed
    const envPath = path.join(__dirname, '../backend/.env');
    if (fs.existsSync(envPath)) {
      let envContent = fs.readFileSync(envPath, 'utf-8');
      envContent = envContent.replace(/^DB_PASSWORD=.*$/m, `DB_PASSWORD="${password}"`);
      fs.writeFileSync(envPath, envContent, 'utf-8');
      console.log('✓ Updated backend/.env with verified DB_PASSWORD.');
    }

    await dbConn.end();
  } catch (err) {
    console.error('Setup error:', err);
    process.exit(1);
  }
}

runSetup();
