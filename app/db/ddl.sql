SET FOREIGN_KEY_CHECKS = 0;
DROP TABLE IF EXISTS `users`;
CREATE TABLE `users` (
    `id` CHAR(36) NOT NULL PRIMARY KEY,
    `auth0_id` VARCHAR(255) NOT NULL,
    `name` VARCHAR(255) NOT NULL,
    `email` VARCHAR(255) NOT NULL
) ENGINE = InnoDB DEFAULT CHARSET = utf8;
INSERT INTO `users` (`id`, `auth0_id`, `name`, `email`)
VALUES (
        '7f649c83-0f24-43f8-b770-8fd07c1fe598',
        'google-oauth2|103593642272149633528',
        'Lucas Jensen',
        'lucas.p.jensen10@gmail.com'
    ),
    (
        'b3e3e3e3-0f24-43f8-b770-8fd07c1fe598',
        'google-oauth2|100050368901887990576',
        'Lucas Jensen',
        'jenseluc@oregonstate.edu'
    ),
    (
        '9b990f7e-70c5-4cd7-b683-6a6026bef728',
        'PT83oQP7fRMyrq5Go8DYozx62JvXfnZ6@clients',
        'Test User',
        'test@chess.com'
    );
DROP TABLE IF EXISTS `games`;
CREATE TABLE `games` (
    `id` CHAR(36) NOT NULL PRIMARY KEY,
    `owner_id` CHAR(36) NOT NULL,
    `black_player_id` CHAR(36) NULL,
    `white_player_id` CHAR(36) NULL,
    FOREIGN KEY (`owner_id`) REFERENCES `users` (`id`)
) ENGINE = InnoDB DEFAULT CHARSET = utf8;
INSERT INTO `games` (`id`, `owner_id`)
VALUES (
        '731fbc84-6919-49cf-b5ec-dc76043fac81',
        '7f649c83-0f24-43f8-b770-8fd07c1fe598'
    ),
    (
        '713302ff-b3df-4724-8148-dc537febb38f',
        '7f649c83-0f24-43f8-b770-8fd07c1fe598'
    ),
    (
        'a8933fe5-abe2-4c56-8a2b-984a2de56d20',
        '9b990f7e-70c5-4cd7-b683-6a6026bef728'
    );
SET FOREIGN_KEY_CHECKS = 1;