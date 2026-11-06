const express = require('express');
const cors = require('cors');
const bcrypt = require('bcrypt');
const pool = require('./db');
require('dotenv').config();

const app = express();
app.use(cors());
app.use(express.json());

// Dummy authentication middleware for demonstration
// In a real application, you would use JWT or sessions.
// Here we expect the user ID to be passed in the headers for simplicity.
const authenticate = (req, res, next) => {
    const userId = req.headers['x-user-id'];
    if (!userId) {
        return res.status(401).json({ error: 'Unauthorized: Missing x-user-id header' });
    }
    req.user = { id: parseInt(userId, 10) };
    next();
};

// 0. GET /
app.get('/', (req, res) => {
    res.json({
        message: 'Welcome to the Social Media DBMS Backend API!',
        status: 'running',
        endpoints: ['/register', '/login', '/posts', '/feed', '/notifications']
    });
});

// 1. POST /register
app.post('/register', async (req, res) => {
    const { username, email, password, bio } = req.body;
    try {
        const hashedPassword = await bcrypt.hash(password, 10);
        const [result] = await pool.query(
            'INSERT INTO Users (username, email, password_hash, bio) VALUES (?, ?, ?, ?)',
            [username, email, hashedPassword, bio]
        );
        res.status(201).json({ message: 'User registered successfully', userId: result.insertId });
    } catch (err) {
        res.status(400).json({ error: err.message });
    }
});

// 2. POST /login
app.post('/login', async (req, res) => {
    const { email, password } = req.body;
    try {
        const [rows] = await pool.query('SELECT * FROM Users WHERE email = ? OR username = ?', [email, email]);
        if (rows.length === 0) return res.status(401).json({ error: 'Invalid credentials' });
        
        const user = rows[0];
        const match = await bcrypt.compare(password, user.password_hash);
        if (!match) return res.status(401).json({ error: 'Invalid credentials' });
        
        res.json({ message: 'Login successful', userId: user.user_id, token: 'dummy-token' });
    } catch (err) {
        res.status(500).json({ error: err.message });
    }
});

// 3. POST /posts
app.post('/posts', authenticate, async (req, res) => {
    const { content, media_url, language = 'English', tone = 'General', tags = [] } = req.body;
    try {
        const [result] = await pool.query(
            'INSERT INTO Posts (user_id, content, media_url, language, tone) VALUES (?, ?, ?, ?, ?)',
            [req.user.id, content, media_url, language, tone]
        );
        const postId = result.insertId;

        if (Array.isArray(tags) && tags.length > 0) {
            for (const tag of tags) {
                const trimmed = String(tag).trim();
                if (!trimmed) continue;
                await pool.query('INSERT IGNORE INTO Tags (name) VALUES (?)', [trimmed]);
                const [[tagRow]] = await pool.query('SELECT tag_id FROM Tags WHERE name = ?', [trimmed]);
                if (tagRow) {
                    await pool.query('INSERT IGNORE INTO PostTags (post_id, tag_id) VALUES (?, ?)', [postId, tagRow.tag_id]);
                }
            }
        }

        res.status(201).json({ message: 'Post created', postId });
    } catch (err) {
        res.status(400).json({ error: err.message });
    }
});

// 4. GET /feed
app.get('/feed', authenticate, async (req, res) => {
    try {
        let [rows] = await pool.query(
            `SELECT p.post_id, p.user_id, p.content, p.media_url, p.like_count, p.language, p.tone, p.created_at,
                    u.username AS author, u.username,
                    GROUP_CONCAT(DISTINCT t.name) AS tags
             FROM Follows f
             JOIN Posts p ON p.user_id = f.following_id
             JOIN Users u ON u.user_id = p.user_id
             LEFT JOIN PostTags pt ON pt.post_id = p.post_id
             LEFT JOIN Tags t ON t.tag_id = pt.tag_id
             WHERE f.follower_id = ? AND p.is_deleted = FALSE
             GROUP BY p.post_id
             ORDER BY p.created_at DESC LIMIT 50`,
            [req.user.id]
        );
        if (rows.length === 0) {
            [rows] = await pool.query(
                `SELECT p.post_id, p.user_id, p.content, p.media_url, p.like_count, p.language, p.tone, p.created_at, 
                        u.username AS author, u.username,
                        GROUP_CONCAT(DISTINCT t.name) AS tags
                 FROM Posts p
                 JOIN Users u ON u.user_id = p.user_id
                 LEFT JOIN PostTags pt ON pt.post_id = p.post_id
                 LEFT JOIN Tags t ON t.tag_id = pt.tag_id
                 WHERE p.is_deleted = FALSE
                 GROUP BY p.post_id
                 ORDER BY p.created_at DESC LIMIT 50`
            );
        }
        const formatted = rows.map(r => ({
            ...r,
            tags: r.tags ? r.tags.split(',') : []
        }));
        res.json(formatted);
    } catch (err) {
        res.status(500).json({ error: err.message });
    }
});


// 5. POST /posts/:id/like
app.post('/posts/:id/like', authenticate, async (req, res) => {
    const postId = req.params.id;
    try {
        await pool.query(
            'INSERT INTO Likes (user_id, post_id) VALUES (?, ?)',
            [req.user.id, postId]
        );
        res.json({ message: 'Post liked' });
    } catch (err) {
        if (err.code === 'ER_DUP_ENTRY') {
            return res.status(400).json({ error: 'Already liked' });
        }
        res.status(500).json({ error: err.message });
    }
});

// 6. DELETE /posts/:id/like
app.delete('/posts/:id/like', authenticate, async (req, res) => {
    const postId = req.params.id;
    try {
        await pool.query(
            'DELETE FROM Likes WHERE user_id = ? AND post_id = ?',
            [req.user.id, postId]
        );
        res.json({ message: 'Post unliked' });
    } catch (err) {
        res.status(500).json({ error: err.message });
    }
});

// 7. POST /users/:id/follow
app.post('/users/:id/follow', authenticate, async (req, res) => {
    const followingId = req.params.id;
    try {
        await pool.query(
            'INSERT INTO Follows (follower_id, following_id) VALUES (?, ?)',
            [req.user.id, followingId]
        );
        res.json({ message: 'User followed' });
    } catch (err) {
        if (err.code === 'ER_DUP_ENTRY') {
            return res.status(400).json({ error: 'Already following' });
        }
        res.status(500).json({ error: err.message });
    }
});

// 7b. DELETE /users/:id/follow (Unfollow)
app.delete('/users/:id/follow', authenticate, async (req, res) => {
    const followingId = req.params.id;
    try {
        await pool.query(
            'DELETE FROM Follows WHERE follower_id = ? AND following_id = ?',
            [req.user.id, followingId]
        );
        res.json({ message: 'User unfollowed' });
    } catch (err) {
        res.status(500).json({ error: err.message });
    }
});

// 8. GET /notifications
app.get('/notifications', authenticate, async (req, res) => {
    try {
        const [rows] = await pool.query(
            `SELECT n.notification_id, n.user_id, n.type, n.reference_id, n.is_read, n.created_at,
                    p.content AS post_snippet
             FROM Notifications n
             LEFT JOIN Posts p ON p.post_id = n.reference_id
             WHERE n.user_id = ?
             ORDER BY n.created_at DESC LIMIT 30`,
            [req.user.id]
        );
        res.json(rows);
    } catch (err) {
        res.status(500).json({ error: err.message });
    }
});

// 8b. PUT /notifications/mark-read
app.put('/notifications/mark-read', authenticate, async (req, res) => {
    try {
        await pool.query(
            'UPDATE Notifications SET is_read = TRUE WHERE user_id = ?',
            [req.user.id]
        );
        res.json({ message: 'All notifications marked as read' });
    } catch (err) {
        res.status(500).json({ error: err.message });
    }
});

// 9. GET /users (List all registered users with optional search & pagination)
app.get('/users', async (req, res) => {
    const { search, limit = 100 } = req.query;
    try {
        let sql = 'SELECT user_id, username, email, bio, created_at FROM Users WHERE 1=1';
        const params = [];
        if (search) {
            sql += ' AND (username LIKE ? OR bio LIKE ?)';
            params.push(`%${search}%`, `%${search}%`);
        }
        sql += ' ORDER BY user_id ASC LIMIT ?';
        params.push(Math.min(parseInt(limit, 10) || 100, 600));

        const [rows] = await pool.query(sql, params);
        res.json(rows);
    } catch (err) {
        res.status(500).json({ error: err.message });
    }
});

// 10. PUT /users/profile (Update bio)
app.put('/users/profile', authenticate, async (req, res) => {
    const { bio } = req.body;
    try {
        await pool.query(
            'UPDATE Users SET bio = ? WHERE user_id = ?',
            [bio, req.user.id]
        );
        res.json({ message: 'Profile updated successfully' });
    } catch (err) {
        res.status(500).json({ error: err.message });
    }
});

// 11. GET /users/:id (Profile details with stats and mutual followers)
app.get('/users/:id', async (req, res) => {
    const targetUserId = parseInt(req.params.id, 10);
    const viewerId = req.headers['x-user-id'] ? parseInt(req.headers['x-user-id'], 10) : null;
    
    try {
        const [users] = await pool.query(
            'SELECT user_id, username, email, bio, created_at FROM Users WHERE user_id = ?',
            [targetUserId]
        );
        if (users.length === 0) {
            return res.status(404).json({ error: 'User not found' });
        }
        const user = users[0];

        const [[{ followers_count }]] = await pool.query(
            'SELECT COUNT(*) AS followers_count FROM Follows WHERE following_id = ?',
            [targetUserId]
        );
        const [[{ following_count }]] = await pool.query(
            'SELECT COUNT(*) AS following_count FROM Follows WHERE follower_id = ?',
            [targetUserId]
        );
        const [[{ posts_count }]] = await pool.query(
            'SELECT COUNT(*) AS posts_count FROM Posts WHERE user_id = ? AND is_deleted = FALSE',
            [targetUserId]
        );

        let is_following = false;
        let mutual_followers = [];

        if (viewerId && viewerId !== targetUserId) {
            const [followRows] = await pool.query(
                'SELECT 1 FROM Follows WHERE follower_id = ? AND following_id = ?',
                [viewerId, targetUserId]
            );
            is_following = followRows.length > 0;

            const [procResults] = await pool.query(
                'CALL get_mutual_followers(?, ?)',
                [viewerId, targetUserId]
            );
            mutual_followers = (procResults && procResults[0]) ? procResults[0] : [];
        }

        res.json({
            ...user,
            followers_count,
            following_count,
            posts_count,
            is_following,
            mutual_followers
        });
    } catch (err) {
        res.status(500).json({ error: err.message });
    }
});

// 12. GET /users/:id/posts (Posts authored by specific user)
app.get('/users/:id/posts', async (req, res) => {
    const targetUserId = parseInt(req.params.id, 10);
    try {
        const [rows] = await pool.query(
            `SELECT p.post_id, p.user_id, p.content, p.media_url, p.like_count, p.language, p.tone, p.created_at, 
                    u.username AS author, u.username,
                    GROUP_CONCAT(DISTINCT t.name) AS tags
             FROM Posts p
             JOIN Users u ON u.user_id = p.user_id
             LEFT JOIN PostTags pt ON pt.post_id = p.post_id
             LEFT JOIN Tags t ON t.tag_id = pt.tag_id
             WHERE p.user_id = ? AND p.is_deleted = FALSE
             GROUP BY p.post_id
             ORDER BY p.created_at DESC`,
            [targetUserId]
        );
        const formatted = rows.map(r => ({
            ...r,
            tags: r.tags ? r.tags.split(',') : []
        }));
        res.json(formatted);
    } catch (err) {
        res.status(500).json({ error: err.message });
    }
});

// 13. GET /users/:id/followers (List of users following this user)
app.get('/users/:id/followers', async (req, res) => {
    const targetUserId = parseInt(req.params.id, 10);
    try {
        const [rows] = await pool.query(
            `SELECT u.user_id, u.username, u.email, u.bio, f.created_at AS followed_at
             FROM Follows f
             JOIN Users u ON u.user_id = f.follower_id
             WHERE f.following_id = ?
             ORDER BY f.created_at DESC`,
            [targetUserId]
        );
        res.json(rows);
    } catch (err) {
        res.status(500).json({ error: err.message });
    }
});

// 14. GET /users/:id/following (List of users followed by this user)
app.get('/users/:id/following', async (req, res) => {
    const targetUserId = parseInt(req.params.id, 10);
    try {
        const [rows] = await pool.query(
            `SELECT u.user_id, u.username, u.email, u.bio, f.created_at AS followed_at
             FROM Follows f
             JOIN Users u ON u.user_id = f.following_id
             WHERE f.follower_id = ?
             ORDER BY f.created_at DESC`,
            [targetUserId]
        );
        res.json(rows);
    } catch (err) {
        res.status(500).json({ error: err.message });
    }
});

const PORT = process.env.PORT || 3000;
app.listen(PORT, () => {
    console.log(`Server running on port ${PORT}`);
});


