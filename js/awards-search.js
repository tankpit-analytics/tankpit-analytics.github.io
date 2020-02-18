function showDoT() {
    $('#awards_search_dot3')
        .removeClass('awards_search_hidden');
        .addClass('awards_search_visible');
}

function showPH() {
    $('#awards_search_ph1')
        .removeClass('awards_search_hidden');
        .addClass('awards_search_visible');
}

function showLB() {
    $('#awards_search_lb1')
        .removeClass('awards_search_hidden');
        .addClass('awards_search_visible');
}

function showWC() {
    $('#awards_search_wc1')
        .removeClass('awards_search_hidden');
        .addClass('awards_search_visible');
}

function hideDoT() {
    $('#awards_search_dot3')
        .removeClass('awards_search_visible');
        .addClass('awards_search_hidden');
}

function hidePH() {
    $('#awards_search_ph1')
        .removeClass('awards_search_visible');
        .addClass('awards_search_hidden');
}

function hideLB() {
    $('#awards_search_lb1')
        .removeClass('awards_search_visible');
        .addClass('awards_search_hidden');
}

function hideWC() {
    $('#awards_search_wc1')
        .removeClass('awards_search_visible');
        .addClass('awards_search_hidden');
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
