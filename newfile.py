import os

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
		
print(string+"\n")


#parsing experimentation
segments = string.split("%?%")
for segment in segments:
	if "@!@" in segment:
		sub_segments = segment.split("@!@")[:-1]
		for sub_segment in sub_segments:
			print(sub_segment)
	else:
		print(segment)