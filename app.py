from flask import *
from flask import request
from fileinput import filename
import os
import shutil
import socket

def get_ip():
	s = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
	try:
		s.connect(("192.168.1.1",1))
		ip = s.getsockname()[0]
	except:
		ip = "127.0.0.1"
	finally:
		s.close()
	return ip

app = Flask(__name__)

@app.route('/')	
@app.route('/index.html')
def index():
	rootdir = './static/manuals'
	
	folders_and_subfolders = []
	folders = os.listdir(rootdir)

	for folder in folders:
		current_path = []
		current_path.append(folder)
		current_path.append(os.listdir(os.path.join(rootdir, folder)))
		folders_and_subfolders.append(current_path)

	return render_template('index.html', folders_and_subfolders=folders_and_subfolders)
	
@app.route('/upload.html')
def get_upload_page():
	return render_template('upload.html',folders=os.listdir('./static/manuals'))
	
@app.route('/settings.html')
def get_settings_page():
	return render_template('settings.html')	
	
@app.route('/database.html')
def get_database_page():
	return render_template('database.html')

@app.route('/about.html')
def get_about_page():
	return render_template('about.html')	
			
@app.route('/book.html')
def get_book_page():
	return render_template('book.html')				
	
@app.route('/manual_view')
def get_manual_view():
	manual = request.args.get('manual')
	
	if "collapsible_" in manual:
		path = f"static/manuals/{manual.replace('collapsible_', '')}"	
	elif "content_|" in manual:
		path = f"static/manuals/{manual.replace('content_|', '').replace('|','/')}"
	#find the paths to the pdf, thumbnail, and name
	path_file = open(f"{path}/paths.txt")
	paths = path_file.readlines()
	for path in paths:
		if "pdf=" in path:
			pdf = path.replace("pdf=","")
		if "thumbnail=" in path:
			thumbnail = path.replace("thumbnail=","")
		if "name=" in path:
			name = path.replace("name=","")
	path_file.close()
	
	return render_template('manual_view.html', thumbnail_image=thumbnail, manual_name=name,manual_path=pdf)

@app.route('/filenames')
def get_filenames():
	rootdir = './static/manuals'

	folders_and_subfolders = []
	folders = os.listdir(rootdir)
	for folder in folders:
	
		current_path = []
	
		current_path.append(folder)
		current_path.append(os.listdir(os.path.join(rootdir,folder)))
	
		folders_and_subfolders.append(current_path)
	string = ""
	for item in folders_and_subfolders:
		item_title = item[0]
		string += "%?%"+item_title+"%?%"
		for items in item[1]:
			string += items+"@!@"
	print(string)
	return string
	#old code below
	file_names = os.listdir('./static/manuals')
	
	file_names_string = ""
	for file_name in file_names:
		file_names_string += file_name + "%?%"
		#%?% is a separator for between file names
		#i dont use a comma because some filenames contain a comma
	#return file_names_string[:-3]			
		
				
@app.route('/add_folder')	
def add_folder():
	source = request.args.get("foldername")
	folders = os.listdir("./static/manuals")
	for folder in folders:
		if source == folder:
			return "folder exists"
	os.mkdir(f"./static/manuals/{source}")
	#create a new folder
	#what about the folder name
	return f"{source}"		
	
@app.route('/delete_item')
def delete_item():
	junk_items = request.args.get("junk_items")
	if junk_items == "":
		return "zero junk items"
	junk_items = junk_items.replace("%20"," ").replace("[","").replace("]","")
	junk_list = junk_items.split(",")
	
	#parsing junk items names into paths
	junk_things_paths = []
	
	
	for junk_thing in junk_list:
		if "collapsible_" in junk_thing:
			path1 = f"static/manuals/{junk_thing.replace('collapsible_', '')}"
			junk_things_paths.append(path1)
			
		elif "content_|" in junk_thing:
			path2 = f"static/manuals/{junk_thing.replace('content_|', '').replace('|','/')}"
			junk_things_paths.append(path2)
			
	for item in junk_things_paths:	
		shutil.move(item, "static/trash")
		print(item)
	
	return "deleting items"	
	
@app.route('/upload', methods=['GET','POST'])			
def save_uploads():
	folder = None
	if request.method == 'POST':
		short_name = request.form['short_name_input']
		thumbnail = request.files['photo_upload']
		pdf_upload = request.files['pdf_upload']
		folder = request.form.get('folder_selection')
		
		
		new_folder_name = pdf_upload.filename.replace('.pdf','')
		
		new_folder = os.mkdir(f"./static/manuals/{folder}/{new_folder_name}")
		pdf_path = f"./static/manuals/{folder}/{new_folder_name}/{pdf_upload.filename}"
		pdf_upload.save(pdf_path)
		
		thumbnail_path = f"./static/manuals/{folder}/{new_folder_name}/{thumbnail.filename}"
		thumbnail.save(thumbnail_path)
		
		short_name_file = open(f"./static/manuals/{folder}/{new_folder_name}/{short_name}",'w')
		short_name_file.close()
		
		paths_file = open(f"./static/manuals/{folder}/{new_folder_name}/paths.txt",'w')
		paths_file.write(f"pdf={pdf_path}\nthumbnail={thumbnail_path}\nname={short_name}")
		paths_file.close()
		return render_template("upload_complete.html")
		
if __name__ == '__main__':
	
	app.run(debug=True, host=get_ip())