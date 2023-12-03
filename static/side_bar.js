function openNav() {
  /* Set the width of the side navigation to 250px */
  document.getElementById("mySidenav").style.width = "250px";
}

function closeNav() {
  /* Set the width of the side navigation to 0 */
  document.getElementById("mySidenav").style.width = "0";
}

function transform_menu_icon(x) {
  let isOpen = (document.getElementById("mySidenav").style.width) == "250px";
  x.classList.toggle("change");
  
  if (!isOpen) {
    openNav();
  } else if (isOpen) {
    closeNav();
  }
}