from backend.main import Grid
from backend.utils import loadAllWordSample, readFileLines, transform
import random


TOTAL_WORDS_IN_SEARCH = 20
ALL_WORDS_MAX_LEN = 7
RETRY_WORD_PLACEMENT_CNT = 1
DIFFICULTY = 0.1

def main():
    # load user word list
    words = readFileLines("./words.txt")
    words_cnt = len(words)
    words_max = max(len(i) for i in words)

    sample = loadAllWordSample(TOTAL_WORDS_IN_SEARCH - words_cnt)

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
