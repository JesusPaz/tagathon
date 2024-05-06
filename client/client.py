"""
client.py
This file contains the client side of the application.
"""

# Standard library imports
import os
import threading
import time
import socket

# Related third party imports
import pygame
import tkinter as tk
from mutagen.mp3 import MP3
from tkinter import messagebox
from tkinter import font

# Define constants for positioning
X_OFFSET = 160
Y_OFFSET = 140
BUTTON_Y_OFFSET = 75

# The server's hostname or IP address
# HOST = "192.168.114.38"
HOST = "127.0.0.1"

# The port used by the server
PORT = 65432

# Flag to indicate whether there is a delay
delay = True

# Counter for the number of delays
delay_counter = 0

# Counter for the number of songs
song_counter = 1

# Create the root window
ROOT = tk.Tk()
ROOT.title("Client")

# Get the maximum size of the window
w, h = ROOT.maxsize()

# Set the window to fullscreen
ROOT.attributes("-fullscreen", True)

number_songs = 10

# Create a label to welcome the user and ask for their ID
welcome_label = tk.Label(
    ROOT,
    text="Thank you for participating in the annotation experiment. \n Please enter your ID",
)

# Create a button for the user to submit their ID
send_button = tk.Button(ROOT, text="Submit")

# Create an entry field for the user to input their ID
user_id_entry = tk.Entry(ROOT, width=20)

# Update idle tasks to ensure the root window is updated
ROOT.update_idletasks()

# Get the current width and height of the root window
width = ROOT.winfo_width()
height = ROOT.winfo_height()

# Calculate the center of the window
x = width // 2
y = height // 2

# Place the label, button, and entry field in the window
welcome_label.place(x=x - X_OFFSET, y=y - Y_OFFSET)
send_button.place(x=x + 30, y=y - BUTTON_Y_OFFSET)
user_id_entry.place(x=x - X_OFFSET, y=y)

# Define constants for positioning
X_OFFSET = 600
Y_OFFSET = 350

# Create buttons for various actions
play_button = tk.Button(ROOT, text="Play")
retry_button = tk.Button(ROOT, text="Retry")
continue_button = tk.Button(ROOT, text="Continue")
back_button = tk.Button(ROOT, text="Back")
yes_button = tk.Button(ROOT, text="Yes")
ok_button = tk.Button(ROOT, text="Ok")
ok_retry_button = tk.Button(ROOT, text="Ok")

# Create a hidden label
hidden_label = tk.Label(ROOT, text="")
hidden_label.place(x=x - X_OFFSET, y=y - Y_OFFSET)

# Create a label for the song name
song_name_label = tk.Label(ROOT, text="Song Name")

# Define a font for the progress label
helv_font = font.Font(size=15, weight="bold")

# Create a label for the progress
progress_label = tk.Label(ROOT, text="1 / " + str(number_songs), font=helv_font)

# Create labels for the total duration and current time
total_duration_label = tk.Label(ROOT, text="Total Duration : --:--")
current_time_label = tk.Label(ROOT, text="Current Time : --:--")


def center_window(window):
    """
    Centers the given window on the screen.
    Taken from: https://stackoverrun.com/es/q/754917
    """
    window.update_idletasks()
    width = window.winfo_width()
    height = window.winfo_height()
    x = (window.winfo_screenwidth() // 2) - (width // 2)
    y = (window.winfo_screenheight() // 2) - (height // 2)
    window.geometry(f"{width}x{height}+{x}+{y}")


def sum_beats(beat_string: str) -> float:
    """
    Sums the beats in a string.

    The string should contain float values separated by spaces. Each float represents a beat.
    If the string is None or empty, the function returns 0.

    Args:
        beat_string (str): A string of beats.

    Returns:
        float: The sum of the beats.
    """
    if beat_string:
        beat_list = beat_string.split(" ")
        total = sum(float(beat) for beat in beat_list)
        return total
    else:
        return 0.0


def write_log(text: str) -> None:
    """
    Writes a log message to a file.

    The message is prefixed with a timestamp and appended to the file "log.txt".

    Args:
        text (str): The log message to write.
    """
    date = time.strftime("%c")
    msg = f"[ {date} ] - {text}\n"

    with open("log.txt", "a") as log_file:
        log_file.write(msg)


def send_user_id(event):
    """
    Sends the user ID to the server and handles the response.

    The user ID is retrieved from the user_id_entry field. The server's response is expected to be a string
    containing a song ID. If the song ID is "INVALID", an error message is displayed. Otherwise, the song is loaded
    and the music player is drawn.

    Args:
        event: The event that triggered this function.
    """
    global user_id
    global song_name
    user_id = user_id_entry.get()
    song_name = "Song Name"

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((HOST, PORT))
        user_id_msg = f"start;{user_id}"
        s.sendall(user_id_msg.encode("utf-8"))
        data = s.recv(65507)
        data = data.decode("utf-8")
        aux = data.split(";")
        if aux[0] == "song_id":
            if aux[1] == "INVALID":
                # Show error message
                print("INVALID")

                messagebox.showerror(message="This ID is not registered", title="ERROR")
            else:
                song_name = aux[1]
                song_name_label["text"] = song_name

                if delay:
                    show_delay_player()
                    load_song("salsa_loop_82bpm.mp3")

                    handle_song_end()
                else:
                    load_song(song_name)
                    print(f"song: {song_name}")
                    write_log(f"song: {song_name} user_id: {user_id}")
                    draw_music_player(event)


def handle_song_end():
    """
    Initializes pygame and sets up an event loop to handle the end of a song.

    The function sets a flag, end, to True and then enters a loop that checks for events. If a USEREVENT is detected,
    the function sets end to False.
    """
    pygame.init()
    song_ended = True

    for event in pygame.event.get():
        if event.type == pygame.constants.USEREVENT:
            song_ended = False


def show_delay_message():
    """
    Hides the player controls and shows a delay message.

    The function hides the play, stop, yes buttons, and the name, length, and current labels. It then shows a message
    thanking the user for practicing and asking them to click 'continue' to hear the first song or 'back' to practice
    the task again.
    """
    X_OFFSET = 140
    Y_OFFSET = 120
    BUTTON_X_OFFSET = 100
    BUTTON_Y_OFFSET = 30

    play_button.place_forget()
    retry_button.place_forget()
    welcome_label.place_forget()
    total_duration_label.place_forget()
    current_time_label.place_forget()
    yes_button.place_forget()

    welcome_label.place(x=x - X_OFFSET, y=y - Y_OFFSET)
    welcome_label["text"] = (
        "Thank you for practicing. Now click 'continue' \n to listen to the first song. Click 'back' if you want \n to practice the task once more."
    )
    continue_button.place(x=x - BUTTON_X_OFFSET, y=y - BUTTON_Y_OFFSET)
    back_button.place(x=x + BUTTON_X_OFFSET, y=y - BUTTON_Y_OFFSET)


def show_delay_player():
    """
    Hides the user data entry and shows the song player.

    The function hides the ID entry, send, continue, back, and yes buttons, and the welcome label. It then shows a message
    instructing the user to listen to salsa songs and mark the beat of the song using the space bar. The message is displayed
    in the name label, and the length and current labels, and the play and stop buttons are placed below the message.
    """
    X_OFFSET = 140
    Y_OFFSET = 120
    BUTTON_X_OFFSET = 100
    BUTTON_Y_OFFSET = 60

    user_id_entry.config(state="disabled")
    user_id_entry.place_forget()
    send_button.config(state="disabled")
    send_button.place_forget()
    welcome_label.place_forget()
    continue_button.place_forget()
    back_button.place_forget()
    yes_button.place_forget()

    song_name_label.place(x=x - X_OFFSET, y=y - Y_OFFSET)
    song_name_label["text"] = (
        "During the experiment, we will ask you to listen to \n salsa songs and mark the beat of the song \n (in quarter notes) using the space bar on your \n keyboard. Practice the task of the experiment \n by listening to a fragment of salsa:"
    )
    total_duration_label.place(x=x - 60, y=y)
    current_time_label.place(x=x - 60, y=y + 20)
    play_button.place(x=x - BUTTON_X_OFFSET, y=y + BUTTON_Y_OFFSET)
    retry_button.place(x=x, y=y + BUTTON_Y_OFFSET)


def draw_music_player(event):
    """
    Hides the user data entry and shows the song player.

    The function hides the ID entry, send, continue, back, yes, and ok retry buttons, and the welcome label. It then shows a message
    instructing the user to listen to the song and mark the beat using the space bar. If the user wants to repeat the song, they can
    click 'retry'. The message is displayed in the name label, and the length and current labels, and the play and stop buttons are placed
    below the message. The progress label is placed at the bottom right of the window.
    """
    X_OFFSET = 130
    Y_OFFSET = 110
    BUTTON_X_OFFSET = 100
    BUTTON_Y_OFFSET = 60
    PROGRESS_X_OFFSET = 450
    PROGRESS_Y_OFFSET = 300

    user_id_entry.config(state="disabled")
    user_id_entry.place_forget()
    send_button.config(state="disabled")
    send_button.place_forget()
    welcome_label.place_forget()
    continue_button.place_forget()
    back_button.place_forget()
    yes_button.place_forget()
    ok_retry_button.place_forget()

    song_name_label.place(x=x - X_OFFSET, y=y - Y_OFFSET)
    song_name_label["text"] = (
        "Listen carefully to the song and mark the beat \n (in quarter notes) using the space bar on your \n keyboard. If for some reason, you want to repeat \n the song, click 'retry'."
    )
    total_duration_label.place(x=x - 60, y=y)
    current_time_label.place(x=x - 60, y=y + 20)
    play_button.place(x=x - BUTTON_X_OFFSET, y=y + BUTTON_Y_OFFSET)
    retry_button.place(x=x, y=y + BUTTON_Y_OFFSET)
    progress_label.place(x=x + PROGRESS_X_OFFSET, y=y + PROGRESS_Y_OFFSET)
    progress_label["text"] = str(cont_song) + " / " + str(number_songs)


def draw_data_entry():
    """
    Hides the song player and shows the data entry.

    The function hides the play, stop, yes, ok, continue, and back buttons, and the name, length, current, and progress labels. It then
    shows the ID entry and send button, and the welcome label is placed above the ID entry.
    """
    X_OFFSET = 160
    Y_OFFSET = 140
    BUTTON_X_OFFSET = 30
    BUTTON_Y_OFFSET = 75
    ENTRY_X_OFFSET = 100
    ENTRY_Y_OFFSET = 70

    play_button.place_forget()
    retry_button.place_forget()
    song_name_label.place_forget()
    total_duration_label.place_forget()
    current_time_label.place_forget()
    yes_button.place_forget()
    progress_label.place_forget()
    ok_button.place_forget()

    continue_button.place_forget()
    back_button.place_forget()

    user_id_entry.config(state="normal")
    send_button.config(state="normal")
    welcome_label.place(x=x - X_OFFSET, y=y - Y_OFFSET)
    send_button.place(x=x + BUTTON_X_OFFSET, y=y - BUTTON_Y_OFFSET)
    user_id_entry.place(x=x - ENTRY_X_OFFSET, y=y - ENTRY_Y_OFFSET)


def show_next_song():
    """
    Hides the song player and shows a message asking the user if they are ready for the next song.

    The function hides the play, stop, continue, and back buttons, and the name, length, and current labels. It then shows a message
    asking the user if they are ready for the next song. The message is displayed in the name label, and the yes button is placed below
    the message. The progress label is placed at the bottom right of the window.
    """
    global number_songs
    X_OFFSET = 140
    Y_OFFSET = 75
    BUTTON_X_OFFSET = 0
    BUTTON_Y_OFFSET = 40
    PROGRESS_X_OFFSET = 450
    PROGRESS_Y_OFFSET = 300

    play_button.place_forget()
    retry_button.place_forget()
    song_name_label.place_forget()
    total_duration_label.place_forget()
    current_time_label.place_forget()

    continue_button.place_forget()
    back_button.place_forget()

    song_name_label.place(x=x - X_OFFSET, y=y - Y_OFFSET)
    song_name_label["text"] = "Thank you. Are you ready to listen to the next song?"
    yes_button.place(x=x + BUTTON_X_OFFSET, y=y - BUTTON_Y_OFFSET)
    progress_label.place(x=x + PROGRESS_X_OFFSET, y=y + PROGRESS_Y_OFFSET)
    progress_label["text"] = str(cont_song) + " / " + str(number_songs)


def handle_space_press(event):
    """
    Handles the event when the space bar is pressed.

    The function checks if music is playing and if the space bar is pressed. If so, it calculates the time difference between the
    current time and the start time, and appends this to the beats list. It also sets space_pressed to True and space_press_time to 0.
    """
    global space_pressed
    global start_time
    space_pressed = False
    pygame.mixer.init()
    if pygame.mixer.music.get_busy():
        if event.char == " ":
            current_time = time.time()
            time_difference = current_time - start_time
            beats.append(time_difference)
            space_pressed = True
            space_press_time = 0


def load_song(song_filename):
    """
    Loads a song into the pygame mixer.

    The function loads a song into the pygame mixer from the Audio directory. It then sets an end event for when the song finishes
    playing, and shows the length of the song.
    """
    song_path = os.path.join("Audio", song_filename)
    pygame.mixer.music.load(song_path)

    pygame.mixer.music.set_endevent(pygame.constants.USEREVENT)
    show_song_length(song_filename)


def show_song_length(song_filename):
    """
    Shows the length of a song.

    The function calculates the length of a song from the Audio directory and displays it in the length label. It then starts a new
    thread to count the duration of the song.
    """
    song_path = os.path.join("Audio", song_filename)
    audio_file = MP3(song_path)
    total_duration = audio_file.info.length

    minutes, seconds = divmod(total_duration, 60)
    minutes = round(minutes)
    seconds = round(seconds)

    time_format = "{:02d}:{:02d}".format(minutes, seconds)

    total_duration_label["text"] = "Total Duration : " + time_format
    thread = threading.Thread(target=start_count, args=(total_duration,))
    thread.start()


def start_count(total_duration):
    """
    Starts counting the duration of a song.

    The function starts counting the duration of a song and updates the current time label. It also handles the event when the song
    finishes playing, and sends a message with the beat times and the sum of the beat times.
    """
    global is_stopped
    global is_delayed
    is_stopped = False
    global current_time
    current_time = 0
    global beat_times
    beat_times = []
    is_ended = True
    global space_press_time
    space_press_time = 0
    global message_to_send
    global song_count
    pygame.init()
    global start_time
    while is_ended:
        while current_time <= total_duration and pygame.mixer.music.get_busy():
            if is_stopped:
                current_time = 0
                space_press_time = 0
                beat_times = []
            else:
                time.sleep(0.1)
                current_time += 0.1
                minutes, seconds = divmod(current_time, 59)
                minutes = round(minutes)
                seconds = round(seconds)
                time_format = "{:02d}:{:02d}".format(minutes, seconds)
                current_time_label["text"] = "Current Time : " + time_format
        for event in pygame.event.get():
            if (
                event.type == pygame.constants.USEREVENT
                and current_time >= total_duration - 5
            ):
                beat_times_message = ""
                count = 0
                for beat_time in beat_times:
                    if count < len(beat_times) - 1:
                        beat_times_message += str(beat_time) + " "
                        count += 1
                    else:
                        beat_times_message += str(beat_time)
                if is_delayed:
                    pygame.mixer.music.stop()
                    message_to_send = (
                        "delay;"
                        + str(user_id)
                        + ";"
                        + beat_times_message
                        + ";"
                        + str(calculate_delay(beat_times_message))
                    )
                    print(message_to_send)
                    write_log(message_to_send)
                    show_delay_message()
                    is_ended = False
                else:
                    are_beats_ok = validate_beats(beat_times)
                    sum_beat_times = sum_beats(beat_times_message)
                    pygame.mixer.music.stop()
                    message_to_send = (
                        "save;"
                        + song_name
                        + ";"
                        + str(user_id)
                        + ";"
                        + str(delay_number)
                        + ";"
                        + str(sum_beat_times)
                        + ";"
                        + beat_times_message
                    )
                    print(message_to_send)
                    write_log(message_to_send)
                    if are_beats_ok:
                        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                            s.connect((HOST, PORT))
                            s.sendall(message_to_send.encode("utf-8"))
                        if song_count < number_songs:
                            show_next_song()
                            song_count += 1
                        else:
                            show_end_message()
                        is_ended = False
                    else:
                        show_bad_bpm_message()
                        is_ended = False


def show_end_message():
    """
    Shows an end message.

    The function hides the player and shows an end message. It also shows an OK button.
    """
    play_button.place_forget()
    retry_button.place_forget()
    song_name_label.place_forget()
    total_duration_label.place_forget()
    current_time_label.place_forget()

    continue_button.place_forget()
    back_button.place_forget()

    song_name_label["text"] = (
        "Thank you very much for participating. You should take a 30-minute break \n to continue with the activity."
    )
    song_name_label.place(x=x - 140, y=y - 75)
    ok_button.place(x=x, y=y - 20)


def restart(event):
    """
    Restarts the song count and sets the delay to True.

    The function draws the data entry, resets the song count to 1, and sets the delay to True.
    """
    global song_count
    global is_delayed
    draw_data_entry()
    song_count = 1
    is_delayed = True


def show_bad_bpm_message():
    """
    Shows a bad BPM message.

    The function hides the player and shows a bad BPM message. It also shows a Retry OK button and loads the song.
    """
    global song_name

    play_button.place_forget()
    retry_button.place_forget()
    song_name_label.place_forget()
    total_duration_label.place_forget()
    current_time_label.place_forget()

    continue_button.place_forget()
    back_button.place_forget()

    song_name_label["text"] = (
        "The data does not have the necessary quality, \n please listen to the song again."
    )
    song_name_label.place(x=x - 90, y=y - 75)

    ok_retry_button.place(x=x, y=y - 20)

    load_song(song_name)


def validate_beats(beats):
    """
    Validates the beats.

    The function counts the number of beats in each minute and checks if they are within the valid range. It returns True if the beats
    are valid and False otherwise.
    """
    count_minute_1 = 0
    count_minute_2 = 0
    count_minute_3 = 0
    is_valid = False

    for beat in beats:
        if beat <= 60:
            count_minute_1 += 1
        elif 60 < beat <= 120:
            count_minute_2 += 1
        elif 120 < beat <= 180:
            count_minute_3 += 1

    print("Minute 1 : " + str(count_minute_1))
    write_log("Minute 1 : " + str(count_minute_1))
    print("Minute 2 : " + str(count_minute_2))
    write_log("Minute 2 : " + str(count_minute_2))
    print("Minute 3 : " + str(count_minute_3))
    write_log("Minute 3 : " + str(count_minute_3))

    if 50 <= count_minute_1 <= 150 and 50 <= count_minute_2 <= 150:
        is_valid = True
        if 60 <= count_minute_3 <= 140:
            print("Valid for 3 minutes")

    print(is_valid)

    return is_valid


def continue_after_delay(event):
    """
    Continues after a delay.

    The function sends a message, sets the delay to False, updates the name label with the song name, loads the song, and draws the music player.
    """
    global is_delayed
    global message_to_send
    global song_name

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((HOST, PORT))
        s.sendall(message_to_send.encode("utf-8"))
        write_log(message_to_send)

    is_delayed = False

    song_name_label["text"] = song_name
    load_song(song_name)
    print("Song: " + song_name)
    write_log("Song: " + song_name)
    draw_music_player(event)


def repeat_delay(event):
    """
    Repeats the delay.

    The function calls the delay player, loads the song "salsa_loop_82bpm.mp3", and sets the delay to True.
    """
    global is_delayed

    show_delay_player()
    load_song("salsa_loop_82bpm.mp3")

    is_delayed = True


def calculate_delay(delayed_beats):
    """
    Calculates the delay.

    The function takes a list of delayed beats and returns the calculated delay. Currently, it returns 0 as a placeholder.
    """
    return 0


def play_song(event):
    """
    Plays the song.

    The function starts playing the song, sets the start time to the current time, and sets is_stopped to False.
    """
    global is_stopped
    global start_time

    pygame.mixer.music.play()
    start_time = time.time()
    is_stopped = False


def play_again(event):
    """
    Stops the song and sets is_stopped to True.

    The function stops the currently playing song and sets the is_stopped variable to True.
    """
    global is_stopped

    pygame.mixer.music.stop()
    is_stopped = True


# Bind events to the buttons and labels
send_button.bind("<Button-1>", send_user_id)
play_button.bind("<Button-1>", play_song)
retry_button.bind("<Button-1>", play_again)
continue_button.bind("<Button-1>", continue_after_delay)
back_button.bind("<Button-1>", repeat_delay)
yes_button.bind("<Button-1>", send_user_id)
hidden_label.bind("<Button-1>", restart)
ok_button.bind("<Button-1>", restart)
ok_retry_button.bind("<Button-1>", draw_music_player)

# Bind the space key to the space_feedback function
ROOT.bind("<Key>", handle_space_press)

# Start the main loop
ROOT.mainloop()
