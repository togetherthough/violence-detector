import tkinter as tk
from tkinter import filedialog
from PIL import Image, ImageTk
import os
from tkinterdnd2 import DND_FILES, TkinterDnD

class VideoUploadFrame(tk.Frame):
    def __init__(self, master, background_image_path):
        super().__init__(master)
        self.master = master
        self.pack(fill=tk.BOTH, expand=True)

        # Load and set background image
        self.bg_image = Image.open(background_image_path)
        self.bg_photo = ImageTk.PhotoImage(self.bg_image)
        self.bg_label = tk.Label(self, image=self.bg_photo)
        self.bg_label.place(x=0, y=0, relwidth=1, relheight=1)

        # Create upload button
        self.upload_button = tk.Button(self, text="Upload Video", command=self.upload_video)
        self.upload_button.place(relx=0.95, rely=0.95, anchor="se")

        # Label to show selected file
        self.file_label = tk.Label(self, text="Drag and drop a video file here", bg="white")
        self.file_label.place(relx=0.5, rely=0.5, anchor="center")

        # Configure drag and drop
        self.drop_target_register(DND_FILES)
        self.dnd_bind('<<Drop>>', self.drop)

    def upload_video(self):
        file_path = filedialog.askopenfilename(filetypes=[("Video files", "*.mp4 *.avi *.mov")])
        if file_path:
            self.process_video(file_path)

    def drop(self, event):
        file_path = event.data
        if file_path:
            self.process_video(file_path)

    def process_video(self, file_path):
        # Here you can add your video processing logic
        file_name = os.path.basename(file_path)
        self.file_label.config(text=f"Selected video: {file_name}")

# Main application
class App(TkinterDnD.Tk):
    def __init__(self):
        super().__init__()
        self.title("Video Upload")
        self.geometry("800x600")
        
        VideoUploadFrame(self, './camera.jpg')

if __name__ == "__main__":
    app = App()
    app.mainloop()