-- SEED DATA FOR SOCIAL MEDIA DBMS
-- Password for all seeded users is: password123
-- Hash: $2b$10$6f6yXSxfu1l6ravXYkqo2uRA1IHNdXuCKbmCiDHP.jsDoPAA97ngS

-- Insert Seed Users
INSERT INTO Users (user_id, username, email, password_hash, bio) VALUES
(1, 'vansh_chadha', 'vansh@kineticsocial.io', '$2b$10$6f6yXSxfu1l6ravXYkqo2uRA1IHNdXuCKbmCiDHP.jsDoPAA97ngS', 'Founder & Lead Engineer @ Kinetic Social | Building high-concurrency database systems.'),
(2, 'rahul_sharma', 'rahul@dev.io', '$2b$10$6f6yXSxfu1l6ravXYkqo2uRA1IHNdXuCKbmCiDHP.jsDoPAA97ngS', 'Full stack developer & open source enthusiast. Exploring high-throughput distributed architectures.'),
(3, 'elena_rostova', 'elena@vektorlab.io', '$2b$10$6f6yXSxfu1l6ravXYkqo2uRA1IHNdXuCKbmCiDHP.jsDoPAA97ngS', 'Lead Product Designer @ Vektor Lab. Obsessed with brutalist typography and micro-interactions.'),
(4, 'marcus_thorne', 'marcus.thorne@cloudscale.net', '$2b$10$6f6yXSxfu1l6ravXYkqo2uRA1IHNdXuCKbmCiDHP.jsDoPAA97ngS', 'Senior Systems Architect. Rust, MariaDB internals, and low-latency network protocols.'),
(5, 'selah_kim', 'selah.kim@gmail.com', '$2b$10$6f6yXSxfu1l6ravXYkqo2uRA1IHNdXuCKbmCiDHP.jsDoPAA97ngS', 'Design Technologist & Creative Coder. Exploring generative UI and tactile digital surfaces.'),
(6, 'tarik_oconnor', 'tarik@foundry.io', '$2b$10$6f6yXSxfu1l6ravXYkqo2uRA1IHNdXuCKbmCiDHP.jsDoPAA97ngS', 'Founding engineer @ Foundry Systems. Writing about database schemas, indexing, and query planners.'),
(7, 'ananya_sen', 'ananya.sen@berkeley.edu', '$2b$10$6f6yXSxfu1l6ravXYkqo2uRA1IHNdXuCKbmCiDHP.jsDoPAA97ngS', 'AI/ML Researcher & Computational Sociologist. Investigating autonomous agent networks.'),
(8, 'dev_arjun', 'arjun.devops@gmail.com', '$2b$10$6f6yXSxfu1l6ravXYkqo2uRA1IHNdXuCKbmCiDHP.jsDoPAA97ngS', 'Cloud Infrastructure & SRE. Kubernetes, observability pipelines, and Linux kernel tuning.')
ON DUPLICATE KEY UPDATE bio=VALUES(bio);

-- Insert Posts
INSERT INTO Posts (user_id, content, media_url, created_at) VALUES
(1, 'Excited to announce our new 3NF relational architecture for Kinetic Social! Benchmarked with MariaDB indexes and stored procedures — sub-5ms query response times under high concurrency. 🚀 #DBMS #Architecture', NULL, DATE_SUB(NOW(), INTERVAL 1 HOUR)),
(3, 'Hot take: Modern software in 2026 feels way too sterile. We need more tactile tension, bold typography hierarchies, and intentional physical friction in digital interfaces. Here is what we learned rebuilding our design token system. #Design #UIUX', NULL, DATE_SUB(NOW(), INTERVAL 2 HOUR)),
(4, 'Friendly reminder to always check your EXPLAIN ANALYZE on complex multi-table joins. Composite B-Tree indexes on (follower_id, following_id) transformed our feed query from an unindexed filesort into a pure index scan. 💡 #Databases #MariaDB #Performance', NULL, DATE_SUB(NOW(), INTERVAL 3 HOUR)),
(5, 'Prototyping fluid gestural feed interactions today. There is something magical about micro-spring physics that makes scrolling feel completely weightless. Check out the demo in our lab! ✨ #CreativeTech #Frontend', NULL, DATE_SUB(NOW(), INTERVAL 4 HOUR)),
(6, 'Normalized schemas (3NF) vs Denormalized stores: You do not have to choose blindly. Using database triggers to maintain aggregate counters like like_count gives you transactional consistency with O(1) read latency. #DataModeling #Engineering', NULL, DATE_SUB(NOW(), INTERVAL 5 HOUR)),
(7, 'Published a new paper today on synthetic consensus mechanisms in agentic coding networks. When multiple autonomous models collaborate with deterministic validation loops, hallucination rates drop by 82%. #AI #Research', NULL, DATE_SUB(NOW(), INTERVAL 6 HOUR)),
(2, 'Just completed migrating our API service to Node.js connection pooling with MariaDB. Handling 10k concurrent socket connections without breaking a sweat! #NodeJS #Backend #Scalability', NULL, DATE_SUB(NOW(), INTERVAL 7 HOUR)),
(8, 'Automated database migrations and zero-downtime schema deployments with CI/CD containers. The peace of mind on Friday afternoons is priceless. 🛡️ #DevOps #Reliability', NULL, DATE_SUB(NOW(), INTERVAL 8 HOUR)),
(3, 'Monochrome palettes paired with high-contrast accent highlights create a timeless editorial presence. Designing with intent > following flat trends. #DesignSystems', NULL, DATE_SUB(NOW(), INTERVAL 9 HOUR)),
(4, 'InnoDB buffer pool tuning tip: Ensure your innodb_buffer_pool_size is sized to fit 70-80% of RAM on dedicated database instances. Watch your disk I/O metrics plummet. #MariaDB #SysAdmin', NULL, DATE_SUB(NOW(), INTERVAL 10 HOUR));

-- Establish Follow Relationships
-- Abhinav (1) follows everyone so his feed is packed with content
INSERT IGNORE INTO Follows (follower_id, following_id) VALUES
(1, 2), (1, 3), (1, 4), (1, 5), (1, 6), (1, 7), (1, 8),
-- Rahul (2) follows Abhinav, Marcus, Arjun
(2, 1), (2, 4), (2, 8),
-- Elena (3) follows Selah, Abhinav, Tarik
(3, 1), (3, 5), (3, 6),
-- Marcus (4) follows Tarik, Arjun, Abhinav
(4, 1), (4, 6), (4, 8),
-- Selah (5) follows Elena, Abhinav
(5, 1), (5, 3),
-- Tarik (6) follows Marcus, Abhinav, Ananya
(6, 1), (6, 4), (6, 7),
-- Ananya (7) follows Marcus, Selah, Abhinav
(7, 1), (7, 4), (7, 5),
-- Arjun (8) follows Marcus, Rahul, Abhinav
(8, 1), (8, 2), (8, 4);

-- Insert Likes (this fires triggers to update like_count and create notifications!)
INSERT IGNORE INTO Likes (user_id, post_id) VALUES
(2, 3), (3, 3), (4, 3), (5, 3), (6, 3), (7, 3),
(1, 4), (4, 4), (5, 4), (6, 4),
(1, 5), (2, 5), (3, 5), (6, 5), (7, 5), (8, 5),
(1, 6), (3, 6), (4, 6),
(1, 7), (3, 7), (4, 7), (5, 7), (8, 7),
(1, 8), (2, 8), (4, 8),
(1, 9), (4, 9), (6, 9), (8, 9),
(1, 10), (2, 10), (3, 10), (5, 10);

-- Insert Comments
INSERT INTO Comments (post_id, user_id, content) VALUES
(3, 2, 'Congratulations on the launch! The query benchmarks look incredible.'),
(3, 4, 'Very clean 3NF layout. Did you benchmark B-Tree vs Hash index on user_id?'),
(4, 5, 'Completely agree Elena! Digital tactile design is sorely missed.'),
(5, 1, 'Composite indexes are a game changer. Thanks for sharing the EXPLAIN breakdown!'),
(6, 3, 'Can not wait to try the gestural interactions on touch displays!'),
(7, 4, 'Triggers for aggregate counters are so underrated in modern relational workflows.'),
(8, 1, 'Fascinating paper Ananya, sending this to our whole team!');
