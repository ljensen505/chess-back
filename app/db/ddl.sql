SET FOREIGN_KEY_CHECKS = 0;
DROP TABLE IF EXISTS `users`;
CREATE TABLE `users` (
    `user_id` CHAR(36) NOT NULL PRIMARY KEY,
    `auth0_id` VARCHAR(255) NOT NULL UNIQUE,
    `name` VARCHAR(255) NOT NULL,
    `email` VARCHAR(255),
    `username` VARCHAR(255) NOT NULL UNIQUE
) ENGINE = InnoDB DEFAULT CHARSET = utf8;
DROP TABLE IF EXISTS `games`;
CREATE TABLE `games` (
    `game_id` CHAR(36) NOT NULL PRIMARY KEY,
    `created_at` DATETIME DEFAULT CURRENT_TIMESTAMP,
    `owner_id` CHAR(36) NOT NULL,
    `black_player_id` CHAR(36) NULL,
    `white_player_id` CHAR(36) NULL,
    `last_updated_at` DATETIME NULL,
    FOREIGN KEY (`owner_id`) REFERENCES `users` (`user_id`)
) ENGINE = InnoDB DEFAULT CHARSET = utf8;
INSERT INTO `users` (
        `user_id`,
        `auth0_id`,
        `name`,
        `email`,
        `username`
    )
VALUES (
        'c816f2c2-2514-4070-84ec-2ea73f6da608',
        'PT83oQP7fRMyrq5Go8DYozx62JvXfnZ6@clients',
        'Test User',
        'test@chess.com',
        'test-user'
    );
SET FOREIGN_KEY_CHECKS = 1;