-- INDEXING STRATEGY

-- Speeds up fetching a user's own posts, newest first
CREATE INDEX idx_posts_user_created ON Posts(user_id, created_at);

-- Speeds up 'who follows user X' and feed joins
CREATE INDEX idx_follows_following ON Follows(following_id);

-- Speeds up 'who does user X follow'
CREATE INDEX idx_follows_follower ON Follows(follower_id);

-- Speeds up counting/listing likers of a post
CREATE INDEX idx_likes_post ON Likes(post_id);

-- Speeds up loading a post's comment thread
CREATE INDEX idx_comments_post ON Comments(post_id);

-- Speeds up 'unread notifications for user X'
CREATE INDEX idx_notifications_user_read ON Notifications(user_id, is_read);
