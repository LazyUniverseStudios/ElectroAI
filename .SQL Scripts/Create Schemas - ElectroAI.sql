CREATE SCHEMA `ElectroAI`;

SET time_zone = '+00:00';

CREATE TABLE `ElectroAI`.`Users` (
    `UserID` BIGINT UNSIGNED NOT NULL,

    PRIMARY KEY (`UserID`)
);

CREATE TABLE `ElectroAI`.`Leveling`(
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

CREATE TABLE `ElectroAI`.`Economy` (
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

CREATE TABLE `ElectroAI`.`Moderation` (
    `CaseID` CHAR(6) NOT NULL,
    `CaseType` CHAR(12) NOT NULL,
    `ModeratorID` BIGINT UNSIGNED NOT NULL,
    `TargetID` BIGINT UNSIGNED NOT NULL,
    `Reason` LONGTEXT NOT NULL,
    `Timestamp` TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    `IsOpen` BOOLEAN NOT NULL DEFAULT TRUE,

    PRIMARY KEY (`CaseID`)
);

CREATE TABLE `ElectroAI`.`Birthdays` (
    `UserID` BIGINT UNSIGNED NOT NULL,
    `BirthDay` TINYINT UNSIGNED NOT NULL,
    `BirthMonth` TINYINT UNSIGNED NOT NULL,
    `ShowYear` BOOLEAN DEFAULT FALSE,
    `BirthYear` SMALLINT UNSIGNED,

    PRIMARY KEY (`UserID`),
    CONSTRAINT `fk_birthdays_uid`
        FOREIGN KEY (`UserID`)
        REFERENCES `ElectroAI`.`Users` (`UserID`)
        ON DELETE CASCADE
);
