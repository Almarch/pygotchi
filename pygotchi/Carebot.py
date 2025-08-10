from .care_p1p2 import carestep as carestep_p1p2, state0 as state0_p1p2
import asyncio

class Carebot:
    def __init__(self, tama):
        self.tama = tama
        self.active = False
        self.param = {
            "disc": True,
            "check_every": 5*60
        }

    async def run(self):
        while True:
            if self.active:
                match self.tama.__version__:
                    case "p1" | "p2":
                        self.state = carestep_p1p2(self.tama, self.state, self.param)
                        await asyncio.sleep(.1)
                    case _:
                        await asyncio.sleep(1)
            else:
                await asyncio.sleep(1)

    def start(self):
        match self.tama.__version__:
            case "p1" | "p2":
                self.active = True
                self.state = state0_p1p2
            case _:
                self.active = False

    def stop(self):
        self.active = False

    def parameterize(self, disc, check_every):
        self.param["disc"] = disc
        self.param["check_every"] = check_every