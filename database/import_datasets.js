const fs = require('fs');
const path = require('path');
const mysql = require('mysql2/promise');

function cleanUsername(name, fallback) {
  let cleaned = name
    .toLowerCase()
    .replace(/<u\+[0-9a-f]+>/gi, '')
    .replace(/[^a-z0-9_]/g, '_')
    .replace(/_+/g, '_')
    .replace(/^_+|_+$/g, '');
  if (!cleaned || cleaned.length < 3) {
    cleaned = fallback.toLowerCase().replace(/[^a-z0-9_]/g, '_');
  }
  return cleaned.substring(0, 30);
}

function formatFollowers(num) {
  const n = Number(num);
  if (n >= 1e9) return (n / 1e9).toFixed(1) + 'B';
  if (n >= 1e6) return (n / 1e6).toFixed(1) + 'M';
  if (n >= 1e3) return (n / 1e3).toFixed(1) + 'K';
  return n.toLocaleString();
}

async function main() {
  const connection = await mysql.createConnection({
    user: 'root',
    database: 'social_media_dbms',
    socketPath: '/home/hp/mysql_data/mysql.sock'
  });

  console.log('Connected to MariaDB.');

  // Drop SocialMediaTop100 table if exists
  await connection.query('DROP TABLE IF EXISTS SocialMediaTop100;');

  // Read SocialMediaTop100.csv and register creators into Users
  const localCsv = path.resolve(__dirname, 'SocialMediaTop100.csv');
  const parentCsv = path.resolve(__dirname, '../SocialMediaTop100.csv');
  const csvPath = fs.existsSync(localCsv) ? localCsv : parentCsv;
  if (fs.existsSync(csvPath)) {
    const csvContent = fs.readFileSync(csvPath, 'utf-8');
    const lines = csvContent.split('\n').filter(l => l.trim().length > 0);
    const defaultHash = '$2b$10$6f6yXSxfu1l6ravXYkqo2uRA1IHNdXuCKbmCiDHP.jsDoPAA97ngS'; // password123
    const seenUsernames = new Set();

    console.log(`Processing ${lines.length - 1} creator profiles from CSV to register as Users...`);

    for (let i = 1; i < lines.length; i++) {
      const parts = lines[i].match(/(".*?"|[^",\s]+)(?=\s*,|\s*$)/g) || lines[i].split(',');
      if (parts.length >= 5) {
        let rawName = parts[1].replace(/"/g, '').replace(/[^\x20-\x7E\u00A0-\uFFFF]/g, '').trim();
        const followers = parseInt(parts[2].replace(/[^0-9]/g, ''), 10) || 0;
        let platform = parts[4].replace(/"/g, '').replace(/[^\x20-\x7E]/g, '').trim();

        if (!rawName) continue;

        let baseUser = cleanUsername(rawName, `creator_${i}`);
        let username = baseUser;
        let counter = 1;
        while (seenUsernames.has(username)) {
          username = `${baseUser}_${counter}`.substring(0, 30);
          counter++;
        }
        seenUsernames.add(username);

        const email = `${username}@kinetic.social`;
        const bio = `${rawName} • Creator on ${platform} (${formatFollowers(followers)} followers)`;

        await connection.query(`
          INSERT INTO Users (username, email, password_hash, bio)
          VALUES (?, ?, ?, ?)
          ON DUPLICATE KEY UPDATE bio = VALUES(bio)
        `, [username, email, defaultHash, bio]);
      }
    }
  }

  // Ingest dataset posts
  const jsonPath = path.resolve(__dirname, 'user_posts_dataset.json');
  if (fs.existsSync(jsonPath)) {
    const [allUsers] = await connection.query('SELECT user_id, username FROM Users ORDER BY user_id ASC');
    const postsData = JSON.parse(fs.readFileSync(jsonPath, 'utf-8'));

    console.log(`Inserting ${postsData.length} posts from dataset onto registered users...`);

    for (let i = 0; i < postsData.length; i++) {
      const p = postsData[i];
      const user = allUsers[i % allUsers.length];

      const [res] = await connection.query(`
        INSERT INTO Posts (user_id, content, like_count, language, tone)
        VALUES (?, ?, ?, ?, ?)
      `, [user.user_id, p.text, p.engagement || 0, p.language || 'English', p.tone || 'General']);

      const postId = res.insertId;

      if (p.tags && Array.isArray(p.tags)) {
        for (const tag of p.tags) {
          const cleanTag = tag.trim().replace(/^#/, '');
          if (!cleanTag) continue;

          await connection.query('INSERT IGNORE INTO Tags (name) VALUES (?)', [cleanTag]);
          const [[tRow]] = await connection.query('SELECT tag_id FROM Tags WHERE name = ?', [cleanTag]);
          if (tRow) {
            await connection.query('INSERT IGNORE INTO PostTags (post_id, tag_id) VALUES (?, ?)', [postId, tRow.tag_id]);
          }
        }
      }
    }
  }

  const [[{ count: uCount }]] = await connection.query('SELECT COUNT(*) as count FROM Users');
  const [[{ count: pCount }]] = await connection.query('SELECT COUNT(*) as count FROM Posts');
  console.log(`Summary: ${uCount} Users, ${pCount} Posts.`);
  await connection.end();
}

main().catch(console.error);
