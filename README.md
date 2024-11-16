# DaVinci Resolve Auto-Importer

A simple tool to **make your recording workflow faster**.
Every time you save a video you have the option to import it into DaVinci Resolve or move it to the trash.

## How it works
1. In OBS (or any other software), set a folder where you want to save your recordings.
2. Start running the app.
3. Select as monitored folder the folder you set in OBS.
4. Every time you save a recording in OBS, you will have 2 choices:
    - Validate: The file will be added to DaVinci Resolve's timeline.
    - Trash: The file will be moved to the trash folder.

## Features

- 🎬 Automatic media file detection
- 🎯 Direct import to DaVinci Resolve timeline
- 🗑️ Quick file management with trash option
- 💻 Simple and intuitive GUI

## Tech Stack

- **Python 3.x**
- **Flet**: Modern Python GUI framework
- **Watchdog**: File system monitoring
- **DaVinci Resolve API**: Media handling and timeline management
- **Send2Trash**: Safe file removal

## Prerequisites

- DaVinci Resolve Studio (or Free version but not tested yet)
- Python installed
- DaVinci Resolve's Scripting API enabled (see below)

### Setting up DaVinci Resolve Scripting API

1. Open DaVinci Resolve
2. Go to Preferences > System > General
3. Set "External Scripting Using" to "Local"
![enable external scripting](https://i.imgur.com/pKpIg0v.png)
