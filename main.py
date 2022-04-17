from flask import Flask, render_template, request, redirect, send_file
from functions import get_jobs
from exporter import save_to_file

app = Flask("SuperScraper")

db = {}

@app.route("/")
def home():
  templates = ["index.html"]
  return render_template(templates)
  
@app.route("/result")
def result():
  word = request.args.get("word")
  if word:
    word = word.lower()
    existingJobs = db.get(word)
    if existingJobs:
      jobs = existingJobs
    else:
      jobs = get_jobs(word)
      db[word] = jobs
  else:
    return redirect("/")
  
  return render_template("result.html", searchInput=word, resultsNumber=len(jobs), jobs=jobs)
  

@app.route("/export")
def export():
  try:
    word = request.args.get("word")
    if not word:
      raise Exception()
    word = word.lower()
    jobs = db.get(word)
    if not jobs:
      raise Exception()
    save_to_file(jobs)
    return send_file("jobs.csv")
  except:
    return redirect("/")


app.run(host="0.0.0.0")

