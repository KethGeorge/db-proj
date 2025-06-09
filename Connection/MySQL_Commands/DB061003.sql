-- MySQL dump 10.13  Distrib 8.0.42, for Win64 (x86_64)
--
-- Host: localhost    Database: devexp
-- ------------------------------------------------------
-- Server version	8.0.42

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!50503 SET NAMES utf8 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `audit`
--

DROP TABLE IF EXISTS `audit`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `audit` (
  `AuditID` char(16) COLLATE utf8mb4_general_ci NOT NULL,
  `AuditTime` varchar(20) COLLATE utf8mb4_general_ci DEFAULT NULL,
  `Comment` varchar(200) COLLATE utf8mb4_general_ci DEFAULT NULL,
  `UserNo` char(8) COLLATE utf8mb4_general_ci NOT NULL,
  `ExperimentNo` char(16) COLLATE utf8mb4_general_ci NOT NULL,
  PRIMARY KEY (`AuditID`),
  KEY `UserNo` (`UserNo`),
  KEY `ExperimentNo` (`ExperimentNo`),
  CONSTRAINT `audit_ibfk_1` FOREIGN KEY (`UserNo`) REFERENCES `users` (`UserNo`),
  CONSTRAINT `audit_ibfk_2` FOREIGN KEY (`ExperimentNo`) REFERENCES `experiment` (`ExperimentNO`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `audit`
--

LOCK TABLES `audit` WRITE;
/*!40000 ALTER TABLE `audit` DISABLE KEYS */;
INSERT INTO `audit` VALUES ('AUD001','2023-10-01 10:00','实验数据合格','U001','EXP001'),('AUD002','2023-10-02 11:30','温度偏差需调整','U002','EXP002'),('AUD003','2023-10-03 12:45','混合时间不足','U003','EXP003'),('AUD004','2023-10-04 13:20','设备校准通过','U004','EXP004'),('AUD005','2023-10-05 14:15','材料用量正确','U005','EXP005'),('AUD006','2023-10-06 15:30','需重复实验验证','U006','EXP006'),('AUD007','2023-10-07 16:45','数据记录完整','U007','EXP007'),('AUD008','2023-10-08 09:10','温度传感器异常','U008','EXP008'),('AUD009','2023-10-09 10:25','实验步骤合规','U009','EXP009'),('AUD010','2023-10-10 11:40','需补充安全措施','U010','EXP010'),('AUD011','2023-10-11 12:55','结果符合预期','U011','EXP011'),('AUD012','2023-10-12 13:05','设备维护记录缺失','U012','EXP012'),('AUD013','2023-10-13 14:20','实验环境达标','U013','EXP013'),('AUD014','2023-10-14 15:35','数据波动较大','U014','EXP014'),('AUD015','2023-10-15 16:50','操作流程规范','U015','EXP015'),('AUD016','2023-10-16 08:15','需更换试剂批次','U016','EXP016'),('AUD017','2023-10-17 09:30','实验报告完整','U017','EXP017'),('AUD018','2023-10-18 10:45','仪器响应延迟','U018','EXP018'),('AUD019','2023-10-19 11:00','样品标识清晰','U019','EXP019'),('AUD020','2023-10-20 12:15','需优化混合速度','U020','EXP020'),('AUD021','2023-10-21 13:30','实验参数正确','U021','EXP021'),('AUD022','2023-10-22 14:45','设备温度超标','U022','EXP022'),('AUD023','2023-10-23 15:00','数据重复性良好','U023','EXP023'),('AUD024','2023-10-24 16:15','需清理设备残留','U024','EXP024'),('AUD025','2023-10-25 08:30','实验时间过长','U025','EXP025'),('AUD026','2023-10-26 09:45','结果超出误差范围','U026','EXP026'),('AUD027','2023-10-27 10:00','操作员培训合格','U027','EXP027'),('AUD028','2023-10-28 11:15','设备日志完整','U028','EXP028'),('AUD029','2023-10-29 12:30','需验证第三方数据','U029','EXP029'),('AUD030','2023-10-30 15:45','最终审核通过','U030','EXP030');
/*!40000 ALTER TABLE `audit` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `devexp`
--

DROP TABLE IF EXISTS `devexp`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `devexp` (
  `DevExpNo` char(36) COLLATE utf8mb4_general_ci NOT NULL,
  `DeviceNo` char(20) COLLATE utf8mb4_general_ci NOT NULL,
  `ExperimentNO` char(16) COLLATE utf8mb4_general_ci NOT NULL,
  PRIMARY KEY (`DevExpNo`),
  KEY `DeviceNo` (`DeviceNo`),
  KEY `ExperimentNO` (`ExperimentNO`),
  CONSTRAINT `devexp_ibfk_1` FOREIGN KEY (`DeviceNo`) REFERENCES `device` (`DeviceNo`),
  CONSTRAINT `devexp_ibfk_2` FOREIGN KEY (`ExperimentNO`) REFERENCES `experiment` (`ExperimentNO`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `devexp`
--

LOCK TABLES `devexp` WRITE;
/*!40000 ALTER TABLE `devexp` DISABLE KEYS */;
INSERT INTO `devexp` VALUES ('DEVEXP001','DEV001','EXP001'),('DEVEXP002','DEV002','EXP002'),('DEVEXP003','DEV003','EXP003'),('DEVEXP004','DEV004','EXP004'),('DEVEXP005','DEV005','EXP005'),('DEVEXP006','DEV006','EXP006'),('DEVEXP007','DEV007','EXP007'),('DEVEXP008','DEV008','EXP008'),('DEVEXP009','DEV009','EXP009'),('DEVEXP010','DEV010','EXP010'),('DEVEXP011','DEV011','EXP011'),('DEVEXP012','DEV012','EXP012'),('DEVEXP013','DEV013','EXP013'),('DEVEXP014','DEV014','EXP014'),('DEVEXP015','DEV015','EXP015'),('DEVEXP016','DEV016','EXP016'),('DEVEXP017','DEV017','EXP017'),('DEVEXP018','DEV018','EXP018'),('DEVEXP019','DEV019','EXP019'),('DEVEXP020','DEV020','EXP020'),('DEVEXP021','DEV021','EXP021'),('DEVEXP022','DEV022','EXP022'),('DEVEXP023','DEV023','EXP023'),('DEVEXP024','DEV024','EXP024'),('DEVEXP025','DEV025','EXP025'),('DEVEXP026','DEV026','EXP026'),('DEVEXP027','DEV027','EXP027'),('DEVEXP028','DEV028','EXP028'),('DEVEXP029','DEV029','EXP029'),('DEVEXP030','DEV030','EXP030');
/*!40000 ALTER TABLE `devexp` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `device`
--

DROP TABLE IF EXISTS `device`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `device` (
  `DeviceNo` char(20) COLLATE utf8mb4_general_ci NOT NULL,
  `DeviceName` char(200) COLLATE utf8mb4_general_ci NOT NULL,
  `DeviceUsage` varchar(10) COLLATE utf8mb4_general_ci DEFAULT NULL,
  `DStartTime` datetime DEFAULT NULL,
  `DMT` datetime DEFAULT NULL,
  `DStopTime` datetime DEFAULT NULL,
  PRIMARY KEY (`DeviceNo`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `device`
--

LOCK TABLES `device` WRITE;
/*!40000 ALTER TABLE `device` DISABLE KEYS */;
INSERT INTO `device` VALUES ('DEV001','黄昏',NULL,NULL,NULL,NULL),('DEV002','搅拌机','混合','2023-02-01 09:00:00','2023-07-01 14:00:00',NULL),('DEV003','离心机','分离','2023-03-01 10:00:00','2023-08-01 10:00:00','2023-12-01 18:00:00'),('DEV004','烘箱','干燥','2023-04-01 11:00:00',NULL,'2023-09-01 17:00:00'),('DEV005','粘度计','测量','2023-05-01 12:00:00','2023-10-01 09:00:00',NULL),('DEV006','pH计','检测','2023-06-01 13:00:00','2023-11-01 08:00:00',NULL),('DEV007','天平','称量','2023-07-01 14:00:00',NULL,'2024-01-01 16:00:00'),('DEV008','分光光度计','分析','2023-08-01 15:00:00','2024-02-01 14:00:00',NULL),('DEV009','超声波清洗机','清洗','2023-09-01 16:00:00','2024-03-01 12:00:00',NULL),('DEV010','电导率仪','检测','2023-10-01 17:00:00',NULL,'2024-04-01 10:00:00'),('DEV011','旋转蒸发仪','浓缩','2023-11-01 18:00:00','2024-05-01 09:00:00',NULL),('DEV012','马弗炉','高温处理','2023-12-01 19:00:00',NULL,'2024-06-01 08:00:00'),('DEV013','冻干机','冷冻干燥','2024-01-01 20:00:00','2024-07-01 07:00:00',NULL),('DEV014','紫外可见分光光度计','光谱分析','2024-02-01 21:00:00',NULL,'2024-08-01 06:00:00'),('DEV015','气相色谱仪','分离分析','2024-03-01 22:00:00','2024-09-01 05:00:00',NULL),('DEV016','液相色谱仪','分离分析','2024-04-01 23:00:00',NULL,'2024-10-01 04:00:00'),('DEV017','质谱仪','成分分析','2024-05-01 00:00:00','2024-11-01 03:00:00',NULL),('DEV018','原子吸收光谱仪','元素分析','2024-06-01 01:00:00',NULL,'2024-12-01 02:00:00'),('DEV019','热重分析仪','热分析','2024-07-01 02:00:00','2025-01-01 01:00:00',NULL),('DEV020','差示扫描量热仪','热分析','2024-08-01 03:00:00',NULL,'2025-02-01 00:00:00'),('DEV021','粒度分析仪','粒径测量','2024-09-01 04:00:00','2025-03-01 23:00:00',NULL),('DEV022','流变仪','流变测量','2024-10-01 05:00:00',NULL,'2025-04-01 22:00:00'),('DEV023','显微镜','显微观察','2024-11-01 06:00:00','2025-05-01 21:00:00',NULL),('DEV024','电泳仪','电泳分析','2024-12-01 07:00:00',NULL,'2025-06-01 20:00:00'),('DEV025','PCR仪','基因扩增','2025-01-01 08:00:00','2025-07-01 19:00:00',NULL),('DEV026','培养箱','细胞培养','2025-02-01 09:00:00',NULL,'2025-08-01 18:00:00'),('DEV027','灭菌锅','灭菌','2025-03-01 10:00:00','2025-09-01 17:00:00',NULL),('DEV028','超净工作台','无菌操作','2025-04-01 11:00:00',NULL,'2025-10-01 16:00:00'),('DEV029','生物安全柜','生物防护','2025-05-01 12:00:00','2025-11-01 15:00:00',NULL),('DEV030','光谱仪','检测','2023-03-30 10:00:00',NULL,'2023-09-30 18:00:00');
/*!40000 ALTER TABLE `device` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `experiment`
--

DROP TABLE IF EXISTS `experiment`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `experiment` (
  `ExperimentNO` char(16) COLLATE utf8mb4_general_ci NOT NULL,
  `MaterialCode` char(16) COLLATE utf8mb4_general_ci DEFAULT NULL,
  `HeatError` float DEFAULT NULL,
  `MixError` float DEFAULT NULL,
  `StartTime` time DEFAULT NULL,
  `EndTime` time DEFAULT NULL,
  `ProtocolNo` char(8) COLLATE utf8mb4_general_ci DEFAULT NULL,
  `UserNo` char(8) COLLATE utf8mb4_general_ci NOT NULL,
  PRIMARY KEY (`ExperimentNO`),
  KEY `MaterialCode` (`MaterialCode`),
  KEY `ProtocolNo` (`ProtocolNo`),
  KEY `UserNo` (`UserNo`),
  CONSTRAINT `experiment_ibfk_1` FOREIGN KEY (`MaterialCode`) REFERENCES `material` (`MaterialCode`),
  CONSTRAINT `experiment_ibfk_2` FOREIGN KEY (`ProtocolNo`) REFERENCES `protocol` (`ProtocolNo`),
  CONSTRAINT `experiment_ibfk_3` FOREIGN KEY (`UserNo`) REFERENCES `users` (`UserNo`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `experiment`
--

LOCK TABLES `experiment` WRITE;
/*!40000 ALTER TABLE `experiment` DISABLE KEYS */;
INSERT INTO `experiment` VALUES ('12312','MAT001',NULL,NULL,'22:16:13','22:16:14','P001','U001'),('ETST123','MAT001',213,213,'23:14:09','23:14:10','P005','U033'),('EXP-TEST-006','MAT001',1010,1010,'00:29:10','00:29:12','P002','U003'),('EXP-TEST-01','MAT001',45,540,'16:06:00','16:06:04','P002','U001'),('EXP001','MAT001',0.5,0.3,'09:00:00','11:30:00','P001','U001'),('EXP002','MAT002',0.7,0.2,'10:00:00','12:45:00','P002','U002'),('EXP003','MAT003',0.4,0.5,'08:30:00','10:15:00','P003','U003'),('EXP004','MAT004',0.6,0.4,'13:00:00','15:20:00','P004','U004'),('EXP005','MAT005',0.3,0.6,'14:30:00','17:00:00','P005','U005'),('EXP006','MAT006',0.8,0.1,'11:00:00','13:10:00','P006','U006'),('EXP007','MAT007',0.2,0.7,'16:00:00','18:30:00','P007','U007'),('EXP008','MAT008',0.9,0.2,'07:45:00','09:50:00','P008','U008'),('EXP009','MAT009',0.5,0.4,'10:30:00','12:40:00','P009','U009'),('EXP010','MAT010',0.4,0.3,'15:15:00','17:25:00','P010','U010'),('EXP011','MAT011',0.7,0.5,'08:00:00','10:05:00','P011','U011'),('EXP012','MAT012',0.6,0.6,'12:00:00','14:15:00','P012','U012'),('EXP013','MAT013',0.3,0.2,'09:45:00','11:55:00','P013','U013'),('EXP014','MAT014',0.8,0.4,'14:00:00','16:10:00','P014','U014'),('EXP015','MAT015',0.5,0.7,'10:20:00','12:30:00','P015','U015'),('EXP016','MAT016',0.2,0.1,'13:30:00','15:40:00','P016','U016'),('EXP017','MAT017',0.9,0.3,'16:45:00','18:55:00','P017','U017'),('EXP018','MAT018',0.4,0.5,'07:30:00','09:35:00','P018','U018'),('EXP019','MAT019',0.6,0.6,'11:10:00','13:20:00','P019','U019'),('EXP020','MAT020',0.3,0.4,'14:50:00','16:55:00','P020','U020'),('EXP021','MAT021',0.7,0.2,'08:15:00','10:25:00','P021','U021'),('EXP022','MAT022',0.5,0.3,'12:30:00','14:35:00','P022','U022'),('EXP023','MAT023',0.8,0.4,'15:00:00','17:05:00','P023','U023'),('EXP024','MAT024',0.4,0.5,'09:20:00','11:25:00','P024','U024'),('EXP025','MAT025',0.6,0.6,'13:40:00','15:45:00','P025','U025'),('EXP026','MAT026',0.3,0.7,'10:10:00','12:15:00','P026','U026'),('EXP027','MAT027',0.9,0.1,'16:20:00','18:25:00','P027','U027'),('EXP028','MAT028',0.5,0.2,'07:50:00','09:55:00','P028','U028'),('EXP029','MAT029',0.7,0.3,'11:30:00','13:35:00','P029','U029'),('EXP030','MAT030',0.4,0.6,'14:00:00','16:15:00','P030','U030');
/*!40000 ALTER TABLE `experiment` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `expreport`
--

DROP TABLE IF EXISTS `expreport`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `expreport` (
  `ExperimentCode` char(16) COLLATE utf8mb4_general_ci NOT NULL,
  `ExperimentNO` char(16) COLLATE utf8mb4_general_ci NOT NULL,
  `ExperimentName` varchar(20) COLLATE utf8mb4_general_ci DEFAULT NULL,
  `ExperimentalStatus` varchar(20) COLLATE utf8mb4_general_ci DEFAULT NULL,
  PRIMARY KEY (`ExperimentCode`),
  KEY `ExperimentNO` (`ExperimentNO`),
  CONSTRAINT `expreport_ibfk_1` FOREIGN KEY (`ExperimentNO`) REFERENCES `experiment` (`ExperimentNO`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `expreport`
--

LOCK TABLES `expreport` WRITE;
/*!40000 ALTER TABLE `expreport` DISABLE KEYS */;
INSERT INTO `expreport` VALUES ('REP001','EXP001','环氧固化测试','已完成'),('REP002','EXP002','聚氨酯粘度测试','进行中'),('REP003','EXP003','硅橡胶硬度测试','已归档'),('REP004','EXP004','聚乙烯密度测试','已完成'),('REP005','EXP005','聚丙烯拉伸测试','进行中'),('REP006','EXP006','PVC热稳定性测试','已终止'),('REP007','EXP007','PS透明度测试','已完成'),('REP008','EXP008','PC耐冲击测试','进行中'),('REP009','EXP009','POM耐磨测试','已归档'),('REP010','EXP010','PTFE摩擦系数测试','已完成'),('REP011','EXP011','尼龙66吸水率测试','进行中'),('REP012','EXP012','ABS抗老化测试','已终止'),('REP013','EXP013','聚酯固化时间测试','已完成'),('REP014','EXP014','酚醛耐热测试','进行中'),('REP015','EXP015','聚酰亚胺介电测试','已归档'),('REP016','EXP016','PEEK生物相容性测试','已完成'),('REP017','EXP017','PLA降解测试','进行中'),('REP018','EXP018','PU泡沫回弹测试','已终止'),('REP019','EXP019','PPS耐腐蚀测试','已完成'),('REP020','EXP020','PVDF介电强度测试','进行中'),('REP021','EXP021','PCL结晶度测试','已归档'),('REP022','EXP022','PB弹性测试','已完成'),('REP023','EXP023','PIP柔韧性测试','进行中'),('REP024','EXP024','PAN纤维强度测试','已终止'),('REP025','EXP025','PMMA透光率测试','已完成'),('REP026','EXP026','PET阻隔性测试','进行中'),('REP027','EXP027','PPO耐化学性测试','已归档'),('REP028','EXP028','PBI耐高温测试','已完成'),('REP029','EXP029','PPSU抗冲击测试','进行中'),('REP030','EXP030','尼龙6拉伸强度测试','已归档');
/*!40000 ALTER TABLE `expreport` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `hec`
--

DROP TABLE IF EXISTS `hec`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `hec` (
  `HEC` char(16) COLLATE utf8mb4_general_ci NOT NULL,
  `ExperimentCode` char(16) COLLATE utf8mb4_general_ci NOT NULL,
  `Temperature` float DEFAULT NULL,
  `Time1` time DEFAULT NULL,
  `SafeArea` float DEFAULT NULL,
  PRIMARY KEY (`HEC`,`ExperimentCode`),
  KEY `ExperimentCode` (`ExperimentCode`),
  CONSTRAINT `hec_ibfk_1` FOREIGN KEY (`ExperimentCode`) REFERENCES `expreport` (`ExperimentCode`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `hec`
--

LOCK TABLES `hec` WRITE;
/*!40000 ALTER TABLE `hec` DISABLE KEYS */;
INSERT INTO `hec` VALUES ('HEC001','REP001',25.5,'09:30:00',5),('HEC002','REP002',30,'10:15:00',6),('HEC003','REP003',28.5,'08:45:00',4.5),('HEC004','REP004',22,'13:30:00',3.8),('HEC005','REP005',35,'15:00:00',7.2),('HEC006','REP006',27.5,'11:30:00',5.5),('HEC007','REP007',20,'16:30:00',2.5),('HEC008','REP008',32,'08:15:00',6.8),('HEC009','REP009',18.5,'11:00:00',3),('HEC010','REP010',40,'15:45:00',8),('HEC011','REP011',24,'08:30:00',4),('HEC012','REP012',29,'12:45:00',5.7),('HEC013','REP013',19.5,'10:15:00',2.8),('HEC014','REP014',26,'14:30:00',6.2),('HEC015','REP015',33.5,'11:00:00',7.5),('HEC016','REP016',21,'14:00:00',3.5),('HEC017','REP017',36,'17:15:00',8.5),('HEC018','REP018',23.5,'08:00:00',4.2),('HEC019','REP019',31,'11:40:00',6.5),('HEC020','REP020',17,'15:20:00',2),('HEC021','REP021',34,'08:45:00',7),('HEC022','REP022',20.5,'13:00:00',3.2),('HEC023','REP023',37,'15:30:00',8.8),('HEC024','REP024',24.5,'09:50:00',4.8),('HEC025','REP025',28,'14:15:00',6),('HEC026','REP026',16.5,'10:40:00',1.8),('HEC027','REP027',38,'16:50:00',9),('HEC028','REP028',22.5,'08:25:00',3.7),('HEC029','REP029',39,'12:00:00',9.5),('HEC030','REP030',22,'15:00:00',7.5);
/*!40000 ALTER TABLE `hec` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `material`
--

DROP TABLE IF EXISTS `material`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `material` (
  `MaterialCode` char(16) COLLATE utf8mb4_general_ci NOT NULL,
  `MaterialName` varchar(20) COLLATE utf8mb4_general_ci DEFAULT NULL,
  PRIMARY KEY (`MaterialCode`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `material`
--

LOCK TABLES `material` WRITE;
/*!40000 ALTER TABLE `material` DISABLE KEYS */;
INSERT INTO `material` VALUES ('MAT001','D32 钢'),('MAT002','聚氨酯'),('MAT003','硅橡胶'),('MAT004','聚乙烯'),('MAT005','聚丙烯'),('MAT006','聚氯乙烯'),('MAT007','聚苯乙烯'),('MAT008','聚碳酸酯'),('MAT009','聚甲醛'),('MAT010','聚四氟乙烯'),('MAT011','尼龙66'),('MAT012','ABS塑料'),('MAT013','聚酯树脂'),('MAT014','酚醛树脂'),('MAT015','聚酰亚胺'),('MAT016','聚醚醚酮'),('MAT017','聚乳酸'),('MAT018','聚氨酯泡沫'),('MAT019','聚苯硫醚'),('MAT020','聚偏氟乙烯'),('MAT021','聚己内酯'),('MAT022','聚丁二烯'),('MAT023','聚异戊二烯'),('MAT024','聚丙烯腈'),('MAT025','聚甲基丙烯酸甲酯'),('MAT026','聚对苯二甲酸乙二醇酯'),('MAT027','聚苯醚'),('MAT028','聚苯并咪唑'),('MAT029','聚苯砜'),('MAT030','尼龙6'),('MAT_MANUAL_001','手动插入的通用材料');
/*!40000 ALTER TABLE `material` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `mec`
--

DROP TABLE IF EXISTS `mec`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `mec` (
  `MEC` char(16) COLLATE utf8mb4_general_ci NOT NULL,
  `ExperimentCode` char(16) COLLATE utf8mb4_general_ci NOT NULL,
  `HeightError` float DEFAULT NULL,
  `PlainError` float DEFAULT NULL,
  `ErrorArea` float DEFAULT NULL,
  `SpeedError` float DEFAULT NULL,
  `Time2` time DEFAULT NULL,
  PRIMARY KEY (`MEC`,`ExperimentCode`),
  KEY `ExperimentCode` (`ExperimentCode`),
  CONSTRAINT `mec_ibfk_1` FOREIGN KEY (`ExperimentCode`) REFERENCES `expreport` (`ExperimentCode`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `mec`
--

LOCK TABLES `mec` WRITE;
/*!40000 ALTER TABLE `mec` DISABLE KEYS */;
INSERT INTO `mec` VALUES ('MEC001','REP001',0.1,0.05,0.5,0.02,'09:45:00'),('MEC002','REP002',0.2,0.1,0.6,0.03,'10:30:00'),('MEC003','REP003',0.15,0.08,0.4,0.01,'09:00:00'),('MEC004','REP004',0.3,0.12,0.7,0.04,'14:00:00'),('MEC005','REP005',0.25,0.15,0.8,0.05,'15:30:00'),('MEC006','REP006',0.18,0.07,0.55,0.03,'12:00:00'),('MEC007','REP007',0.4,0.2,1,0.08,'17:00:00'),('MEC008','REP008',0.12,0.06,0.45,0.02,'08:30:00'),('MEC009','REP009',0.22,0.09,0.65,0.04,'11:15:00'),('MEC010','REP010',0.35,0.18,0.9,0.06,'16:10:00'),('MEC011','REP011',0.28,0.11,0.75,0.05,'09:15:00'),('MEC012','REP012',0.17,0.05,0.5,0.02,'13:20:00'),('MEC013','REP013',0.19,0.08,0.6,0.03,'10:45:00'),('MEC014','REP014',0.24,0.13,0.7,0.04,'15:00:00'),('MEC015','REP015',0.31,0.16,0.85,0.05,'11:30:00'),('MEC016','REP016',0.14,0.04,0.4,0.01,'14:45:00'),('MEC017','REP017',0.42,0.22,1.1,0.09,'17:45:00'),('MEC018','REP018',0.26,0.12,0.75,0.04,'08:15:00'),('MEC019','REP019',0.33,0.17,0.95,0.06,'12:30:00'),('MEC020','REP020',0.16,0.03,0.35,0.02,'16:00:00'),('MEC021','REP021',0.29,0.14,0.8,0.05,'09:30:00'),('MEC022','REP022',0.21,0.07,0.55,0.03,'13:45:00'),('MEC023','REP023',0.37,0.19,1.05,0.07,'16:20:00'),('MEC024','REP024',0.23,0.1,0.65,0.04,'10:10:00'),('MEC025','REP025',0.27,0.11,0.7,0.04,'14:30:00'),('MEC026','REP026',0.13,0.02,0.3,0.01,'11:00:00'),('MEC027','REP027',0.45,0.25,1.2,0.1,'17:30:00'),('MEC028','REP028',0.18,0.05,0.45,0.02,'08:50:00'),('MEC029','REP029',0.39,0.21,1,0.08,'13:00:00'),('MEC030','REP030',0.15,0.08,0.4,0.01,'15:20:00');
/*!40000 ALTER TABLE `mec` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `modification`
--

DROP TABLE IF EXISTS `modification`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `modification` (
  `ModificationID` varchar(36) COLLATE utf8mb4_general_ci NOT NULL,
  `OperationType` varchar(20) COLLATE utf8mb4_general_ci DEFAULT NULL,
  `OperationTime` datetime DEFAULT NULL,
  `UserNo` char(8) COLLATE utf8mb4_general_ci NOT NULL,
  `EntityType` varchar(20) COLLATE utf8mb4_general_ci DEFAULT NULL,
  `EntityID` varchar(20) COLLATE utf8mb4_general_ci DEFAULT NULL,
  `FieldName` varchar(20) COLLATE utf8mb4_general_ci DEFAULT NULL,
  `OldValue` varchar(100) COLLATE utf8mb4_general_ci DEFAULT NULL,
  `NewValue` varchar(100) COLLATE utf8mb4_general_ci DEFAULT NULL,
  PRIMARY KEY (`ModificationID`),
  KEY `UserNo` (`UserNo`),
  CONSTRAINT `modification_ibfk_1` FOREIGN KEY (`UserNo`) REFERENCES `users` (`UserNo`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `modification`
--

LOCK TABLES `modification` WRITE;
/*!40000 ALTER TABLE `modification` DISABLE KEYS */;
INSERT INTO `modification` VALUES ('393fed43-4580-11f0-a690-00ffc7429290','UPDATE','2025-06-10 06:22:26','ADMIN','Device','DEV001','DeviceName','恒温箱','黄昏'),('39400d80-4580-11f0-a690-00ffc7429290','UPDATE','2025-06-10 06:22:26','ADMIN','Device','DEV001','DeviceUsage','加热12324','造成一定的伤害。'),('53f684f4-4580-11f0-a690-00ffc7429290','UPDATE','2025-06-10 06:23:11','ADMIN','Device','DEV001','DeviceUsage','造成一定的伤害。',NULL),('99311982-4580-11f0-a690-00ffc7429290','INSERT','2025-06-10 06:25:07','ADMIN','Device','DEV-TEST-002','DeviceName',NULL,'星际物流塔'),('99311cbd-4580-11f0-a690-00ffc7429290','INSERT','2025-06-10 06:25:07','ADMIN','Device','DEV-TEST-002','DeviceUsage',NULL,'运输星际间的货物。'),('a005ada5-4580-11f0-a690-00ffc7429290','DELETE','2025-06-10 06:25:19','ADMIN','Device','DEV-TEST-002',NULL,NULL,NULL),('MOD001','UPDATE','2025-05-22 10:30:00','U001','User','U001','Password','old123','zhangsan123'),('MOD002','INSERT','2025-05-22 11:00:00','U002','Material','MAT002','Name',NULL,'聚氨酯'),('MOD003','DELETE','2025-05-22 12:15:00','U003','Device','DEV003','Status','active','inactive'),('MOD004','UPDATE','2025-05-22 13:45:00','U004','Protocol','P004','SHT','20.0','22.0'),('MOD005','INSERT','2025-05-22 14:20:00','U005','Experiment','EXP005','HeatError',NULL,'0.3'),('MOD006','DELETE','2025-05-22 15:10:00','U006','National_Standard','GB/T 006','Description','旧描述',NULL),('MOD007','UPDATE','2025-05-22 16:30:00','U007','User','U007','Email','old@lab.com','sunjiu@lab.com'),('MOD008','INSERT','2025-05-22 09:25:00','U008','Device','DEV008','DeviceUsage',NULL,'分析'),('MOD009','DELETE','2025-05-22 10:50:00','U009','Material','MAT009','Name','旧名称',NULL),('MOD010','UPDATE','2025-05-22 11:35:00','U010','Protocol','P010','MixingAngle','250.0','270.0'),('MOD011','INSERT','2025-05-22 12:40:00','U011','Experiment','EXP011','MixError',NULL,'0.5'),('MOD012','DELETE','2025-05-22 13:55:00','U012','Device','DEV012','DStopTime','2024-06-01 08:00:00',NULL),('MOD013','UPDATE','2025-05-22 14:10:00','U013','User','U013','Telephone','13800000013','13811111113'),('MOD014','INSERT','2025-05-22 15:20:00','U014','Material','MAT014','Name',NULL,'酚醛树脂'),('MOD015','DELETE','2025-05-22 16:45:00','U015','Protocol','P015','SMS','55.0',NULL),('MOD016','UPDATE','2025-05-22 08:05:00','U016','Experiment','EXP016','StartTime','13:00:00','13:30:00'),('MOD017','INSERT','2025-05-22 09:15:00','U017','Device','DEV017','DeviceName',NULL,'质谱仪'),('MOD018','DELETE','2025-05-22 10:25:00','U018','National_Standard','GB/T 018','StandardName','旧标准名',NULL),('MOD019','UPDATE','2025-05-22 11:50:00','U019','User','U019','Permissions','user','admin'),('MOD020','INSERT','2025-05-22 12:55:00','U020','Material','MAT020','Name',NULL,'聚偏氟乙烯'),('MOD021','DELETE','2025-05-22 13:30:00','U021','Protocol','P021','MixingRadius','20.0',NULL),('MOD022','UPDATE','2025-05-22 14:45:00','U022','Experiment','EXP022','EndTime','14:00:00','14:35:00'),('MOD023','INSERT','2025-05-22 15:50:00','U023','Device','DEV023','DStartTime',NULL,'2024-11-01 06:00:00'),('MOD024','DELETE','2025-05-22 16:05:00','U024','User','U024','Email','old@lab.com',NULL),('MOD025','UPDATE','2025-05-22 08:20:00','U025','Material','MAT025','MaterialName','旧名称','聚甲基丙烯酸甲酯'),('MOD026','INSERT','2025-05-22 09:35:00','U026','Protocol','P026','MeasurementInterval',NULL,'1.0'),('MOD027','DELETE','2025-05-22 10:40:00','U027','Experiment','EXP027','ProtocolNo','P027',NULL),('MOD028','UPDATE','2025-05-22 11:55:00','U028','Device','DEV028','DeviceUsage','操作','无菌操作'),('MOD029','INSERT','2025-05-22 12:10:00','U029','National_Standard','GB/T 029','Description',NULL,'聚苯砜抗冲击性能测试'),('MOD030','DELETE','2025-05-22 13:25:00','U030','User','U030','Permissions','guest',NULL);
/*!40000 ALTER TABLE `modification` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `mtec`
--

DROP TABLE IF EXISTS `mtec`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `mtec` (
  `MTEC` char(16) COLLATE utf8mb4_general_ci NOT NULL,
  `ExperimentCode` char(16) COLLATE utf8mb4_general_ci NOT NULL,
  `PhotoPath` varchar(20) COLLATE utf8mb4_general_ci DEFAULT NULL,
  `Is_solid` tinyint(1) DEFAULT NULL,
  `Time3` time DEFAULT NULL,
  PRIMARY KEY (`MTEC`,`ExperimentCode`),
  KEY `ExperimentCode` (`ExperimentCode`),
  CONSTRAINT `mtec_ibfk_1` FOREIGN KEY (`ExperimentCode`) REFERENCES `expreport` (`ExperimentCode`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `mtec`
--

LOCK TABLES `mtec` WRITE;
/*!40000 ALTER TABLE `mtec` DISABLE KEYS */;
INSERT INTO `mtec` VALUES ('MTEC001','REP001','/photos/exp1.jpg',1,'10:00:00'),('MTEC002','REP002','/photos/exp2.jpg',0,'11:00:00'),('MTEC003','REP003','/photos/exp3.jpg',1,'09:15:00'),('MTEC004','REP004','/photos/exp4.jpg',0,'14:30:00'),('MTEC005','REP005','/photos/exp5.jpg',1,'16:00:00'),('MTEC006','REP006','/photos/exp6.jpg',0,'12:15:00'),('MTEC007','REP007','/photos/exp7.jpg',1,'17:30:00'),('MTEC008','REP008','/photos/exp8.jpg',0,'09:00:00'),('MTEC009','REP009','/photos/exp9.jpg',1,'11:45:00'),('MTEC010','REP010','/photos/exp10.jpg',0,'16:45:00'),('MTEC011','REP011','/photos/exp11.jpg',1,'09:45:00'),('MTEC012','REP012','/photos/exp12.jpg',0,'13:45:00'),('MTEC013','REP013','/photos/exp13.jpg',1,'11:00:00'),('MTEC014','REP014','/photos/exp14.jpg',0,'15:15:00'),('MTEC015','REP015','/photos/exp15.jpg',1,'12:00:00'),('MTEC016','REP016','/photos/exp16.jpg',0,'15:30:00'),('MTEC017','REP017','/photos/exp17.jpg',1,'18:00:00'),('MTEC018','REP018','/photos/exp18.jpg',0,'08:30:00'),('MTEC019','REP019','/photos/exp19.jpg',1,'13:15:00'),('MTEC020','REP020','/photos/exp20.jpg',0,'16:30:00'),('MTEC021','REP021','/photos/exp21.jpg',1,'10:15:00'),('MTEC022','REP022','/photos/exp22.jpg',0,'14:00:00'),('MTEC023','REP023','/photos/exp23.jpg',1,'16:45:00'),('MTEC024','REP024','/photos/exp24.jpg',0,'10:40:00'),('MTEC025','REP025','/photos/exp25.jpg',1,'15:00:00'),('MTEC026','REP026','/photos/exp26.jpg',0,'11:30:00'),('MTEC027','REP027','/photos/exp27.jpg',1,'17:15:00'),('MTEC028','REP028','/photos/exp28.jpg',0,'09:20:00'),('MTEC029','REP029','/photos/exp29.jpg',1,'13:45:00'),('MTEC030','REP030','/photos/exp30.jpg',1,'16:00:00');
/*!40000 ALTER TABLE `mtec` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `national_standard`
--

DROP TABLE IF EXISTS `national_standard`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `national_standard` (
  `NSN` char(20) COLLATE utf8mb4_general_ci NOT NULL,
  `StandardName` varchar(50) COLLATE utf8mb4_general_ci DEFAULT NULL,
  `Description` varchar(200) COLLATE utf8mb4_general_ci DEFAULT NULL,
  `MaterialCode` char(16) COLLATE utf8mb4_general_ci NOT NULL,
  PRIMARY KEY (`NSN`),
  KEY `MaterialCode` (`MaterialCode`),
  CONSTRAINT `national_standard_ibfk_1` FOREIGN KEY (`MaterialCode`) REFERENCES `material` (`MaterialCode`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `national_standard`
--

LOCK TABLES `national_standard` WRITE;
/*!40000 ALTER TABLE `national_standard` DISABLE KEYS */;
INSERT INTO `national_standard` VALUES ('3PbXKBnx0P','1232222','','MAT_MANUAL_001'),('4HSJQ04CMK','123133','2312312333','MAT_MANUAL_001'),('6B1D3R9QW','ISO_9001_2015','Quality Management Systems','MAT001'),('aNSN-test1','Test11','123','MAT001'),('FLZc2gmkaT','123','123','MAT_MANUAL_001'),('GB/T 001','环氧固化标准','环氧树脂固化测试标准','MAT001'),('GB/T 002','聚氨酯粘度标准','聚氨酯粘度检测标准','MAT002'),('GB/T 003','硅橡胶硬度标准','硅橡胶硬度测定标准','MAT003'),('GB/T 004','聚乙烯密度标准','聚乙烯密度测试方法','MAT004'),('GB/T 005','聚丙烯拉伸标准','聚丙烯拉伸强度标准','MAT005'),('GB/T 006','PVC热稳定性标准','聚氯乙烯热稳定性测试','MAT006'),('GB/T 007','PS透明度标准','聚苯乙烯透明度检测','MAT007'),('GB/T 008','PC耐冲击标准','聚碳酸酯耐冲击测试','MAT008'),('GB/T 009','POM耐磨标准','聚甲醛耐磨性能标准','MAT009'),('GB/T 010','PTFE摩擦系数标准','聚四氟乙烯摩擦系数测定','MAT010'),('GB/T 011','尼龙66吸水率标准','尼龙66吸水率测试方法','MAT011'),('GB/T 012','ABS抗老化标准','ABS塑料抗老化测试','MAT012'),('GB/T 013','聚酯固化时间标准','聚酯树脂固化时间测定','MAT013'),('GB/T 014','酚醛耐热标准','酚醛树脂耐热性标准','MAT014'),('GB/T 015','聚酰亚胺介电标准','聚酰亚胺介电性能测试','MAT015'),('GB/T 016','PEEK生物相容性标准','聚醚醚酮生物相容性检测','MAT016'),('GB/T 017','PLA降解标准','聚乳酸降解性能测试','MAT017'),('GB/T 018','PU泡沫回弹标准','聚氨酯泡沫回弹性标准','MAT018'),('GB/T 019','PPS耐腐蚀标准','聚苯硫醚耐腐蚀性测试','MAT019'),('GB/T 020','PVDF介电强度标准','聚偏氟乙烯介电强度测定','MAT020'),('GB/T 021','PCL结晶度标准','聚己内酯结晶度测试','MAT021'),('GB/T 022','PB弹性标准','聚丁二烯弹性性能标准','MAT022'),('GB/T 023','PIP柔韧性标准','聚异戊二烯柔韧性测试','MAT023'),('GB/T 024','PAN纤维强度标准','聚丙烯腈纤维强度测定','MAT024'),('GB/T 025','PMMA透光率标准','聚甲基丙烯酸甲酯透光率测试','MAT025'),('GB/T 026','PET阻隔性标准','聚对苯二甲酸乙二醇酯阻隔性检测','MAT026'),('GB/T 027','PPO耐化学性标准','聚苯醚耐化学性测试','MAT027'),('GB/T 028','PBI耐高温标准','聚苯并咪唑耐高温性能标准','MAT028'),('GB/T 029','PPSU抗冲击标准','聚苯砜抗冲击性能测试','MAT029'),('GB/T 030','尼龙6拉伸强度标准','尼龙6拉伸强度测定方法','MAT030'),('gQKjBwdYrC','updated 123123','123','MAT_MANUAL_001'),('GryGP83YYv','updated 123123','123','MAT_MANUAL_001'),('h2DOTNA2kc','updated 20250528 0410','123','MAT_MANUAL_001'),('hbZnQ7fi3w','updated 20250528 0410','123','MAT_MANUAL_001'),('iDwcq5Jgya','123','123','MAT_MANUAL_001'),('JxtGmlykvZ','updated 20250528 0410','123','MAT_MANUAL_001'),('k9R27vCm3T','123','123','MAT_MANUAL_001'),('LpBwnQVDFA','updated currentlyNow','123','MAT_MANUAL_001'),('LqlTy9KdDH','123','123','MAT_MANUAL_001'),('NNrKMLmmN4','updated 20250528 0410','123','MAT_MANUAL_001'),('oKZ1tZJWAZ','123','123','MAT_MANUAL_001'),('QIVM6BZIDN','123133','2312312333','MAT_MANUAL_001'),('qmwMWWV9qT','updated 20250528 0410','123','MAT_MANUAL_001'),('STD-3T3VZ1T0','Test','123','MAT001'),('STD-Y75V7DIN','测试的国家标准','测试','MAT001'),('Vq8WnSA4Ty','updated 20250528 0410','123','MAT_MANUAL_001'),('VvBB7aWnME','123','123','MAT_MANUAL_001'),('vzQAQbqabz','updated 123123','123','MAT_MANUAL_001'),('WFCESRJMD3','123','123','MAT_MANUAL_001'),('WqpZz5Yhql','updated 123123','123','MAT_MANUAL_001'),('wunBdPlD73','updated 20250528 0410','123','MAT_MANUAL_001'),('WwFJCzAaWX','123','123','MAT_MANUAL_001'),('X3V4OIMRBJ','1231','23123123','MAT_MANUAL_001'),('YadooB94tu','updated 123123','123','MAT_MANUAL_001'),('YZR65gHVB2','updated currentlyNow','123','MAT_MANUAL_001'),('zEMQtNj33Y','updated 123123','123','MAT_MANUAL_001');
/*!40000 ALTER TABLE `national_standard` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `protocol`
--

DROP TABLE IF EXISTS `protocol`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `protocol` (
  `ProtocolNo` char(8) COLLATE utf8mb4_general_ci NOT NULL,
  `NSN` char(20) COLLATE utf8mb4_general_ci DEFAULT NULL,
  `SHT` float DEFAULT NULL,
  `SMS` float DEFAULT NULL,
  `MixingAngle` float DEFAULT NULL,
  `MixingRadius` float DEFAULT NULL,
  `MeasurementInterval` float DEFAULT NULL,
  `MaterialCode` char(16) COLLATE utf8mb4_general_ci NOT NULL,
  `UserNo` char(8) COLLATE utf8mb4_general_ci NOT NULL,
  PRIMARY KEY (`ProtocolNo`),
  KEY `NSN` (`NSN`),
  KEY `MaterialCode` (`MaterialCode`),
  KEY `UserNo` (`UserNo`),
  CONSTRAINT `protocol_ibfk_1` FOREIGN KEY (`NSN`) REFERENCES `national_standard` (`NSN`),
  CONSTRAINT `protocol_ibfk_2` FOREIGN KEY (`MaterialCode`) REFERENCES `material` (`MaterialCode`),
  CONSTRAINT `protocol_ibfk_3` FOREIGN KEY (`UserNo`) REFERENCES `users` (`UserNo`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `protocol`
--

LOCK TABLES `protocol` WRITE;
/*!40000 ALTER TABLE `protocol` DISABLE KEYS */;
INSERT INTO `protocol` VALUES ('P001','3PbXKBnx0P',25.5,50,30,10,10000,'MAT001','U001'),('P002','GB/T 002',30,45,45,15,10,'MAT002','U002'),('P003','GB/T 003',28.5,55,60,12,8,'MAT003','U003'),('P004','GB/T 004',22,40,90,8,3,'MAT004','U004'),('P005','GB/T 005',35,60,180,20,15,'MAT005','U005'),('P006','GB/T 006',27.5,48,120,18,12,'MAT006','U006'),('P007','GB/T 007',20,35,75,5,2,'MAT007','U007'),('P008','GB/T 008',32,52,150,25,20,'MAT008','U008'),('P009','GB/T 009',18.5,42,45,7,4,'MAT009','U009'),('P010','GB/T 010',40,65,270,30,25,'MAT010','U010'),('P011','GB/T 011',24,47,90,9,6,'MAT011','U011'),('P012','GB/T 012',29,53,135,22,18,'MAT012','U012'),('P013','GB/T 013',19.5,38,60,6,3,'MAT013','U013'),('P014','GB/T 014',26,49,180,15,10,'MAT014','U014'),('P015','GB/T 015',33.5,58,240,28,22,'MAT015','U015'),('P016','GB/T 016',21,43,30,4,1,'MAT016','U016'),('P017','GB/T 017',36,62,300,35,30,'MAT017','U017'),('P018','GB/T 018',23.5,46,90,10,7,'MAT018','U018'),('P019','GB/T 019',31,54,150,20,15,'MAT019','U019'),('P020','GB/T 020',17,37,45,5,2,'MAT020','U020'),('P021','GB/T 021',34,59,210,25,18,'MAT021','U021'),('P022','GB/T 022',20.5,41,75,8,4,'MAT022','U022'),('P023','GB/T 023',37,63,270,32,28,'MAT023','U023'),('P024','GB/T 024',24.5,48,120,12,9,'MAT024','U024'),('P025','GB/T 025',28,51,180,18,12,'MAT025','U025'),('P026','GB/T 026',16.5,36,30,3,1,'MAT026','U026'),('P027','GB/T 027',38,64,240,30,25,'MAT027','U027'),('P028','GB/T 028',22.5,44,90,7,5,'MAT028','U028'),('P029','GB/T 029',39,66,300,40,35,'MAT029','U029'),('P030','GB/T 030',22,48.5,60,20,15,'MAT030','U030'),('PTest001','GB/T 001',123,123,45,67,98,'MAT001','QL0FSAC6');
/*!40000 ALTER TABLE `protocol` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `users`
--

DROP TABLE IF EXISTS `users`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `users` (
  `UserNo` char(8) COLLATE utf8mb4_general_ci NOT NULL,
  `UserName` char(20) COLLATE utf8mb4_general_ci NOT NULL,
  `UserPassword` char(20) COLLATE utf8mb4_general_ci NOT NULL,
  `UserPermissions` char(5) COLLATE utf8mb4_general_ci DEFAULT NULL,
  `Email` varchar(255) COLLATE utf8mb4_general_ci DEFAULT NULL,
  `Telephone` char(13) COLLATE utf8mb4_general_ci DEFAULT NULL,
  PRIMARY KEY (`UserNo`),
  CONSTRAINT `users_chk_1` CHECK ((length(`UserPassword`) >= 4))
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `users`
--

LOCK TABLES `users` WRITE;
/*!40000 ALTER TABLE `users` DISABLE KEYS */;
INSERT INTO `users` VALUES ('ADMIN','tumu1t','tumumu1tt','admin','tumu1222t@lab.com','123123123'),('BKGSGSU2','admin1111','admin','user','asfdsafd@pp.com',''),('K3IB3QTA','adminqq','admin','user','qerwer@lab.com',''),('QL0FSAC6','admin123123','admin2','user','asfdsafd1@pp.com','123123'),('SX56C9F0','admin1','123123123','admin','kethgeorgeov22o@gmail.com','123123123123'),('U001','张三1','zhangsan123','admin','zhangsan@lab.com','13800000001'),('U002','李四','lisi4567','user','lisi@lab.com','13800000002'),('U003','王五','wangwu890','user','wangwu@lab.com','13800000003'),('U004','赵六','zhaoliu654','guest','zhaoliu@lab.com','13800000004'),('U005','陈七','chenqi789','user','chenqi@lab.com','13800000005'),('U006','刘八','liuba321','admin','liuba@lab.com','13800000006'),('U007','孙九','sunjiu123','user','sunjiu@lab.com','13800000007'),('U008','周十','zhoushi456','guest','zhoushi@lab.com','13800000008'),('U009','吴十一','wusy789','user','wusy@lab.com','13800000009'),('U010','郑十二','zhengse123','admin','zhengse@lab.com','13800000010'),('U011','冯十三','fengss456','user','fengss@lab.com','13800000011'),('U012','蒋十四','jiangss789','guest','jiangss@lab.com','13800000012'),('U013','沈十五','shensw123','user','shensw@lab.com','13800000013'),('U014','韩十六','hansl456','admin','hansl@lab.com','13800000014'),('U015','杨十七','yangsq789','user','yangsq@lab.com','13800000015'),('U016','朱十八','zhushb123','guest','zhushb@lab.com','13800000016'),('U017','秦十九','qinsj456','user','qinsj@lab.com','13800000017'),('U018','许二十','xues789','admin','xues@lab.com','13800000018'),('U019','何廿一','henian123','user','henian@lab.com','13800000019'),('U020','吕廿二','lvne456','guest','lvne@lab.com','13800000020'),('U021','施廿三','shinn789','user','shinn@lab.com','13800000021'),('U022','张廿四','zhangns123','admin','zhangns@lab.com','13800000022'),('U023','孔廿五','kongnw456','user','kongnw@lab.com','13800000023'),('U024','曹廿六','caonl789','guest','caonl@lab.com','13800000024'),('U025','严廿七','yannq123','user','yannq@lab.com','13800000025'),('U026','华廿八','huanb456','admin','huanb@lab.com','13800000026'),('U027','金廿九','jinnj789','user','jinnj@lab.com','13800000027'),('U028','魏三十','weiss123','guest','weiss@lab.com','13800000028'),('U029','陶三一','taosy456','user','taosy@lab.com','13800000029'),('U030','姜三二','jiangse789','admin','jiangse@lab.com','13800000030'),('U031','新用户','newpassword123','user','newuser@lab.com','13800000031'),('U032','admin','admin','admin','adminadmin@lab.com','13800138001'),('U033','user','user','user','useruser@lab.com','13800138002');
/*!40000 ALTER TABLE `users` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Temporary view structure for view `v_modification_details`
--

DROP TABLE IF EXISTS `v_modification_details`;
/*!50001 DROP VIEW IF EXISTS `v_modification_details`*/;
SET @saved_cs_client     = @@character_set_client;
/*!50503 SET character_set_client = utf8mb4 */;
/*!50001 CREATE VIEW `v_modification_details` AS SELECT 
 1 AS `ModificationID`,
 1 AS `OperationType`,
 1 AS `OperationTime`,
 1 AS `OperatorUserNo`,
 1 AS `OperatorUserName`,
 1 AS `EntityType`,
 1 AS `EntityID`,
 1 AS `FieldName`,
 1 AS `OldValue`,
 1 AS `NewValue`*/;
SET character_set_client = @saved_cs_client;

--
-- Final view structure for view `v_modification_details`
--

/*!50001 DROP VIEW IF EXISTS `v_modification_details`*/;
/*!50001 SET @saved_cs_client          = @@character_set_client */;
/*!50001 SET @saved_cs_results         = @@character_set_results */;
/*!50001 SET @saved_col_connection     = @@collation_connection */;
/*!50001 SET character_set_client      = utf8mb4 */;
/*!50001 SET character_set_results     = utf8mb4 */;
/*!50001 SET collation_connection      = utf8mb4_0900_ai_ci */;
/*!50001 CREATE ALGORITHM=UNDEFINED */
/*!50013 DEFINER=`root`@`localhost` SQL SECURITY DEFINER */
/*!50001 VIEW `v_modification_details` AS select `m`.`ModificationID` AS `ModificationID`,`m`.`OperationType` AS `OperationType`,`m`.`OperationTime` AS `OperationTime`,`m`.`UserNo` AS `OperatorUserNo`,`u`.`UserName` AS `OperatorUserName`,`m`.`EntityType` AS `EntityType`,`m`.`EntityID` AS `EntityID`,`m`.`FieldName` AS `FieldName`,`m`.`OldValue` AS `OldValue`,`m`.`NewValue` AS `NewValue` from (`modification` `m` left join `users` `u` on((`m`.`UserNo` = `u`.`UserNo`))) */;
/*!50001 SET character_set_client      = @saved_cs_client */;
/*!50001 SET character_set_results     = @saved_cs_results */;
/*!50001 SET collation_connection      = @saved_col_connection */;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2025-06-10  7:00:51
