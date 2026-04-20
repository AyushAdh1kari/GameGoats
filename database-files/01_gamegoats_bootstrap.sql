DROP DATABASE IF EXISTS gamegoats_db;
CREATE DATABASE IF NOT EXISTS gamegoats_db;
USE gamegoats_db;

CREATE TABLE IF NOT EXISTS users (
    user_id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(64) NOT NULL UNIQUE,
    persona ENUM('player', 'moderator', 'admin') NOT NULL,
    region VARCHAR(32) NOT NULL,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS games (
    game_id INT AUTO_INCREMENT PRIMARY KEY,
    title VARCHAR(128) NOT NULL,
    genre VARCHAR(48) NOT NULL,
    platform ENUM('PC', 'PlayStation', 'Xbox', 'Nintendo', 'Mobile') NOT NULL,
    release_year SMALLINT NOT NULL,
    average_rating DECIMAL(3, 2) NOT NULL DEFAULT 0.00,
    lifecycle_status ENUM('active', 'maintenance', 'sunset') NOT NULL DEFAULT 'active',
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    UNIQUE KEY uq_game_title_platform (title, platform)
);

CREATE TABLE IF NOT EXISTS comments (
    comment_id INT AUTO_INCREMENT PRIMARY KEY,
    game_id INT NOT NULL,
    player_id INT NOT NULL,
    comment_text VARCHAR(500) NOT NULL,
    toxicity_score DECIMAL(4, 3) NOT NULL DEFAULT 0.000,
    moderation_status ENUM('visible', 'hidden', 'flagged') NOT NULL DEFAULT 'visible',
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    CONSTRAINT fk_comments_game FOREIGN KEY (game_id) REFERENCES games(game_id),
    CONSTRAINT fk_comments_player FOREIGN KEY (player_id) REFERENCES users(user_id),
    INDEX idx_comments_game (game_id),
    INDEX idx_comments_player (player_id),
    INDEX idx_comments_status (moderation_status)
);

CREATE TABLE IF NOT EXISTS favorites (
    favorite_id INT AUTO_INCREMENT PRIMARY KEY,
    player_id INT NOT NULL,
    game_id INT NOT NULL,
    priority TINYINT NOT NULL DEFAULT 3,
    added_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT fk_favorites_player FOREIGN KEY (player_id) REFERENCES users(user_id),
    CONSTRAINT fk_favorites_game FOREIGN KEY (game_id) REFERENCES games(game_id),
    UNIQUE KEY uq_favorites_player_game (player_id, game_id),
    INDEX idx_favorites_game (game_id)
);

CREATE TABLE IF NOT EXISTS recommendations (
    recommendation_id INT AUTO_INCREMENT PRIMARY KEY,
    player_id INT NOT NULL,
    game_id INT NOT NULL,
    recommendation_reason VARCHAR(255) NOT NULL,
    match_score DECIMAL(5, 2) NOT NULL,
    recommendation_status ENUM('new', 'accepted', 'dismissed', 'hidden') NOT NULL DEFAULT 'new',
    generated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    refreshed_at TIMESTAMP NULL,
    CONSTRAINT fk_recommendations_player FOREIGN KEY (player_id) REFERENCES users(user_id),
    CONSTRAINT fk_recommendations_game FOREIGN KEY (game_id) REFERENCES games(game_id),
    UNIQUE KEY uq_recommendation_player_game (player_id, game_id),
    INDEX idx_recommendations_status (recommendation_status)
);

CREATE TABLE IF NOT EXISTS reports (
    report_id INT AUTO_INCREMENT PRIMARY KEY,
    reporter_id INT NOT NULL,
    comment_id INT NULL,
    game_id INT NULL,
    reason_code ENUM('abuse', 'cheating', 'spam', 'harassment', 'other') NOT NULL,
    details VARCHAR(255) NOT NULL,
    report_status ENUM('open', 'in_review', 'resolved', 'rejected') NOT NULL DEFAULT 'open',
    assigned_moderator_id INT NULL,
    resolution_notes VARCHAR(255) NULL,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    CONSTRAINT fk_reports_reporter FOREIGN KEY (reporter_id) REFERENCES users(user_id),
    CONSTRAINT fk_reports_comment FOREIGN KEY (comment_id) REFERENCES comments(comment_id),
    CONSTRAINT fk_reports_game FOREIGN KEY (game_id) REFERENCES games(game_id),
    CONSTRAINT fk_reports_assignee FOREIGN KEY (assigned_moderator_id) REFERENCES users(user_id),
    INDEX idx_reports_status (report_status),
    INDEX idx_reports_assignee (assigned_moderator_id)
);

CREATE TABLE IF NOT EXISTS servers (
    server_id INT AUTO_INCREMENT PRIMARY KEY,
    server_name VARCHAR(64) NOT NULL UNIQUE,
    region VARCHAR(32) NOT NULL,
    environment ENUM('production', 'staging') NOT NULL DEFAULT 'production',
    health_status ENUM('healthy', 'degraded', 'down') NOT NULL DEFAULT 'healthy',
    capacity_percent DECIMAL(5, 2) NOT NULL DEFAULT 0.00,
    last_heartbeat TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS alerts (
    alert_id INT AUTO_INCREMENT PRIMARY KEY,
    server_id INT NULL,
    severity ENUM('low', 'medium', 'high', 'critical') NOT NULL,
    alert_type VARCHAR(80) NOT NULL,
    alert_message VARCHAR(255) NOT NULL,
    alert_status ENUM('active', 'acknowledged', 'resolved') NOT NULL DEFAULT 'active',
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    acknowledged_by INT NULL,
    acknowledged_at TIMESTAMP NULL,
    resolved_at TIMESTAMP NULL,
    CONSTRAINT fk_alerts_server FOREIGN KEY (server_id) REFERENCES servers(server_id) ON DELETE SET NULL,
    CONSTRAINT fk_alerts_ack_user FOREIGN KEY (acknowledged_by) REFERENCES users(user_id) ON DELETE SET NULL,
    INDEX idx_alerts_status (alert_status),
    INDEX idx_alerts_severity (severity),
    INDEX idx_alerts_server (server_id)
);
