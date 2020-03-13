function markdoc_javascript_logger(id, text) {
    var e = document.getElementById(id);
    e.innerHTML += text + "<br />";
}

var vega_options = {
    "renderer":"canvas",
    "scaleFactor": 4
};

window.addEventListener('renderrequest', function () {
    for (var i = 0; i < server_side_output.length; i++) {
        var log = server_side_output[i]
        switch (log.type) {
            case "python_output":
                markdoc_javascript_logger(log.id, log.text);
                break;
            case "python_plot":
                vegaEmbed('#'+log.id, JSON.parse(log.text),vega_options);
                break;
        }
    }
});