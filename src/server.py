from flask import Flask, render_template, request
from backend.utils import getLines, loadAllWordSample, transform
from backend.main import Grid

app = Flask(__name__)

@app.route("/")
def root():
    return render_template("index.html")

@app.route("/wordsearch", methods=["POST"])
def get_search():
    wordsBox = request.form['words']
    difficulty = request.form['difficulty']
    words = getLines(wordsBox)
    wordMax  = max(len(i) for i in words)
    wordSample = loadAllWordSample(15)
    grid = Grid(wordMax + 1)
    for word in words + wordSample:
        grid.put(*transform(word, difficulty))

    grid.randomize_empty_cells() 
    print(grid.size)
    print(grid)

    return render_template("search.html", size=grid.size, grid=grid.to_list(), words=words)
