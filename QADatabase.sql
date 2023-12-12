-- MySQL dump 10.13  Distrib 8.1.0, for macos13.3 (arm64)
--
-- Host: localhost    Database: QADatabase
-- ------------------------------------------------------
-- Server version	8.1.0

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!50503 SET NAMES utf8mb4 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Current Database: `QADatabase`
--

CREATE DATABASE /*!32312 IF NOT EXISTS*/ `QADatabase` /*!40100 DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci */ /*!80016 DEFAULT ENCRYPTION='N' */;

USE `QADatabase`;

--
-- Table structure for table `importance`
--

DROP TABLE IF EXISTS `importance`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `importance` (
  `importance_id` int NOT NULL AUTO_INCREMENT,
  `score` float DEFAULT NULL,
  `last_updated` datetime DEFAULT NULL,
  PRIMARY KEY (`importance_id`)
) ENGINE=InnoDB AUTO_INCREMENT=43 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `importance`
--

LOCK TABLES `importance` WRITE;
/*!40000 ALTER TABLE `importance` DISABLE KEYS */;
INSERT INTO `importance` VALUES (6,1,'2023-12-05 21:33:48'),(7,0,'2023-12-05 23:23:29'),(8,2.4,'2023-12-07 23:14:42'),(9,0,'2023-12-06 01:48:23'),(10,0,'2023-12-06 01:50:07'),(11,0,'2023-12-07 23:08:59'),(12,2,'2023-12-07 23:08:59'),(13,0.96,'2023-12-09 22:15:18'),(14,1.12,'2023-12-09 22:15:18'),(15,0.92,'2023-12-11 22:25:16'),(16,0,'2023-12-07 14:48:38'),(17,0,'2023-12-07 14:49:26'),(18,9,'2023-12-07 23:15:09'),(19,0,'2023-12-07 15:03:52'),(20,1.1,'2023-12-11 22:25:16'),(21,0,'2023-12-07 22:22:53'),(22,0,'2023-12-07 22:33:32'),(23,0,'2023-12-07 22:49:35'),(24,0,'2023-12-07 22:53:46'),(25,0,'2023-12-07 22:55:57'),(26,0,'2023-12-07 22:56:09'),(27,0,'2023-12-07 22:56:52'),(28,0,'2023-12-07 22:57:04'),(29,0,'2023-12-07 22:57:23'),(30,0,'2023-12-07 22:58:08'),(31,7,'2023-12-07 23:15:09'),(32,0,'2023-12-07 23:00:47'),(33,0,'2023-12-07 23:00:58'),(34,0,'2023-12-07 23:14:55'),(35,0,'2023-12-07 23:15:21'),(36,3.36,'2023-12-11 22:25:17'),(37,0,'2023-12-09 22:19:39'),(38,0,'2023-12-11 21:06:29'),(39,6,'2023-12-11 22:25:17'),(40,0,'2023-12-11 22:13:11'),(41,0,'2023-12-11 22:14:00'),(42,0,'2023-12-11 22:24:25');
/*!40000 ALTER TABLE `importance` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `post`
--

DROP TABLE IF EXISTS `post`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `post` (
  `post_id` int NOT NULL AUTO_INCREMENT,
  `author_id` int NOT NULL,
  `importance_id` int NOT NULL,
  `created_time` datetime DEFAULT NULL,
  `updated_time` datetime DEFAULT NULL,
  `content` text,
  `view_count` int DEFAULT '0',
  `title` text,
  `help_count` int DEFAULT '0',
  PRIMARY KEY (`post_id`),
  KEY `author_id` (`author_id`),
  KEY `importance_id` (`importance_id`),
  CONSTRAINT `post_ibfk_1` FOREIGN KEY (`author_id`) REFERENCES `users` (`user_id`),
  CONSTRAINT `post_ibfk_2` FOREIGN KEY (`importance_id`) REFERENCES `importance` (`importance_id`)
) ENGINE=InnoDB AUTO_INCREMENT=25 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `post`
--

LOCK TABLES `post` WRITE;
/*!40000 ALTER TABLE `post` DISABLE KEYS */;
INSERT INTO `post` VALUES (21,8,36,'2023-12-09 22:19:15','2023-12-09 22:19:15','You can sort by views, date, help count ! \nYou can also write in **markdown** style (like this post) \nYou can click on update importance score, and that will delete all useless and old stories(nobody want to see them😇)\nI made this with FastAPI and Svelte, which was a really good experience. \nHope you enjoy 😉',11,'Welcome to my DB project 😀',10),(23,13,39,'2023-12-11 21:12:27','2023-12-11 21:14:27','## New content test\n- supports markdown! \n- can embed image\n\n<img width=\"423\" alt=\"image\" src=\"https://github.com/ddoddii/ddoddii.github.io/assets/95014836/da086b2f-c371-435c-8d0a-dc7359fa69e9\">\n\nThis is my relational schema . \n\nI can fix my post !! 😀 \n',4,'New Article Test - fixed',2);
/*!40000 ALTER TABLE `post` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `reply`
--

DROP TABLE IF EXISTS `reply`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `reply` (
  `reply_id` int NOT NULL AUTO_INCREMENT,
  `post_id` int NOT NULL,
  `author_id` int NOT NULL,
  `importance_id` int NOT NULL,
  `content` text,
  `created_time` datetime NOT NULL,
  `updated_time` datetime DEFAULT NULL,
  `help_count` int DEFAULT '0',
  `view_count` int DEFAULT '0',
  PRIMARY KEY (`reply_id`),
  KEY `post_id` (`post_id`),
  KEY `author_id` (`author_id`),
  KEY `importance_id` (`importance_id`),
  CONSTRAINT `reply_ibfk_1` FOREIGN KEY (`post_id`) REFERENCES `post` (`post_id`),
  CONSTRAINT `reply_ibfk_2` FOREIGN KEY (`author_id`) REFERENCES `users` (`user_id`),
  CONSTRAINT `reply_ibfk_3` FOREIGN KEY (`importance_id`) REFERENCES `importance` (`importance_id`)
) ENGINE=InnoDB AUTO_INCREMENT=17 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `reply`
--

LOCK TABLES `reply` WRITE;
/*!40000 ALTER TABLE `reply` DISABLE KEYS */;
INSERT INTO `reply` VALUES (16,23,13,42,'My reply for this post','2023-12-11 22:24:25','2023-12-11 22:24:25',0,0);
/*!40000 ALTER TABLE `reply` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `users`
--

DROP TABLE IF EXISTS `users`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `users` (
  `user_id` int NOT NULL AUTO_INCREMENT,
  `username` varchar(255) DEFAULT NULL,
  `password` varchar(255) NOT NULL,
  `name` varchar(1000) NOT NULL,
  `type` int DEFAULT '0',
  `birth` varchar(64) DEFAULT NULL,
  `sex` varchar(64) DEFAULT NULL,
  `address` text,
  `phone` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`user_id`)
) ENGINE=InnoDB AUTO_INCREMENT=14 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `users`
--

LOCK TABLES `users` WRITE;
/*!40000 ALTER TABLE `users` DISABLE KEYS */;
INSERT INTO `users` VALUES (2,'user1','1234','user계정1',0,NULL,NULL,NULL,NULL),(3,'user2','1234','user계정2',0,NULL,NULL,NULL,NULL),(4,'user3','1234','user계정3',0,NULL,NULL,NULL,NULL),(5,'user4','1234','user계정4',0,NULL,NULL,NULL,NULL),(6,'user5','1234','user계정5',0,NULL,NULL,NULL,NULL),(8,'soeun','$2b$12$tZVDnpP42jEihAYtz9H7/e/maYGQgcnL2JUp7G2f0SzJJZyWbqlwW','soeun',0,'2023-12-05 13:02:19','1','seoul','010-0000-0000'),(9,'uhm','$2b$12$ReHPKRqcmf/IE0Wd1qoZguHCGQNVHSK5vU.MZdpko8OPP3AW/OCDW','엄',0,'1970-01-12 08:33:43','female','서울시','01098870000'),(10,'test','$2b$12$Yaqzx4jhb6VCHcJiJmWt2.DiGhETckpoXwK8a4WsdnCdtfpVxP8ey','test',0,'1970-01-01 00:01:41','female','seoul','01012345678'),(11,'test2','$2b$12$UxfRb7p8AKe9KiU1miLMr.YuI9Jcy4sYqmdWYtVgUPxGfOz/WxOf2','test2',0,'1970-01-01 02:48:21','male','seoul','01012345949'),(12,'admin','$2b$12$vzkJOVf8S6NGSdPqf0F3zOcAC3pTWUyLiY93i29B.7z0nnJ39Ex8i','admin',1,'1970-01-01 00:01:41','female','yonsei','010-0000-0000'),(13,'newuser','$2b$12$zMR0j/74Bean2PPqL8J12uZ9ZmmJf3gyyOGOXTBxkZNq.W8h89e8G','소은',0,'1970-01-12 08:33:43','female','yonsei-ro','010-0000-0000');
/*!40000 ALTER TABLE `users` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2023-12-12 19:49:19
