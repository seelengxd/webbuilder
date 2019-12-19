from flask import Flask, render_template, redirect, request
import sqlite3
import os
app = Flask(__name__)

def open_DB(db):
	return sqlite3.connect(db)

@app.route("{form_url}")
def formTemplate():
	return render_template("{form_template}", err=None, success=False)

{otherCode}

app.run()