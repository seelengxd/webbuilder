@app.route("{formaction}", methods=["POST"])
def submit():
	data = request.form
	imageNames = []	
	try:
		#os thing is needed for it to work when run in vs code
		{imageCode}
		{limitCode}
		con = open_DB("{dbName}")
		con.execute("""CREATE TABLE IF NOT EXISTS {tableName}(
			{createDbStuff}
		);""")
		if any([i == "" for i in [{toAddStuff}]]):
			raise ValueError("You left something empty. Fill in all inputs.")
		con.execute("INSERT INTO {tableName}({columnNames}) " + \
			"VALUES({questionMarks})", ({toAddStuff}, *imageNames))
		con.commit()
	except Exception as err:
		return render_template("{to}",success=False,err=err)
	con.close()
	return render_template("{to}", success=True,err=None)