import numpy as np
import random

EMPTY_CELL_CHAR = b"."
TOTAL_WORDS_IN_SEARCH = 20
ALL_WORDS_MAX_LEN = 7
RETRY_WORD_PLACEMENT_CNT = 1
DIFFICULTY = 0.1

T_coord = tuple[int, int]

class Grid():
    storage: np.ndarray
    horizMask: np.ndarray
    vertMask: np.ndarray
    diagMask: np.ndarray
    size: int

    def __init__(self, size: int) -> None:
        self.storage = np.chararray((size, size))
        self.storage.fill(EMPTY_CELL_CHAR)
        self.size = size
        self.horizMask = np.zeros((size, size), dtype=np.int8)
        self.vertMask = np.zeros((size, size), dtype=np.int8)
        self.diagMask = np.zeros((size, size), dtype=np.int8)
    
    def __repr__(self) -> str:
        return "\n".join(" ".join(i.decode("utf-8") for i in j) for j in self.storage)

    def randomize_empty_cells(self):
            for i in range(self.size):
                for j in range(self.size):
                    if  self.storage[i, j] == EMPTY_CELL_CHAR:
                        self.storage[i, j] = chr(np.random.randint(65, 65+26)).encode()

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
        raise ValueError(f"Invalid axis {axis}")

    def put(self, word: str, axis: int) -> bool:
        primary_mask = self.get_mask(axis)
        word = word.upper().replace(" ", "")

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

def calc_coord(origin: T_coord, offset: int, axis: int) -> T_coord:
    if axis == 0:
        return (origin[0], origin[1] + offset)
    elif axis == 1:
        return (origin[0] + offset, origin[1])
    else:
        return (origin[0] + offset, origin[1] + offset)
    
def readFileLines(fname: str) -> list[str]:
    with open(fname, "r") as f:
        data = f.read()
    return [i.upper() for i in data.split("\n") if len(i) > 0]

def transform(word: str, difficulty: float) -> tuple[str, int]:
    if difficulty < 0.2:
        return word, random.randint(0, 1)
    elif difficulty < 0.6:
        return word, random.randint(0, 2)
    if random.getrandbits(1) == 1:
        word = word[::-1]
    return word, random.randint(0, 2)

def main():
    # load user word list
    words = readFileLines("./words.txt")
    words_cnt = len(words)
    words_max = max(len(i) for i in words)

    # load global word list
    all_words = readFileLines("./all-words.txt")
    all_words = [i for i in all_words if len(i) <= ALL_WORDS_MAX_LEN]
    sample = random.sample(all_words, TOTAL_WORDS_IN_SEARCH - words_cnt)

    # write user words into search
    grid_size = int(words_max + 3)
    search = Grid(grid_size)
    for word in words:
        worked = False
        for _ in range(RETRY_WORD_PLACEMENT_CNT):
            worked = search.put(*transform(word, DIFFICULTY))
            if worked:
                break
        if not worked:
            print(search)
            raise ValueError(f"Failed to put word {word }")

    # write global words into search
    for word in sample:
        search.put(word, 0)

    # ensure there are no empty cells
    search.randomize_empty_cells()
    print(search)
    print("Find: " + ", ".join(words))

if __name__ == "__main__":
    main()
