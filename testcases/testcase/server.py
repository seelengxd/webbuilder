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
		if "image" in request.files and request.files["image"].filename != "":
			image_file = request.files["image"]
			image_file_name = image_file.filename
			image_file.save("static/images/" + image_file_name)
			imageNames.append(image_file_name)
		else:
			raise ValueError("You are missing an image.")
		image_file_name = ""
		if "image2" in request.files and request.files["image2"].filename != "":
			image_file = request.files["image2"]
			image_file_name = image_file.filename
			image_file.save("static/images/" + image_file_name)
			imageNames.append(image_file_name)
		else:
			raise ValueError("You are missing an image.")
		if len(data["name"]) > 20:
			raise ValueError("name should be only maximum 20 chars long.")
		
		if len(data["test"]) > 50:
			raise ValueError("test should be only maximum 50 chars long.")
		
		con = open_DB("test.db")
		con.execute("""CREATE TABLE IF NOT EXISTS Test(
			img_name TEXT,
			img_test2 TEXT,
			name TEXT,
			test TEXT,
			testbox_res TEXT
		);""")
		if any([i == "" for i in [data['name'],data['test'],data['testbox']]]):
			raise ValueError("You left something empty. Fill in all inputs.")
		con.execute("INSERT INTO Test(name,test,testbox_res,img_name,img_test2) " + \
			"VALUES(?,?,?,?,?)", (data['name'],data['test'],data['testbox'], *imageNames))
		con.commit()
	except Exception as err:
		return render_template("form.html",success=False,err=err)
	con.close()
	return render_template("form.html", success=True,err=None)

app.run()