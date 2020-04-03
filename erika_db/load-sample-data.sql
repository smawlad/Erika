BEGIN;
INSERT INTO `User` (UserID, Password, BirthYear, BirthMonth, BirthDay, Bio)  VALUES ('sadat1', '098f6bcd4621d373cade4e832627b4f6', 1998, 11, 26, 'i like cats');
INSERT INTO `User` (UserID, Password, BirthYear, BirthMonth, BirthDay, Bio)  VALUES ('mark1', '82c7e573a77c35a0901da6258d459b6a', 1996, 04, 21, 'why am i here');
INSERT INTO `User` (UserID, Password, BirthYear, BirthMonth, BirthDay, Bio)  VALUES ('jon1', 'ee4728baa37cb2163dd4ef228b98e55a', 1999, 12, 26, 'software dev');
INSERT INTO `User` (UserID, Password, BirthYear, BirthMonth, BirthDay, Bio)  VALUES ('kiran1', 'dc0df1739c6ef34a4c1f7d1f17187184', 1997, 03, 14, 'i am tired, i am weary, i could sleep for a thousand years');
COMMIT;