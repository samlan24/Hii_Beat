# HiiBeat Audio App

This is a full-stack web application for analyzing and processing audio files. The backend is built with Flask and integrates powerful audio processing libraries like Essentia, Librosa, and FFmpeg. The front end is built with React (using Vite) for a seamless user experience.

## Features

- Upload and analyze audio files (up to 10MB, less than 4 minutes long).
- Retrieve song data such as BPM, key, and other attributes using audio analysis tools.
- Change pitch of a song without affecting BPM.
- Convert audio formats (MP3, WAV, M4A).

## Prerequisites

Before you start, ensure you have the following installed:

- Python 3.8+
- MongoDB

## Installation

Follow these steps to set up the application:

1. Clone the Repository and cd into it

2. Setup the Backend
Create a virtual environment

```bash
python3 -m venv venv
```

Activate the virtual environment

 - Linux/MacOS

```bash
source venv/bin/activate
```

- Windows

```bash
venv\Scripts\activate
```
