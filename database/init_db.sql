-- Create the beats_db database if it does not exist
CREATE DATABASE IF NOT EXISTS beats_db;

-- Switch to the beats_db database
USE beats_db;

-- Set SQL mode, transaction properties, and character set
SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
SET AUTOCOMMIT = 0;
START TRANSACTION;
SET time_zone = "+00:00";

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;


-- Create table structure for `databeats`
CREATE TABLE `databeats` (
  `FK_SONG_ID` int(11) NOT NULL,
  `FK_USER_ID` int(11) NOT NULL,
  `BEATS` text COLLATE utf8_spanish_ci NOT NULL,
  `DELAY` float NOT NULL,
  `DATE` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_spanish_ci;

-- Create table structure for `delay`
CREATE TABLE `delay` (
  `ID` int(11) NOT NULL,
  `USER_ID` int(11) NOT NULL,
  `BEATS_MSG` text COLLATE utf8_spanish_ci NOT NULL,
  `DELAY_VALUE` int(11) NOT NULL,
  `DATE` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_spanish_ci;

-- Create table structure for `song_dispatch`
CREATE TABLE `song_dispatch` (
  `SONG_ID` int(11) NOT NULL,
  `SONG_NAME` text COLLATE utf8_spanish_ci NOT NULL,
  `REPEATS` int(11) NOT NULL,
  `USER_1` int(11) NOT NULL,
  `DATE_1` timestamp NOT NULL DEFAULT '0000-00-00 00:00:00',
  `USER_2` int(11) NOT NULL,
  `DATE_2` timestamp NOT NULL DEFAULT '0000-00-00 00:00:00',
  `USER_3` int(11) NOT NULL,
  `DATE_3` timestamp NOT NULL DEFAULT '0000-00-00 00:00:00'
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_spanish_ci;

-- Create table structure for `users`
CREATE TABLE `users` (
  `USER_ID` int(11) NOT NULL,
  `USER_NAME` text COLLATE utf8_spanish_ci NOT NULL,
  `USER_LASTNAME` text COLLATE utf8_spanish_ci NOT NULL,
  `PROFESSION` text COLLATE utf8_spanish_ci NOT NULL,
  `VALIDATION_DATES` text COLLATE utf8_spanish_ci NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_spanish_ci;

-- Add indices
ALTER TABLE `databeats`
  ADD PRIMARY KEY (`FK_SONG_ID`,`FK_USER_ID`),
  ADD KEY `FK_USER_ID` (`FK_USER_ID`);

ALTER TABLE `delay`
  ADD PRIMARY KEY (`ID`);

ALTER TABLE `song_dispatch`
  ADD PRIMARY KEY (`SONG_ID`);

ALTER TABLE `users`
  ADD PRIMARY KEY (`USER_ID`);

-- Set AUTO_INCREMENT values
ALTER TABLE `delay`
  MODIFY `ID` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=259;

ALTER TABLE `song_dispatch`
  MODIFY `SONG_ID` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=733;

-- Add foreign key constraints
ALTER TABLE `databeats`
  ADD CONSTRAINT `databeats_fk_1` FOREIGN KEY (`FK_SONG_ID`) REFERENCES `song_dispatch` (`SONG_ID`),
  ADD CONSTRAINT `databeats_fk_2` FOREIGN KEY (`FK_USER_ID`) REFERENCES `users` (`USER_ID`);

-- Commit transaction
COMMIT;

-- Reset character set and collation
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
