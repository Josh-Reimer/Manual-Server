  
    /*
  code in this script is for the file explorer
  drop-down
  */

// Attach listeners on page load
document.addEventListener('DOMContentLoaded', function() {
  if (typeof attachCollapsibleListeners === 'function') {
    attachCollapsibleListeners();
  }
});