# <img src="https://static.wikia.nocookie.net/tamagotchi/images/7/7c/Nyorotchi_anim_gen1.gif/revision/latest?cb=20181014132249" alt="TaMaGoTcHi" width="50"/> PyGoTcHi

Implements first-gen Tamagotchis in Python

## Overview

The goal of this package is to carry [Tamalib](https://github.com/jcrona/tamalib) to the [most famous language in Github in 2024](https://github.blog/news-insights/octoverse/octoverse-2024/). Bringing this low-level library an an high-level language aims at facilitating its implementation in a server-client logic.

The server-client logic is meaningful for Tamagotchis as it allows 2 functionnalities that were pivotal at the time of the original toy

- Ubiquity. Just like the original toy could be carried everywhere in a kid's pocket, a web service can be accessed from anywhere using a smartphone.
- Real-time consistency. The original toy was real time, embedding an actual watch ; and the creature had a strict schedule that the player had to respect. The server can keep track of time.

## Background

- TamaLib
- ArduinoGotchi
- TamaR
- New ROMs !

## Installation

### As a Python package

Currently the tamalib is only compilable from linux (or WSL). It was compilable from windows on tamaR so this may likely be fixed later.

```sh
pip install build
cd pygotchi
python -m build
cd ..
pip install ./pygotchi
```

## With Docker


## Start the emulation

A Tamagotchi must be instanciated. Then, use the `start` and `stop` methods in order to activate it or to pause it:

```py
tama = Tama()
tama.start()
tama.stop()
```

## ROM

The emulator comes with a blank ROM slot. The ROM must be `flash`ed and `dump`ed using the methods:

```py
rom_file = open("roms/p1.bin", "rb")
bin = rom_file.read() 
tama.flash(bin)
```

and:

```py
bin = tama.dump()
rom_file = open("roms/tmp.bin", "wb")  
rom_file.write(bin)  
rom_file.close()
```

To do:

- windows compilation (why does it work with rcpp)
- test each cpp method
- add py methods (background, icons...)
- webapp (streamlit ?)
- implement new compatibility (recent tamalib commits)
- readme