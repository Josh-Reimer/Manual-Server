//this script is the controller
function get_file_explorer_contents() {
  const manual_explorer = document.getElementById("manual_explorer");

  load_url("/filenames", function(responseText) {

    let html = create_explorer_dropdown_items(responseText);
    manual_explorer.insertAdjacentHTML("afterbegin", html);
  });
}

function check_for_updates() {
  var targetContainer = document.getElementById("p");
  var eventSource = new EventSource("/update");
  eventSource.addEventListener("refresh", function(e) {
    targetContainer.textContent = e.data;
    console.log(e.data);
    refresh_file_explorer(e.data);
    if (e.data > 20) {
      targetContainer.style.color = "red";
    }
  });
}

function refresh_file_explorer(data) {
  const manual_explorer = document.getElementById("manual_explorer");
  
}


function add_folder() {
  const folder_name = prompt("enter a name for your new folder", "new_folder");
  console.log("add_folder function called");
  if (folder_name != null) {
    const manual_explorer = document.getElementById("manual_explorer");
    const url = "/add_folder?foldername="+folder_name;

    load_url(url, function(responseText) {
      if (responseText == "folder exists") {
        alert("The folder you are trying to create already exists");
      } else {
        let html = create_manual_explorer_item(responseText);
        //const fake_id = "collapsible_random1";
        //let html = `<button class='collapsible'><svg onclick='make_delete_list("${fake_id}")' id='collapsible_random1' class='thumbnail' width='32' height='32' viewBox='0 0 24 22' xmlns='http://www.w3.org/2000/svg' version='1.1' preserveAspectRatio='xMinYMin'><use xlink:href='#img-file-icon'></use></svg>random1</button><div class='content'></div>`;
        /*
        To do make sure to add the onclick and the dynamic id to each item added in the client side
        */
        manual_explorer.insertAdjacentHTML("afterbegin", html);
      }
    });
  }
}

var delete_list = []; //delete_list stores the dom elements that are to be removed on the client side and moved to trash on the server side
var icons_in_use = [];

function make_delete_list(item_to_delete) {
  console.log("item to delete>>"+item_to_delete);
  let item_to_delete_object = document.getElementById(item_to_delete);
  //item_to_delete is a string containing info on whether the item to delete is a collapsible or content and which item it is.
  //the info is delimited using _ or  _| or |
  //** also, the string is that item's html id **
  icons_in_use.push(item_to_delete_object);
  //adding the manual or folder that was selected to the icons_in_use list together with the icon state that particular item has

  let icon_in_use_index; //stores which item in the icons_in_use list is the one this function uses this moment
  var icon_in_use; //stores the item from the icons_in_use list at the index icon_in_use_index
  for (let i = 0; i < icons_in_use.length; i++) {
    //loop through the icons_in_use list^
    console.log(item_to_delete_object.id + " >> " + icons_in_use[i].id);
    if (icons_in_use[i].id == item_to_delete_object.id) {
      //if the object to be deleted(the argument) is equal to the current object in the list as we are looping through, assign that object to the icon_in_use variable and make the icon_in_use_index equal to i
      icon_in_use = icons_in_use[i];
      icon_in_use_index = i;
    }
  }

  const selectable_elements = document.getElementsByClassName('collapsible');
  const file_icons = document.getElementsByClassName('thumbnail');


  // Select the SVG element using its ID
  const svgIcon = document.getElementById(item_to_delete_object.id.toString());

  console.log("icon in use:"+icon_in_use.querySelector('use').getAttribute('xlink:href'));

  if (icon_in_use.querySelector('use').getAttribute('xlink:href') == "#img-file-icon") {
    svgIcon.querySelector('use').setAttribute('xlink:href', '#img-checkbox-icon');
    if (!delete_list.includes(item_to_delete_object)) {
      delete_list.push(item_to_delete_object);
    }
  } else {
    svgIcon.querySelector('use').setAttribute('xlink:href', '#img-file-icon');
    if (delete_list.includes(item_to_delete_object)) {
      const index = delete_list.indexOf(item_to_delete_object);
      if (index > -1) {
        // only splice array when item is found
        delete_list.splice(index, 1); // 2nd parameter means remove one item only
      }
    }
  }

}

function delete_folder() {
  //first check if there is anything selected before sending a delete request to server
  if (delete_list.length != 0) {
    let confirm_text = "";
    if (delete_list.length > 1) {
      confirm_text = `Are you sure you want to delete these ${delete_list.length} items? All items inside these items will also be deleted.`;
    } else {
      confirm_text = "Are you sure you want to delete 1 item? All items inside this item will also be deleted.";
    }
    if (confirm(confirm_text)) {
      // ask for confirmation of delete before sending delete list to flask server

      let delete_list_string = "[";
      for (let thing of delete_list) {
        delete_list_string += thing.id+",";
        //remove elements from dom
        let parent_element = thing.parentElement;
        parent_element.remove();
      }
      delete_list_string = delete_list_string.slice(0, -1);
      delete_list_string += "]";
      console.log("are you sure you want to delete these items?\n"+delete_list_string);

      const url = "/delete_item?junk_items="+delete_list_string;

      load_url(url, function(responseText) {
        console.log(responseText);
      });

    }
  }
}

var manual_views_already_loaded = [];

function get_manual_view(manual) {
  const manual_clicked_on = document.getElementById(manual);

  if (!manual_views_already_loaded.includes(manual_clicked_on)) {
    const url = `/manual_view?manual=${manual}`;
    load_url(url, function(responseText) {
      manual_views_already_loaded.push(manual_clicked_on);
      const manual_view = document.getElementsByClassName("modal-content");
      const modal = document.getElementById("myModal");
      const close_button = document.getElementById("spanclose");

      close_button.insertAdjacentHTML("afterend", responseText);
      //get the responseText displayed on the page as rendered html
    });
    /*
  send the name of the manual to get the view for to the server
  */
  }
  modal.style.display = "block";
}