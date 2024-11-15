# DaVinci Resolve Auto-Import

A Python application that automatically monitors a folder and imports new media files directly into DaVinci Resolve's timeline.

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

- DaVinci Resolve Studio (or Free version)
- Python 3.x installed
- DaVinci Resolve's Scripting API enabled

### Setting up DaVinci Resolve Scripting

1. Open DaVinci Resolve
2. Go to Preferences > System > General
3. Enable "External Scripting Using" option

## Installation

1. Clone this repository:
2. 
3. git clone https://github.com/yourusername/davinci-auto-import.git
4. cd davinci-auto-import