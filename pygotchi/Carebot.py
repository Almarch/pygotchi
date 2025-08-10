from .carestep_p1 import carestep as carestep_p1
from .carestep_p2 import carestep as carestep_p2
import asyncio

class Carebot:
    def __init__(self, tama):
        self.tama = tama
        self.active = False

    async def run(self):
        while True:
            if self.active:
                match self.tama.__version__:
                    case "p1":
                        await carestep_p1(self.tama)
                    case "p2":
                        await carestep_p2(self.tama)
                    case _:
                        await asyncio.sleep(1)
            else:
                await asyncio.sleep(1)

    def start(self):
        self.active = True

    def stop(self):
        self.active = False