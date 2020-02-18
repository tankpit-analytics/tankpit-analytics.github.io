function showDoT() {
    $('#awards_search_dot3').css({'display': 'table'});
    $('#awards_search_header_dot3').css({'display': 'block'});
}

function showPH() {
    $('#awards_search_ph1').css({'display': 'table'});
    $('#awards_search_header_ph1').css({'display': 'block'});
}

function showWC() {
    $('#awards_search_wc1').css({'display': 'table'});
    $('#awards_search_header_wc1').css({'display': 'block'});
}

function showLB() {
    $('#awards_search_lb1').css({'display': 'table'});
    $('#awards_search_header_lb1').css({'display': 'block'});
}

function hideDoT() {
    $('#awards_search_dot3').css({'display': 'none'});
    $('#awards_search_header_dot3').css({'display': 'none'});
}

function hidePH() {
    $('#awards_search_ph1').css({'display': 'none'});
    $('#awards_search_header_ph1').css({'display': 'none'});
}

function hideWC() {
    $('#awards_search_wc1').css({'display': 'none'});
    $('#awards_search_header_wc1').css({'display': 'none'});
}

function hideLB() {
    $('#awards_search_lb1').css({'display': 'none'});
    $('#awards_search_header_lb1').css({'display': 'none'});
}


function searchDoT() {
    showDoT();
    hidePH();
    hideWC();
    hideLB();
}

function searchPH() {
    hideDoT();
    showPH();
    hideWC();
    hideLB();
}

function searchLB() {
    hideDoT();
    hidePH();
    hideWC();
    showLB();
}

function searchWC() {
    hideDoT();
    hidePH();
    showWC();
    hideLB();
}
