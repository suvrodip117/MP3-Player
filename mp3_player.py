from tkinter import *
import pygame
from PIL import ImageTk, Image
from tkinter import filedialog
import tkinter.ttk as ttk
from mutagen.mp3 import MP3
import time
from ttkthemes import themed_tk

root=themed_tk.ThemedTk(theme="arc")

pygame.mixer.init()

root.title("Music At Your Fingertips")

root.geometry("800x350")

root.resizable(0,0)


#Add songs function
def add_song():
	songs = filedialog.askopenfilenames(initialdir='songs/', title="Choose songs", filetypes=(("mp3 Files", "*.mp3"), ("WAV files", "*.wav"), ))

	for song in songs:
		song_listbox.insert(END, song)


#Song play updation
def playtime():
	current_time = pygame.mixer.music.get_pos() / 1000

	#Song length using mutagen
	current_song_list = song_listbox.curselection()
	current_song = song_listbox.get(current_song_list)
	song_muta = MP3(current_song)
	global song_length
	song_length = song_muta.info.length #returns length in seconds

	slider_pos = int(song_length)
	my_slider.config(to=slider_pos)

	if int(my_slider.get()) == int(current_time):
		my_slider.config(to=slider_pos)
		my_slider.config(value=int(current_time))

	else:
		new_slider_pos = int(my_slider.get()) + 1
		my_slider.config(to=slider_pos, value=new_slider_pos)
		pygame.mixer.music.set_pos(new_slider_pos+2)

	root.after(1000, playtime)


#Play a song
def play():
	song = song_listbox.get(ACTIVE)

	pygame.mixer.music.load(song)
	playtime()
	pygame.mixer.music.play(loops=0)

	
 
#pause a song
paused = False
def pause(ispaused):
	global paused

	if paused:
		pygame.mixer.music.unpause()
		paused = False
	else:
		pygame.mixer.music.pause()
		paused = True


#Forward playlist
def forward_song():
	next_song = song_listbox.curselection() #returns tuple
	next_song = next_song[0] + 1
	song = song_listbox.get(next_song)
	pygame.mixer.music.load(song)
	pygame.mixer.music.play(loops=0)
	
	my_slider.config(value=0)

	song_listbox.selection_clear(0, END)
	song_listbox.activate(next_song)
	song_listbox.selection_set(next_song, last=None)


	playtime()

	#Adjusting slider to song length
	slider_pos = int(song_length)
	my_slider.config(to=slider_pos)



#Rewind playlist
def rewind_song():
	previous_song = song_listbox.curselection()
	previous_song = previous_song[0]-1
	song = song_listbox.get(previous_song)
	pygame.mixer.music.load(song)
	pygame.mixer.music.play(loops=0)
	
	my_slider.config(value=0)

	song_listbox.selection_clear(0, END)
	song_listbox.activate(previous_song)
	song_listbox.selection_set(previous_song, last=None)

	global current_volume
	current_volume = song.get_volume()

	playtime()

	#Adjusting slider to song length
	slider_pos = int(song_length)
	my_slider.config(to=slider_pos)


#Slider function
def slide(x):
	pass
	

#mute volume
muted = False
def mute_vol():
	global muted
	if muted:
		pygame.mixer.music.set_volume(0.7)
		muted = False
	else:
		pygame.mixer.music.set_volume(0.0)
		muted = True


#Volume slider func
def fn_vol_slider(x):
	pygame.mixer.music.set_volume(vol_slider.get())

#master frame
master_frame = Frame(root)
master_frame.pack()

#left frame
left_frame = Frame(master_frame)
left_frame.grid(row=0, column=0, padx=30)


#right frame
right_frame = Frame(master_frame)
right_frame.grid(row=0, column=1, padx=10)


#User button frames
user_control_frame = Frame(right_frame)
user_control_frame.grid(row=0, column=0)

#Creating user's listbox
song_listbox = Listbox(left_frame, width=50, height=15)
song_listbox.grid(row=0, column=0, pady=20)


#Importing and resizing button Images
rewind_img = Image.open('G:/mp3 player/images/rewind.png').resize((160,80), Image.ANTIALIAS)
rewind_btnimg = ImageTk.PhotoImage(rewind_img)

forward_img = Image.open('G:/mp3 player/images/forward.png').resize((160,80), Image.ANTIALIAS)
forward_btnimg = ImageTk.PhotoImage(forward_img)

play_img = Image.open('G:/mp3 player/images/play.png').resize((160,80), Image.ANTIALIAS)
play_btnimg = ImageTk.PhotoImage(play_img)

pause_img = Image.open('G:/mp3 player/images/pause.png').resize((160,80), Image.ANTIALIAS)
pause_btnimg = ImageTk.PhotoImage(pause_img)

vol_img = Image.open('G:/mp3 player/images/Volumebutton.png').resize((45,45), Image.ANTIALIAS)
vol_btnimg = ImageTk.PhotoImage(vol_img)


#Slider
my_slider = ttk.Scale(left_frame, from_=0, to=100, length=300, orient=HORIZONTAL, value=0, command=slide)
my_slider.grid(row=1, column=0)


#creating user control buttons
rewind_btn = 	Button(user_control_frame, image=rewind_btnimg, borderwidth=0, width=38, command=rewind_song)
forward_btn =	Button(user_control_frame, image=forward_btnimg, borderwidth=0, width=44, command=forward_song)
play_btn =		Button(user_control_frame, image=play_btnimg, borderwidth=0, width=55, command=play)
pause_btn =		Button(user_control_frame, image=pause_btnimg, borderwidth=0, width=55, command=lambda:pause(paused))
vol_btn = 		Button(root, image=vol_btnimg, borderwidth=0,width=40, command=mute_vol)


#Arranging the user ctrl buttons in the grid
rewind_btn.grid(row=0, column=0, padx=20)
play_btn.grid(row=0, column=1, padx=20)
pause_btn.grid(row=0, column=2, padx=20)
forward_btn.grid(row=0, column=3, padx=25)
vol_btn.place(x=460,y=172)


#Volume slider
vol_slider = ttk.Scale(right_frame, from_=0, to=1, length=150, orient=HORIZONTAL, value=100, command=fn_vol_slider)
vol_slider.grid(row=1, column=0, pady=20)


#Creating menu to add songs
my_menus = Menu(root)
root.config(menu=my_menus)


#Add Menu
addsong_menu = Menu(my_menus)
my_menus.add_cascade(label="Add:", menu=addsong_menu)
addsong_menu.add_command(label="Add songs to playlist", command=add_song)

root.mainloop()