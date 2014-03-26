/* Javascript to make AJAX requests on behalf of the Marem homepage */

function get_state() { 
  /* call the get_state endpoint and populate the form fields */
  $.getJSON($SCRIPT_ROOT + '/state', {}, function(data) { 
    $("#volume").value(state['volume']);

    var spkr_id = '.spkr_' + state['speakers'];
    $(".spkr_state").deselect(); //probably does not work
    $(spkr_id).selected();

    var src_opt = '#' + state['source'];
    $("#source", src_opt).selected();
    
    //surround is not yet implemented
    //var surr = '#' + state['surround']
  });
}

function set_state() {
  
