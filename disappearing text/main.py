from tkinter import *

# Constants
TIMER_FONT = ("Helvetica", 60, "bold")
LARGE_FONT = ("Helvetica", 36, "bold")
MEDIUM_FONT = ("Helvetica", 24)
SMALL_FONT = ("Helvetica", 18)
BEGINNING_BACKGROUND_COLOR = "yellow"
TYPING_BACKGROUND_COLOR = "skyblue"
RESULTS_BACKGROUND_COLOR = "lightgreen"
DEATH_BACKGROUND_COLOR = "red"
MAIN_SECONDS_REMAINING = 120
DEATH_SECONDS_REMAINING = 6
DISCLAIMER_DEFAULT = "You have 2 minutes to type! Don't fall asleep!"

# Global Variables
started_typing = False
first_death_timer_started = False
main_timer_finished = False
main_timer = None
death_timer = None


# Functions for Timer
def main_countdown(count):
    """The 2-minute timer for the program"""
    global main_timer_finished
    count_min = count // 60
    count_sec = count % 60

    if count_sec < 10:
        count_sec = f"0{count_sec}"

    main_timer_label["text"] = f"{count_min}:{count_sec}"
    if count > 0:
        global main_timer
        main_timer = window.after(1000, main_countdown, count - 1)
    else:
        main_timer_finished = True
        window.config(background=RESULTS_BACKGROUND_COLOR)
        disappearing_text_label.config(background=RESULTS_BACKGROUND_COLOR)
        disclaimer_label.config(background=RESULTS_BACKGROUND_COLOR, text="You Did It! Take Your Prompt With You!")
        main_timer_label.config(background=RESULTS_BACKGROUND_COLOR)
        stop_death_countdown()
        reset_button.place(relheight=0.07, relwidth=0.2, relx=0.4, rely=0.92)
        death_timer_label.place_forget()


def stop_death_countdown():
    """Stops the death timer"""
    window.after_cancel(death_timer)


def death_countdown(count):
    """Starts the death timer. If the death timer reaches 0 before the main timer,
    the screen turns black with a 'game over' message in the middle of the screen."""
    death_timer_label.place_forget()
    death_seconds = int(count)

    death_timer_label["text"] = death_seconds

    if count <= 5:
        death_timer_label.place(relx=0.9, rely=0.02)

    if count > 0:
        global death_timer
        death_timer = window.after(1000, death_countdown, count - 1)
    else:
        window.config(background=DEATH_BACKGROUND_COLOR)
        disappearing_text_label.config(background=DEATH_BACKGROUND_COLOR)
        disclaimer_label.config(background=DEATH_BACKGROUND_COLOR)
        main_timer_label.config(background=DEATH_BACKGROUND_COLOR)
        death_timer_label.config(background=DEATH_BACKGROUND_COLOR)
        window.after_cancel(main_timer)
        you_lose_label.place(relx=0.2, rely=0.3)
        typing_field.place_forget()
        reset_button.place(relheight=0.07, relwidth=0.2, relx=0.4, rely=0.7)


def activate(event=None):
    """Starts the program"""
    global started_typing, first_death_timer_started, main_timer_finished
    if not started_typing:
        main_countdown(MAIN_SECONDS_REMAINING)
        window.config(background=TYPING_BACKGROUND_COLOR)
        disappearing_text_label.config(background=TYPING_BACKGROUND_COLOR)
        disclaimer_label.config(background=TYPING_BACKGROUND_COLOR)
        main_timer_label.config(background=TYPING_BACKGROUND_COLOR)
        death_timer_label.config(background=TYPING_BACKGROUND_COLOR)
        started_typing = True
    if not main_timer_finished:
        if not first_death_timer_started:
            death_countdown(DEATH_SECONDS_REMAINING)
            first_death_timer_started = True
        else:
            stop_death_countdown()
            death_countdown(DEATH_SECONDS_REMAINING)


def reset_program():
    """Resets window to starting orientation"""
    global started_typing, first_death_timer_started, main_timer, death_timer, main_timer_finished
    started_typing = False
    first_death_timer_started = False
    main_timer_finished = False
    main_timer = None
    death_timer = None
    window.config(background=BEGINNING_BACKGROUND_COLOR)
    disappearing_text_label.config(background=BEGINNING_BACKGROUND_COLOR)
    disclaimer_label.config(background=BEGINNING_BACKGROUND_COLOR)
    main_timer_label.config(background=BEGINNING_BACKGROUND_COLOR)
    death_timer_label.config(background=BEGINNING_BACKGROUND_COLOR)
    you_lose_label.place_forget()
    typing_field.delete("1.0", "end")
    typing_field.place_forget()
    typing_field.place(relheight=0.7, relwidth=0.8, relx=0.1, rely=0.2)
    main_timer_label["text"] = "2:00"
    death_timer_label.place_forget()
    reset_button.place_forget()
    disclaimer_label["text"] = DISCLAIMER_DEFAULT


# Set up window
window = Tk()
window.geometry("1000x600")
window.title("Disappearing Text App")
window.config(background=BEGINNING_BACKGROUND_COLOR)


# GUI
disappearing_text_label = Label(text="Disappearing Text App", font=LARGE_FONT,
                                background=BEGINNING_BACKGROUND_COLOR)
disappearing_text_label.place(relx=0.09, rely=0.01)

disclaimer_label = Label(text=DISCLAIMER_DEFAULT,
                         font=MEDIUM_FONT, background=BEGINNING_BACKGROUND_COLOR)
disclaimer_label.place(relx=0.09, rely=0.11)

main_timer_label = Label(text="2:00", font=TIMER_FONT, background=BEGINNING_BACKGROUND_COLOR)
main_timer_label.place(relx=0.73, rely=0.02)

death_timer_label = Label(text="10", font=TIMER_FONT, background=BEGINNING_BACKGROUND_COLOR)

typing_field = Text(font=SMALL_FONT)
typing_field.place(relheight=0.7, relwidth=0.8, relx=0.1, rely=0.2)
typing_field.bind("<Key>", activate)

reset_button = Button(text="Reset", font=MEDIUM_FONT, command=reset_program)
you_lose_label = Label(text="You Fell Asleep!\nYou Lose!", fg="white",
                       font=TIMER_FONT, background=DEATH_BACKGROUND_COLOR)

window.mainloop()