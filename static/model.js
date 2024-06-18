
/*
this script is the model
it only process data and fetches it.
it is queried by the controller
*/
function load_url(url, callback) {
  
  var xhr = new XMLHttpRequest();
  xhr.onreadystatechange = function() {
    if (this.readyState == 4 && this.status == 200) {
      // Process the response here
      callback(this.responseText);
    }
  };

  xhr.open("GET", url, true);
  xhr.send();
}

function create_links(string) {
  list_of_file_names = string.split("%?%");
  let html = "<a ";
  for (let i = 0; i < list_of_file_names.length; ++i) {
    html += "href='static/manuals/"+list_of_file_names[i]+"'>"+list_of_file_names[i]+"</a><br><a ";
  }
  html += "></a>";
  return html;
}

function create_manual_explorer_item(item_name) {
  return `<button class="collapsible"><svg onclick="make_delete_list('collapsible_${item_name}') id='collapsible_${item_name}' class="thumbnail" width="32" height="32" viewBox="0 0 24 22" xmlns="http://www.w3.org/2000/svg" version="1.1" preserveAspectRatio="xMinYMin"><use xlink:href="#img-file-icon"></use></svg>${item_name}</button><div class="content"></div>`;
}

function create_explorer_dropdown_items(input_string) {
  const segments = input_string.split("%?%");
  segments.shift();
  let html = "";
  for (const segment of segments) {
    if (segment.includes("@!@")) {
      subSegments = segment.split("@!@");
      subSegments = subSegments.slice(0, -1);
      html += '<div class="content">\n';
      for (const subSegment of subSegments) {
        html += '<button class="manual_buttons">\n<object class="thumbnail" id="file_icon" data="/static/file_icon.svg">\n</object>'+subSegment+'</button>\n';
        console.log(subSegment);
      }
    } else {
      //this html is the parent of a drop-down folder
      //the first part, that div closing, closes the collapsible content that will have started before
      if (html == "") {
        html += '<button class="collapsible">\n<object class="thumbnail" id="file_icon" data="/static/file_icon.svg">\n</object>'+segment+'</button>\n';

      } else {
        html += '</div><button class="collapsible">\n<object class="thumbnail" id="file_icon" data="/static/file_icon.svg">\n</object>'+segment+'</button>\n';
      }
      console.log(segment.toUpperCase());
    }
  }
  console.log(html);
  return html;
}