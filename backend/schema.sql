# ************************************************************
# Sequel Pro SQL dump
# Version 4541
#
# http://www.sequelpro.com/
# https://github.com/sequelpro/sequelpro
#
# Host: 127.0.0.1 (MySQL 5.7.21)
# Database: Sudoku
# Generation Time: 2018-08-29 02:52:29 +0000
# ************************************************************


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;


# Dump of table difficulties
# ------------------------------------------------------------

DROP TABLE IF EXISTS `difficulties`;

CREATE TABLE `difficulties` (
  `difficulty_id` int(11) unsigned NOT NULL AUTO_INCREMENT,
  `difficulty_name` varchar(50) NOT NULL DEFAULT '',
  PRIMARY KEY (`difficulty_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

LOCK TABLES `difficulties` WRITE;
/*!40000 ALTER TABLE `difficulties` DISABLE KEYS */;

INSERT INTO `difficulties` (`difficulty_id`, `difficulty_name`)
VALUES
	(1,'hard'),
	(2,'medium'),
	(3,'easy');

/*!40000 ALTER TABLE `difficulties` ENABLE KEYS */;
UNLOCK TABLES;


# Dump of table hiscores
# ------------------------------------------------------------

DROP TABLE IF EXISTS `hiscores`;

CREATE TABLE `hiscores` (
  `hiscore_id` int(11) unsigned NOT NULL AUTO_INCREMENT,
  `hiscore_user_id` int(11) NOT NULL,
  `hiscore_time` int(20) NOT NULL,
  `hiscore_difficulty` int(11) NOT NULL,
  PRIMARY KEY (`hiscore_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

LOCK TABLES `hiscores` WRITE;
/*!40000 ALTER TABLE `hiscores` DISABLE KEYS */;

INSERT INTO `hiscores` (`hiscore_id`, `hiscore_user_id`, `hiscore_time`, `hiscore_difficulty`)
VALUES
	(2,12,120,1),
	(3,13,110,1),
	(4,12,100,2),
	(5,9,120,3),
	(6,9,120,3),
	(7,11,90,3),
	(8,13,131,2),
	(9,13,130,2),
	(10,13,130,2),
	(11,13,150,1),
	(12,12,50,3),
	(13,12,30,3),
	(14,12,200,3),
	(15,12,200,3),
	(16,10,123,3),
	(17,10,127,3),
	(18,10,127,3);

/*!40000 ALTER TABLE `hiscores` ENABLE KEYS */;
UNLOCK TABLES;


# Dump of table users
# ------------------------------------------------------------

DROP TABLE IF EXISTS `users`;

CREATE TABLE `users` (
  `user_id` int(11) unsigned NOT NULL AUTO_INCREMENT,
  `user_name` varchar(50) NOT NULL DEFAULT '',
  `user_hash` varchar(256) NOT NULL DEFAULT '',
  `user_token` varchar(32) DEFAULT NULL,
  PRIMARY KEY (`user_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

LOCK TABLES `users` WRITE;
/*!40000 ALTER TABLE `users` DISABLE KEYS */;

INSERT INTO `users` (`user_id`, `user_name`, `user_hash`, `user_token`)
VALUES
	(9,'mgo1869','$2b$12$EDHGRmiF/45jM2iUAOij9uplPs9sEJrl9mib6OPrKRzgBzB0C16BK',''),
	(10,'mgo81','$2b$12$rrxDPvKsv2gI5YT9qwG3secONeTy1HfFnomUziNzAaX3TCvuohEmK','5CU1DBO1WGNPQIG8EAN79HJC8TWXZ2WE'),
	(11,'rgo51','$2b$12$s2yO53txePJR2JQHZSPVOuj99PhEIdchCMVR7lDY47Y9A3ZP2X8YG',''),
	(12,'cme69','$2b$12$UItHmD9ague4kY.bA7mdTOpWsCuYvJRmliNP5dTVXk42d/qzKvwze','7ECPH9IIBDBHZ5IL0W3X9PCS65SEOPB1'),
	(13,'gcoc','$2b$12$04uBW/.0StaFfZnZ4QQwZuyiT5K2B/ddrInYFj2DdA6gxT.cHF1NK',NULL),
	(14,'testtest','$2b$12$iWLqEfco0Ihriyq6Q4ozU.bwK/YWXbRtEqVhzErA2o44V6PCXn8vW',NULL);

/*!40000 ALTER TABLE `users` ENABLE KEYS */;
UNLOCK TABLES;



/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;
/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
