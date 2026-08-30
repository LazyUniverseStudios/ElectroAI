CREATE SCHEMA IF NOT EXISTS `ElectroAI`;

SET time_zone = '+00:00';

CREATE TABLE IF NOT EXISTS `ElectroAI`.`Users` (
    `UserID` BIGINT UNSIGNED NOT NULL,

    PRIMARY KEY (`UserID`)
);

CREATE TABLE IF NOT EXISTS `ElectroAI`.`Leveling`(
    `UserID` BIGINT UNSIGNED NOT NULL,
    `Level` BIGINT UNSIGNED NOT NULL DEFAULT 0,
    `XP` BIGINT UNSIGNED NOT NULL DEFAULT 0,
    `XPForNextLevel` BIGINT UNSIGNED NOT NULL DEFAULT 100,
    `TotalXP` BIGINT UNSIGNED NOT NULL DEFAULT 0,

    PRIMARY KEY (`UserID`),
    CONSTRAINT `fk_leveling_uid`
        FOREIGN KEY (`UserID`)
        REFERENCES `ElectroAI`.`Users` (`UserID`)
        ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS `ElectroAI`.`Economy` (
    `UserID` BIGINT UNSIGNED NOT NULL,
    `Coins` BIGINT UNSIGNED NOT NULL DEFAULT 0,
    `DailyRewardNextUse` TIMESTAMP DEFAULT NULL,
    `WeeklyRewardNextUse` TIMESTAMP DEFAULT NULL,
    `MonthlyRewardNextUse` TIMESTAMP DEFAULT NULL,

    PRIMARY KEY (`UserID`),
    CONSTRAINT `fk_economy_id`
        FOREIGN KEY (`UserID`)
        REFERENCES `ElectroAI`.`Users` (`UserID`)
        ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS `ElectroAI`.`Moderation` (
    `CaseID` CHAR(6) NOT NULL,
    `CaseType` CHAR(12) NOT NULL,
    `ModeratorID` BIGINT UNSIGNED NOT NULL,
    `TargetID` BIGINT UNSIGNED NOT NULL,
    `Reason` LONGTEXT NOT NULL,
    `Timestamp` TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    `IsOpen` BOOLEAN NOT NULL DEFAULT TRUE,

    PRIMARY KEY (`CaseID`)
);

CREATE TABLE IF NOT EXISTS `ElectroAI`.`Birthdays` (
    `UserID` BIGINT UNSIGNED NOT NULL,
    `Birthday` DATE,

    PRIMARY KEY (`UserID`),
    CONSTRAINT `fk_birthdays_uid`
        FOREIGN KEY (`UserID`)
        REFERENCES `ElectroAI`.`Users` (`UserID`)
        ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS `ElectroAI`.`Reminders` (
    `ReminderID` CHAR(6) NOT NULL,
    `UserID` BIGINT UNSIGNED NOT NULL,
    `ReminderName` VARCHAR(32) NOT NULL,
    `ReminderText` LONGTEXT,
    `ReminderTime` TIMESTAMP NOT NULL,

    PRIMARY KEY (`ReminderID`),
    CONSTRAINT `fk_reminders_uid`
        FOREIGN KEY (`UserID`)
        REFERENCES `ElectroAI`.`Users` (`UserID`)
        ON DELETE CASCADE
);


    
CREATE TABLE IF NOT EXISTS `ElectroAI`.`Family` (
    `UserID` BIGINT UNSIGNED NOT NULL,
    `ParentID` BIGINT UNSIGNED NULL DEFAULT NULL,
    `Partner1ID` BIGINT UNSIGNED NULL DEFAULT NULL,
    `Partner2ID` BIGINT UNSIGNED NULL DEFAULT NULL,
    `Partner3ID` BIGINT UNSIGNED NULL DEFAULT NULL,
    `Partner4ID` BIGINT UNSIGNED NULL DEFAULT NULL,
    `Child1ID` BIGINT UNSIGNED NULL DEFAULT NULL,
    `Child2ID` BIGINT UNSIGNED NULL DEFAULT NULL,
    `Child3ID` BIGINT UNSIGNED NULL DEFAULT NULL,
    `Child4ID` BIGINT UNSIGNED NULL DEFAULT NULL,
    `Child5ID` BIGINT UNSIGNED NULL DEFAULT NULL,
    `Child6ID` BIGINT UNSIGNED NULL DEFAULT NULL,

    PRIMARY KEY (`UserID`),

    CONSTRAINT `fk_family_uid`
        FOREIGN KEY (`UserID`) 
        REFERENCES `ElectroAI`.`Users` (`UserID`)
        ON DELETE CASCADE,
        
    CONSTRAINT `fk_family_parent`
        FOREIGN KEY (`ParentID`) 
        REFERENCES `ElectroAI`.`Users` (`UserID`)
        ON DELETE SET NULL,

    CONSTRAINT `fk_family_partner1` 
        FOREIGN KEY (`Partner1ID`) 
        REFERENCES `ElectroAI`.`Users` (`UserID`) 
        ON DELETE SET NULL,
    CONSTRAINT `fk_family_partner2` 
        FOREIGN KEY (`Partner2ID`) 
        REFERENCES `ElectroAI`.`Users` (`UserID`) 
        ON DELETE SET NULL,
    CONSTRAINT `fk_family_partner3` 
        FOREIGN KEY (`Partner3ID`)
        REFERENCES `ElectroAI`.`Users` (`UserID`)
        ON DELETE SET NULL,
    CONSTRAINT `fk_family_partner4`
        FOREIGN KEY (`Partner4ID`) 
        REFERENCES `ElectroAI`.`Users` (`UserID`) 
        ON DELETE SET NULL,

    CONSTRAINT `fk_family_child1` 
        FOREIGN KEY (`Child1ID`) 
        REFERENCES `ElectroAI`.`Users` (`UserID`) 
        ON DELETE SET NULL,
    CONSTRAINT `fk_family_child2` 
        FOREIGN KEY (`Child2ID`) 
        REFERENCES `ElectroAI`.`Users` (`UserID`) 
        ON DELETE SET NULL,
    CONSTRAINT `fk_family_child3` 
        FOREIGN KEY (`Child3ID`) 
        REFERENCES `ElectroAI`.`Users` (`UserID`) 
        ON DELETE SET NULL,
    CONSTRAINT `fk_family_child4` 
        FOREIGN KEY (`Child4ID`) 
        REFERENCES `ElectroAI`.`Users` (`UserID`) 
        ON DELETE SET NULL,
    CONSTRAINT `fk_family_child5` 
        FOREIGN KEY (`Child5ID`) 
        REFERENCES `ElectroAI`.`Users` (`UserID`) 
        ON DELETE SET NULL,
    CONSTRAINT `fk_family_child6` 
        FOREIGN KEY (`Child6ID`) 
        REFERENCES `ElectroAI`.`Users` (`UserID`) 
        ON DELETE SET NULL
);

CREATE TABLE IF NOT EXISTS `ElectroAI`.`CustomVCs`(
    `ChannelID` BIGINT UNSIGNED NOT NULL,
    `OwnerID` BIGINT UNSIGNED NOT NULL,

    PRIMARY KEY (`ChannelID`)
);

CREATE TABLE IF NOT EXISTS `ElectroAI`.`CustomVCPresets`(
    `UserID` BIGINT UNSIGNED NOT NULL,
    `ChannelName` VARCHAR(32),
    `ChannelUserLimit` TINYINT UNSIGNED,

    PRIMARY KEY (`UserID`),
    CONSTRAINT `fk_customvcpresets_uid`
        FOREIGN KEY (`UserID`)
        REFERENCES `ElectroAI`.`Users` (`UserID`)
        ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS `ElectroAI`.`CustomRole` (
    `RoleID` BIGINT UNSIGNED NOT NULL,
    `UserID` BIGINT UNSIGNED UNIQUE NOT NULL,

    PRIMARY KEY (`RoleID`),
    CONSTRAINT `fk_customrole_uid`
        FOREIGN KEY (`UserID`)
        REFERENCES `ElectroAI`.`Users` (`UserID`)
        ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS `ElectroAI`.`Persistent_Messages` (
    `MessageID` BIGINT UNSIGNED NOT NULL,
    `MessagePurpose` VARCHAR(32) NOT NULL,

    PRIMARY KEY (`MessagePurpose`)
)

DROP TRIGGER IF EXISTS `ElectroAI`.`Users_AFTER_INSERT`;
DELIMITER $$
CREATE TRIGGER `ElectroAI`.`Users_AFTER_INSERT` 
AFTER INSERT ON `ElectroAI`.`Users`
FOR EACH ROW
BEGIN
    INSERT INTO `ElectroAI`.`Leveling` (`UserID`) VALUES (NEW.`UserID`);
    INSERT INTO `ElectroAI`.`Economy` (`UserID`) VALUES (NEW.`UserID`);
    INSERT INTO `ElectroAI`.`Birthdays` (`UserID`) VALUES (NEW.`UserID`);
    INSERT INTO `ElectroAI`.`Family` (`UserID`) VALUES (NEW.`UserID`);
    INSERT INTO `ElectroAI`.`CustomVCPresets` (`UserID`) VALUES (NEW.`UserID`);
END;
$$
DELIMITER ;
