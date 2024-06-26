"""
server.py
A module for handling server operations.
"""

# Standard library imports
import os
import socket
import traceback
from threading import Thread
from datetime import datetime, timezone
from random import randint

# Third party imports
from pymysqlpool.pool import Pool

# Constants
HOST = "127.0.0.1"
PORT = 65432  # Port to listen on (non-privileged ports are > 1023)

# Get database credentials from environment variables
DB_HOST = os.getenv("DB_HOST", "127.0.0.1")
DB_USER = os.getenv("DB_USER", "root")
DB_PASSWORD = os.getenv("DB_PASSWORD", "your_password")
DB_NAME = os.getenv("DB_NAME", "beats_db")


class PersistentServer:
    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.bind((self.host, self.port))
        self.server_socket.listen()
        print(f"Server listening on {self.host}:{self.port}")

    def handle_client(self, connection, address):
        with connection:
            print("Connected by", address)
            while True:
                try:
                    data = connection.recv(65507)
                    if not data:
                        break
                    data = data.decode("utf-8")
                    print(data)
                    data_parts = data.split(";")
                    if data_parts[0] == "start":
                        print("Received ", data_parts[0])
                        connection.sendall(start_handler(data_parts[1]).encode("utf-8"))
                    elif data_parts[0] == "save":
                        print("Received ", data_parts[0])
                        save_handler(data)
                    elif data_parts[0] == "delay":
                        print("Received ", data_parts[0])
                        delay_handler(data)
                except Exception as e:
                    print(f"Error handling client {address}: {e}")
                    break

    def start(self):
        try:
            while True:
                connection, address = self.server_socket.accept()
                client_thread = Thread(
                    target=self.handle_client, args=(connection, address)
                )
                client_thread.start()
        except KeyboardInterrupt:
            print("Keyboard interrupt caught, exiting")
        finally:
            self.server_socket.close()


# Create a new connection pool
pool = Pool(host=DB_HOST, user=DB_USER, password=DB_PASSWORD, db=DB_NAME)


def insert_beat(song_id, user_id, beats, delay):
    # Get a connection from the pool
    connection = pool.get_conn()

    try:
        with connection.cursor() as cursor:
            # Create a new record
            sql = "INSERT INTO `databeats` (`FK_SONG_ID`, `FK_USER_ID`, `BEATS`, `DELAY`, `DATE`) VALUES (%s, %s, %s, %s, CURRENT_TIMESTAMP)"
            cursor.execute(sql, (song_id, user_id, beats, delay))

        # connection is not autocommit by default. So you must commit to save
        # your changes.
        connection.commit()

    finally:
        # Return the connection to the pool
        pool.release(connection)


def sum_beats(beat_string):
    """
    Sum the beats in a string.

    Parameters:
    beat_string (str): A string of beats separated by spaces.

    Returns:
    float: The sum of the beats, or None if an error occurred.
    """
    if not beat_string:
        return 0

    beats = beat_string.split(" ")
    total = 0.0

    for beat in beats:
        try:
            total += float(beat)
        except ValueError:
            print("Error: Invalid beat value")
            return None

    return total


def update_usr_song(song_id, user_id, repetition, user_num):
    """
    Update a user's song in the database.

    Parameters:
    song_id (int): The song ID.
    user_id (int): The user ID.
    repetition (int): The number of repetitions.
    user_num (int): The user number.

    Returns:
    None
    """
    # Get a connection from the pool
    connection = pool.get_conn()

    try:
        with connection.cursor() as cursor:
            # Create a base SQL query
            sql = "UPDATE `song_dispatch` SET `REPEATS`=%s,`USER_"

            # Append the different parts based on the user_num value
            if user_num == 1:
                sql += "1`=%s,`DATE_1`=CURRENT_TIMESTAMP WHERE `SONG_ID`=%s"
            elif user_num == 2:
                sql += "2`=%s,`DATE_2`=CURRENT_TIMESTAMP WHERE `SONG_ID`=%s"
            elif user_num == 3:
                sql += "3`=%s,`DATE_3`=CURRENT_TIMESTAMP WHERE `SONG_ID`=%s"

            cursor.execute(sql, (repetition, user_id, song_id))

        # Commit the changes
        connection.commit()

    except Exception as e:
        print(f"Failed to update user song: {e}")

    finally:
        # Return the connection to the pool
        pool.release(connection)


def validate_user(user_id):
    """
    Validate a user in the database.

    Parameters:
    user_id (int): The user ID.

    Returns:
    bool: True if the user was successfully validated, False otherwise.
    """
    # Get a connection from the pool
    connection = pool.get_conn()

    try:
        with connection.cursor() as cursor:
            # Select the validation dates for the user
            select_query = "SELECT `VALIDATION_DATES` FROM `users` WHERE `USER_ID`=%s"
            cursor.execute(select_query, (user_id,))
            query = cursor.fetchone()

            # If the query didn't find a user, return False
            if query is None:
                print(f"No user found with ID {user_id}")
                return False

            # Get the current date and time
            now = datetime.now(timezone.utc)
            current_date = now.strftime("%Y-%m-%d %H:%M:%S")

            # Update the validation dates for the user
            data = ""
            if query["VALIDATION_DATES"] == "":
                data = current_date
            else:
                data = query["VALIDATION_DATES"] + "," + current_date

            update_query = (
                "UPDATE `users` SET `VALIDATION_DATES`=%s WHERE `USER_ID`= %s"
            )
            cursor.execute(update_query, (data, user_id))

            # Commit the changes
            connection.commit()

        return True

    except Exception as e:
        print(f"Failed to validate user: {e}")
        print(traceback.format_exc())
        return False

    finally:
        # Return the connection to the pool
        pool.release(connection)


def select_songs(user_id):
    """
    Select a song for a user from the database.

    Parameters:
    user_id (int): The user ID.

    Returns:
    str: The ID of the selected song, or None if no song was selected.
    """
    # Get a connection from the pool
    connection = pool.get_conn()

    try:
        with connection.cursor() as cursor:
            # Select the songs with less than 3 repetitions
            select_query = "SELECT * FROM `song_dispatch` WHERE `REPEATS`<3"
            cursor.execute(select_query)
            songs = cursor.fetchall()

            # Randomly select a song
            for _ in range(len(songs)):
                song_index = randint(0, len(songs) - 1)

                song = songs[song_index]
                song_id = song["SONG_ID"]
                repetitions = song["REPEATS"]
                user_1 = song["USER_1"]
                user_2 = song["USER_2"]
                user_3 = song["USER_3"]

                if (
                    repetitions == 0
                    or (user_1 != user_id and user_2 == 0 and user_3 == 0)
                    or (
                        user_1 != user_id
                        and user_2 != user_id
                        and user_2 != 0
                        and user_3 == 0
                    )
                ):
                    repetitions += 1
                    user_num = 1 if repetitions == 1 else 2 if user_2 == 0 else 3
                    update_usr_song(song_id, user_id, repetitions, user_num)
                    print(f"Song with id {song_id} is assigned to {user_id}")
                    return str(song_id)

                print(f"Discarded song with id {song_id}")

    except Exception as e:
        print(f"Failed to select song: {e}")
        print(traceback.format_exc())

    finally:
        # Return the connection to the pool
        pool.release(connection)

    return None


def get_song_id(song_name):
    """
    Get the ID of a song from the database.

    Parameters:
    song_name (str): The name of the song.

    Returns:
    int: The ID of the song, or None if the song was not found.
    """
    # Get a connection from the pool
    connection = pool.get_conn()

    try:
        with connection.cursor() as cursor:
            # Select the ID of the song
            select_query = "SELECT `SONG_ID` FROM `song_dispatch` WHERE `SONG_NAME`=%s"
            cursor.execute(select_query, (song_name,))
            query = cursor.fetchone()

            if query is not None:
                print(query["SONG_ID"])
                return query["SONG_ID"]

    except Exception as e:
        print(f"Failed to get song ID: {e}")
        print(traceback.format_exc())

    finally:
        # Return the connection to the pool
        pool.release(connection)

    return None


def write_log(text):
    """
    Write a log message to the "log_bad_beat.txt" file.

    Parameters:
    text (str): The log message.

    Returns:
    None
    """
    # Get the current date and time
    current_date = datetime.now().strftime("%d/%m/%Y %H:%M:%S")

    # Write the log message
    with open("log_bad_beat.txt", "a") as log:
        msg = f"[ {current_date} ] - {text}\n"
        log.write(msg)


def write_total_log(text):
    """
    Write a log message to the "log_total.txt" file.

    Parameters:
    text (str): The log message.

    Returns:
    None
    """
    # Get the current date and time
    current_date = datetime.now().strftime("%d/%m/%Y %H:%M:%S")

    # Write the log message
    with open("log_total.txt", "a") as log:
        msg = f"[ {current_date} ] - {text}\n"
        log.write(msg)


def save_handler(save):
    """
    Handle the save operation for a song.

    Parameters:
    save (str): The save data in the format "song_id;user_id;beats;delay".

    Returns:
    None
    """
    try:
        data = save.split(";")
        song_parts = data[1].split(".")
        song_id = get_song_id(song_parts[0])
        user_id = data[2]
        beats = data[5]
        delay = data[3]
        sum_recv = data[4]

        print(f"Recv: {sum_recv}")
        print(sum_beats(beats))

        if str(sum_recv) == str(sum_beats(beats)):
            insert_beat(song_id, user_id, beats, delay)
            msg = f"Beats from song {song_id}, usr {user_id} saved"
            print(msg)
        else:
            print(
                "--------------------------ERROR: Check Sum Wrong -------------------------"
            )
            insert_beat(song_id, user_id, beats, delay)
            msg = f"Beats from song {song_id}, usr {user_id} saved"
            print(msg)
            write_log(f"ID_SONG: {song_id} ID_USER: {user_id} BEATS: {beats}")

    except Exception as e:
        print(f"Failed to save: {e}")

    return


def user_exists(user_id):
    """
    Check if a user exists in the database.

    Parameters:
    user_id (int): The user ID.

    Returns:
    bool: True if the user exists, False otherwise.
    """
    # Get a connection from the pool
    connection = pool.get_conn()

    try:
        with connection.cursor() as cursor:
            # Check if the user exists
            select_query = "SELECT `USER_ID` FROM `users` WHERE `USER_ID`=%s"
            cursor.execute(select_query, user_id)
            query = cursor.fetchone()

            return query is not None

    except Exception as e:
        print(f"Failed to check if user exists: {e}")
        print(traceback.format_exc())

    finally:
        # Return the connection to the pool
        pool.release(connection)

    return False


def get_song_name(id_song):
    """
    Get the name of a song from the database.

    Parameters:
    id_song (int): The ID of the song.

    Returns:
    str: The name of the song, or None if the song was not found.
    """
    # Get a connection from the pool
    connection = pool.get_conn()

    try:
        with connection.cursor() as cursor:
            # Select the name of the song
            select_query = "SELECT `SONG_NAME` FROM `song_dispatch` WHERE `SONG_ID`=%s"
            cursor.execute(select_query, (id_song,))
            query = cursor.fetchone()

            if query is not None:
                print(query["SONG_NAME"])
                return query["SONG_NAME"]

    except Exception as e:
        print(f"Failed to get song name: {e}")
        print(traceback.format_exc())

    finally:
        # Return the connection to the pool
        pool.release(connection)

    return None


def insert_delay(user_id, beats, delay):
    """
    Insert a delay record into the database.

    Parameters:
    user_id (int): The user ID.
    beats (str): The beats message.
    delay (str): The delay value.

    Returns:
    None
    """
    # Get a connection from the pool
    connection = pool.get_conn()

    try:
        with connection.cursor() as cursor:
            # Insert a new record
            insert_query = "INSERT INTO `delay`(`USER_ID`, `BEATS_MSG`, `DELAY_VALUE`, `DATE`) VALUES (%s, %s, %s, CURRENT_TIMESTAMP)"
            cursor.execute(insert_query, (user_id, beats, delay))

        # Commit the transaction
        connection.commit()

    except Exception as e:
        print(f"Failed to insert delay: {e}")

    finally:
        # Return the connection to the pool
        pool.release(connection)


def delay_handler(msg):
    """
    Handle the delay operation for a user.

    Parameters:
    msg (str): The delay data in the format "idUser;beats;delay".

    Returns:
    None
    """
    try:
        data = msg.split(";")
        user_id = data[1]
        beats = data[2]
        delay = data[3]

        insert_delay(user_id, beats, delay)

    except Exception as e:
        print(f"Failed to handle delay: {e}")

    return


def start_handler(msg):
    """
    Handle the start operation for a user.

    Parameters:
    msg (str): The user ID.

    Returns:
    str: The song ID and name if the user exists, or "INVALID" if the user does not exist or there are no more songs.
    """
    try:
        user_id = int(msg)
        if user_exists(user_id):
            validate_user(user_id)
            song_id = select_songs(user_id)
            if song_id is None:
                return "song_id;NO_MORE_SONGS"
            song_name = get_song_name(song_id)
            if song_name is not None:
                return f"song_id;{song_name}.mp3"
            else:
                return "song_id;INVALID"

    except Exception as e:
        print(f"Failed to handle start: {e}")

    return "song_id;INVALID"


server = PersistentServer(HOST, PORT)
server.start()
