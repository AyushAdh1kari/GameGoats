USE gamegoats_db;

INSERT INTO users (username, persona, region, created_at)
WITH RECURSIVE seq AS (
    SELECT 1 AS n
    UNION ALL
    SELECT n + 1 FROM seq WHERE n < 36
)
SELECT
    CASE
        WHEN n <= 28 THEN CONCAT('player_', LPAD(n, 2, '0'))
        WHEN n <= 33 THEN CONCAT('mod_', LPAD(n - 28, 2, '0'))
        ELSE CONCAT('admin_', LPAD(n - 33, 2, '0'))
    END AS username,
    CASE
        WHEN n <= 28 THEN 'player'
        WHEN n <= 33 THEN 'moderator'
        ELSE 'admin'
    END AS persona,
    ELT(((n - 1) % 4) + 1, 'NA-East', 'NA-West', 'EU-Central', 'AP-South') AS region,
    DATE_SUB(NOW(), INTERVAL (200 - n) DAY) AS created_at
FROM seq;

INSERT INTO games (title, genre, platform, release_year, average_rating, lifecycle_status, created_at, updated_at)
WITH RECURSIVE seq AS (
    SELECT 1 AS n
    UNION ALL
    SELECT n + 1 FROM seq WHERE n < 35
)
SELECT
    CONCAT(
        ELT(((n - 1) % 7) + 1, 'Crimson', 'Neon', 'Mystic', 'Solar', 'Frost', 'Echo', 'Titan'),
        ' ',
        ELT(((n - 1) % 5) + 1, 'Frontier', 'Chronicles', 'Assault', 'Odyssey', 'Legends'),
        ' ',
        LPAD(n, 2, '0')
    ) AS title,
    ELT(((n - 1) % 7) + 1, 'Shooter', 'RPG', 'Strategy', 'Simulation', 'Sports', 'Adventure', 'Puzzle') AS genre,
    ELT(((n - 1) % 5) + 1, 'PC', 'PlayStation', 'Xbox', 'Nintendo', 'Mobile') AS platform,
    2010 + (n % 15) AS release_year,
    ROUND(2.80 + ((n % 18) * 0.11), 2) AS average_rating,
    CASE
        WHEN n % 11 = 0 THEN 'sunset'
        WHEN n % 6 = 0 THEN 'maintenance'
        ELSE 'active'
    END AS lifecycle_status,
    DATE_SUB(NOW(), INTERVAL (400 - n) DAY) AS created_at,
    DATE_SUB(NOW(), INTERVAL (120 - n) DAY) AS updated_at
FROM seq;

INSERT INTO servers (server_name, region, environment, health_status, capacity_percent, last_heartbeat, created_at)
WITH RECURSIVE seq AS (
    SELECT 1 AS n
    UNION ALL
    SELECT n + 1 FROM seq WHERE n < 30
)
SELECT
    CASE
        WHEN n <= 24 THEN CONCAT('gg-prod-', LPAD(n, 2, '0'))
        ELSE CONCAT('gg-stage-', LPAD(n - 24, 2, '0'))
    END AS server_name,
    ELT(((n - 1) % 6) + 1, 'NA-East', 'NA-West', 'EU-Central', 'EU-West', 'AP-South', 'AP-Northeast') AS region,
    CASE WHEN n <= 24 THEN 'production' ELSE 'staging' END AS environment,
    CASE
        WHEN n % 17 = 0 THEN 'down'
        WHEN n % 5 = 0 THEN 'degraded'
        ELSE 'healthy'
    END AS health_status,
    ROUND(35 + ((n * 7) % 61), 2) AS capacity_percent,
    DATE_SUB(NOW(), INTERVAL (n * 3) MINUTE) AS last_heartbeat,
    DATE_SUB(NOW(), INTERVAL (90 - n) DAY) AS created_at
FROM seq;

INSERT INTO comments (game_id, player_id, comment_text, toxicity_score, moderation_status, created_at, updated_at)
WITH RECURSIVE seq AS (
    SELECT 1 AS n
    UNION ALL
    SELECT n + 1 FROM seq WHERE n < 60
)
SELECT
    ((n - 1) % 35) + 1 AS game_id,
    ((n - 1) % 28) + 1 AS player_id,
    CONCAT(
        'Session ', LPAD(n, 3, '0'), ': ',
        ELT(((n - 1) % 6) + 1,
            'Great balance after the latest patch.',
            'Queue times were long, but gameplay felt smooth.',
            'Matchmaking felt fair for my skill level.',
            'Server lag spikes appeared near peak hours.',
            'Content update added useful progression goals.',
            'Found a bug in the inventory menu flow.'
        )
    ) AS comment_text,
    ROUND((n % 17) * 0.041, 3) AS toxicity_score,
    CASE
        WHEN n % 14 = 0 THEN 'flagged'
        WHEN n % 18 = 0 THEN 'hidden'
        ELSE 'visible'
    END AS moderation_status,
    DATE_SUB(NOW(), INTERVAL (180 - n) HOUR) AS created_at,
    DATE_SUB(NOW(), INTERVAL (180 - n) HOUR) AS updated_at
FROM seq;

INSERT INTO favorites (player_id, game_id, priority, added_at)
SELECT
    seeded.player_id,
    seeded.game_id,
    1 + ((seeded.rn - 1) % 5) AS priority,
    DATE_SUB(NOW(), INTERVAL seeded.rn DAY) AS added_at
FROM (
    SELECT
        p.user_id AS player_id,
        g.game_id,
        ROW_NUMBER() OVER (ORDER BY p.user_id, g.game_id) AS rn
    FROM users p
    CROSS JOIN games g
    WHERE p.persona = 'player'
) AS seeded
WHERE seeded.rn <= 140;

INSERT INTO recommendations (
    player_id,
    game_id,
    recommendation_reason,
    match_score,
    recommendation_status,
    generated_at,
    refreshed_at
)
SELECT
    seeded.player_id,
    seeded.game_id,
    ELT(((seeded.rn - 1) % 5) + 1,
        'Because you favor strategy-heavy titles.',
        'Similar players recently rated this game highly.',
        'Recent play sessions indicate strong genre match.',
        'Trending title in your preferred region.',
        'Matches your recent engagement and favorites.'
    ) AS recommendation_reason,
    ROUND(55 + ((seeded.rn * 1.7) % 45), 2) AS match_score,
    CASE
        WHEN seeded.rn % 9 = 0 THEN 'dismissed'
        WHEN seeded.rn % 7 = 0 THEN 'accepted'
        WHEN seeded.rn % 13 = 0 THEN 'hidden'
        ELSE 'new'
    END AS recommendation_status,
    DATE_SUB(NOW(), INTERVAL (75 - seeded.rn) HOUR) AS generated_at,
    DATE_SUB(NOW(), INTERVAL (70 - seeded.rn) HOUR) AS refreshed_at
FROM (
    SELECT
        p.user_id AS player_id,
        g.game_id,
        ROW_NUMBER() OVER (ORDER BY p.user_id, g.game_id) AS rn
    FROM users p
    JOIN games g ON ((p.user_id + g.game_id) % 4 = 0)
    WHERE p.persona = 'player'
) AS seeded
WHERE seeded.rn <= 60;

INSERT INTO reports (
    reporter_id,
    comment_id,
    game_id,
    reason_code,
    details,
    report_status,
    assigned_moderator_id,
    resolution_notes,
    created_at,
    updated_at
)
WITH RECURSIVE seq AS (
    SELECT 1 AS n
    UNION ALL
    SELECT n + 1 FROM seq WHERE n < 55
)
SELECT
    ((n - 1) % 28) + 1 AS reporter_id,
    ((n - 1) % 60) + 1 AS comment_id,
    ((n - 1) % 35) + 1 AS game_id,
    ELT(((n - 1) % 5) + 1, 'abuse', 'cheating', 'spam', 'harassment', 'other') AS reason_code,
    ELT(((n - 1) % 5) + 1,
        'Offensive chat language reported.',
        'Suspicious gameplay behavior observed.',
        'Repeated promotional spam in comments.',
        'Personal harassment targeting players.',
        'General policy violation requiring review.'
    ) AS details,
    CASE
        WHEN n % 8 = 0 THEN 'resolved'
        WHEN n % 10 = 0 THEN 'rejected'
        WHEN n % 3 = 0 THEN 'in_review'
        ELSE 'open'
    END AS report_status,
    CASE
        WHEN n % 4 = 0 THEN NULL
        ELSE 29 + ((n - 1) % 5)
    END AS assigned_moderator_id,
    CASE
        WHEN n % 8 = 0 THEN 'Action taken and content sanitized.'
        WHEN n % 10 = 0 THEN 'Insufficient evidence after review.'
        ELSE NULL
    END AS resolution_notes,
    DATE_SUB(NOW(), INTERVAL (70 - n) DAY) AS created_at,
    DATE_SUB(NOW(), INTERVAL (69 - n) DAY) AS updated_at
FROM seq;

INSERT INTO alerts (
    server_id,
    severity,
    alert_type,
    alert_message,
    alert_status,
    created_at,
    acknowledged_by,
    acknowledged_at,
    resolved_at
)
WITH RECURSIVE seq AS (
    SELECT 1 AS n
    UNION ALL
    SELECT n + 1 FROM seq WHERE n < 55
)
SELECT
    ((n - 1) % 30) + 1 AS server_id,
    CASE
        WHEN n % 11 = 0 THEN 'critical'
        WHEN n % 6 = 0 THEN 'high'
        WHEN n % 4 = 0 THEN 'medium'
        ELSE 'low'
    END AS severity,
    ELT(((n - 1) % 5) + 1, 'latency', 'cpu', 'memory', 'disk', 'matchmaking') AS alert_type,
    ELT(((n - 1) % 5) + 1,
        'Latency exceeded target threshold.',
        'CPU saturation above 90 percent.',
        'Memory pressure detected on match node.',
        'Disk usage above policy watermark.',
        'Matchmaking queue delay exceeded SLA.'
    ) AS alert_message,
    CASE
        WHEN n % 9 = 0 THEN 'resolved'
        WHEN n % 4 = 0 THEN 'acknowledged'
        ELSE 'active'
    END AS alert_status,
    DATE_SUB(NOW(), INTERVAL (120 - n) HOUR) AS created_at,
    CASE
        WHEN n % 9 = 0 OR n % 4 = 0 THEN 29 + ((n - 1) % 8)
        ELSE NULL
    END AS acknowledged_by,
    CASE
        WHEN n % 9 = 0 OR n % 4 = 0 THEN DATE_SUB(NOW(), INTERVAL (118 - n) HOUR)
        ELSE NULL
    END AS acknowledged_at,
    CASE
        WHEN n % 9 = 0 THEN DATE_SUB(NOW(), INTERVAL (116 - n) HOUR)
        ELSE NULL
    END AS resolved_at
FROM seq;
