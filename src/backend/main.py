import numpy as np
import random
from .types import T_coord

EMPTY_CELL_CHAR = b"."

class Grid():
    storage: np.ndarray
    horizMask: np.ndarray
    vertMask: np.ndarray
    diagMask: np.ndarray
    diagInvMask: np.ndarray
    size: int

    def __init__(self, size: int) -> None:
        self.storage = np.zeros((size, size), dtype=bytes)
        self.storage.fill(EMPTY_CELL_CHAR)
        self.size = size
        self.horizMask = np.zeros((size, size), dtype=np.int8)
        self.vertMask = np.zeros((size, size), dtype=np.int8)
        self.diagMask = np.zeros((size, size), dtype=np.int8)
        self.diagInvMask = np.zeros((size, size), dtype=np.int8)
    
    def __repr__(self) -> str:
        return "\n".join(" ".join(i.decode("utf-8") for i in j) for j in self.storage)

    def to_list(self) -> list[list[str]]:
        return [j.decode("utf-8") for i in self.storage.tolist() for j in i]

    def randomize_empty_cells(self):
        self.storage = np.vectorize(is_empty)(self.storage)

    def valid_coords(self, coord: T_coord) -> bool:
        i, j = coord
        valid = i >= 0 and j >= 0 and i < self.size and j < self.size
        return valid


    def valid_underlying(self, coord: T_coord, char: bytes) -> bool:
        ii, jj = coord
        char_at_coord = self.storage[ii, jj]
        return char_at_coord in [EMPTY_CELL_CHAR, char]


    def get_mask(self, axis: int) -> np.ndarray:
        if axis == 0:
            return self.horizMask
        elif axis == 1:
            return self.vertMask
        elif axis == 2:
            return self.diagMask
        elif axis == 3:
            return self.diagInvMask
        raise ValueError(f"Invalid axis {axis}")

    def put(self, word: str, axis: int) -> bool:
        primary_mask = self.get_mask(axis)
        word = word.upper().replace(" ", "").replace("\n", "").replace("\r", "")

        valid_starts: list[T_coord] = []
        for i in range(self.size):
            for j in range(self.size):
                coords = list(iter_coords((i, j), len(word), axis))
                if not all(self.valid_coords(coord) for coord in coords):
                    continue
                elif any(hits_mask(coord, primary_mask) for coord in coords):
                    continue
                elif not all(self.valid_underlying(coord, word[idx].encode()) for idx, coord in enumerate(coords)):
                    continue
                valid_starts.append((i, j))

        if len(valid_starts) == 0:
            return False

        origin = random.choice(valid_starts)
        for idx, (i, j) in enumerate(iter_coords(origin, len(word), axis)):
            primary_mask[i, j] = 1
            self.storage[i, j] = word[idx]

        return True

def hits_mask(coords: T_coord, mask: np.ndarray) -> bool:
    i, j = coords
    return mask[i, j] != 0

def iter_coords(origin: T_coord, end: int, axis: int):
    for i in range(end):
        yield calc_coord(origin, i, axis)

def is_empty(ch: bytes) -> bytes:
    if ch != EMPTY_CELL_CHAR:
        return ch
    return chr(np.random.randint(65, 65+26)).encode()

def calc_coord(origin: T_coord, offset: int, axis: int) -> T_coord:
    if axis == 0:
        return (origin[0], origin[1] + offset)
    elif axis == 1:
        return (origin[0] + offset, origin[1])
    elif axis == 2:
        return (origin[0] + offset, origin[1] + offset)
    elif axis == 3:
        return (origin[0] + offset, origin[1] - offset)
    else:
        raise ValueError(f"Invalid axis {axis}")
    
