from .care_p1p2 import carestep as carestep_p1p2, state0 as state0_p1p2
import asyncio
from threading import Lock
import copy

class Carebot:
    def __init__(self, tama):
        self.tama = tama
        self.active = False
        self.param = {
            "disc": True,
            "check_every": 5*60
        }
        self._lock = Lock()

    async def run(self):
        while True:
            if self.active:
                match self.tama.version:
                    case "p1" | "p2":
                        new_state = await carestep_p1p2(
                            self.tama,
                            self.state,
                            self.param
                        )
                        with self._lock:
                            self.state = new_state
                        await asyncio.sleep(0.1)
                    case _:
                        await asyncio.sleep(1)
            else:
                await asyncio.sleep(1)

    def start(self):
        match self.tama.version:
            case "p1" | "p2":
                with self._lock:
                    self.active = True
            case _:
                with self._lock:
                    self.active = False

    def stop(self):
        with self._lock:
            self.active = False

    def reset(self):
        with self._lock:
            match self.tama.version:
                case "p1" | "p2":
                    self.state = copy.deepcopy(state0_p1p2)

    def parameterize(self, disc, check_every):
        with self._lock:
            self.param["disc"] = disc
            self.param["check_every"] = check_every
