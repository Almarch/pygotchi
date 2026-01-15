# <img src="pygotchi/www/img/favicon.png" alt="PyGoTcHi" width="40"/> The Tamagotchi is live online ! 

The purpose of this Python package is to provide a Tamagotchi emulator as a web service. The client–server logic enables two core features from the original game:

- **Ubiquity**: Just like the original toy could be carried in a kid’s pocket, the web service can be accessed anytime, anywhere from a smartphone.

- **Real-time consistency**: The creature follows a strict schedule that the player must handle throughout the day. The server ensures time is properly tracked.

Unlike the original though, this project also includes [a bot](#-Automatic-care) able to care for the pet when the user is busy.

It delivers a ready-to-use, secure web [application](#%EF%B8%8F-deploy-a-tamagotchi-server) that hosts Tamagotchis for multiple authenticated users.

Its [Python core API](#-Python-core-API) can also be reused for further development projects.

<div align="center">
    <img src="https://github.com/user-attachments/assets/c7f53848-8d65-4571-b077-dde5c283520e" width="300px"/>
</div>

## 🚀 Run the app locally

Clone the repo:

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

Pygotchi can only be built and installed on linux (or the WSL). Build the package with `build` and install it with `pip`:

```sh
pip install build
python -m build ./pygotchi
pip install ./pygotchi
```

The app may then be launched using Python:

```sh
python -m pygotchi
```

The app is now available at http://localhost:8000.

## 🎮 How to use

The game is controlled with 3 buttons (A, B, C) with respect to the original toy. Click the screen to "poke" the toy.

A menu (☰) allows administration over the game.

<div align="center">
    <img src="https://github.com/user-attachments/assets/eb8ed074-ed9d-47f1-a861-f574fe64841e" width="300px" />
</div>

### 🧬 Load a ROM

From the administration menu, flash a ROM. It should be a 12ko `.bin` file. Use the switch button to get the emulation started. The ROM is loaded on the server, and the emulation runs server-side. The ROM version is automatically detected and the graphical theme (background, icons) is adapted accordindingly.

### 💾 Save the game

The game may be saved any time using the Save CPU button from the administration menu. The `save.bin` file may then be loaded again. Ensure consistency between the loaded CPU and the ROM.

### 💞 Automatic care

The Tamagotchi won an [Ig Nobel prize](https://improbable.com/ig/winners/#ig1997) for diverting millions of people from their professional duties. It is not a fatality: check this option and a friendly bot will care for your pet, freeing you up for more important (though probably less fun) stuff.

The automatic care works on the server side, so the bot keeps caring for the pet when the user session is closed. It is automatically adapted to the ROM version. Currently, only P1 and P2 are supported.

### 🎵 Control the sound

The sound is controlled using the native Tamagotchi functionnality, with the **A+C** button. This feature works on the server side.

### 🛠️ Swagger
Not all APIs are implemented on the UI, and a swagger allows for a few more functionalities.

## ☁️ Deploy a Tamagotchi server

If you have a PC that may stay on and a personal fixed IP, then you can turn it into a Tamagotchi server.

<img width="800" alt="image" src="https://github.com/user-attachments/assets/7f513e2c-ec32-4367-9fc5-6d1005afa889" />

### 🏠 IPs & router configuration

You need to know the public IP of your network and the private IP of your server.

- The public IP can be accessed from [here](https://api.ipify.org) ;
- The private IP can be accessed with the command:

```bash
hostname -I
```

The router configuration depends on the internet supplier. The router configuration page may for instance be reached from within the network at `http://<your public ip>:80`.

The router should be parameterized as such:
- ports 80 and 443 should be open to TCP ;
- ports 80 and 443 should redirect to your linux server, identified with its private IP.

If you don't have a PC that can be used as a server, or you don't have a fixed, personal IP ; then you may opt for a VPS. A "bare-metal" VPS does the job and is relatively cheap. The public IP is provided by the cloud provider. Very little configuration is required.

### 🧱 Firewall

A firewall is needed to ensure you open the relevant port and this port only. Uncomplicated firewall (ufw) is a fair option.

**Warning**: if you are connected to a VPS with SSH, open port 22 before enabling ufw or you would be locked out.

**Warning**: ufw applies to the whole system. If you already have a firewall, configure your existing firewall instead.

```sh
sudo apt install ufw
sudo ufw default deny incoming
sudo ufw default allow outgoing
sudo ufw allow 22/tcp   # If using a VPS
sudo ufw allow 80/tcp
sudo ufw allow 443/tcp
sudo ufw enable
sudo systemctl enable ufw
sudo ufw status
```

### 🔑 Keys & secrets

The connection has to be encrypted using a SSL key.

From `/pygotchi`:

```sh
openssl req -x509 -nodes -days 365 -newkey rsa:2048 -keyout nginx/ssl/ssl.key -out nginx/ssl/ssl.crt -subj "/CN=localhost"
```

This key will have to be renewed after one year. The certificates are self-signed so the browser will present a warning. See [this section](#-domain-name) to use CA-signed certificate.

Then set up the secrets. Still from `/pygotchi`:

```sh
echo "KEYCLOAK_ADMIN_PASSWORD=$(cat /dev/urandom | tr -dc 'A-Za-z0-9' | fold -w 32 | head -n 1)" > .env
echo "KEYCLOAK_DB_PASSWORD=$(cat /dev/urandom | tr -dc 'A-Za-z0-9' | fold -w 32 | head -n 1)" >> .env
cat .env
```

Keep the `KEYCLOAK_ADMIN_PASSWORD` at hand.

### 🐙 Run with docker-compose

Update the docker daemon to forbid direct iptables manipulation by docker and to enable IPv6.

**Warning**: this overwrites `/etc/docker/daemon.json`. If you already have custom parameters, edit the file instead of overwriting it.

```sh
echo '{
  "iptables": false,
  "ipv6": true
}' | sudo tee /etc/docker/daemon.json
sudo systemctl restart docker
```

Launch the web app with its dependency services using docker-compose.

From `/pygotchi`:

```sh
docker compose build
docker compose pull
docker compose up
```

### 🧙‍♂️ Keycloak

Access keycloak administration board at `https://<your public>/keycloak`.

The first launch is very long as all services have to be set-up. Once it is ready, authentify as :

- user: `admin`
- password: `KEYCLOAK_ADMIN_PASSWORD`

From there:

- Create a new realm: **game**.
- From the realm **game**, create a new client : **game_client**. For this client:
    - Enable client authentication.
    - Enable the standard authentication flow. Keep all other authentication flows disabled. This is the standard configuration.
    - Configure the valid redirect URI & Web origin: `https://<your public IPv4>/*` and/or `https://[<your public IPv6>]/*`.
    - Collect the **game_client** secret and keep it at hand.
- Still from the realm **game**, create one or more new users with custom credentials. Each user access their own Tamagotchi.

Then, update `nginx/nginx.conf`, in the  `location / { access_by_lua_block { local opts = {...}}}` compartment:
- Replace `your_client_secret` by your actual game **game_client** secret.
- Replace `127.0.0.1` by either `<your public IPv4>` or `[<your public IPv6>]`.

Finally, re-launch the docker-compose cluster :

```sh
docker compose down
docker compose up -d
```

The app is now secured & available world-wide at `https://<your public IP>`.

### 🏰 Domain name

For further security, purchase a domain name and use a trusted connection. To do so, include [certbot](https://hub.docker.com/r/certbot/certbot) to the docker-compose stack and parameterize keycloak and `nginx.conf` accordingly.

## 📐 Technical aspects

### ☕ Background

<img src="https://static.wikia.nocookie.net/tamagotchi/images/a/a9/ZucchitchiScan.png/revision/latest?cb=20220513211400" alt="zucchitchi" width="80" align="right"/>

The Tamagotchi has been a social phenomenon back in the 1990's. The original game has been revived through [TamaLIB](https://github.com/jcrona/tamalib), an agnostic, cross platform emulator. TamaLIB has then been implemented on [Arduino](https://github.com/GaryZ88/Arduinogotchi) with a refactoring. From the Arduino version, TamaLIB was ported on 2 high-abstraction level, object-oriented languages: [R](https://github.com/almarch/tamaR), then Python. Currently, all C++ code has been merged into a monolithic `tamalib.cpp` file as the dependency management was not trivial for binding to Python.

Python is more production oriented, with a [broad community](https://github.blog/news-insights/octoverse/octoverse-2024/) and better performances than R. The following features were permitted by switching the project from R to Python:
- implementing the buzzer sound using websockets ;
- switching the carebot server-side using the better distinction between back and front ;
- multiplayer management using the multiprocesses & async framework.

There is still work to do. Pygotchi has to be adapted to all new first generation Tamagotchis, following TamaLIB recent developments ([Issue #3](https://github.com/Almarch/pygotchi/issues/3)). From there, a specific carebot could be developed for each species.

The automatic care feature is inspired from [Tamatrix](https://github.com/hortinstein/tamatrix) (see also the [dockerized version](https://github.com/greysonp/tamatrix)).

### 🥚 Python core API

The Python core of the project may be distinguished from the auxiliary web application infrastructure. The Python core is nested like Russian dolls of increasing abstraction. Tamalib is the C++ deepest layer. The intermediate abstraction layer is [`Tama()`](https://github.com/Almarch/pygotchi/blob/main/pygotchi/Tama.py), a Python object bound to the C++ engine serving as an API for user-level commands. Finally, the last layers are the FastAPI web service and the carebot that both operate on `Tama()`.

The Python core API may directly be interacted with in an async framework.

In CLI:

```python
from pygotchi import Tama
import asyncio
tama = asyncio.run(Tama.new("rom.bin"))
asyncio.run(tama.print())
asyncio.run(tama.click("B"))
```

In a notebook:

```python
from pygotchi import Tama
import nest_asyncio
nest_asyncio.apply()
tama = await Tama.new("rom.bin")
await tama.print()
await tama.click("B")
```


## ⚖️ License

This work is licensed under GPL-2.0.

All graphical resources come from the extraordinarily rich Tamagotchi [fandom](https://tamagotchi.fandom.com/wiki/Tamagotchi_(1996_Pet)).
