import multiprocessing as mp
import asyncio
import hashlib
import numpy as np
from threading import Lock
import time

def _worker(conn):
    from ._tamalib import Tama as Tamalib
    from .conversion import int2bin, bin2int

    tamalib = Tamalib()

    _0ROM = [0 for _ in range(9216)]
    _0CPU = [0 for _ in range(384)]
    _0CPU[ 1] = 1
    _0CPU[ 8] = 1
    _0CPU[32] = 96
    _0CPU[33] = 219
    _0CPU[34] = 127
    _0CPU[35] = 42
    _0CPU[36] = 203
    _0CPU[37] = 113
    _0CPU[43] = 12
    _0CPU[47] = 10
    _0CPU[51] = 8
    _0CPU[55] = 6
    _0CPU[59] = 4
    _0CPU[63] = 2

    def click(button, value: bool = True):
        for b in button:
            tamalib.SetButton({"A": 0, "B": 1, "C": 2}[b], value)

    def runs():
        return tamalib.Runs()

    def start():
        if not runs():
            tamalib.Start()

    def stop():
        tamalib.Stop()
        time.sleep(0.1)

    def matrix():
        return tamalib.GetMatrix()

    def freq():
        return tamalib.GetFreq()

    def icons():
        return tamalib.GetIcons()

    def reset(what):
        stop()
        if what == "CPU":
            tamalib.SetCPU(_0CPU)
        elif what == "ROM":
            tamalib.SetROM(_0ROM)
            tamalib.SetCPU(_0CPU)

    def dump(what):
        running = tamalib.Runs()
        stop()
        if what == "CPU":
            obj = tamalib.GetCPU()
        elif what == "ROM":
            obj = tamalib.GetROM()
        else:
            raise ValueError("dump: 'what' must be 'CPU' or 'ROM'")
        if running:
            tamalib.Start()
        return int2bin(obj)

    def load(what, binbuf):
        obj = bin2int(binbuf)
        stop()
        if what == "CPU":
            tamalib.SetCPU(obj)
        elif what == "ROM":
            tamalib.SetROM(obj)
        else:
            raise ValueError("load: what must be 'CPU' or 'ROM'")
        if what == "ROM":
            reset("CPU")

    while True:
        try:
            msg = conn.recv()
        except EOFError:
            break

        cmd = msg.get("cmd")
        if cmd == "stop":
            break

        if cmd != "call":
            conn.send({"ok": False, "error": f"unknown cmd {cmd}"})
            continue

        method = msg.get("method")
        args = msg.get("args", [])
        kwargs = msg.get("kwargs", {})

        try:
            if method == "runs":
                result = runs()
            elif method == "start":
                start(); result = True
            elif method == "stop":
                stop(); result = True
            elif method == "matrix":
                result = matrix()
            elif method == "freq":
                result = freq()
            elif method == "icons":
                result = icons()
            elif method == "click":
                click(*args, **kwargs); result = True
            elif method == "reset":
                reset(*args, **kwargs); result = True
            elif method == "dump":
                result = dump(*args, **kwargs)
            elif method == "load":
                load(*args, **kwargs); result = True
            else:
                raise AttributeError(f"Unknown method {method}")

            conn.send({"ok": True, "result": result})
        except Exception as e:
            conn.send({"ok": False, "error": repr(e)})


class Tama:
    
    @classmethod
    async def new(cls, ROM: str, CPU: str = None):
        self = cls()
        with open(ROM, "rb") as file:
            await self.load("ROM", file.read())
        if CPU is not None:
            with open(CPU, "rb") as file:
                await self.load("CPU", file.read())
        await self.start()
        return self
    
    def __init__(self):
        self.version = None
        ctx = mp.get_context("spawn")
        parent_conn, child_conn = ctx.Pipe()
        self._conn = parent_conn
        self._proc = ctx.Process(target=_worker, args=(child_conn,), daemon=True)
        self._proc.start()
        self._lock = Lock()

    def close(self):
        if self._proc.is_alive():
            self._conn.send({"cmd": "stop"})
            self._proc.join(timeout=1)

    def __del__(self):
        try:
            self.close()
        except Exception:
            pass
    
    async def _call(self, method, *args, **kwargs):
        loop = asyncio.get_running_loop()

        def sync_call():
            with self._lock:
                self._conn.send({"cmd": "call", "method": method, "args": args, "kwargs": kwargs})
                return self._conn.recv()

        res = await loop.run_in_executor(None, sync_call)

        if not res["ok"]:
            raise RuntimeError(res["error"])
        return res["result"]

    async def runs(self) -> bool:
        return await self._call("runs")

    async def start(self):
        return await self._call("start")

    async def stop(self):
        return await self._call("stop")

    async def matrix(self):
        return await self._call("matrix")

    async def Matrix(self) -> np.ndarray:
        mat = await self.matrix()
        return np.array(mat).reshape((16, 32))
    
    async def print(self):
        mat = await self.Matrix()
        for row in mat:
            print("".join("██" if val else "  " for val in row))
        return True

    async def freq(self):
        return await self._call("freq")

    async def icons(self):
        return await self._call("icons")

    async def click(self, button, delay: float = 0.1):
        await self._call("click", button, True)
        await asyncio.sleep(delay)
        return await self._call("click", button, False)

    async def poke(self):
        pass # not implemented yet

    async def reset(self, what: str):
        return await self._call("reset", what)

    async def dump(self, what: str) -> bytes:
        return await self._call("dump", what)

    async def load(self, what: str, binbuf: bytes):
        
        if what == "ROM":    
            digest = hashlib.sha256(binbuf).hexdigest()
            print("ROM digest: " + digest)

            match digest:
                case '67b6388f26e2e3f15674932baf2fc2fb1c6f388cc0f16ea1aa0f441db1a4f43c':
                    ''' Original P1 '''
                    self.version = "p1"
                case 'eaa515606427eae26d0bf5c14ac437c12b96935238280d944b0b4b1d98ce701b':
                    ''' P1 with alternative secret character '''
                    self.version = "p1"
                case '6c7af647b3f10e4da83c46a75ea6a62da29d26315677fbfd270d15c278a24b39':
                    ''' Pseudo-P2: P1 with P2 sprites '''
                    self.version = "p2"
                case _:
                    self.version = None

        return await self._call("load", what, binbuf)

