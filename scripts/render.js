var IdCounter = function () {
    this.counter = 0;
}

IdCounter.prototype = new String();

IdCounter.prototype.toString = function() {
    this.counter++;
    return this.counter+'-';
};

IdCounter.prototype.valueOf = function() {
    this.counter++;
    return this.counter+'-';
}

window.MathJax = {
    loader: {load: ['[tex]/physics', '[tex]/newcommand']},
    tex: {
      inlineMath: [['$', '$'], ['\\(', '\\)']],
      packages: {'[+]': ['physics', 'newcommand']},
      processEscapes: false,
      processEnvironments: true
    },
    svg: {
      fontCache: 'global'
    },
  };

var delimiters = [
    ["<tikz>", "</tikz>"],
    ["$%", "%$"],
    ["$$", "$$"],
    ["$", "$"]
];

var replacements = [
    [/<tikz>/g, '<div class="tikz-output script-output"><center><sc'+'ript type="text/tikz">\\begin{tikzpicture}[scale=2]'],
    [/<\/tikz>/g, '\\end{tikzpicture}</scr'+'ipt></center></div>'],
    [/\$%/g, "\\begin{align}"],
    [/%\$/g, "\\end{align}"],
    [/<table>/g, '<table class="table table-bordered table-nonfluid">'],
];

var converter;

function render(input) {
    var text = input;
    var cuts = [];
    var scripts = [];
    var i = text.indexOf('<script');
    var script_count = 0;
    while (i != -1) {
        var j = text.indexOf('</script>');
        if (j == -1) {
            console.log("missing close script tag");
            return "missing close script tag";
        }
        var script = text.slice(i, j+'</script>'.length);
        var close_hairpin = script.indexOf('>');
        scripts.push(script);
        text = text.slice(0,i) + text.slice(j+'</script>'.length);
        script_count++;
        i = text.indexOf('<script');
    }
    var cut_counter = 0;
    for (var d = 0; d < delimiters.length; d++) {
        var pair = delimiters[d];
        var i = text.indexOf(pair[0]);
        while (i != -1) {
            var j = text.indexOf(pair[1], i+1);
            if (j == -1) {
                console.log("missing close delimiter: " + pair[1]);
                return "missing close delimiter: " + pair[1];
            }
            var cut = text.slice(i, j+pair[1].length);
            cuts.push(cut);
            text = text.slice(0, i) + "%%%" + cut_counter++ + "%%%" + text.slice(j+pair[1].length);
            i = text.indexOf(pair[0]);
        }
    };
    converter = new showdown.Converter();
    converter.setOption('tables', true);
    converter.setOption('literalMidWordUnderscores', false);
    converter.setFlavor('github');
    converter.setOption('prefixHeaderId', new IdCounter());
    text = converter.makeHtml(text);
    for (var i = 0; i < cuts.length; i++) {
        text = text.replace(new RegExp("%%%" + i + "%%%","g"), function() {return cuts[i];});
    }
    for (var i = 0; i < replacements.length; i++) {
        text = text.replace(replacements[i][0], replacements[i][1]);
    }
    document.getElementById("pastebox").innerHTML = text;
    for (var i = 0; i < scripts.length; i++) {
        $('head').append(scripts[i]);
    }
    generate_toc();
    window.dispatchEvent(new CustomEvent("renderrequest"));
    MathJax.typesetPromise();
    set_title();
    $(document).keydown(function(e) {
        if (e.key == "Escape") {
            document.body.scrollTop = 0;
            document.documentElement.scrollTop = 0;
        }
    })
}

function prettify_code(text) {

}

var canvas_id_count = 0;
function spawn_canvas(id) {
    console.log(id);
}

function generate_toc() {
    var div = document.getElementById("toc");
    if (div) {
        var md = ''
        var pastebox = document.getElementById("pastebox");
        var sections = $("h2,h3,h4,toc")
        for (var i = 0; i < sections.length; i++) {
            var node = sections[i];
            switch (node.tagName) {
                case "H2":
                    md += "- [" + node.innerHTML + "](#"+node.id+")\n";
                    break;
                case "H3":
                    md += "\t- [" + node.innerHTML + "](#"+node.id+")\n";
                    break;
                case "H4":
                    md += "\t\t- [" + node.innerHTML + "](#"+node.id+")\n";
                    break;
                case "TOC": {
                    md += "\t".repeat(node.attributes.level.value);
                    md += "- [" + node.attributes.name.value + "](#"+node.id+")\n";
                    break;
                }
            }
        }
        html = "<center><h3>Table of Contents</h3></center>" + converter.makeHtml(md);
        div.innerHTML = html;
    }
}

window.addEventListener('renderrequest', (event) => {
    document.querySelectorAll('pre code').forEach((block) => {
      hljs.highlightBlock(block);
    });
  });

function set_title() {
	var title = document.getElementsByTagName("h1")[0].innerHTML;
	document.title = title;
}

