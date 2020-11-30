from flask import Flask, render_template, redirect, request
import sqlite3
import os
app = Flask(__name__)

def open_DB(db):
	return sqlite3.connect(db)

@app.route("/")
def formTemplate():
	return render_template("form.html", err=None, success=False)

@app.route("/submit", methods=["POST"])
def submit():
	data = request.form
	imageNames = []	
	try:
		image_file_name = ""
		if "image name" in request.files and request.files["image name"].filename != "":
			image_file = request.files["image name"]
			image_file_name = image_file.filename
			image_file.save("static/images/" + image_file_name)
			imageNames.append(image_file_name)
		else:
			raise ValueError("You are missing an image.")
		image_file_name = ""
		if "another image" in request.files and request.files["another image"].filename != "":
			image_file = request.files["another image"]
			image_file_name = image_file.filename
			image_file.save("static/images/" + image_file_name)
			imageNames.append(image_file_name)
		else:
			raise ValueError("You are missing an image.")
		
		con = open_DB("test2.db")
		con.execute("""CREATE TABLE IF NOT EXISTS test2(
			image TEXT,
			image2 TEXT,
			name TEXT,
			desc TEXT,
			letters TEXT
		);""")
		if any([i == "" for i in [data['name'],data['desc'],data['whatever']]]):
			raise ValueError("You left something empty. Fill in all inputs.")
		con.execute("INSERT INTO test2(name,desc,letters,image,image2) " + \
			"VALUES(?,?,?,?,?)", (data['name'],data['desc'],data['whatever'], *imageNames))
		con.commit()
	except Exception as err:
		return render_template("form.html",success=False,err=err)
	con.close()
	return render_template("form.html", success=True,err=None)

app.run()