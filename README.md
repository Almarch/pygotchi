# PyGoTcHi <img src="https://static.wikia.nocookie.net/tamagotchi/images/7/7c/Nyorotchi_anim_gen1.gif/revision/latest?cb=20181014132249" alt="PyGoTcHi" align="right" width="100"/>

The goal of this package is to port [Tamalib](https://github.com/jcrona/tamalib) to the [most famous language in Github in 2024](https://github.blog/news-insights/octoverse/octoverse-2024/). Bringing the low-level emulator to a high-level language aims at easing its deployment as a web service.

The web server-client logic makes a special sense for Tamagotchis as it unlocks two key functionnalities of the original game:

- Ubiquity: Just like the original toy could be carried everywhere in a kid's pocket, a web service can be accessed from anywhere using a smartphone.
- Real-time consistency: The creature has a strict schedule that the player has to deal with all along the day. The server can endorse the role to keep track of time.

## State of developement

Tamalib is well bound to the `Tama` class of this package. The package builds on Linux and on the WSL, but not on pure Windows yet. All methods seem to work, but tests without an UI are approximative. The next steps are:

- develop a web UI ;
- adapt Tamalib to a variety of 1st gen ROMs, following the recent Tamalib developments ;
- dockerize the web UI ;
- write this documentation.

## Background
*pass*

<!--

- TamaLib
- ArduinoGotchi
- C++...
- TamaR
    - automatic care: will not be implemented here but looking forward to see the same as tamaR
    - p2 conversion: now useless
- New ROMs !

-->

## Installation

### As a Python package

Build the package with `build` and install it with `pip`:

```sh
pip install build
cd pygotchi
python -m build
cd ..
pip install ./pygotchi
```

## Use from Python

### Start the emulation

A new Tamagotchi must be instanciated:

```py
tama = Tama()
```

The emulator comes with a blank ROM slot. The ROM must be inserted with the `flash` method:

```py
rom_file = open("roms/p1.bin", "rb")
bin = rom_file.read() 
tama.flash(bin)
```

The emulation can be launched and paused with the corresponding methods: `start` and `stop`:

```py
tama.start()
```

### Commands

The screen can be rendered using `display` and the sound frequency is available with `GetFreq`.

Action the 3 buttons `A`, `B` and `C` with the `click` method. Beware the click method use `await asyncio.sleep(delay)` so it should be run as an asynchronous task.

```py
import time
from threading import Thread

Thread(target=tama.click, args=("B", 0.5)).start()
time.sleep(3)
tama.display()
```

The game may be saved anytime using the `save` command:

```py
tama.stop()
bin = tama.save()
cpu_file = open("pets/save.bin", "wb")  
cpu_file.write(bin)  
cpu_file.close()
```

It can then be resumed with `load`:

```py
cpu_file = open("pets/save.bin", "rb")
bin = cpu_file.read() 
tama.load(bin)
tama.start()
```

## Web deployment

### Launch with Docker
*pass*

### Open to the web
*pass*