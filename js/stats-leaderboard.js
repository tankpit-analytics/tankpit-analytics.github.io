function showPlaytime() {
    $('#stats_leaderboard_playtime').css({'display': 'table'});
}

function showKills() {
    $('#stats_leaderboard_kills').css({'display': 'table'});
}

function showDeaths() {
    $('#stats_leaderboard_deaths').css({'display': 'table'});
}

function hidePlaytime() {
    $('#stats_leaderboard_playtime').css({'display': 'none'});
}

function hideKills() {
    $('#stats_leaderboard_kills').css({'display': 'none'});
}

function hideDeaths() {
    $('#stats_leaderboard_deaths').css({'display': 'none'});
}

function searchPlaytime() {
    showPlaytime();
    hideKills();
    hideDeaths();
}

function searchKills() {
    hidePlaytime();
    showKills();
    hideDeaths();
}

function searchDeaths() {
    hidePlaytime();
    hideKills();
    showDeaths();
}
