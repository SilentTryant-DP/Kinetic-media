-- TRIGGERS, VIEWS, AND STORED PROCEDURES

-- 8.1 Trigger: Keep like_count in Sync
DELIMITER $$
CREATE TRIGGER trg_like_insert
AFTER INSERT ON Likes
FOR EACH ROW
BEGIN
    UPDATE Posts SET like_count = like_count + 1
    WHERE post_id = NEW.post_id;
END$$

CREATE TRIGGER trg_like_delete
AFTER DELETE ON Likes
FOR EACH ROW
BEGIN
    UPDATE Posts SET like_count = like_count - 1
    WHERE post_id = OLD.post_id;
END$$
DELIMITER ;

-- 8.2 Trigger: Auto-generate a Notification on Like
DELIMITER $$
CREATE TRIGGER trg_notify_on_like
AFTER INSERT ON Likes
FOR EACH ROW
BEGIN
    INSERT INTO Notifications (user_id, type, reference_id)
    SELECT p.user_id, 'like', NEW.post_id
    FROM Posts p
    WHERE p.post_id = NEW.post_id
      AND p.user_id <> NEW.user_id;   -- don't notify yourself
END$$
DELIMITER ;

-- 8.3 View: User Feed
CREATE OR REPLACE VIEW user_feed AS
SELECT f.follower_id AS viewer_id,
       p.post_id, p.user_id, p.content, p.media_url, p.like_count, p.language, p.tone, p.created_at,
       u.username AS author,
       u.username AS username
FROM Follows f
JOIN Posts p ON p.user_id = f.following_id
JOIN Users u ON u.user_id = p.user_id
WHERE p.is_deleted = FALSE;

-- 8.4 Stored Procedure: Mutual Followers
DELIMITER $$
CREATE PROCEDURE get_mutual_followers(IN user_a INT, IN user_b INT)
BEGIN
    SELECT u.user_id, u.username
    FROM Follows f1
    JOIN Follows f2 ON f1.follower_id = f2.follower_id
    JOIN Users u    ON u.user_id = f1.follower_id
    WHERE f1.following_id = user_a
      AND f2.following_id = user_b;
END$$
DELIMITER ;
