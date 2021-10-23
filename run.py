from flask import Flask
from flask import render_template

app = Flask(__name__)

@app.route("/")
def index():
  return render_template('index.html')

@app.route("/sports")
def sports():
  return render_template('sports.html')

@app.route("/arts")
def arts():
  return render_template('arts.html')

@app.route("/concerts")
def concerts():
  return render_template('concerts.html')

@app.route("/event")
def event():
  return render_template('event.html')

@app.route("/tickets")
def tickets():
  return render_template('tickets.html')

if __name__ == "__main__":
  app.run()