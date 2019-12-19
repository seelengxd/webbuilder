image_file_name = ""
if "{imageNameAttri}" in request.files and request.files["{imageNameAttri}"].filename != "":
	image_file = request.files["{imageNameAttri}"]
	image_file_name = image_file.filename
	image_file.save("static/images/" + image_file_name)
	imageNames.append(image_file_name)
else:
	raise ValueError("You are missing an image.")