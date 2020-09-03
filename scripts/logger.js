function markdoc_javascript_logger(id, text, newline) {
    var e = document.getElementById(id);
    if (newline) {
        e.innerHTML += text + "<br />";
    } else {
        e.innerHTML += text;
    }
}

var vega_options = {
    "renderer": "canvas",
    "scaleFactor": 4
};

window.addEventListener('renderrequest', function () {
    for (var i = 0; i < server_side_output.length; i++) {
        var log = server_side_output[i]
        switch (log.type) {
            case "python_output":
                markdoc_javascript_logger(log.id, log.text, true);
                break;
            case "hadron_print":
                markdoc_javascript_logger(log.id, log.text, false);
                break;
            case "hadron_println":
                markdoc_javascript_logger(log.id, log.text, true);
                break;
            case "python_plot":
                vegaEmbed('#' + log.id, JSON.parse(log.text), vega_options);
                break;
        }
    }
});