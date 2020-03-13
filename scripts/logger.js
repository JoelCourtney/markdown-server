function markdoc_logger(id, text) {
    var e = document.getElementById(id);
    e.innerHTML += text + "<br />";
}

window.addEventListener('renderrequest', function () {
    for (var i = 0; i < server_side_logs.length; i++) {
        markdoc_logger(server_side_logs[i].id, server_side_logs[i].text);
    }
});