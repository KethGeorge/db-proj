DELIMITER $$

CREATE TRIGGER trg_users_after_insert
AFTER INSERT ON users
FOR EACH ROW
BEGIN
    DECLARE current_operator_no CHAR(8);
    SET current_operator_no = @current_user_id;
    IF current_operator_no IS NULL THEN
        SET current_operator_no = 'SYSTEM';
    END IF;

    -- 对每一个被插入的字段，如果它不是NULL，就记录下来
    -- NEW 关键字代表新插入的这一行数据
    IF NEW.UserName IS NOT NULL THEN
        INSERT INTO modification (ModificationID, OperationType, OperationTime, UserNo, EntityType, EntityID, FieldName, OldValue, NewValue)
        VALUES (UUID(), 'INSERT', NOW(), current_operator_no, 'User', NEW.UserNo, 'UserName', NULL, NEW.UserName);
    END IF;
    -- 对于密码，我们只记录事件，不记录值
    IF NEW.UserPassword IS NOT NULL THEN
        INSERT INTO modification (ModificationID, OperationType, OperationTime, UserNo, EntityType, EntityID, FieldName, OldValue, NewValue)
        VALUES (UUID(), 'INSERT', NOW(), current_operator_no, 'User', NEW.UserNo, 'UserPassword', NULL, '******');
    END IF;
    IF NEW.UserPermissions IS NOT NULL THEN
        INSERT INTO modification (ModificationID, OperationType, OperationTime, UserNo, EntityType, EntityID, FieldName, OldValue, NewValue)
        VALUES (UUID(), 'INSERT', NOW(), current_operator_no, 'User', NEW.UserNo, 'UserPermissions', NULL, NEW.UserPermissions);
    END IF;
    IF NEW.Email IS NOT NULL THEN
        INSERT INTO modification (ModificationID, OperationType, OperationTime, UserNo, EntityType, EntityID, FieldName, OldValue, NewValue)
        VALUES (UUID(), 'INSERT', NOW(), current_operator_no, 'User', NEW.UserNo, 'Email', NULL, NEW.Email);
    END IF;
    IF NEW.Telephone IS NOT NULL THEN
        INSERT INTO modification (ModificationID, OperationType, OperationTime, UserNo, EntityType, EntityID, FieldName, OldValue, NewValue)
        VALUES (UUID(), 'INSERT', NOW(), current_operator_no, 'User', NEW.UserNo, 'Telephone', NULL, NEW.Telephone);
    END IF;
END$$

DELIMITER ;

DELIMITER $$

CREATE TRIGGER trg_users_after_update
AFTER UPDATE ON users
FOR EACH ROW
BEGIN
    DECLARE current_operator_no CHAR(8);
    SET current_operator_no = @current_user_id;
    IF current_operator_no IS NULL THEN
        SET current_operator_no = 'SYSTEM';
    END IF;

    -- 使用 NULL-safe <=> 比较操作符，逐个检查字段是否发生变化
    -- OLD 代表更新前的行，NEW 代表更新后的行
    IF NOT (OLD.UserName <=> NEW.UserName) THEN
        INSERT INTO modification (ModificationID, OperationType, OperationTime, UserNo, EntityType, EntityID, FieldName, OldValue, NewValue)
        VALUES (UUID(), 'UPDATE', NOW(), current_operator_no, 'User', OLD.UserNo, 'UserName', OLD.UserName, NEW.UserName);
    END IF;
    IF NOT (OLD.UserPassword <=> NEW.UserPassword) THEN
        INSERT INTO modification (ModificationID, OperationType, OperationTime, UserNo, EntityType, EntityID, FieldName, OldValue, NewValue)
        VALUES (UUID(), 'UPDATE', NOW(), current_operator_no, 'User', OLD.UserNo, 'UserPassword', '******', '******');
    END IF;
    IF NOT (OLD.UserPermissions <=> NEW.UserPermissions) THEN
        INSERT INTO modification (ModificationID, OperationType, OperationTime, UserNo, EntityType, EntityID, FieldName, OldValue, NewValue)
        VALUES (UUID(), 'UPDATE', NOW(), current_operator_no, 'User', OLD.UserNo, 'UserPermissions', OLD.UserPermissions, NEW.UserPermissions);
    END IF;
    IF NOT (OLD.Email <=> NEW.Email) THEN
        INSERT INTO modification (ModificationID, OperationType, OperationTime, UserNo, EntityType, EntityID, FieldName, OldValue, NewValue)
        VALUES (UUID(), 'UPDATE', NOW(), current_operator_no, 'User', OLD.UserNo, 'Email', OLD.Email, NEW.Email);
    END IF;
    IF NOT (OLD.Telephone <=> NEW.Telephone) THEN
        INSERT INTO modification (ModificationID, OperationType, OperationTime, UserNo, EntityType, EntityID, FieldName, OldValue, NewValue)
        VALUES (UUID(), 'UPDATE', NOW(), current_operator_no, 'User', OLD.UserNo, 'Telephone', OLD.Telephone, NEW.Telephone);
    END IF;
END$$

DELIMITER ;

DELIMITER $$

CREATE TRIGGER trg_users_after_delete
AFTER DELETE ON users
FOR EACH ROW
BEGIN
    DECLARE current_operator_no CHAR(8);
    SET current_operator_no = @current_user_id;
    IF current_operator_no IS NULL THEN
        SET current_operator_no = 'SYSTEM';
    END IF;

    -- 只需记录一条删除日志即可，无需关心具体字段
    -- OLD 关键字代表被删除的那一行数据
    INSERT INTO modification (ModificationID, OperationType, OperationTime, UserNo, EntityType, EntityID, FieldName, OldValue, NewValue)
    VALUES (UUID(), 'DELETE', NOW(), current_operator_no, 'User', OLD.UserNo, NULL, NULL, NULL);
END$$

DELIMITER ;

DELIMITER $$

CREATE TRIGGER trg_material_after_insert
AFTER INSERT ON material
FOR EACH ROW
BEGIN
    DECLARE current_operator_no CHAR(8);
    SET current_operator_no = @current_user_id;
    IF current_operator_no IS NULL THEN
        SET current_operator_no = 'SYSTEM';
    END IF;

    IF NEW.MaterialName IS NOT NULL THEN
        INSERT INTO modification (ModificationID, OperationType, OperationTime, UserNo, EntityType, EntityID, FieldName, OldValue, NewValue)
        VALUES (UUID(), 'INSERT', NOW(), current_operator_no, 'Material', NEW.MaterialCode, 'MaterialName', NULL, NEW.MaterialName);
    END IF;
END$$

DELIMITER ;

DELIMITER $$

CREATE TRIGGER trg_material_after_update
AFTER UPDATE ON material
FOR EACH ROW
BEGIN
    DECLARE current_operator_no CHAR(8);
    SET current_operator_no = @current_user_id;
    IF current_operator_no IS NULL THEN
        SET current_operator_no = 'SYSTEM';
    END IF;

    IF NOT (OLD.MaterialName <=> NEW.MaterialName) THEN
        INSERT INTO modification (ModificationID, OperationType, OperationTime, UserNo, EntityType, EntityID, FieldName, OldValue, NewValue)
        VALUES (UUID(), 'UPDATE', NOW(), current_operator_no, 'Material', OLD.MaterialCode, 'MaterialName', OLD.MaterialName, NEW.MaterialName);
    END IF;
END$$

DELIMITER ;

DELIMITER $$

CREATE TRIGGER trg_material_after_delete
AFTER DELETE ON material
FOR EACH ROW
BEGIN
    DECLARE current_operator_no CHAR(8);
    SET current_operator_no = @current_user_id;
    IF current_operator_no IS NULL THEN
        SET current_operator_no = 'SYSTEM';
    END IF;

    INSERT INTO modification (ModificationID, OperationType, OperationTime, UserNo, EntityType, EntityID, FieldName, OldValue, NewValue)
    VALUES (UUID(), 'DELETE', NOW(), current_operator_no, 'Material', OLD.MaterialCode, NULL, NULL, NULL);
END$$

DELIMITER ;

DELIMITER $$

CREATE TRIGGER trg_device_after_insert
AFTER INSERT ON device
FOR EACH ROW
BEGIN
    DECLARE current_operator_no CHAR(8);
    SET current_operator_no = @current_user_id;
    IF current_operator_no IS NULL THEN
        SET current_operator_no = 'SYSTEM';
    END IF;

    -- 假设审计 device 表的所有字段
    IF NEW.DeviceName IS NOT NULL THEN
        INSERT INTO modification (ModificationID, OperationType, OperationTime, UserNo, EntityType, EntityID, FieldName, OldValue, NewValue)
        VALUES (UUID(), 'INSERT', NOW(), current_operator_no, 'Device', NEW.DeviceNo, 'DeviceName', NULL, NEW.DeviceName);
    END IF;
    IF NEW.DeviceUsage IS NOT NULL THEN
        INSERT INTO modification (ModificationID, OperationType, OperationTime, UserNo, EntityType, EntityID, FieldName, OldValue, NewValue)
        VALUES (UUID(), 'INSERT', NOW(), current_operator_no, 'Device', NEW.DeviceNo, 'DeviceUsage', NULL, NEW.DeviceUsage);
    END IF;
    -- ... 为 DStartTime, DMT, DStopTime, Operator 等字段添加类似的 IF 块 ...
END$$

DELIMITER ;

DELIMITER $$

CREATE TRIGGER trg_device_after_update
AFTER UPDATE ON device
FOR EACH ROW
BEGIN
    DECLARE current_operator_no CHAR(8);
    SET current_operator_no = @current_user_id;
    IF current_operator_no IS NULL THEN
        SET current_operator_no = 'SYSTEM';
    END IF;

    IF NOT (OLD.DeviceName <=> NEW.DeviceName) THEN
        INSERT INTO modification (ModificationID, OperationType, OperationTime, UserNo, EntityType, EntityID, FieldName, OldValue, NewValue)
        VALUES (UUID(), 'UPDATE', NOW(), current_operator_no, 'Device', OLD.DeviceNo, 'DeviceName', OLD.DeviceName, NEW.DeviceName);
    END IF;
    IF NOT (OLD.DeviceUsage <=> NEW.DeviceUsage) THEN
        INSERT INTO modification (ModificationID, OperationType, OperationTime, UserNo, EntityType, EntityID, FieldName, OldValue, NewValue)
        VALUES (UUID(), 'UPDATE', NOW(), current_operator_no, 'Device', OLD.DeviceNo, 'DeviceUsage', OLD.DeviceUsage, NEW.DeviceUsage);
    END IF;
    -- ... 为 DStartTime, DMT, DStopTime, Operator 等字段添加类似的 IF 块 ...
END$$

DELIMITER ;

DELIMITER $$

CREATE TRIGGER trg_device_after_delete
AFTER DELETE ON device
FOR EACH ROW
BEGIN
    DECLARE current_operator_no CHAR(8);
    SET current_operator_no = @current_user_id;
    IF current_operator_no IS NULL THEN
        SET current_operator_no = 'SYSTEM';
    END IF;

    INSERT INTO modification (ModificationID, OperationType, OperationTime, UserNo, EntityType, EntityID, FieldName, OldValue, NewValue)
    VALUES (UUID(), 'DELETE', NOW(), current_operator_no, 'Device', OLD.DeviceNo, NULL, NULL, NULL);
END$$

DELIMITER ;