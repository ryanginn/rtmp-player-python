import vlc
import tkinter as tk
from tkinter import ttk
from tkinter import Canvas
from ctypes import cast, POINTER
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume

# Create a VLC instance
instance = vlc.Instance("--no-xlib")

# Create a MediaPlayer instance
media_player = instance.media_player_new()

# Create a list of streams from the m3u file (you can fetch this from a URL or load from a local file)
streams = [
    {"url": "rtmp://rtmp-ie.one-tv.uk/stream/MPB1", "channel_name": "MPB1", "channel_number": "101"},
    {"url": "rtmp://rtmp-ie.one-tv.uk/stream/MPB2", "channel_name": "MPB2", "channel_number": "102"},
    {"url": "http://radiozender.mpbnetwerken.nl/radio2.mp3", "channel_name": "Channel 3", "channel_number": "103"},
]

current_stream_index = 0

# Function to play or pause the current stream
def play_pause_stream():
    if media_player.is_playing():
        media_player.pause()
    else:
        media = instance.media_new(streams[current_stream_index]["url"])
        media.get_mrl()
        media_player.set_media(media)
        media_player.play()

        # Update the channel name and number labels
        channel_name_label.config(text=streams[current_stream_index]["channel_name"])
        channel_number_label.config(text=streams[current_stream_index]["channel_number"])

# Function to switch to the next stream
def next_stream():
    global current_stream_index
    current_stream_index = (current_stream_index + 1) % len(streams)
    play_pause_stream()

# Function to switch to the previous stream
def prev_stream():
    global current_stream_index
    current_stream_index = (current_stream_index - 1) % len(streams)
    play_pause_stream()

# Function to adjust the system volume using pycaw
def set_program_volume(volume, vlc_instance):
    volume_level = float(volume) / 100.0
    try:
        sessions = AudioUtilities.GetAllSessions()
        for session in sessions:
            if session.Process and session.Process.name() == "vlc.exe":
                interface = session._ctl.QueryInterface(IAudioEndpointVolume)
                interface.SetMasterVolumeLevelScalar(volume_level, None)
    except Exception as e:
        print(f"Volume adjustment failed: {e}")

# Create the GUI window
root = tk.Tk()
root.title("M3U Stream Player")

# Create a Frame to contain both video and controls
video_frame = ttk.Frame(root)
video_frame.pack()

# Create a Canvas widget to display the video
video_canvas = Canvas(video_frame)
video_canvas.pack()

# Set the media player to use the Canvas as its output
media_player.set_hwnd(video_canvas.winfo_id())

# Create buttons
play_pause_button = ttk.Button(root, text="Play/Pause", command=play_pause_stream)
next_button = ttk.Button(root, text="Next", command=next_stream)
prev_button = ttk.Button(root, text="Previous", command=prev_stream)

# Create labels for the Channel name and Channel number
channel_number_label = ttk.Label(root, text=streams[current_stream_index]["channel_number"])
channel_name_label = ttk.Label(root, text=streams[current_stream_index]["channel_name"])

# Create a Volume control slider
volume_label = ttk.Label(root, text="Volume:")
volume_slider = ttk.Scale(root, from_=0, to=100, orient="horizontal", command=lambda volume: set_program_volume(volume))

# Layout the GUI elements
play_pause_button.pack(side=tk.LEFT)
next_button.pack(side=tk.LEFT)
prev_button.pack(side=tk.LEFT)
channel_number_label.pack(side=tk.LEFT)
channel_name_label.pack(side=tk.LEFT)
volume_slider.pack(side=tk.RIGHT)
volume_label.pack(side=tk.RIGHT)


# Play the initial stream
play_pause_stream()

# Start the GUI main loop
root.mainloop()
