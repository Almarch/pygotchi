from threading import Lock
from .translate import translate as do_translation

class Translator:

    def __init__(self, tama):
        self.tama = tama
        self.active = True
        self._lock = Lock()

    @property
    def available(self) -> bool:
        return self.tama.language == "ja" and self.tama.version in ["p1", "p2", "angel"]

    def start(self) -> None:
        with self._lock:
            self.active = True

    def stop(self) -> None:
        with self._lock:
            self.active = False

    async def translate(self) -> bytes:
        """Return the translated frame if enabled, the raw frame otherwise."""

        matrix = await self.tama.matrix_bytes()
        if not (self.active and self.available):
            return matrix
        return await do_translation(matrix)
