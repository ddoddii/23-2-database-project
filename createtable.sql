CREATE DATABASE IF NOT EXISTS `QADatabase`;
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
    `title` TEXT,
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

INSERT INTO `users` (`user_id`, `email_id`, `password`, `name`, `type`, `birth`, `sex`, `address`, `phone`) VALUES
	(1, 'admin', 'admin', '관리자계정', 1, NULL, NULL, NULL, NULL),
	(2, 'user1', '1234', 'user계정1', 0, NULL, NULL, NULL, NULL),
	(3, 'user2', '1234', 'user계정2', 0, NULL, NULL, NULL, NULL),
	(4, 'user3', '1234', 'user계정3', 0, NULL, NULL, NULL, NULL),
	(5, 'user4', '1234', 'user계정4', 0, NULL, NULL, NULL, NULL),
	(6, 'user5', '1234', 'user계정5', 0, NULL, NULL, NULL, NULL);