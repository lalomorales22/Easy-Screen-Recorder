# Easy Screen Recorder

A lightweight, user-friendly screen recording application built with Python and Tkinter. This application allows you to record your screen with audio in a customizable, draggable window.

## Features

- Simple and intuitive user interface
- Screen recording with audio capture
- Draggable and resizable window
- Transparent window overlay
- Customizable recording area
- Keyboard shortcuts support
- MP4 video output
- 30 FPS recording capability

## Requirements

To run this application, you'll need Python 3.6+ and the following dependencies (see requirements.txt):

```
tkinter
pyautogui
numpy
opencv-python
sounddevice
Pillow
```

## Installation

1. Clone the repository:
```bash
git clone https://github.com/lalomorales22/Easy-Screen-Recorder.git
cd Easy-Screen-Recorder
```

2. Install the required dependencies:
```bash
pip install -r requirements.txt
```

## Usage

1. Run the application:
```bash
python Screen-Recorder.py
```

2. The application will appear as a transparent, draggable window on your screen.

3. Controls:
   - Click and drag the window to position it
   - Click "⏺️ Record" to start recording
   - Click "⏹️ Stop" to stop recording
   - Click "✖️ Close" or press ESC to exit the application

4. When you stop recording, you'll be prompted to save the video file in MP4 format.

## Keyboard Shortcuts

- `ESC`: Exit application
- `Command + Q`: Exit application (macOS)

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License - see the LICENSE file for details.
