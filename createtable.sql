USE QADatabase;

CREATE TABLE `user` (
    `user_id` INT NOT NULL AUTO_INCREMENT,
    `email_id` VARCHAR(255) NOT NULL,
    `password` VARCHAR(255) NOT NULL,
    `name` VARCHAR(255) NOT NULL,
    `type` VARCHAR(255) NOT NULL,
    `birth` VARCHAR(255),
    `sex` VARCHAR(255),
    `address` VARCHAR(255),
    `phone` VARCHAR(255),
    PRIMARY KEY (`user_id`)
);

CREATE TABLE `importance` (
    `importance_id` INT NOT NULL AUTO_INCREMENT,
    `score` INT DEFAULT 0,
    `last_updated` DATETIME,
    PRIMARY KEY (`importance_id`)
);

CREATE TABLE `post` (
    `post_id` INT NOT NULL AUTO_INCREMENT,
    `author_id` INT NOT NULL,
    `importance_id` INT NOT NULL,
    `created_time` DATETIME NOT NULL,
    `updated_time` DATETIME,
    `content` TEXT,
    `view_count` INT DEFAULT 0,
    PRIMARY KEY (`post_id`),
    FOREIGN KEY (`author_id`) REFERENCES `user` (`user_id`),
    FOREIGN KEY (`importance_id`) REFERENCES `importance` (`importance_id`)
);

CREATE TABLE `reply` (
    `reply_id` INT NOT NULL AUTO_INCREMENT,
    `post_id` INT NOT NULL,
    `author_id` INT NOT NULL,
    `importance_id` INT NOT NULL,
    `content` TEXT,
    `created_time` DATETIME NOT NULL,
    `updated_time` DATETIME,
    `help_count` INT DEFAULT 0,
    PRIMARY KEY (`reply_id`),
    FOREIGN KEY (`post_id`) REFERENCES `post` (`post_id`),
    FOREIGN KEY (`author_id`) REFERENCES `user` (`user_id`),
    FOREIGN KEY (`importance_id`) REFERENCES `importance` (`importance_id`)
);
