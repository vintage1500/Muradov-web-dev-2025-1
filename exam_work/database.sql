-- MySQL dump 10.13  Distrib 8.0.42, for Win64 (x86_64)
--
-- Host: localhost    Database: exam_work_db
-- ------------------------------------------------------
-- Server version	8.0.42

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
-- Table structure for table `adoptions`
--

DROP TABLE IF EXISTS `adoptions`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `adoptions` (
  `id` int NOT NULL AUTO_INCREMENT,
  `animal_id` int NOT NULL,
  `user_id` int NOT NULL,
  `contact_info` varchar(255) NOT NULL,
  `created_at` date DEFAULT NULL,
  `status` varchar(32) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `animal_id` (`animal_id`),
  KEY `user_id` (`user_id`),
  CONSTRAINT `adoptions_ibfk_1` FOREIGN KEY (`animal_id`) REFERENCES `animals` (`id`) ON DELETE CASCADE,
  CONSTRAINT `adoptions_ibfk_2` FOREIGN KEY (`user_id`) REFERENCES `users` (`id`) ON DELETE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=8 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `adoptions`
--

LOCK TABLES `adoptions` WRITE;
/*!40000 ALTER TABLE `adoptions` DISABLE KEYS */;
INSERT INTO `adoptions` VALUES (1,1,1,'ivan@example.com, +79001234567','2025-06-22','rejected_adopted'),(2,2,1,'ivan@example.com, +79001234567','2025-06-22','approved'),(3,1,2,'╨£╤â╤Ç╨░╨┤╨╛╨▓ ╨á╨░╤â╨╗╤î ','2025-06-23','accepted'),(4,1,2,'╨£╤â╤Ç╨░╨┤╨╛╨▓ ╨á╨░╤â╨╗╤î ','2025-06-23','rejected');
/*!40000 ALTER TABLE `adoptions` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `alembic_version`
--

DROP TABLE IF EXISTS `alembic_version`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `alembic_version` (
  `version_num` varchar(32) NOT NULL,
  PRIMARY KEY (`version_num`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `alembic_version`
--

LOCK TABLES `alembic_version` WRITE;
/*!40000 ALTER TABLE `alembic_version` DISABLE KEYS */;
INSERT INTO `alembic_version` VALUES ('e83551433526');
/*!40000 ALTER TABLE `alembic_version` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `animals`
--

DROP TABLE IF EXISTS `animals`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `animals` (
  `id` int NOT NULL AUTO_INCREMENT,
  `name` varchar(64) DEFAULT NULL,
  `description` text NOT NULL,
  `age_months` int NOT NULL,
  `breed` varchar(64) NOT NULL,
  `gender` varchar(10) NOT NULL,
  `status` varchar(20) NOT NULL,
  `created_at` datetime DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=23 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `animals`
--

LOCK TABLES `animals` WRITE;
/*!40000 ALTER TABLE `animals` DISABLE KEYS */;
INSERT INTO `animals` VALUES (1,'╨æ╨░╤Ç╤ü╨╕╨║','╨ö╨╛╨▒╤Ç╤ï╨╣ ╨╕ ╨╗╨░╤ü╨║╨╛╨▓╤ï╨╣ ╨║╨╛╤é',24,'╨ö╨▓╨╛╤Ç╤Å╨╜╨╕╨╜','╨£','adopted','2025-06-22 18:05:53'),(2,'╨æ╨╡╨╗╨║╨░','╨í╨╛╨▒╨░╨║╨░-╨║╨╛╨╝╨┐╨░╨╜╤î╨╛╨╜, ╨╗╤Ä╨▒╨╕╤é ╨┤╨╡╤é╨╡╨╣',36,'╨¢╨░╨▒╤Ç╨░╨┤╨╛╤Ç','╨û','available','2025-06-22 18:05:53'),(14,'Test1','Test1',3,'Test1','male','available','2025-06-23 20:24:28'),(15,'Test2','Test2',4,'Test2','male','available','2025-06-23 20:24:49'),(16,'Test3','Test3',2,'Test3','male','available','2025-06-23 20:25:06'),(17,'Test4','Test4',1,'Test4','male','available','2025-06-23 20:25:20'),(18,'Test5','Test5',6,'Test5','male','available','2025-06-23 20:25:38'),(19,'Test6','Test6',2,'Test6','male','available','2025-06-23 20:25:49'),(20,'Test7','Test7',5,'Test7','male','available','2025-06-23 20:26:00'),(21,'Test8','Test8',12,'Test8','male','available','2025-06-23 20:26:12'),(22,'Test9','Test9',14,'Test9','male','available','2025-06-23 20:27:15');
/*!40000 ALTER TABLE `animals` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `photos`
--

DROP TABLE IF EXISTS `photos`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `photos` (
  `id` int NOT NULL AUTO_INCREMENT,
  `filename` varchar(255) NOT NULL,
  `mime_type` varchar(64) NOT NULL,
  `animal_id` int NOT NULL,
  PRIMARY KEY (`id`),
  KEY `animal_id` (`animal_id`),
  CONSTRAINT `photos_ibfk_1` FOREIGN KEY (`animal_id`) REFERENCES `animals` (`id`) ON DELETE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=14 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `photos`
--

LOCK TABLES `photos` WRITE;
/*!40000 ALTER TABLE `photos` DISABLE KEYS */;
INSERT INTO `photos` VALUES (1,'barsik.jpg','image/jpeg',1),(2,'belka.jpg','image/jpeg',2);
/*!40000 ALTER TABLE `photos` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `roles`
--

DROP TABLE IF EXISTS `roles`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `roles` (
  `id` int NOT NULL AUTO_INCREMENT,
  `name` varchar(64) NOT NULL,
  `description` text NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=5 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `roles`
--

LOCK TABLES `roles` WRITE;
/*!40000 ALTER TABLE `roles` DISABLE KEYS */;
INSERT INTO `roles` VALUES (1,'user','╨₧╨▒╤ï╤ç╨╜╤ï╨╣ ╨┐╨╛╨╗╤î╨╖╨╛╨▓╨░╤é╨╡╨╗╤î, ╨╝╨╛╨╢╨╡╤é ╨┐╨╛╨┤╨░╨▓╨░╤é╤î ╨╖╨░╤Å╨▓╨║╨╕ ╨╜╨░ ╤â╤ü╤ï╨╜╨╛╨▓╨╗╨╡╨╜╨╕╨╡'),(2,'admin','╨É╨┤╨╝╨╕╨╜╨╕╤ü╤é╤Ç╨░╤é╨╛╤Ç ╤ü ╨┐╨╛╨╗╨╜╤ï╨╝ ╨┤╨╛╤ü╤é╤â╨┐╨╛╨╝'),(3,'moderator','╨£╨╛╨┤╨╡╤Ç╨░╤é╨╛╤Ç, ╨╝╨╛╨╢╨╡╤é ╤â╨┐╤Ç╨░╨▓╨╗╤Å╤é╤î ╨╢╨╕╨▓╨╛╤é╨╜╤ï╨╝╨╕ ╨╕ ╨╖╨░╤Å╨▓╨║╨░╨╝╨╕'),(4,'user','╨₧╨▒╤ï╤ç╨╜╤ï╨╣ ╨┐╨╛╨╗╤î╨╖╨╛╨▓╨░╤é╨╡╨╗╤î');
/*!40000 ALTER TABLE `roles` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `users`
--

DROP TABLE IF EXISTS `users`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `users` (
  `id` int NOT NULL AUTO_INCREMENT,
  `username` varchar(64) NOT NULL,
  `password_hash` varchar(256) NOT NULL,
  `last_name` varchar(64) NOT NULL,
  `first_name` varchar(64) NOT NULL,
  `patronymic` varchar(64) DEFAULT NULL,
  `role_id` int NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `username` (`username`),
  KEY `role_id` (`role_id`),
  CONSTRAINT `users_ibfk_1` FOREIGN KEY (`role_id`) REFERENCES `roles` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=5 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `users`
--

LOCK TABLES `users` WRITE;
/*!40000 ALTER TABLE `users` DISABLE KEYS */;
INSERT INTO `users` VALUES (1,'admin','scrypt:32768:8:1$PIRb5kqmC8Us8w0R$878db374503b8f0c8a386e0f343d0e22eb503993046b2f4435f7230857a64642a81d72f03676543e53ba6e18c09f2f38d8ba1156a0067672f548c209352df63c','╨ÿ╨▓╨░╨╜╨╛╨▓','╨ÿ╨▓╨░╨╜','╨ÿ╨▓╨░╨╜╨╛╨▓╨╕╤ç',2),(2,'newuser','scrypt:32768:8:1$yHETzDgtIyRl00UM$b381b4574b87f9586eb8e53e27e7108315b44fda09a7a3756c15e2e97637c82301e57a505de3fbacf1a1c8193a4ea73139fdab741d44f24914cf428b5c1ac7eb','╨í╨╕╨┤╨╛╤Ç╨╛╨▓','╨ƒ╨╡╤é╤Ç','╨É╨╗╨╡╨║╤ü╨╡╨╡╨▓╨╕╤ç',4),(4,'moderator','scrypt:32768:8:1$g21rWB5UdSGJinHj$b2c5fb00111d500e06903363e300bddaaa550a5c049ae9dcd50d53ede837006c4e4d5a8a3a7852cb7af8929af537afe03d3872c9fc8dc6549cf8314be05ee83f','╨í╨╕╨┤╨╛╤Ç╨╛╨▓','╨ƒ╨╡╤é╤Ç','╨É╨╗╨╡╨║╤ü╨╡╨╡╨▓╨╕╤ç',3);
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

-- Dump completed on 2025-06-28  1:04:52
