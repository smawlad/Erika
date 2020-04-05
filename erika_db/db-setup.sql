CREATE DATABASE  IF NOT EXISTS `ErikaDB`;
USE `ErikaDB`;

SET NAMES utf8mb4;
SET FOREIGN_KEY_CHECKS = 0;

DROP TABLE IF EXISTS `User`;
CREATE TABLE `User` (
    `UserID` VARCHAR(10) NOT NULL,
    `Password` VARCHAR(255) NOT NULL,
    `BirthYear` INT NOT NULL,
    `BirthMonth` INT NOT NULL,
    `BirthDay` INT NOT NULL,
    `Bio` VARCHAR(255) DEFAULT NULL,
    PRIMARY KEY	(`UserID`)    
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

DROP TABLE IF EXISTS `Post`;
CREATE TABLE `Post` (
	`PostID` INT NOT NULL AUTO_INCREMENT,
    `Type` ENUM ('Text', 'Image', 'Both') NOT NULL,
    `Body` VARCHAR(1000) NOT NULL,
    `ImageURL` VARCHAR(255) DEFAULT NULL,
    `CreatedBy` VARCHAR(10) NOT NULL,
    `YearCreated` INT NOT NULL,
    `MonthCreated` INT NOT NULL,
    `DayCreated` INT NOT NULL,
    PRIMARY KEY	(`PostID`),
    FOREIGN KEY (`CreatedBy`) REFERENCES User(`UserID`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

DROP TABLE IF EXISTS `Topic`;
CREATE TABLE `Topic` (
	`TopicID` VARCHAR(255) NOT NULL,
    PRIMARY KEY	(`TopicID`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

DROP TABLE IF EXISTS `UserGroup`;
CREATE TABLE `UserGroup` (
	`GroupID` VARCHAR(255) NOT NULL,
    `About` VARCHAR(255) NOT NULL,
    `CreatedBy` VARCHAR(10) NOT NULL,
    PRIMARY KEY	(`GroupID`),
    FOREIGN KEY (`CreatedBy`) REFERENCES User(`UserID`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

DROP TABLE IF EXISTS `Conversation`;
CREATE TABLE `Conversation` (
	`ConversationID` INT NOT NULL AUTO_INCREMENT,
	`User1` VARCHAR(10) NOT NULL,
    `User2` VARCHAR(10) NOT NULL,
    PRIMARY KEY (`ConversationID`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8;

# use MyISAM engine it allows AUTO_INCREMENT by group, see https://dev.mysql.com/doc/refman/8.0/en/example-auto-increment.html
DROP TABLE IF EXISTS `Message`;
CREATE TABLE `Message` (
	`ConversationID` INT NOT NULL,
    `MessageID` INT NOT NULL AUTO_INCREMENT,
    `SenderID` VARCHAR(10) NOT NULL,
    `Body` VARCHAR(1000) NOT NULL,
    `YearSent` INT NOT NULL,
    `MonthSent` INT NOT NULL,
    `DaySent` INT NOT NULL,
    PRIMARY KEY	(`ConversationID`, `MessageID`),
    FOREIGN KEY (`SenderID`) REFERENCES User(`UserID`),
    FOREIGN KEY(`ConversationID`) REFERENCES Conversation(`ConversationID`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8;

DROP TABLE IF EXISTS `UserFollowsUser`;
CREATE TABLE `UserFollowsUser` (
	`FollowerID` VARCHAR(10) NOT NULL,
    `FollowingID` VARCHAR(10) NOT NULL,
    `LastReadPost` INT DEFAULT NULL,
    PRIMARY KEY (`FollowerID`, `FollowingID`),
    FOREIGN KEY (`FollowerID`) REFERENCES User(`UserID`),
    FOREIGN KEY (`FollowingID`) REFERENCES User(`UserID`),
    FOREIGN KEY (`LastReadPost`) REFERENCES Post(`PostID`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

DROP TABLE IF EXISTS `UserFollowsTopic`;
CREATE TABLE `UserFollowsTopic` (
	`FollowerID` VARCHAR(10) NOT NULL,
    `TopicID` VARCHAR(255) NOT NULL,
    `LastReadPost` INT DEFAULT NULL,
    PRIMARY KEY (`FollowerID`, `TopicID`),
    FOREIGN KEY (`FollowerID`) REFERENCES User(`UserID`),
    FOREIGN KEY (`TopicID`) REFERENCES Topic(`TopicID`),
    FOREIGN KEY (`LastReadPost`) REFERENCES Post(`PostID`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

DROP TABLE IF EXISTS `UserJoinsGroup`;
CREATE TABLE `UserJoinsGroup` (
	`UserID` VARCHAR(10) NOT NULL,
    `GroupID` VARCHAR(255) NOT NULL,
    PRIMARY KEY (`UserID`, `GroupID`),
    FOREIGN KEY (`UserID`) REFERENCES User(`UserID`),
    FOREIGN KEY (`GroupID`) REFERENCES `UserGroup`(`GroupID`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

DROP TABLE IF EXISTS `UserReactsToPost`;
CREATE TABLE `UserReactsToPost` (
	`UserID` VARCHAR(10) NOT NULL,
    `PostID` INT NOT NULL,
    `Reaction` ENUM('Like', 'Dislike', 'Love', 'Funny', 'Sad', 'WTF') DEFAULT NULL,
    PRIMARY KEY (`UserID`, `PostID`),
    FOREIGN KEY (`UserID`) REFERENCES User(`UserID`),
    FOREIGN KEY (`PostID`) REFERENCES Post(`PostID`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

DROP TABLE IF EXISTS `PostResponse`;
CREATE TABLE `PostResponse` (
	`PostID` INT NOT NULL,
    `ResponseID` INT NOT NULL,
    PRIMARY KEY (`PostID`, `ResponseID`),
    FOREIGN KEY (`PostID`) REFERENCES Post(`PostID`),
    FOREIGN KEY (`ResponseID`) REFERENCES Post(`PostID`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

DROP TABLE IF EXISTS `PostTopic`;
CREATE TABLE `PostTopic` (
	`PostID` INT NOT NULL,
    `TopicID` VARCHAR(255) NOT NULL,
    PRIMARY KEY (`PostID`, `TopicID`),
    FOREIGN KEY (`PostID`) REFERENCES Post(`PostID`),
    FOREIGN KEY (`TopicID`) REFERENCES Topic(`TopicID`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

