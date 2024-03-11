from .types import DIFFICULTY
import random

def readFileLines(fname: str) -> list[str]:
    with open(fname, "r") as f:
        data = f.read()
    return getLines(data)

def getLines(data: str) -> list[str]:
    return [i.upper() for i in data.split("\n") if len(i) > 0]

def transform(word: str, difficulty: DIFFICULTY) -> tuple[str, int]:
    if difficulty == "easy":
        return word, random.randint(0, 1)
    elif difficulty == "medium":
        return word, random.randint(0, 3)
    elif difficulty == "hard":
        if random.getrandbits(1) == 1:
            word = word[::-1]
        return word, random.randint(0, 3)
    return word, 0

def loadAllWordSample(n: int, max_len = 7) -> list[str]:
    # load global word list
    all_words = readFileLines("/Users/ellis/Git/wordSearch/all-words.txt")
    all_words = [i for i in all_words if len(i) <= max_len]
    return random.sample(all_words, n)

