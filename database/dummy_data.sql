-- Switch to the beats_db database
USE beats_db;

-- Insert dummy users
INSERT INTO `users` (`USER_ID`, `USER_NAME`, `USER_LASTNAME`, `PROFESSION`, `VALIDATION_DATES`)
VALUES
(1, 'John', 'Doe', 'Software Engineer', '2019-5-28 15:41:7,2019-5-28 15:44:58'),
(2, 'Jane', 'Smith', 'Data Analyst', '2019-5-28 15:41:7,2019-5-28 15:44:58'),
(3, 'Robert', 'Smith', 'Data Analyst', '2019-5-28 15:41:7,2019-5-28 15:44:58');

-- Insert dummy songs
INSERT INTO `song_dispatch` (`SONG_ID`, `SONG_NAME`, `REPEATS`, `USER_1`, `DATE_1`, `USER_2`, `DATE_2`, `USER_3`, `DATE_3`)
VALUES
(1, 'song_1', 0, 0, NOW(), 0, NOW(), 0, NOW()),
(2, 'song_2', 0, 0, NOW(), 0, NOW(), 0, NOW()),
(3, 'song_3', 0, 0, NOW(), 0, NOW(), 0, NOW()),
(4, 'song_4', 0, 0, NOW(), 0, NOW(), 0, NOW()),
(5, 'song_5', 0, 0, NOW(), 0, NOW(), 0, NOW()),
(6, 'song_6', 0, 0, NOW(), 0, NOW(), 0, NOW()),
(7, 'song_7', 0, 0, NOW(), 0, NOW(), 0, NOW()),
(8, 'song_8', 0, 0, NOW(), 0, NOW(), 0, NOW()),
(9, 'song_9', 0, 0, NOW(), 0, NOW(), 0, NOW()),
(10, 'song_10', 0, 0, NOW(), 0, NOW(), 0, NOW());
