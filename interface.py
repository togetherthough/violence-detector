import tkinter as tk
from tkinter import filedialog
from PIL import Image, ImageTk
import os
from tkinterdnd2 import DND_FILES, TkinterDnD
import cv2

class VideoUploadFrame(tk.Frame):
    def __init__(self, master):
        super().__init__(master)
        self.master = master
        self.pack(fill=tk.BOTH, expand=True)
        self.sand_color = '#C2B888'

        self.master.configure(bg=self.sand_color)

        # Create video display area
        self.video_label = tk.Label(self, bg='black')
        self.video_label.place(relx=0.5, rely=0.4, anchor="center", relwidth=0.8, relheight=0.6)

        # Create upload button
        self.upload_button = tk.Button(self, text="Upload Video", fg=self.sand_color, bg='white', command=self.upload_video)
        self.upload_button.place(relx=0.5, rely=0.8, anchor="center")

        # Create file name label
        self.file_label = tk.Label(self, text="", bg=self.sand_color)
        self.file_label.place(relx=0.5, rely=0.85, anchor="center")

        # Create playback control buttons
        self.play_button = tk.Button(self, text="Play", command=self.play_video, state=tk.DISABLED)
        self.play_button.place(relx=0.45, rely=0.9, anchor="center")
        
        self.pause_button = tk.Button(self, text="Pause", command=self.pause_video, state=tk.DISABLED)
        self.pause_button.place(relx=0.55, rely=0.9, anchor="center")

        # Configure drag and drop
        self.drop_target_register(DND_FILES)
        self.dnd_bind('<<Drop>>', self.drop)

        # Video playback variables
        self.video_path = None
        self.cap = None
        self.is_playing = False

    def upload_video(self):
        file_path = filedialog.askopenfilename(filetypes=[("Video files", "*.mp4 *.avi *.mov")])
        if file_path:
            self.process_video(file_path)

    def drop(self, event):
        file_path = event.data
        if file_path:
            self.process_video(file_path)

    def process_video(self, file_path):
        self.video_path = file_path
        file_name = os.path.basename(file_path)
        self.file_label.config(text=f"Selected video: {file_name}")
        
        self.cap = cv2.VideoCapture(file_path)
        self.show_frame()

        # Enable playback buttons
        self.play_button.config(state=tk.NORMAL)
        self.pause_button.config(state=tk.NORMAL)

    def show_frame(self):
        if self.cap is not None:
            ret, frame = self.cap.read()
            if ret:
                frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                img = Image.fromarray(frame)
                img = img.resize((int(self.video_label.winfo_width()), int(self.video_label.winfo_height())))
                photo = ImageTk.PhotoImage(image=img)
                self.video_label.config(image=photo)
                self.video_label.image = photo
                return True
        return False

    def play_video(self):
        self.is_playing = True
        self.play_next_frame()

    def play_next_frame(self):
        if self.is_playing:
            ret = self.show_frame()
            if ret:
                self.master.after(33, self.play_next_frame)  # ~30 fps
            else:
                self.cap.set(cv2.CAP_PROP_POS_FRAMES, 0)  # Reset to beginning
                self.play_next_frame()

    def pause_video(self):
        self.is_playing = False

# Main application class
class App(TkinterDnD.Tk):
    def __init__(self):
        super().__init__()
        self.title("Video Upload and Player")
        self.geometry("800x600")
        
        VideoUploadFrame(self)

if __name__ == "__main__":
    app = App()
    app.mainloop()