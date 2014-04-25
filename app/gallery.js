//set global variables
var dom_img_zoom = document.getElementById("img_zoom");
var dom_img_wide = document.getElementById("img_wide");
var dom_info = document.getElementById("info");
var dom_tbody = document.getElementById("tbody");

var my_n = d.length;
var my_i = -1;

var url = {
    "nsa": "http://www.nsatlas.org/getAtlas.html?submit_form=Submit&search=nsaid&nsaID=",
    "sdss": "http://skyserver.sdss3.org/dr10/en/tools/chart/navi.aspx?scale=0.7",
    "ned": "http://ned.ipac.caltech.edu/cgi-bin/objsearch?objname="
};

var a_template = document.createElement("a");
a_template.target="_blank";
a_template.setAttribute("class", "pure-button");

//set global functions
var add_hyperlink = function(href, text){
    var a = a_template.cloneNode();
    a.href = href;
    a.innerHTML = text;
    dom_info.appendChild(a);
};

var load_object = function(i){
    var di = d[i];
    var nsa = di.nsa;
    //load images
    dom_img_zoom.setAttribute("src", "images/zoom_" + nsa + ".jpg");
    dom_img_wide.setAttribute("src", "images/wide_" + nsa + ".jpg");
    //write info
    dom_info.innerHTML = "";
    add_hyperlink(url.nsa + nsa, "NSA " + nsa);
    add_hyperlink(url.sdss + "&ra="+di.ra+"&dec="+di.dec, "SDSS "  + di.iau);
    if("ned" in di) add_hyperlink(url.ned+encodeURIComponent(di.ned), di.ned);
    //write table
    dom_tbody.innerHTML = "<tr><td>" 
        + ([di.ra, di.dec, di.dist].concat(di.userdata)).join("</td><td>") 
        + "</td></tr>";
    window.location.hash = "#" + nsa;
    my_i = i;
};

var load_object_by_nsa = function(nsa){
    if (nsa in nsa_map) load_object(nsa_map[nsa]);
};

//initialize
document.getElementById("footer").innerHTML += " Total # = " + my_n.toString();
document.getElementById("thead").innerHTML = "<tr><th>" 
    + (["RA", "Dec", "NSA dist (Mpc/h)"].concat(ud_header)).join("</th><th>") 
    + "</th></tr>";
load_object_by_nsa(window.location.hash.substring(1));
if (my_i < 0) load_object(0);

//binding events
$('#btn_next').click(function() {
    load_object((my_i+1)%my_n);
    $('#nsa_id').val("");
});

$('#btn_prev').click(function() {
    load_object((my_i+my_n-1)%my_n);
    $('#nsa_id').val("");
});

$('#nsa_id').change(function(){
    load_object_by_nsa($(this).val());
});

$('#nsa_id').keyup(function(event){
    load_object_by_nsa($(this).val());
});

$('#nsa_id').keydown(function(event){
    if (event.which==13 || event.which==27){
        event.preventDefault();
        $(this).blur();
    }
});

$(document).keydown(function(event){
    if (event.target.tagName.toUpperCase() !== 'INPUT'){
        switch(event.which){
            case 37:
            case 74:
                $('#btn_prev').click();
                break;
            case 39:
            case 75:
                $('#btn_next').click();
                break;
            case 70:
            case 191:
                event.preventDefault();
                $('#nsa_id').focus();
                break;
        }
    }
});

