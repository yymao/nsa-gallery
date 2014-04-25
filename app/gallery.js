//set global variables
var dom_img_zoom = document.getElementById("img_zoom");
var dom_img_wide = document.getElementById("img_wide");
var dom_info = document.getElementById("info");
var dom_tbody = document.getElementById("tbody");

var my_n = d.length;
var my_i = nsa_map[window.location.hash.substring(1)];

var url = {"nsa": "http://www.nsatlas.org/getAtlas.html?submit_form=Submit&search=nsaid&nsaID=",
    "sdss": "http://skyserver.sdss3.org/dr10/en/tools/chart/navi.aspx?scale=0.7",
    "ned": "http://ned.ipac.caltech.edu/cgi-bin/objsearch?objname="};

var a_proto = document.createElement("a");
a_proto.target="_blank";
a_proto.setAttribute("class", "pure-button");

//set global functions
var add_hyperlink = function(href, text){
    var a = a_proto.cloneNode();
    a.href = href;
    a.innerHTML = text;
    dom_info.appendChild(a);
};

var change_img = function(i){
    var nsa = d[i].nsa;
    dom_img_zoom.setAttribute("src", "images/zoom_" + nsa + ".jpg");
    dom_img_wide.setAttribute("src", "images/wide_" + nsa + ".jpg");
    load_info(i);
    load_table(i);
    window.location.hash = "#" + d[i].nsa;
    my_i = i;
};

var load_info = function(i){
    var di = d[i];
    dom_info.innerHTML = "";
    add_hyperlink(url.nsa + di.nsa, "NSA " + di.nsa);
    add_hyperlink(url.sdss + "&ra="+di.ra+"&dec="+di.dec, "SDSS "  + di.iau);
    if("ned" in di) add_hyperlink(url.ned+encodeURIComponent(di.ned), di.ned);
};

var load_table = function(i){
    var di = d[i];
    var a = [di.ra, di.dec, di.dist].concat(di.userdata);
    dom_tbody.innerHTML = "<tr><td>" + a.join("</td><td>") + "</td></tr>";
}

//initialize
document.getElementById("footer").innerHTML += " Total # = " + my_n.toString();
document.getElementById("thead").innerHTML = "<tr><th>" 
    + (["RA", "Dec", "NSA dist (Mpc/h)"].concat(ud_header)).join("</th><th>") 
    + "</th></tr>";
if (my_i === undefined) my_i = 0;
change_img(my_i);

//binding events
$('#btn_next').click(function() {
    change_img((my_i+1)%my_n);
    $('#nsa_id').val("");
});

$('#btn_prev').click(function() {
    change_img((my_i+my_n-1)%my_n);
    $('#nsa_id').val("");
});

$('#nsa_id').keyup(function(event){
    var tmp_i = nsa_map[$(this).val()];
    if (tmp_i !== undefined) change_img(tmp_i);
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

