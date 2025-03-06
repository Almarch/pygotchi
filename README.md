# <img src="pygotchi/www/img/favicon.png" alt="PyGoTcHi" width="40"/> The Tamagotchi is live online ! 

The goal of this [Python](https://www.python.org/) package is to deliver [TamaLIB](https://github.com/jcrona/tamalib) as a web service.

The web server-client logic makes a special sense for Tamagotchis as it unlocks two key functionnalities of the original game:

- **Ubiquity**: Just like the original toy could be carried everywhere in a kid's pocket, a web service can be accessed from anywhere using a smartphone.
- **Real-time consistency**: The creature has a strict schedule that the player has to deal with all along the day. The server can endorse the role to keep track of time.

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

### 🛠️ Swagger

[FastAPI](https://fastapi.tiangolo.com/) apps come with a swagger. Once the app is launched, have a look at: http://localhost:8000/docs. Not all API are implemented on the UI.

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

### 🎵 Control the sound

The buzzer may be controlled at 2 levels:

- Using the 🔊 icon: controls the sound on the client side.
- Using the **A+C** button: controls the sound on the server side, using the native Tamagotchi functionnality.

## ☁️ Deploy a Tamagotchi server

If you have a PC that may stay on and a personal fixed IP, then you can turn it into a Tamagotchi server.

You need to know the public IP of your network and the private IP of your server. The public IP can be accessed from one of the many dedicated website, for instance [this one](https://www.mon-ip.com/). The private IP can be accessed with the command:

```bash
hostname -I
```

The router configuration depends on the internet supplier. The router configuration page may for instance be reached from within the network at `http://<your public ip>:80`.

The router should be parameterized as such:
- port 443 should be open to TCP ;
- port 443 should redirect to your linux server, identified with its private IP.

If you don't have a PC that can be used as a server, or you don't have a fixed, personal IP ; then you may opt for a VPS. A "bare-metal" VPS does the job and is relatively cheap. The public IP is provided by the cloud provider. Very little configuration is required.

### 🧱 Firewall

A firewall is needed to ensure you open the relevant port and this port only. For instance using [ufw](https://fr.wikipedia.org/wiki/Uncomplicated_Firewall):

```sh
sudo apt install ufw
sudo ufw enable
sudo systemctl enable ufw
sudo ufw allow 443/tcp
sudo ufw status
sudo systemctl restart ufw
```

### 🔑 Keys & secrets

The connection has to be encrypted using a SSL key.

From `/pygotchi`:

```sh
openssl req -x509 -nodes -days 365 -newkey rsa:2048 -keyout nginx/ssl/ssl.key -out nginx/ssl/ssl.crt -subj "/CN=localhost"
```

This key will have to be renewed after one year.

Then set up the secrets. Still from `/pygotchi`:

```sh
echo "KEYCLOAK_ADMIN_PASSWORD=$(cat /dev/urandom | tr -dc 'A-Za-z0-9' | fold -w 32 | head -n 1)" > .env
echo "KEYCLOAK_DB_PASSWORD=$(cat /dev/urandom | tr -dc 'A-Za-z0-9' | fold -w 32 | head -n 1)" >> .env
cat .env
```

### 🐙 Launch with docker-compose

Launch the web app with its dependency services using docker-compose.

From `/pygotchi`:

```sh
docker compose build
docker compose pull
docker compose up
```

The app is now available world-wide at `https://<your public ip>`.

Note that we self-signed our certificate, so the browser will present a warning.

### 🧙‍♂️ Keycloak

Once the web app will be launched, use `KEYCLOAK_ADMIN_PASSWORD` to access keycloak administration board at `https://<your public ip>/keycloak`. From there:

- Create a new realm: **game**.
- into the realm **game**, create a new client : **game_client**. For this client:
    - Enable client authentication.
    - Enable the standard authentication flow and the direct access grants (this are default). Keep all other authentication flows disabled.
    - Configure the valid redirect URI & Web origin: `https://<your public ip>/*` .
    - Collect the **game_client** secret.
- Still into the realm **game**, create one or more new users with custom credentials.
- Update `nginx/nginx.conf`, in the  `location / { access_by_lua_block { local opts = {...}}}` compartment:
    - replace `your_client_secret` by your actual game **game_client** secret.
    - replace `127.0.0.1` by `<your public ip>`.
    - re-launch the docker-compose cluster.

### 🗺️ Next step: use a domain name

You may move a step further, purchase a domain name and use a trusted connection. In this case, it will be necessary to include [certbot](https://hub.docker.com/r/certbot/certbot) to the docker-compose cluster, and to parameterize `nginx.conf` accordingly.

Be extra careful as the certbot can (and will) directly access the linux `iptables` \(docker daemon has admin privileges\), opening ports and by-passing `ufw`.
>>>>>>> 3468e279b5a2296c987b6db567f1dce6a3079970

## ☕ Background

<img src="https://static.wikia.nocookie.net/tamagotchi/images/a/a9/ZucchitchiScan.png/revision/latest?cb=20220513211400" alt="zucchitchi" width="80" align="right"/>

The Tamagotchi has been a social phenomenon back in the 1990's. The original game has been revived through [TamaLIB](https://github.com/jcrona/tamalib), an agnostic, cross platform emulator. TamaLIB has then been implemented on [Arduino](https://github.com/GaryZ88/Arduinogotchi) with a refactoring. From the Arduino version, I ported tamaLIB on 2 high-abstraction level, object-oriented languages: R and Python.

The [R](https://github.com/almarch/tamaR) project was developed aiming the sole P1 ROM that was available at this time. The app encompassed a function to switch the sprites to the P2 ones, and an algorithm to automatically care for the pet. Nevertheless, the core functionnality of the R project had been to deploy TamaLIB as a web app, in a server-client logic.

More recently, new first-generation ROMs have been released and TamaLIB has been adapted to allow the emulation for all first-gen Tamagotchis. In this view, I recycled the R project into a Python framework. Python is more production oriented, with a [broad community](https://github.blog/news-insights/octoverse/octoverse-2024/) and far better performances than R. The goal of this new version is to deliver an improved version of TamaLIB as a web service.

On the technical side, all C++ code has been merged into a monolithic `tamalib.cpp` file as the dependency management was not trivial for binding to Python. The same code and dependencies compiled on both windows and linux in the tamaR project, but currently pygotchi only builds on linux (or the WSL).


- The C++ core is being adapted following the evolution of TamaLIB aiming at emulating all first-gen ROMs:
    - In [this feature](https://github.com/Almarch/pygotchi/tree/feature/new-roms) I tried to reflect the changes into the monolithic C++ but it is sketchy.
    - In [this feature](https://github.com/Almarch/pygotchi/tree/feature/src-tamalib) I am trying to use the official tamaLIB repository with a minimal C++ binding to Python. I think at the end of the day this is the best approach.

## ⚖️ License

This work is licensed under GPL-2.0.

All graphical resources come from the extraordinarily rich Tamagotchi [fandom](https://tamagotchi.fandom.com/wiki/Tamagotchi_(1996_Pet)).
