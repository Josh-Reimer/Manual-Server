import os

rootdir = './static/manuals'

folders_and_subfolders = []
folders = os.listdir(rootdir)

for folder in folders:
    current_path = []
    current_path.append(folder)
    current_path.append(os.listdir(os.path.join(rootdir, folder)))
    folders_and_subfolders.append(current_path)

html = ""

for item in folders_and_subfolders:
    item_title = item[0]
    html += '<button class="collapsible">\n<object class="thumbnail" id="file_icon" data="/static/file_icon.svg">\n</object>' + item_title + '</button>\n'
    
    for items in item[1]:
        html += '<div class="content">\n'
        html += '<button class="manual_buttons">\n<object class="thumbnail" id="file_icon" data="/static/file_icon.svg">\n</object>' + items + '</button>\n'
        html += '</div>\n'

print(html)


'''
this code was written by chatgpt on a request to merge two code snippets
'''