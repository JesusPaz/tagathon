-- Switch to the beats_db database
USE beats_db;

-- Insert dummy users
INSERT INTO `users` (`USER_ID`, `USER_NAME`, `USER_LASTNAME`, `PROFESSION`, `VALIDATION_DATES`)
VALUES
(1234, 'John', 'Doe', 'Software Engineer', ''),
(5678, 'Jane', 'Smith', 'Data Analyst', '');

-- Insert dummy songs
INSERT INTO `song_dispatch` (`SONG_ID`, `SONG_NAME`, `REPEATS`, `USER_1`, `DATE_1`, `USER_2`, `DATE_2`, `USER_3`, `DATE_3`)
VALUES
(1, 'Song 1', 0, 0, NOW(), 0, NOW(), 0, NOW()),
(2, 'Song 2', 0, 0, NOW(), 0, NOW(), 0, NOW()),
(3, 'Song 3', 0, 0, NOW(), 0, NOW(), 0, NOW()),
(4, 'Song 4', 0, 0, NOW(), 0, NOW(), 0, NOW()),
(5, 'Song 5', 0, 0, NOW(), 0, NOW(), 0, NOW());
