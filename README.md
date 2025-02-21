# <img src="pygotchi/www/img/icon.png" alt="PyGoTcHi" width="40"/> The Tamagotchi is live on Python ! 

The goal of this package is to port [TamaLIB](https://github.com/jcrona/tamalib) to Python. Bringing the low-level emulator to a high-level language aims at easing its deployment as a web service.

The web server-client logic makes a special sense for Tamagotchis as it unlocks two key functionnalities of the original game:

- Ubiquity: Just like the original toy could be carried everywhere in a kid's pocket, a web service can be accessed from anywhere using a smartphone.
- Real-time consistency: The creature has a strict schedule that the player has to deal with all along the day. The server can endorse the role to keep track of time.

A web app is readily available with the package. It is dockerized for ease of deployment.

## 1. Run the app

Start by cloning the repo:

```sh
git clone https://github.com/almarch/pygotchi.git
```

### 1.1. Run with Docker

```sh
cd pygotchi
docker build -t tama .
docker run -d -p 8000:80 tama
```

The app is now available at http://localhost:8000.

### 1.2. Run with Python

Build the package with `build` and install it with `pip`:

```sh
pip install build
python -m build ./pygotchi
pip install ./pygotchi
```

It may then be launched directly:

```sh
python -m pygotchi
```

The app is now available at http://localhost:8000.

### 1.3. Swagger

FastAPI apps come with a swagger. Once the app is launched, have a look at: http://localhost:8000/docs

## 2. Deploy the app

Now that the app is available at port 8000, it may be deployed online. The server will be assumed to be a linux computer behind a router with a fixed public IP. It may just as well be a VPS.

First of all, you need the public IP of your network and the private IP of your server. The public IP can be accessed from one of the many benevolent website, for instance [this one](https://myip.com). The private IP can be accessed with the command:

```bash
hostname -I
```

### 2.1. Router

The router configuration depends on the internet supplier. The router configuration page may for instance be reached from within the network at http://`<public ip>`:80. Because port 80 might be in competition with other resources, for instance the internet supplier configuration page, we will set up the application to listen to port 8000, which is less commonly used.

The router should be parameterized as such:

- port 8000 should be open to TCP ;

- port 8000 should redirect to your linux server, identified with its private IP.

### 2.2. Firewall

Using a firewall is a first security step for a web server. For instance, [ufw](https://fr.wikipedia.org/wiki/Uncomplicated_Firewall) is free, open-source and easy to use.

```bash
sudo apt install ufw
sudo ufw enable
sudo systemctl enable ufw
```

Port 8000 should be open to TCP. After configuring the router it may be checked and it has to be restarted.

```bash
sudo ufw allow 8000/tcp
sudo ufw status
sudo systemctl restart ufw
```
### 2.3. Web server

A web server software is required to deploy the shiny app with its functionalities. For instance, [nginx](https://nginx.com) is a free, open-source popular solution.

```bash
sudo apt install nginx
sudo systemctl enable nginx
```

A configuration file should be provided for the app. Place the following configuration in an app file in the /etc/nginx/sites-available/ folder:

```
server {
        listen 8000;
        server_name _;

        location / {
                proxy_pass http://localhost:8000;
                proxy_redirect http://localhost:8000/ $scheme://$http_host/;
                proxy_http_version 1.1;
                proxy_set_header Upgrade $http_upgrade;
                proxy_read_timeout 20d;
                proxy_buffering off;
        }
}
```

Create a symlink in the /etc/nginx/sites-enabled/ folder, and restard nginx:

```bash
sudo ln -s /etc/nginx/sites-available/app /etc/nginx/sites-enabled/app
sudo systemctl restart nginx
```

### 2.4. Connection

The app is now available world-wide at http://`<public ip>`:8000

It can be played from a smartphone. A shortcut to the webpage may be added to the home screen. 

The Tamagotchi runs backend, so it remains alive when the user disconnects.

## 3. Use from Python

The package binds a `Tama` Python class to TamaLIB. It is thus possible to interact directly with it once the package has been installed.

### 3.1. Launch the emulation

A Tamagotchi object must be instanciated:

```py
from pygotchi import Tama
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

### 3.2. Commands

The screen can be rendered using `display` and the sound frequency is available with `GetFreq`.

Action the 3 buttons `A`, `B` and `C` with the `click` method.

```py
import time
tama.click("B", 0.5)
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

## 4. Background

The Tamagotchi has been a social phenomenon back in the 1990's. The original game has been revived through [TamaLIB](https://github.com/jcrona/tamalib), an agnostic, cross platform emulator. TamaLIB has then been implemented on [Arduino](https://github.com/GaryZ88/Arduinogotchi) with a refactoring. The Arduino version is the starting point for a C++ module aiming portage on higher-level object-oriented languages.

I ported TamaLIB on the [R](https://github.com/almarch/tamaR) software environment, with an R-Shiny web app. The R project was developed aiming the sole P1 ROM that was available at this time. The app encompassed a function to switch the sprites to the P2 ones, and an algorithm to automatically care for the pet. Nevertheless, the core functionnality of the R project had been to deploy TamaLIB on the web, in a server-client logic.

More recently, new first-generation ROMs have leaked and TamaLIB has been adapted to allow the emulation for all first-gen Tamagotchis. In this view, I recycled the R project into a Python framework. Python is more production oriented, with a [broad community](https://github.blog/news-insights/octoverse/octoverse-2024/) and far better performances than R. The goal of this new version is to deliver an improved version of TamaLIB as a web service.

On the technical side, all C++ code has been merged into a monolithic `tamalib.cpp` file as the dependency management was not trivial for binding to Python. The same code and dependencies compiled on both windows and linux in the tamaR project, but currently pygotchi only builds on linux (or the WSL). A solution to build the package on windows has to be developped.

🚧 Adaptation to the whole new first-generation ROM collection is still on the backlog.

## 5. License

This work is licensed under Attribution-NonCommercial 4.0 International.
