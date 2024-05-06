"""
client.py
This file contains the client side of the application.
"""

# Standard library imports
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
lbl_welcome = tk.Label(
    ROOT,
    text="Thank you for participating in the salsa annotation experiment. \n Please enter your ID",
)

# Create a button for the user to submit their ID
btn_send = tk.Button(ROOT, text="Submit")

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
lbl_welcome.place(x=x - X_OFFSET, y=y - Y_OFFSET)
btn_send.place(x=x + 30, y=y - BUTTON_Y_OFFSET)
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


def write_log(text):
    log = open("log.txt", "a")
    date = time.strftime("%c")
    msg = "[ " + date + " ] - " + text + "\n"
    log.write(msg)
    log.close()


def send_cedula(event):
    global id_user
    cedula = txt_cedula.get()
    id_user = cedula
    global nom_song
    nom_song = "Nombre de la canción"

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((HOST, PORT))
        user_id_msg = "start;" + cedula
        s.sendall(user_id_msg.encode("utf-8"))
        data = s.recv(65507)
        data = data.decode("utf-8")
        aux = data.split(";")
        if aux[0] == "song_id":
            if aux[1] == "NO_VALIDO":
                # mostrar mensage error
                print("NO_VALIDO")

                messagebox.showerror(
                    message="Este documento no se encuentra registrado", title="ERROR"
                )
            else:
                nom_song = aux[1]
                lbl_name["text"] = nom_song

                if delay:
                    delay_player()
                    load_song("salsa_loop_82bpm.mp3")

                    song_end()
                else:
                    load_song(nom_song)
                    print("cancion:" + nom_song)
                    write_log("cancion:" + nom_song + " idUser:" + id_user)
                    draw_music_player(event)


def song_end():
    pygame.init()
    end = True

    # time.sleep(20)

    for evento in pygame.event.get():

        if evento.type == pygame.constants.USEREVENT:

            end = False


def show_delay_msg():
    btn_play.place_forget()
    btn_stop.place_forget()
    lbl_name.place_forget()
    lbl_length.place_forget()
    lbl_current.place_forget()
    btn_yes.place_forget()

    lbl_name.place(x=x - 140, y=y - 120)
    lbl_name["text"] = (
        "Gracias por practicar. Ahora da click en 'continuar' \n para escuchar la primera canción. Da click en \n 'regresar' si deseas practicar la tarea una vez más."
    )
    btn_cont.place(x=x - 100, y=y - 30)
    btn_reg.place(x=x + 20, y=y - 30)


# metodo para pintar el player del delay
def delay_player():

    # OCULTA ENTRADA DATOS
    txt_cedula.config(state="disabled")
    txt_cedula.place_forget()
    btn_send.config(state="disabled")
    btn_send.place_forget()
    lbl_welcome.place_forget()
    btn_cont.place_forget()
    btn_reg.place_forget()
    btn_yes.place_forget()

    # HACE VISIBLE LA REPRODUCCION DE LA CANCION

    lbl_name.place(x=x - 140, y=y - 120)
    lbl_name["text"] = (
        "Durante el experimento te pediremos que escuches \n canciones de salsa y que marques el pulso de la \n canción (en negras) usando la barra espaciadora \n del teclado. Practica la tarea del experimento \n escuchando un fragmento de salsa:"
    )
    lbl_length.place(x=x - 60, y=y)
    lbl_current.place(x=x - 60, y=y + 20)
    btn_play.place(x=x - 100, y=y + 60)
    btn_stop.place(x=x, y=y + 60)
    # fm_feedback.place(x=x - 110, y=y + 110)


def draw_music_player(event):
    global number_songs
    # OCULTA ENTRADA DATOS
    txt_cedula.config(state="disabled")
    txt_cedula.place_forget()
    btn_send.config(state="disabled")
    btn_send.place_forget()
    lbl_welcome.place_forget()

    btn_cont.place_forget()
    btn_reg.place_forget()
    btn_yes.place_forget()
    btn_ok_retry.place_forget()
    # HACE VISIBLE LA REPRODUCCION DE LA CANCION

    lbl_name.place(x=x - 130, y=y - 110)
    lbl_name["text"] = (
        "Escucha con atención la canción y marca el \n pulso (en negras) usando la barra espaciadora \n del teclado. Si por alguna razón, deseas repetir \n la canción haz click en 'volver a intentar'"
    )
    lbl_length.place(x=x - 60, y=y)
    lbl_current.place(x=x - 60, y=y + 20)
    btn_play.place(x=x - 100, y=y + 60)
    btn_stop.place(x=x, y=y + 60)
    lbl_prog.place(x=x + 450, y=y + 300)
    lbl_prog["text"] = str(cont_song) + " / " + str(number_songs)
    # fm_feedback.place(x=x - 110, y=y + 110)


def draw_data_entry():
    # OCULTA EL REPRODUCTOR
    btn_play.place_forget()
    btn_stop.place_forget()
    lbl_name.place_forget()
    lbl_length.place_forget()
    lbl_current.place_forget()
    btn_yes.place_forget()
    lbl_prog.place_forget()
    btn_ok.place_forget()

    btn_cont.place_forget()
    btn_reg.place_forget()
    # fm_feedback.place_forget()

    # HACE VISIBLE LA ENTRADA DE DATOS
    txt_cedula.config(state="normal")
    btn_send.config(state="normal")
    lbl_welcome.place(x=x - 160, y=y - 140)
    btn_send.place(x=x + 30, y=y - 75)
    txt_cedula.place(x=x - 100, y=y - 70)


def show_next_song():
    global number_songs
    # OCULTA EL REPRODUCTOR
    btn_play.place_forget()
    btn_stop.place_forget()
    lbl_name.place_forget()
    lbl_length.place_forget()
    lbl_current.place_forget()

    btn_cont.place_forget()
    btn_reg.place_forget()
    # fm_feedback.place_forget()

    lbl_name.place(x=x - 140, y=y - 75)
    lbl_name["text"] = "Gracias. ¿Estás listo para escuchar la siguiente canción?"
    btn_yes.place(x=x, y=y - 40)
    lbl_prog.place(x=x + 450, y=y + 300)
    lbl_prog["text"] = str(cont_song) + " / " + str(number_songs)


def space_feedback(event):
    global space_boolean
    global inicio_de_tiempo
    space_boolean = False
    pygame.mixer.init()
    if pygame.mixer.music.get_busy():
        if event.char == " ":
            act = time.time()
            aux = act - inicio_de_tiempo
            # print("BEAT", aux)
            beats.append(aux)
            # Feedback visual
            space_boolean = True
            space_time = 0
        # fm_feedback.place(x=x - 110, y=y + 110)


def load_song(song_name):
    # WINDOWS
    # pygame.mixer.music.load("Audio\\" + song_name)
    # MAC
    pygame.mixer.music.load("Audio/" + song_name)

    pygame.mixer.music.set_endevent(pygame.constants.USEREVENT)
    show_length_song(song_name)


def show_length_song(song_name):
    # WINDOWS
    # audio = MP3("Audio\\" + song_name)
    # MAC
    audio = MP3("Audio/" + song_name)
    total_length = audio.info.length

    mins, secs = divmod(total_length, 60)
    mins = round(mins)
    secs = round(secs)

    timeformat = "{:02d}:{:02d}".format(mins, secs)

    lbl_length["text"] = "Duración Total : " + timeformat
    # start_count(total_length)
    t1 = threading.Thread(target=start_count, args=(total_length,))
    t1.start()


def start_count(t):
    # mixer.music.get_busy(): - Returns FALSE when we press the stop button (music stop playing)
    # Continue - Ignores all of the statements below it. We check if music is paused or not.
    global stop
    global delay
    stop = False
    global current_time
    current_time = 0
    global beats
    beats = []
    end = True
    global space_time
    space_time = 0
    global msg_send
    global cont_song
    pygame.init()
    global inicio_de_tiempo
    while end:
        while current_time <= t and pygame.mixer.music.get_busy():
            if stop:
                current_time = 0
                space_time = 0
                beats = []

            else:

                time.sleep(0.1)
                current_time += 0.1

                mins, secs = divmod(current_time, 59)
                mins = round(mins)
                secs = round(secs)
                timeformat = "{:02d}:{:02d}".format(mins, secs)
                lbl_current["text"] = "Tiempo Actual : " + timeformat

            # >= t-260:
        for evento in pygame.event.get():

            if evento.type == pygame.constants.USEREVENT and current_time >= t - 5:

                beats_msg = ""
                cont = 0
                for item in beats:
                    if cont < len(beats) - 1:
                        beats_msg += str(item) + " "
                        cont += 1
                    else:
                        beats_msg += str(item)
                if delay:
                    pygame.mixer.music.stop()
                    msg_send = (
                        "delay;"
                        + str(id_user)
                        + ";"
                        + beats_msg
                        + ";"
                        + str(get_delay(beats_msg))
                    )
                    print(msg_send)
                    write_log(msg_send)
                    show_delay_msg()
                    end = False

                else:
                    beats_ok = beats_validation(beats)
                    sum = sum_beats(beats_msg)
                    pygame.mixer.music.stop()
                    msg_send = (
                        "save;"
                        + nom_song
                        + ";"
                        + str(id_user)
                        + ";"
                        + str(delay_num)
                        + ";"
                        + str(sum)
                        + ";"
                        + beats_msg
                    )
                    print(msg_send)
                    write_log(msg_send)
                    if beats_ok:
                        # linea 378 da error
                        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                            s.connect((HOST, PORT))
                            s.sendall(msg_send.encode("utf-8"))

                        if cont_song < number_songs:
                            show_next_song()
                            cont_song += 1
                        else:
                            show_end_message()
                        end = False
                    else:
                        show_msg_bad_bpm()
                        end = False


def show_end_message():
    # OCULTA EL REPRODUCTOR
    btn_play.place_forget()
    btn_stop.place_forget()
    lbl_name.place_forget()
    lbl_length.place_forget()
    lbl_current.place_forget()

    btn_cont.place_forget()
    btn_reg.place_forget()

    lbl_name["text"] = (
        "Muchas gracias por participar debes tomar un descanso \n de 30 minutos para continuar con la actividad."
    )
    lbl_name.place(x=x - 140, y=y - 75)
    btn_ok.place(x=x, y=y - 20)


def restart(event):
    global cont_song
    global delay
    draw_data_entry()
    cont_song = 1
    delay = True


def show_msg_bad_bpm():
    global nom_song
    # OCULTA EL REPRODUCTOR
    btn_play.place_forget()
    btn_stop.place_forget()
    lbl_name.place_forget()
    lbl_length.place_forget()
    lbl_current.place_forget()

    btn_cont.place_forget()
    btn_reg.place_forget()

    lbl_name["text"] = (
        "Los datos no tienen la calidad necesaria, por \n favor escucha nuevamente la canción."
    )
    lbl_name.place(x=x - 90, y=y - 75)

    btn_ok_retry.place(x=x, y=y - 20)

    load_song(nom_song)


def beats_validation(beats):
    cont_minute_1 = 0
    cont_minute_2 = 0
    cont_minute_3 = 0
    is_ok = False

    for x in beats:
        if x <= 60:
            cont_minute_1 += 1
        if x > 60 and x <= 120:
            cont_minute_2 += 1
        if x > 120 and x <= 180:
            cont_minute_3 += 1

    print("Minuto 1 : " + str(cont_minute_1))
    write_log("Minuto 1 : " + str(cont_minute_1))
    print("Minuto 2 : " + str(cont_minute_2))
    write_log("Minuto 2 : " + str(cont_minute_2))
    print("Minuto 3 : " + str(cont_minute_3))
    write_log("Minuto 3 : " + str(cont_minute_3))

    if (cont_minute_1 >= 50) and (cont_minute_1 <= 150):
        if (cont_minute_2 >= 50) and (cont_minute_2 <= 150):
            is_ok = True
            if (cont_minute_3 >= 60) and (cont_minute_3 <= 140):
                print("ook 3 minutos")

    print(is_ok)

    return is_ok


def continue_delay(event):
    global delay
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((HOST, PORT))
        s.sendall(msg_send.encode("utf-8"))
        write_log(msg_send)
    delay = False

    lbl_name["text"] = nom_song
    load_song(nom_song)
    print("cancion:" + nom_song)
    write_log("cancion:" + nom_song)
    draw_music_player(event)


def repeat_delay(event):
    global delay
    delay_player()
    load_song("salsa_loop_82bpm.mp3")

    delay = True


def get_delay(beats_delay):
    return 0


def play_song(event):
    global stop
    global inicio_de_tiempo
    pygame.mixer.music.play()
    inicio_de_tiempo = time.time()
    stop = False


def play_again(event):
    global stop
    pygame.mixer.music.stop()
    stop = True


btn_send.bind("<Button-1>", send_cedula)
btn_play.bind("<Button-1>", play_song)
btn_stop.bind("<Button-1>", play_again)
btn_cont.bind("<Button-1>", continue_delay)
btn_reg.bind("<Button-1>", repeat_delay)
btn_yes.bind("<Button-1>", send_cedula)
lbl_hidden.bind("<Button-1>", restart)
btn_ok.bind("<Button-1>", restart)
btn_ok_retry.bind("<Button-1>", draw_music_player)

ROOT.bind("<Key>", space_feedback)

ROOT.mainloop()
