# Database

## Setting Up MySQL Server in Docker

To set up a MySQL server using Docker, follow these steps:

1. Run the MySQL Docker container:

   ```bash
   docker run --name mysql-container -e MYSQL_ROOT_PASSWORD=your_password -p 3306:3306 -d mysql
   ```

2. Check the status of running Docker containers:

   ```bash
   docker ps
   ```

3. Use `docker inspect` to obtain the IP address of the MySQL container:

   ```bash
   docker inspect mysql-container
   ```

4. Use the following command to initialize the database using the provided SQL script (`init_db.sql`):

   ```bash
   mysql -u root -p -h <container_ip_address> < init_db.sql
   ```

5. Optionally, populate the database with initial data using the provided SQL script (`dummy_data.sql`). This step is recommended to have some sample data for testing the application:

   ```bash
   mysql -u root -p -h <container_ip_address> < dummy_data.sql
   ```

6. Note that the server uses MySQL as the database management system (DBMS), and it can be executed anywhere the server has access, such as a virtual machine (VM) in the cloud, the local machine, or any desired location. For this example, Docker is used. However, it is recommended to assign a volume to the Docker image to prevent data loss if the container is deleted.

7. After following these steps, the MySQL server should be set up and ready to use.

## beats_db Database

This document provides a detailed description of the `beats_db` database, including the structure of the tables and an explanation of each field.

## Table: `databeats`

This table stores the beats annotated by users for each song.

- **FK_SONG_ID**: Unique identifier for the song. It is a foreign key that references `song_dispatch.SONG_ID`.
- **FK_USER_ID**: Unique identifier for the user. It is a foreign key that references `users.USER_ID`.
- **BEATS**: Text containing the sequence of beats annotated by the user.
- **DELAY**: Delay value in seconds.
- **DATE**: Timestamp of when the data was recorded. It updates automatically every time the row is modified.

## Table: `delay`

This table stores delay messages and their values for each user.

- **ID**: Unique identifier for the delay entry. It is the primary key.
- **USER_ID**: Unique identifier for the user associated with the delay. References `users.USER_ID`.
- **BEATS_MSG**: Text containing the message of the annotated beats.
- **DELAY_VALUE**: Delay value in seconds.
- **DATE**: Timestamp of when the delay data was recorded. It updates automatically every time the row is modified.

## Table: `song_dispatch`

This table stores information about the songs and their distribution to users.

- **SONG_ID**: Unique identifier for the song. It is the primary key.
- **SONG_NAME**: Text containing the name of the song.
- **REPEATS**: Number of times the song has been dispatched.
- **USER_1**: Unique identifier for the first user to receive the song.
- **DATE_1**: Timestamp of when the first user received the song. Defaults to '0000-00-00 00:00:00'.
- **USER_2**: Unique identifier for the second user to receive the song.
- **DATE_2**: Timestamp of when the second user received the song. Defaults to '0000-00-00 00:00:00'.
- **USER_3**: Unique identifier for the third user to receive the song.
- **DATE_3**: Timestamp of when the third user received the song. Defaults to '0000-00-00 00:00:00'.

## Table: `users`

This table stores information about the users.

- **USER_ID**: Unique identifier for the user. It is the primary key.
- **USER_NAME**: Text containing the first name of the user.
- **USER_LASTNAME**: Text containing the last name of the user.
- **PROFESSION**: Text containing the profession of the user.
- **VALIDATION_DATES**: Text containing the dates when the user's data was validated.

## Indices and Foreign Key Constraints

### Indices

- **databeats**:
  - Primary key: (`FK_SONG_ID`, `FK_USER_ID`)
  - Index: `FK_USER_ID`

- **delay**:
  - Primary key: `ID`

- **song_dispatch**:
  - Primary key: `SONG_ID`

- **users**:
  - Primary key: `USER_ID`

### Foreign Key Constraints

- **databeats**:
  - Foreign key constraint: `databeats_fk_1` references `song_dispatch(SONG_ID)`
  - Foreign key constraint: `databeats_fk_2` references `users(USER_ID)`

## Auto-Increment Values

- **delay**:
  - `ID` is set to auto-increment starting from 259.

- **song_dispatch**:
  - `SONG_ID` is set to auto-increment starting from 733.

## Character Set and Collation

The database and tables use the `utf8` character set with `utf8_spanish_ci` collation.

## Transaction Control

The database creation and table setup are wrapped in a transaction to ensure atomicity.
