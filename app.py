# Import modules
from tkinter import *
from tkinter import messagebox
from customtkinter import *
from PIL import Image, ImageTk
import sqlite3
import random
import matplotlib.pyplot as plt
import sys, os

from application.authentication import Register, Login


def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS2
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)


# Basic settings
root = CTk()
root.title("Rock Paper Scissors | Login")
root.iconbitmap(resource_path("assets\\icon_trs.ico"))
x = root.winfo_screenwidth() // 2
y = int(root.winfo_screenheight() * 0.1)
root.geometry("360x640+" + str(x) + "+" + str(y))
root.resizable(False, False)

# Connect to the database
conn = sqlite3.connect(resource_path("data\\players.db"))
c = conn.cursor()

# Create the db tables
c.execute(
    """CREATE TABLE IF NOT EXISTS users(
		username text NOT NULL, 
        email text NOT NULL, 
        password text NOT NULL
)"""
)

c.execute(
    """CREATE TABLE IF NOT EXISTS stats(
		id INTEGER PRIMARY KEY AUTOINCREMENT,
		username text NOT NULL,
		wins int NOT NULL,
        draws int NOT NULL,
        losses int NOT NULL,
        rock_used int NOT NULL,
        papers_used int NOT NULL,
        scissors_used int NOT NULL,
        FOREIGN KEY (username) REFERENCES users (username) ON DELETE CASCADE
)"""
)

# Load images
rock_image = ImageTk.PhotoImage(
    Image.open(("assets\\rock_trs.ico")).resize((20, 20), Image.LANCZOS)
)
paper_image = ImageTk.PhotoImage(
    Image.open(resource_path("assets\\paper_trs.ico")).resize((20, 20), Image.LANCZOS)
)
scissors_image = ImageTk.PhotoImage(
    Image.open(resource_path("assets\\scissors_trs.ico")).resize(
        (20, 20), Image.LANCZOS
    )
)

stats_image = ImageTk.PhotoImage(
    Image.open(resource_path("assets\\stats_trs.ico")).resize((20, 20), Image.LANCZOS)
)

rock_image_to_play = ImageTk.PhotoImage(
    Image.open(resource_path("assets\\rock_trs.ico")).resize((80, 80), Image.LANCZOS)
)
paper_image_to_play = ImageTk.PhotoImage(
    Image.open(resource_path("assets\\paper_trs.ico")).resize((80, 80), Image.LANCZOS)
)
scissors_image_to_play = ImageTk.PhotoImage(
    Image.open(resource_path("assets\\scissors_trs.ico")).resize(
        (80, 80), Image.LANCZOS
    )
)

# Create Choices for the Computer
choices = ["rock", "paper", "scissors"]


# Functions
def stats_callback():
    conn = sqlite3.connect(resource_path("data\\players.db"))
    c = conn.cursor()

    user = get_user(main_frame)

    c.execute("SELECT wins FROM stats WHERE username = ?", (user,))
    wins = (c.fetchall())[0][0]

    c.execute("SELECT draws FROM stats WHERE username = ?", (user,))
    draws = (c.fetchall())[0][0]

    c.execute("SELECT losses FROM stats WHERE username = ?", (user,))
    losses = (c.fetchall())[0][0]

    c.execute("SELECT rock_used FROM stats WHERE username = ?", (user,))
    rock_used = (c.fetchall())[0][0]

    c.execute("SELECT papers_used FROM stats WHERE username = ?", (user,))
    papers_used = (c.fetchall())[0][0]

    c.execute("SELECT scissors_used FROM stats WHERE username = ?", (user,))
    scissors_used = (c.fetchall())[0][0]

    used_data = [rock_used, papers_used, scissors_used]
    used_labels = ["Rock", "Paper", "Scissors"]

    score_data = [wins, draws, losses]
    score_labels = ["Wins", "Draws", "Losses"]
    figure, axis = plt.subplots(2)
    axis[0].pie(used_data, labels=used_labels, autopct="%1.1f%%")
    axis[0].set_title("Times used Rock/Paper/Scissors:")

    axis[1].pie(score_data, labels=score_labels, autopct="%1.1f%%")
    axis[1].set_title("Wins-Draws-Losses Percentages:")

    plt.show()

    conn.commit()
    conn.close()


def choice_callback(choice):
    conn = sqlite3.connect(resource_path("data\\players.db"))
    c = conn.cursor()

    user = get_user(main_frame)

    c.execute("SELECT wins FROM stats WHERE username = ?", (user,))
    user_score = (c.fetchall())[0][0]

    c.execute("SELECT losses FROM stats WHERE username = ?", (user,))
    comp_score = (c.fetchall())[0][0]

    c.execute("SELECT draws FROM stats WHERE username = ?", (user,))
    draw = (c.fetchall())[0][0]

    c.execute("SELECT rock_used FROM stats WHERE username = ?", (user,))
    rock_used = (c.fetchall())[0][0]

    c.execute("SELECT papers_used FROM stats WHERE username = ?", (user,))
    papers_used = (c.fetchall())[0][0]

    c.execute("SELECT scissors_used FROM stats WHERE username = ?", (user,))
    scissors_used = (c.fetchall())[0][0]

    computer_choice = random.choice(choices)

    if choice == "rock" and computer_choice == "rock":
        rock_used += 1
        draw += 1

        player_choice_lbl = CTkLabel(
            master=results_frame,
            image=rock_image_to_play,
            text=None,
        )
        player_choice_lbl.place(relx=0.15, rely=0.1)

        vs_lbl = CTkLabel(
            master=results_frame,
            text="VS",
            font=("Comic Sans MS", 20, "bold", "italic"),
            text_color="#FF69B4",
        )
        vs_lbl.place(relx=0.45, rely=0.45)

        computer_choice_lbl = CTkLabel(
            master=results_frame,
            image=rock_image_to_play,
            text=None,
        )
        computer_choice_lbl.place(relx=0.65, rely=0.65)

        msg = messagebox.showinfo("Result", "Rock against Rock. Draw!")
        if msg == "ok":
            player_choice_lbl.configure(text="", image="")
            computer_choice_lbl.configure(text="", image="")
            vs_lbl.configure(text="")

    elif choice == "rock" and computer_choice == "paper":
        rock_used += 1
        comp_score += 1

        player_choice_lbl = CTkLabel(
            master=results_frame,
            image=rock_image_to_play,
            text=None,
        )
        player_choice_lbl.place(relx=0.15, rely=0.1)

        vs_lbl = CTkLabel(
            master=results_frame,
            text="VS",
            font=("Comic Sans MS", 20, "bold", "italic"),
            text_color="#FF69B4",
        )
        vs_lbl.place(relx=0.45, rely=0.45)

        computer_choice_lbl = CTkLabel(
            master=results_frame,
            image=paper_image_to_play,
            text=None,
        )
        computer_choice_lbl.place(relx=0.65, rely=0.65)

        msg = messagebox.showinfo("Result", "Paper wraps Rock. Loss!")
        if msg == "ok":
            player_choice_lbl.configure(text="", image="")
            computer_choice_lbl.configure(text="", image="")
            vs_lbl.configure(text="", image="")

    elif choice == "rock" and computer_choice == "scissors":
        rock_used += 1
        user_score += 1

        player_choice_lbl = CTkLabel(
            master=results_frame,
            image=rock_image_to_play,
            text=None,
        )
        player_choice_lbl.place(relx=0.15, rely=0.1)

        vs_lbl = CTkLabel(
            master=results_frame,
            text="VS",
            font=("Comic Sans MS", 20, "bold", "italic"),
            text_color="#FF69B4",
        )
        vs_lbl.place(relx=0.45, rely=0.45)

        computer_choice_lbl = CTkLabel(
            master=results_frame,
            image=scissors_image_to_play,
            text=None,
        )
        computer_choice_lbl.place(relx=0.65, rely=0.65)

        msg = messagebox.showinfo("Result", "Rock crashes Scissors. Win!")
        if msg == "ok":
            player_choice_lbl.configure(text="", image="")
            computer_choice_lbl.configure(text="", image="")
            vs_lbl.configure(text="", image="")

    elif choice == "paper" and computer_choice == "rock":
        papers_used += 1
        user_score += 1

        player_choice_lbl = CTkLabel(
            master=results_frame,
            image=paper_image_to_play,
            text=None,
        )
        player_choice_lbl.place(relx=0.15, rely=0.1)

        vs_lbl = CTkLabel(
            master=results_frame,
            text="VS",
            font=("Comic Sans MS", 20, "bold", "italic"),
            text_color="#FF69B4",
        )
        vs_lbl.place(relx=0.45, rely=0.45)

        computer_choice_lbl = CTkLabel(
            master=results_frame,
            image=rock_image_to_play,
            text=None,
        )
        computer_choice_lbl.place(relx=0.65, rely=0.65)

        msg = messagebox.showinfo("Result", "Paper wraps Rock. Win!")
        if msg == "ok":
            player_choice_lbl.configure(text="", image="")
            computer_choice_lbl.configure(text="", image="")
            vs_lbl.configure(text="", image="")

    elif choice == "paper" and computer_choice == "paper":
        papers_used += 1
        draw += 1

        player_choice_lbl = CTkLabel(
            master=results_frame,
            image=paper_image_to_play,
            text=None,
        )
        player_choice_lbl.place(relx=0.15, rely=0.1)

        vs_lbl = CTkLabel(
            master=results_frame,
            text="VS",
            font=("Comic Sans MS", 20, "bold", "italic"),
            text_color="#FF69B4",
        )
        vs_lbl.place(relx=0.45, rely=0.45)

        computer_choice_lbl = CTkLabel(
            master=results_frame,
            image=paper_image_to_play,
            text=None,
        )
        computer_choice_lbl.place(relx=0.65, rely=0.65)

        msg = messagebox.showinfo("Result", "Paper against Paper. Draw!")
        if msg == "ok":
            player_choice_lbl.configure(text="", image="")
            computer_choice_lbl.configure(text="", image="")
            vs_lbl.configure(text="")

    elif choice == "paper" and computer_choice == "scissors":
        papers_used += 1
        comp_score += 1

        player_choice_lbl = CTkLabel(
            master=results_frame,
            image=paper_image_to_play,
            text=None,
        )
        player_choice_lbl.place(relx=0.15, rely=0.1)

        vs_lbl = CTkLabel(
            master=results_frame,
            text="VS",
            font=("Comic Sans MS", 20, "bold", "italic"),
            text_color="#FF69B4",
        )
        vs_lbl.place(relx=0.45, rely=0.45)

        computer_choice_lbl = CTkLabel(
            master=results_frame,
            image=scissors_image_to_play,
            text=None,
        )
        computer_choice_lbl.place(relx=0.65, rely=0.65)

        msg = messagebox.showinfo("Result", "Scissors cut Paper. Loss!")
        if msg == "ok":
            player_choice_lbl.configure(text="", image="")
            computer_choice_lbl.configure(text="", image="")
            vs_lbl.configure(text="", image="")

    elif choice == "scissors" and computer_choice == "rock":
        scissors_used += 1
        comp_score += 1

        player_choice_lbl = CTkLabel(
            master=results_frame,
            image=scissors_image_to_play,
            text=None,
        )
        player_choice_lbl.place(relx=0.15, rely=0.1)

        vs_lbl = CTkLabel(
            master=results_frame,
            text="VS",
            font=("Comic Sans MS", 20, "bold", "italic"),
            text_color="#FF69B4",
        )
        vs_lbl.place(relx=0.45, rely=0.45)

        computer_choice_lbl = CTkLabel(
            master=results_frame,
            image=rock_image_to_play,
            text=None,
        )
        computer_choice_lbl.place(relx=0.65, rely=0.65)

        msg = messagebox.showinfo("Result", "Rock smashes Scissors. Loss!")
        if msg == "ok":
            player_choice_lbl.configure(text="", image="")
            computer_choice_lbl.configure(text="", image="")
            vs_lbl.configure(text="", image="")

    elif choice == "scissors" and computer_choice == "paper":
        scissors_used += 1
        user_score += 1

        player_choice_lbl = CTkLabel(
            master=results_frame,
            image=scissors_image_to_play,
            text=None,
        )
        player_choice_lbl.place(relx=0.15, rely=0.1)

        vs_lbl = CTkLabel(
            master=results_frame,
            text="VS",
            font=("Comic Sans MS", 20, "bold", "italic"),
            text_color="#FF69B4",
        )
        vs_lbl.place(relx=0.45, rely=0.45)

        computer_choice_lbl = CTkLabel(
            master=results_frame,
            image=paper_image_to_play,
            text=None,
        )
        computer_choice_lbl.place(relx=0.65, rely=0.65)

        msg = messagebox.showinfo("Result", "Scissors cut Paper. Win!")
        if msg == "ok":
            player_choice_lbl.configure(text="", image="")
            computer_choice_lbl.configure(text="", image="")
            vs_lbl.configure(text="", image="")

    else:
        scissors_used += 1
        draw += 1

        player_choice_lbl = CTkLabel(
            master=results_frame,
            image=scissors_image_to_play,
            text=None,
        )
        player_choice_lbl.place(relx=0.15, rely=0.1)

        vs_lbl = CTkLabel(
            master=results_frame,
            text="VS",
            font=("Comic Sans MS", 20, "bold", "italic"),
            text_color="#FF69B4",
        )
        vs_lbl.place(relx=0.45, rely=0.45)

        computer_choice_lbl = CTkLabel(
            master=results_frame,
            image=scissors_image_to_play,
            text=None,
        )
        computer_choice_lbl.place(relx=0.65, rely=0.65)

        msg = messagebox.showinfo("Result", "Scissors against Scissors. Draw!")
        if msg == "ok":
            player_choice_lbl.configure(text="", image="")
            computer_choice_lbl.configure(text="", image="")
            vs_lbl.configure(text="")

    updated_values = (
        user_score,
        comp_score,
        draw,
        rock_used,
        papers_used,
        scissors_used,
        user,
    )
    c.execute(
        "UPDATE stats SET wins = ?, losses = ?, draws = ?, rock_used = ?, papers_used = ?, scissors_used = ? WHERE username = ?",
        updated_values,
    )

    p_score_lbl.configure(text=user_score)
    c_score_lbl.configure(text=comp_score)

    conn.commit()
    conn.close()


def go_to_login_callback():
    root.title("Rock Paper Scissors | Login")
    register_frame.grid_forget()
    login_frame.grid(row=0, column=0)


def register_callback():
    conn = sqlite3.connect(resource_path("data\\players.db"))
    c = conn.cursor()

    username = register_username_entry.get()
    email = register_email_entry.get()
    password = register_password_entry.get()
    user = (username, email, password)

    admin = Register(users_db=resource_path("data\\players.db"))
    registered = admin.register_user(user)
    if registered:
        register_username_entry.delete(0, END)
        register_email_entry.delete(0, END)
        register_password_entry.delete(0, END)
        c.execute(
            "INSERT INTO stats (username, wins, draws, losses, rock_used, papers_used, scissors_used) VALUES (?, 0, 0, 0, 0, 0, 0)",
            (username,),
        )
        conn.commit()
        register_frame.grid_forget()
        main_frame.grid(row=0, column=0)
        greet_user(username)
        root.title("Rock Paper Scissors | Play!")
    else:
        pass

    root.focus()
    conn.commit()
    conn.close()


def go_to_register_callback():
    root.title("Rock Paper Scissors | Register")
    login_frame.grid_forget()
    register_frame.grid(row=0, column=0)


def login_callback():
    username = login_username_entry.get()
    password = login_password_entry.get()
    user = (username, password)

    admin = Login(users_db=resource_path("data\\players.db"))
    logged_in = admin.login_user(user)
    if logged_in:
        login_username_entry.delete(0, END)
        login_password_entry.delete(0, END)
        login_frame.grid_forget()
        main_frame.grid(row=0, column=0)
        greet_user(username)
        root.title("Rock Paper Scissors | Play!")
    else:
        pass

    root.focus()


def greet_user(user):
    global p_score_lbl, c_score_lbl
    lbl = CTkLabel(
        master=main_frame,
        text=f"Time to play {user}",
        font=("Comic Sans MS", 18, "bold"),
        text_color="#7DF9FF",
    )
    lbl.place(relx=0.15, rely=0.05)

    c.execute("SELECT wins FROM stats WHERE username = ?", (user,))
    p_value = (c.fetchall())[0][0]
    wins = IntVar(value=p_value)

    c.execute("SELECT losses FROM stats WHERE username = ?", (user,))
    c_value = (c.fetchall())[0][0]
    losses = IntVar(value=c_value)

    p_score_lbl = CTkLabel(
        master=stats_frame,
        text=f"{wins.get()}",
        font=("Comic Sans MS", 15, "bold"),
        text_color="#39FF14",
        width=5,
    )
    p_score_lbl.place(relx=0.25, rely=0.3)

    wins_lbl = CTkLabel(
        master=stats_frame,
        text=f"{user}:",
        font=("Comic Sans MS", 15, "bold", "underline"),
        text_color="#39FF14",
    )
    wins_lbl.place(relx=0.1, rely=0.3)

    c_score_lbl = CTkLabel(
        master=stats_frame,
        text=f"{losses.get()}",
        font=("Comic Sans MS", 15, "bold"),
        text_color="#39FF14",
        width=5,
    )
    c_score_lbl.place(relx=0.37, rely=0.5)

    losses_lbl = CTkLabel(
        master=stats_frame,
        text=f"Computer:",
        font=("Comic Sans MS", 15, "bold", "underline"),
        text_color="#39FF14",
    )
    losses_lbl.place(relx=0.1, rely=0.5)


def get_user(container):
    for child in container.winfo_children():
        if isinstance(child, CTkLabel):
            label_text = child.cget("text")
            if label_text.startswith("Time to play"):
                return label_text.split(" ")[-1]
    return None


# Create window-frames
login_frame = CTkFrame(
    master=root,
    width=360,
    height=640,
    border_width=3,
    border_color="#FFA500",
    corner_radius=8,
)
login_frame.grid(row=0, column=0)

register_frame = CTkFrame(
    master=root,
    width=360,
    height=640,
    border_width=3,
    border_color="#FFA500",
    corner_radius=8,
)
register_frame.grid(row=0, column=0)

main_frame = CTkFrame(
    master=root,
    width=360,
    height=640,
    border_width=3,
    border_color="#FFA500",
    corner_radius=8,
)
main_frame.grid(row=0, column=0)

# Add widgets to the login frame
login_username_entry = CTkEntry(
    master=login_frame,
    placeholder_text="Username",
    text_color="#7DF9FF",
    placeholder_text_color="#7DF9FF",
    border_color="#FFA500",
    border_width=2,
    width=200,
    font=("Comic Sans MS", 13, "bold"),
    corner_radius=12,
)
login_username_entry.place(relx=0.22, rely=0.1)

login_password_entry = CTkEntry(
    master=login_frame,
    placeholder_text="Password",
    text_color="#7DF9FF",
    placeholder_text_color="#7DF9FF",
    border_color="#FFA500",
    border_width=2,
    width=200,
    font=("Comic Sans MS", 13, "bold"),
    corner_radius=12,
)
login_password_entry.place(relx=0.22, rely=0.2)

login_submit_btn = CTkButton(
    master=login_frame,
    text="Login",
    text_color="#7DF9FF",
    border_color="#FFA500",
    corner_radius=4,
    border_spacing=3,
    border_width=2,
    fg_color="transparent",
    hover_color="#FFA500",
    width=100,
    font=("Comic Sans MS", 13, "bold"),
    command=login_callback,
)
login_submit_btn.place(relx=0.35, rely=0.3)

go_to_register_lbl = CTkLabel(
    master=login_frame,
    text="Don't have an account?",
    text_color="#7DF9FF",
    font=("Comic Sans MS", 15, "bold"),
).place(relx=0.25, rely=0.5)

go_to_register_btn = CTkButton(
    master=login_frame,
    text="Register",
    text_color="#7DF9FF",
    border_color="#FFA500",
    corner_radius=4,
    border_spacing=3,
    border_width=2,
    width=100,
    fg_color="transparent",
    hover_color="#FFA500",
    font=("Comic Sans MS", 13, "bold"),
    command=go_to_register_callback,
)
go_to_register_btn.place(relx=0.35, rely=0.6)

# Add widgets to the register frame
register_username_entry = CTkEntry(
    master=register_frame,
    text_color="#7DF9FF",
    placeholder_text_color="#7DF9FF",
    placeholder_text="Username",
    border_color="#FFA500",
    border_width=2,
    font=("Comic Sans MS", 13, "bold"),
    width=200,
    corner_radius=12,
)
register_username_entry.place(relx=0.22, rely=0.1)

register_email_entry = CTkEntry(
    master=register_frame,
    text_color="#7DF9FF",
    placeholder_text_color="#7DF9FF",
    placeholder_text="Email address",
    border_color="#FFA500",
    border_width=2,
    font=("Comic Sans MS", 13, "bold"),
    width=200,
    corner_radius=12,
)
register_email_entry.place(relx=0.22, rely=0.2)

register_password_entry = CTkEntry(
    master=register_frame,
    text_color="#7DF9FF",
    placeholder_text_color="#7DF9FF",
    placeholder_text="Password",
    border_color="#FFA500",
    border_width=2,
    font=("Comic Sans MS", 13, "bold"),
    width=200,
    corner_radius=12,
)
register_password_entry.place(relx=0.22, rely=0.3)

register_submit_btn = CTkButton(
    master=register_frame,
    text="Register!",
    text_color="#7DF9FF",
    border_color="#FFA500",
    corner_radius=4,
    border_spacing=3,
    border_width=2,
    fg_color="transparent",
    hover_color="#FFA500",
    width=100,
    font=("Comic Sans MS", 13, "bold"),
    command=register_callback,
)
register_submit_btn.place(relx=0.35, rely=0.4)

go_to_login_lbl = CTkLabel(
    master=register_frame,
    text="Already have an account?",
    text_color="#7DF9FF",
    font=("Comic Sans MS", 15, "bold"),
).place(relx=0.25, rely=0.6)

go_to_login_btn = CTkButton(
    master=register_frame,
    text="Login!",
    text_color="#7DF9FF",
    border_color="#FFA500",
    corner_radius=4,
    border_spacing=3,
    border_width=2,
    width=100,
    fg_color="transparent",
    hover_color="#FFA500",
    font=("Comic Sans MS", 13, "bold"),
    command=go_to_login_callback,
)
go_to_login_btn.place(relx=0.35, rely=0.7)

# Add widgets to the main frame
choices_frame = CTkFrame(
    master=main_frame,
    width=300,
    height=50,
    border_color="#7DF9FF",
    border_width=2,
    corner_radius=12,
)
choices_frame.place(relx=0.1, rely=0.1)

results_frame = CTkFrame(
    master=main_frame,
    width=300,
    height=300,
    border_color="#FF69B4",
    border_width=2,
    corner_radius=12,
)
results_frame.place(relx=0.1, rely=0.2)

stats_frame = CTkFrame(
    master=main_frame,
    width=300,
    height=150,
    border_color="#39FF14",
    border_width=2,
    corner_radius=12,
)
stats_frame.place(relx=0.1, rely=0.7)

# Add the option buttons to the choices frame
rock_btn = CTkButton(
    master=choices_frame,
    text=None,
    border_color="#7DF9FF",
    corner_radius=4,
    border_spacing=3,
    border_width=2,
    fg_color="transparent",
    hover_color="#7DF9FF",
    width=20,
    height=20,
    font=("Comic Sans MS", 13, "bold"),
    image=rock_image,
    command=lambda: choice_callback("rock"),
).place(relx=0.15, rely=0.2)

paper_btn = CTkButton(
    master=choices_frame,
    text=None,
    border_color="#7DF9FF",
    corner_radius=4,
    border_spacing=3,
    border_width=2,
    fg_color="transparent",
    hover_color="#7DF9FF",
    width=20,
    height=20,
    font=("Comic Sans MS", 13, "bold"),
    image=paper_image,
    command=lambda: choice_callback("paper"),
).place(relx=0.45, rely=0.2)

scissors_btn = CTkButton(
    master=choices_frame,
    text=None,
    border_color="#7DF9FF",
    corner_radius=4,
    border_spacing=3,
    border_width=2,
    fg_color="transparent",
    hover_color="#7DF9FF",
    width=20,
    height=20,
    font=("Comic Sans MS", 13, "bold"),
    image=scissors_image,
    command=lambda: choice_callback("scissors"),
).place(relx=0.75, rely=0.2)

# Add widgets to the stats frame
view_stats_btn = CTkButton(
    master=stats_frame,
    text="View stats",
    border_color="#39FF14",
    corner_radius=4,
    border_spacing=3,
    border_width=2,
    fg_color="transparent",
    text_color="white",
    hover_color="#39FF14",
    width=50,
    font=("Comic Sans MS", 13, "bold"),
    image=stats_image,
    compound="right",
    command=stats_callback,
)
view_stats_btn.place(relx=0.6, rely=0.35)

# Forget other frames
main_frame.grid_forget()
register_frame.grid_forget()

# Commit changes and close the connection
conn.commit()

# Run the app
root.mainloop()
