"""
server.py
A module for handling server operations.
"""

# Standard library imports
import os
import socket
from datetime import datetime
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
DB_NAME = os.getenv("DB_NAME", "beatsalsa")

# Create a new connection pool
pool = Pool(host=DB_HOST, user=DB_USER, password=DB_PASSWORD, db=DB_NAME)


def insert_beat(id_cancion, id_usuario, beats, delay):
    # Get a connection from the pool
    connection = pool.get_conn()

    try:
        with connection.cursor() as cursor:
            # Create a new record
            sql = "INSERT INTO `databeats` (`FK_ID_CANCION`, `FK_CEDULA_USUARIO`, `BEATS`, `DELAY`, `FECHA`) VALUES (%s, %s, %s, %s, CURRENT_TIMESTAMP)"
            cursor.execute(sql, (id_cancion, id_usuario, beats, delay))

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
            sql = "UPDATE `despacho_cancion` SET `REPETICIONES`=%s,`USUARIO_"

            # Append the different parts based on the user_num value
            if user_num == 1:
                sql += "1`=%s,`FECHA_1`=CURRENT_TIMESTAMP WHERE `ID_CANCION`=%s"
            elif user_num == 2:
                sql += "2`=%s,`FECHA_2`=CURRENT_TIMESTAMP WHERE `ID_CANCION`=%s"
            elif user_num == 3:
                sql += "3`=%s,`FECHA_3`=CURRENT_TIMESTAMP WHERE `ID_CANCION`=%s"

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
            select_query = (
                "SELECT `FECHAS_VALIDACION` FROM `usuarios` WHERE `CEDULA_USUARIO`=%s"
            )
            cursor.execute(select_query, user_id)
            query = cursor.fetchone()

            # Get the current date and time
            now = datetime.now().utcnow()
            current_date = now.strftime("%Y-%m-%d %H:%M:%S")

            # Update the validation dates for the user
            data = ""
            if query[0] == "":
                data = current_date
            else:
                for i in query:
                    data += i + ","
                data += current_date

            update_query = "UPDATE `usuarios` SET `FECHAS_VALIDACION`=%s WHERE `CEDULA_USUARIO`= %s"
            cursor.execute(update_query, (data, user_id))

            # Commit the changes
            connection.commit()

        return True

    except Exception as e:
        print(f"Failed to validate user: {e}")
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
            select_query = "SELECT * FROM `despacho_cancion` WHERE `REPETICIONES`<3"
            cursor.execute(select_query)
            songs = cursor.fetchall()

            # Randomly select a song
            for _ in range(len(songs)):
                song_index = randint(0, len(songs) - 1)

                song = songs[song_index]
                song_id = song[0]
                repetitions = song[2]
                user_1 = song[3]
                user_2 = song[5]
                user_3 = song[7]

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
            select_query = (
                "SELECT `ID_CANCION` FROM `despacho_cancion` WHERE `NOMBRE_CANCION`=%s"
            )
            cursor.execute(select_query, song_name)
            query = cursor.fetchone()

            if query is not None:
                print(query[0])
                return query[0]

    except Exception as e:
        print(f"Failed to get song ID: {e}")

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
    save (str): The save data in the format "idCancion;idUsuario;Beats;Delay".

    Returns:
    None
    """
    try:
        data = save.split(";")
        song_parts = data[1].split(".")
        id_cancion = get_song_id(song_parts[0])
        id_usuario = data[2]
        beats = data[5]
        delay = data[3]
        sum_recv = data[4]

        print(f"Recv: {sum_recv}")
        print(sum_beats(beats))

        if str(sum_recv) == str(sum_beats(beats)):
            insert_beat(id_cancion, id_usuario, beats, delay)
            msg = f"Beats from song {id_cancion}, usr {id_usuario} saved"
            print(msg)
        else:
            print(
                "--------------------------ERROR: Check Sum Wrong -------------------------"
            )
            insert_beat(id_cancion, id_usuario, beats, delay)
            msg = f"Beats from song {id_cancion}, usr {id_usuario} saved"
            print(msg)
            write_log(f"ID_SONG: {id_cancion} ID_USER: {id_usuario} BEATS: {beats}")

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
            select_query = (
                "SELECT `CEDULA_USUARIO` FROM `usuarios` WHERE `CEDULA_USUARIO`=%s"
            )
            cursor.execute(select_query, user_id)
            query = cursor.fetchone()

            return query is not None

    except Exception as e:
        print(f"Failed to check if user exists: {e}")

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
            select_query = (
                "SELECT `NOMBRE_CANCION` FROM `despacho_cancion` WHERE `ID_CANCION`=%s"
            )
            cursor.execute(select_query, id_song)
            query = cursor.fetchone()

            if query is not None:
                print(query[0])
                return query[0]

    except Exception as e:
        print(f"Failed to get song name: {e}")

    finally:
        # Return the connection to the pool
        pool.release(connection)

    return None


def insert_delay(id_usuario, beats, delay):
    """
    Insert a delay record into the database.

    Parameters:
    id_usuario (int): The user ID.
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
            insert_query = "INSERT INTO `delay`(`CEDULA_USUARIO`, `BEATS_MSG`, `DELAY_VALUE`, `FECHA`) VALUES (%s, %s, %s, CURRENT_TIMESTAMP)"
            cursor.execute(insert_query, (id_usuario, beats, delay))

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
    str: The song ID and name if the user exists, or "INVALID" if the user does not exist.
    """
    try:
        user_id = int(msg)
        if user_exists(user_id):
            validate_user(user_id)
            song_id = select_songs(user_id)
            song_name = get_song_name(song_id)

            if song_name is not None:
                return f"song_id;{song_name}.mp3"
            else:
                return "song_id;INVALID"

    except Exception as e:
        print(f"Failed to handle start: {e}")

    return "song_id;INVALID"


try:
    # The server runs indefinitely until interrupted
    while True:
        # Create a new socket using the AF_INET address family (IPv4) and SOCK_STREAM socket type (TCP)
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
            # Bind the socket to the specified host and port
            server_socket.bind((HOST, PORT))
            # Listen for incoming connections
            server_socket.listen()
            # Accept a connection; this will pause the script until a connection is received
            connection, address = server_socket.accept()
            # Use the connection
            with connection:
                print("Connected by", address)
                # Keep receiving data from the client
                while True:
                    # Receive up to 65507 bytes of data from the client
                    data = connection.recv(65507)
                    # If no data was received, break the loop and wait for another connection
                    if not data:
                        break
                    else:
                        # Decode the data from bytes to a string
                        data = data.decode("utf-8")
                        print(data)
                        # Split the data by semicolon
                        data_parts = data.split(";")
                        # Check the first part of the data to determine the action
                        if data_parts[0] == "start":
                            print("Received ", data_parts[0])
                            # Handle the 'start' action and send the result back to the client
                            connection.sendall(
                                start_handler(data_parts[1]).encode("utf-8")
                            )
                        elif data_parts[0] == "save":
                            print("Received ", data_parts[0])
                            # Handle the 'save' action
                            save_handler(data)
                        elif data_parts[0] == "delay":
                            print("Received ", data_parts[0])
                            # Handle the 'delay' action
                            delay_handler(data)

# If a keyboard interrupt (Ctrl+C) is received, print a message and exit the script
except KeyboardInterrupt:
    print("Keyboard interrupt caught, exiting")
