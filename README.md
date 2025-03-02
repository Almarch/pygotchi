# <img src="pygotchi/www/img/favicon.png" alt="PyGoTcHi" width="40"/> The Tamagotchi is live online ! 

The goal of this Python package is to deliver [TamaLIB](https://github.com/jcrona/tamalib) as a web service.

The web server-client logic makes a special sense for Tamagotchis as it unlocks two key functionnalities of the original game:

- Ubiquity: Just like the original toy could be carried everywhere in a kid's pocket, a web service can be accessed from anywhere using a smartphone.
- Real-time consistency: The creature has a strict schedule that the player has to deal with all along the day. The server can endorse the role to keep track of time.

A web app is readily available and dockerized for ease of deployment.

<div align="center">
        <img src="https://github.com/user-attachments/assets/98100f88-279b-4cb2-84cf-29b0c25926db" width="300px"/>
</div>

## 🚀 Run the app

Start by cloning the repo:

```sh
git clone https://github.com/almarch/pygotchi.git
```

### 🐋 Run with Docker

```sh
cd pygotchi
docker build -t tama .
docker run -d -p 8000:80 tama
```

The app is now available at http://localhost:8000.

### 🐍 Run with Python

Build the package with `build` and install it with `pip`:

```sh
pip install build
python -m build ./pygotchi
pip install ./pygotchi
```

It may then be launched using Python:

```sh
python -m pygotchi
```

The app is now available at http://localhost:8000.

### 🌐 Swagger

FastAPI apps come with a swagger. Once the app is launched, have a look at: http://localhost:8000/docs. Not all API are implemented on the UI.

## 🎮 How to use

The game is controlled with 3 buttons (A, B, C) with respect to the original toy. Click the screen to "poke" the toy.

A menu (☰) allows administration over the game.

<div align="center">
<img src="https://github.com/user-attachments/assets/c8a2d21a-9858-4273-b648-29c2455fc771" width="300px" />
</div>

### 🧬 Load a ROM

From the administration menu, flash a ROM. It should be a 12ko .bin file. Use the switch button to get the emulation started. The ROM is loaded on the server, and the emulation runs server-side.

### 💾 Save the game

The game may be saved any time using the Save CPU button from the administration menu. The save.bin file may then be loaded again. Ensure consistency between the loaded CPU and the ROM.

### 🔊 Control the sound

The buzzer may be controlled at 2 levels:

- Using the 🔊 icon: controls the sound on the client side.
- Using the **A+C** button: controls the sound on the server side, using the native Tamagotchi functionnality.

## ☁️ Deploy the app

This section is being re-written in a [dedicated feature](https://github.com/Almarch/pygotchi/tree/feature/keycloak?tab=readme-ov-file#2-deploy-the-app-online) in order to add a security layer.

## ☕ Background

<img src="https://static.wikia.nocookie.net/tamagotchi/images/a/a9/ZucchitchiScan.png/revision/latest?cb=20220513211400" alt="zucchitchi" width="80" align="right"/>

The Tamagotchi has been a social phenomenon back in the 1990's. The original game has been revived through [TamaLIB](https://github.com/jcrona/tamalib), an agnostic, cross platform emulator. TamaLIB has then been implemented on [Arduino](https://github.com/GaryZ88/Arduinogotchi) with a refactoring. From the Arduino version, I ported tamaLIB on 2 high-abstraction level, object-oriented languages: R and Python.

The [R](https://github.com/almarch/tamaR) project was developed aiming the sole P1 ROM that was available at this time. The app encompassed a function to switch the sprites to the P2 ones, and an algorithm to automatically care for the pet. Nevertheless, the core functionnality of the R project had been to deploy TamaLIB as a web app, in a server-client logic.

More recently, new first-generation ROMs have been released and TamaLIB has been adapted to allow the emulation for all first-gen Tamagotchis. In this view, I recycled the R project into a Python framework. Python is more production oriented, with a [broad community](https://github.blog/news-insights/octoverse/octoverse-2024/) and far better performances than R. The goal of this new version is to deliver an improved version of TamaLIB as a web service.

On the technical side, all C++ code has been merged into a monolithic `tamalib.cpp` file as the dependency management was not trivial for binding to Python. The same code and dependencies compiled on both windows and linux in the tamaR project, but currently pygotchi only builds on linux (or the WSL).

Adaptation to the new first-generation ROM collection is [being developed](https://github.com/Almarch/pygotchi/tree/feature/new-roms).

## 🚧 Ongoing

As already mentionned, 2 features are being developed:
- The web deployment is being secured with a HTTPS and an indentity and access manager. Check out [here](https://github.com/Almarch/pygotchi/tree/feature/keycloak).
- The C++ core is being updated following recent evolutions of TamaLIB main repo. This evolution aims at integration the new ROMs. Check out [here](https://github.com/Almarch/pygotchi/tree/feature/new-roms).

## ⚖️ License

This work is licensed under GPL-2.0 license.

All graphical resources come from the extraordinarily rich Tamagotchi [fandom](https://tamagotchi.fandom.com/wiki/Tamagotchi_(1996_Pet)).
