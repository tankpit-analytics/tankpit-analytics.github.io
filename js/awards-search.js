function showDoT() {
    $('#awards_search_dot3')
        .css({'display': 'table'});
}

function showPH() {
    $('#awards_search_ph1')
        .css({'display': 'table'});
}

function showLB() {
    $('#awards_search_lb1')
        .css({'display': 'table'});
}

function showWC() {
    $('#awards_search_wc1')
        .css({'display': 'table'});
}

function hideDoT() {
    $('#awards_search_dot3')
        .css({'display': 'none'});
}

function hidePH() {
    $('#awards_search_ph1')
        .css({'display': 'none'});
}

function hideLB() {
    $('#awards_search_lb1')
        .css({'display': 'none'});
}

function hideWC() {
    $('#awards_search_wc1')
        .css({'display': 'none'});
}

function searchDoT() {
    showDoT();
    hidePH();
    hideLB();
    hideWC();
}

function searchPH() {
    hideDoT();
    showPH();
    hideLB();
    hideWC();
}

function searchLB() {
    hideDoT();
    hidePH();
    showLB();
    hideWC();
}

function searchWC() {
    hideDoT();
    hidePH();
    hideLB();
    showWC();
}
