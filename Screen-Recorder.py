import tkinter as tk
from tkinter import ttk, filedialog
import pyautogui
import numpy as np
import cv2
import sounddevice as sd
import threading
import time
import os
from datetime import datetime
import queue
import threading
from PIL import Image, ImageTk

class ScreenRecorder:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Screen Recorder")
        
        # Make window transparent
        self.root.attributes('-alpha', 0.7)
        
        # Remove window decorations for a cleaner look
        self.root.overrideredirect(True)
        
        # Variables
        self.recording = False
        self.frames = []
        self.audio_data = queue.Queue()
        
        # Configure main window
        self.setup_window()
        self.setup_ui()
        
        # Bind keyboard shortcuts
        self.root.bind('<Command-q>', lambda e: self.root.quit())
        self.root.bind('<Escape>', lambda e: self.root.quit())
        
        # Variables for window dragging
        self.x = None
        self.y = None
        self.start_x = None
        self.start_y = None
        
    def setup_window(self):
        # Set default size
        self.root.geometry('400x300')
        
        # Make window draggable
        self.root.bind('<Button-1>', self.start_drag)
        self.root.bind('<B1-Motion>', self.drag)
        
        # Make window resizable
        self.root.resizable(True, True)
        
    def setup_ui(self):
        # Create main frame
        self.main_frame = tk.Frame(self.root, bg='black')
        self.main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Control buttons frame
        self.control_frame = tk.Frame(self.main_frame, bg='black')
        self.control_frame.pack(side=tk.BOTTOM, pady=10)
        
        # Record button
        self.record_button = tk.Button(
            self.control_frame,
            text="⏺️ Record",
            command=self.toggle_recording,
            bg='red',
            fg='white'
        )
        self.record_button.pack(side=tk.LEFT, padx=5)
        
        # Close button
        self.close_button = tk.Button(
            self.control_frame,
            text="✖️ Close",
            command=self.root.quit,
            bg='gray',
            fg='white'
        )
        self.close_button.pack(side=tk.LEFT, padx=5)
        
    def start_drag(self, event):
        self.start_x = event.x
        self.start_y = event.y
        
    def drag(self, event):
        if self.start_x is not None and self.start_y is not None:
            dx = event.x - self.start_x
            dy = event.y - self.start_y
            x = self.root.winfo_x() + dx
            y = self.root.winfo_y() + dy
            self.root.geometry(f"+{x}+{y}")
            
    def record_screen(self):
        while self.recording:
            # Get the window position and size
            x = self.root.winfo_x()
            y = self.root.winfo_y()
            width = self.root.winfo_width()
            height = self.root.winfo_height()
            
            # Capture the screen area
            screenshot = pyautogui.screenshot(region=(x, y, width, height))
            frame = np.array(screenshot)
            frame = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)
            self.frames.append(frame)
            
            # Small delay to control frame rate
            time.sleep(1/30)  # 30 FPS
            
    def record_audio(self):
        with sd.InputStream(channels=2, callback=self.audio_callback, samplerate=44100):
            while self.recording:
                time.sleep(0.1)
                
    def audio_callback(self, indata, frames, time, status):
        if status:
            print('Audio callback error:', status)
        self.audio_data.put(indata.copy())
        
    def toggle_recording(self):
        if not self.recording:
            # Start recording
            self.recording = True
            self.record_button.config(text="⏹️ Stop", bg='gray')
            
            # Start screen recording thread
            self.screen_thread = threading.Thread(target=self.record_screen)
            self.screen_thread.start()
            
            # Start audio recording thread
            self.audio_thread = threading.Thread(target=self.record_audio)
            self.audio_thread.start()
        else:
            # Stop recording
            self.recording = False
            self.record_button.config(text="⏺️ Record", bg='red')
            
            # Wait for threads to finish
            self.screen_thread.join()
            self.audio_thread.join()
            
            # Save the recording
            self.save_recording()
            
    def save_recording(self):
        if not self.frames:
            return
            
        # Ask user for save location
        filename = filedialog.asksaveasfilename(
            defaultextension=".mp4",
            filetypes=[("MP4 files", "*.mp4")]
        )
        
        if filename:
            # Get the first frame's dimensions
            height, width = self.frames[0].shape[:2]
            
            # Create video writer
            fourcc = cv2.VideoWriter_fourcc(*'mp4v')
            out = cv2.VideoWriter(filename, fourcc, 30.0, (width, height))
            
            # Write frames
            for frame in self.frames:
                out.write(frame)
                
            out.release()
            
            # Clear frames
            self.frames = []
            
    def run(self):
        self.root.mainloop()

if __name__ == "__main__":
    # Create and run the application
    app = ScreenRecorder()
    app.run()
