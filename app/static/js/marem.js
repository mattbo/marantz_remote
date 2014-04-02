/* Javascript to make AJAX requests on behalf of the Marem homepage */

function get_state() { 
  /* call the get_state endpoint and populate the form fields */
  console.log("in get_state");
  $.getJSON($SCRIPT_ROOT + '/get_state', {}, function(state) { 

    console.log("got state, volume " + state['volume']);
    $("#volume").val(state['volume']);

    var spkr_id = '#speakers option[value="' + state['speakers'] + '"]';
    $(spkr_id).attr("selected", true);

    var src_opt = '#source option[value="' + state['source'] + '"]';
    $(src_opt).attr("selected", true);
    
    var surr = '#surround_mode option[value="' + state['surround'] + '"]';
    console.log(surr);
    $(surr).attr("selected", true);
  });
}

/* Attach the javascript to the reload button */
$(function() {  $('#reload').on('click', get_state); });

function set_state() { 
    /* call the set_state endpoint */
    console.log("in set state");
    $.post($SCRIPT_ROOT + '/set_state', $(this).serialize());
}

$(function() { $('#volume').on('change', set_state); });
$(function() { $('#speakers').on('change', set_state); });
$(function() { $('#source').on('change', set_state); });
$(function() { $('#surround_mode').on('change', set_state); });
  
