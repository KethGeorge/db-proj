-- 1. 创建数据库
CREATE DATABASE IF NOT EXISTS `凝胶时间测定` 
CHARACTER SET utf8mb4 
COLLATE utf8mb4_general_ci;

USE `凝胶时间测定`;

-- 2. 创建基本表（无外键依赖）
CREATE TABLE IF NOT EXISTS `users` (
    UserNo CHAR(8) PRIMARY KEY,
    UserName CHAR(20) NOT NULL,
    UserPassword CHAR(20) NOT NULL CHECK (LENGTH(UserPassword) >= 6),
    UserPermissions CHAR(5),
    Email VARCHAR(20),
    Telephone CHAR(13)
) ENGINE=InnoDB;

CREATE TABLE IF NOT EXISTS Material (
    MaterialCode CHAR(16) PRIMARY KEY,
    MaterialName VARCHAR(20)
) ENGINE=InnoDB;

CREATE TABLE IF NOT EXISTS Device (
    DeviceNo CHAR(20) PRIMARY KEY,
    DeviceName CHAR(8) NOT NULL,
    DeviceUsage VARCHAR(10),
    DStartTime DATETIME,
    DMT DATETIME,
    DStopTime DATETIME
) ENGINE=InnoDB;

-- 3. 创建依赖表
CREATE TABLE IF NOT EXISTS National_Standard (
    NSN CHAR(20) PRIMARY KEY,
    StandardName VARCHAR(50),
    Description VARCHAR(200),
    MaterialCode CHAR(16) NOT NULL,
    FOREIGN KEY (MaterialCode) REFERENCES Material(MaterialCode)
) ENGINE=InnoDB;

CREATE TABLE IF NOT EXISTS Protocol (
    ProtocolNo CHAR(8) PRIMARY KEY,
    NSN CHAR(20),
    SHT FLOAT,
    SMS FLOAT,
    MixingAngle FLOAT,
    MixingRadius FLOAT,
    MeasurementInterval FLOAT,
    MaterialCode CHAR(16) NOT NULL,
    UserNo CHAR(8) NOT NULL,
    FOREIGN KEY (NSN) REFERENCES National_Standard(NSN),
    FOREIGN KEY (MaterialCode) REFERENCES Material(MaterialCode),
    FOREIGN KEY (UserNo) REFERENCES `Users`(UserNo)
) ENGINE=InnoDB;

CREATE TABLE IF NOT EXISTS Experiment (
    ExperimentNO CHAR(16) PRIMARY KEY,
    MaterialCode CHAR(16),
    HeatError FLOAT(6),
    MixError FLOAT(6),
    StartTime TIME,
    EndTime TIME,
    ProtocolNo CHAR(8),
    UserNo CHAR(8) NOT NULL,
    FOREIGN KEY (MaterialCode) REFERENCES Material(MaterialCode),
    FOREIGN KEY (ProtocolNo) REFERENCES Protocol(ProtocolNo),
    FOREIGN KEY (UserNo) REFERENCES `Users`(UserNo)
) ENGINE=InnoDB;

-- 4. 创建关联表
CREATE TABLE IF NOT EXISTS Modification (
    ModificationID CHAR(16) PRIMARY KEY,
    OperationType VARCHAR(20),
    OperationTime TIME,
    UserNo CHAR(8) NOT NULL,
    EntityType VARCHAR(20),
    EntityID VARCHAR(20),
    FieldName VARCHAR(20),
    OldValue VARCHAR(100),
    NewValue VARCHAR(100),
    FOREIGN KEY (UserNo) REFERENCES `Users`(UserNo)
) ENGINE=InnoDB;

CREATE TABLE IF NOT EXISTS Audit (
    AuditID CHAR(16) PRIMARY KEY,
    AuditTime VARCHAR(20),
    Comment VARCHAR(200),
    UserNo CHAR(8) NOT NULL,
    ExperimentNo CHAR(16) NOT NULL,
    FOREIGN KEY (UserNo) REFERENCES `Users`(UserNo),
    FOREIGN KEY (ExperimentNo) REFERENCES Experiment(ExperimentNO)
) ENGINE=InnoDB;

CREATE TABLE IF NOT EXISTS ExpReport (
    ExperimentCode CHAR(16) PRIMARY KEY,
    ExperimentNO CHAR(16) NOT NULL,
    ExperimentName VARCHAR(20),
    ExperimentalStatus VARCHAR(20),
    FOREIGN KEY (ExperimentNO) REFERENCES Experiment(ExperimentNO)
) ENGINE=InnoDB;

-- 5. 创建弱实体表
CREATE TABLE IF NOT EXISTS HEC (
    HEC CHAR(16) NOT NULL,
    ExperimentCode CHAR(16) NOT NULL,
    Temperature FLOAT(6),
    Time1 TIME,
    SafeArea FLOAT(6),
    PRIMARY KEY (HEC, ExperimentCode),
    FOREIGN KEY (ExperimentCode) REFERENCES ExpReport(ExperimentCode)
) ENGINE=InnoDB;

CREATE TABLE IF NOT EXISTS MEC (
    MEC CHAR(16) NOT NULL,
    ExperimentCode CHAR(16) NOT NULL,
    HeightError FLOAT(6),
    PlainError FLOAT(6),
    ErrorArea FLOAT(6),
    SpeedError FLOAT(6),
    Time2 TIME,
    PRIMARY KEY (MEC, ExperimentCode),
    FOREIGN KEY (ExperimentCode) REFERENCES ExpReport(ExperimentCode)
) ENGINE=InnoDB;

CREATE TABLE IF NOT EXISTS MTEC (
    MTEC CHAR(16) NOT NULL,
    ExperimentCode CHAR(16) NOT NULL,
    PhotoPath VARCHAR(20),
    Is_solid BOOLEAN,
    Time3 TIME,
    PRIMARY KEY (MTEC, ExperimentCode),
    FOREIGN KEY (ExperimentCode) REFERENCES ExpReport(ExperimentCode)
) ENGINE=InnoDB;

-- 6. 创建联系表
CREATE TABLE IF NOT EXISTS DevExp (
    DevExpNo CHAR(36) PRIMARY KEY,
    DeviceNo CHAR(20) NOT NULL,
    ExperimentNO CHAR(16) NOT NULL,
    FOREIGN KEY (DeviceNo) REFERENCES Device(DeviceNo),
    FOREIGN KEY (ExperimentNO) REFERENCES Experiment(ExperimentNO)
) ENGINE=InnoDB;