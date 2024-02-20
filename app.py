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
	
messages = []
	
@app.route('/update')
def update():
	def event_stream():
		previous_messages = 0
		while True:
			if len(messages) > previous_messages:
				previous_messages += 1
				yield f"event:refresh\ndata:{messages[-1]}\n\n"
	return Response(event_stream(), mimetype="text/event-stream")	
	
	
	
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
	messages.append("folder-added")
	#updating other clients
	return f"{source}"		
	
	
	
@app.route('/delete_item')
def delete_item():
	junk_items = request.args.get("junk_items")
	if junk_items == "":
		return "zero junk items"
	junk_items = junk_items.replace("%20"," ").replace("[","").replace("]","")
	
	junk_list = junk_items.split(",")
	#junk_list is a list of all the items that are going to be deleted. these are not paths, just folder names
	class Junk_item:
		trash_path = ""
		
		def __init__(self, path,name):
			self.path = path
			self.name = name
			
	junk_classes = []
	junk_things_paths = []
	#junk_things_paths is a list of strings which are paths to all the items that are going to be deleted
	
	#parsing junk items names into paths
	for junk_thing in junk_list:
		if "collapsible_" in junk_thing:
			name = junk_thing.replace('collapsible_', '')
			
			path1 = f"static/manuals/{name}"
			junk_obj = Junk_item(path1,name)
			junk_classes.append(junk_obj)
			junk_things_paths.append(path1)
			
		elif "content_|" in junk_thing:
			name = junk_thing.replace('content_|', '').replace('|','/')
			
			path2 = f"static/manuals/{name}"
			junk_obj = Junk_item(path2,name.split("/")[1])
			junk_classes.append(junk_obj)
			junk_things_paths.append(path2)
			
	
	#items_in_trash is a list of the items already in the trash; these are not paths, just folder names
	
	#check if any of the items to be trashed have the same name as one of the already trashed items and rename the next one to be trashed
	
	for item in junk_classes:
		new_name = item.name
		count = 1
			
		while os.path.exists(f"static/trash/{new_name}"):
				
			new_name = f"{item.name}_duplicate{count}"
			
			count += 1
				
		os.mkdir(f"static/trash/{new_name}")			
		new_path = f"static/trash/{new_name}"
		shutil.move(item.path,new_path)
	messages.append("item-deleted")
	#updating other clients
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
		messages.append("item-uploaded")
		#updating other clients
		return render_template("upload_complete.html")
		
if __name__ == '__main__':
	
	app.run(debug=True, host=get_ip())