import json
import os

logs = []
def markdoc_python_logger(id, text):
    logs.append({'type':'python_output', 'id':id, 'text':str(text)})

def markdoc_python_plotter(id, chart):
    logs.append({'type':'python_plot', 'id':id, 'text':chart.to_json()})

def generate_html(path):
    paste = ''
    template = ''
    logs.clear()
    with open(path, mode='r') as file:
        paste = file.read()
    with open('index.html', mode='r') as file:
        template = file.read()
    for f in pipeline:
        paste = f(paste)
    paste = paste.replace("\\", "\\\\").replace('"', r'\"').replace('<','<"+"').replace('\n', r'\n')
    text = template.replace("%%%paste%%%", paste)
    text = text.replace("%%%server_side_output%%%", json.dumps(logs))
    encoded = text.encode("utf-8", 'surrogateescape')
    return encoded

def process_code(text):
    output_counter = 0

    python_code = ''
    hadron_code = 'fn markdoc_hadron_print_logger(id,s) {println(id+" print%%%:"+s)}\n'
    hadron_code += 'fn markdoc_hadron_println_logger(id,s) {println(id+" println%%%:"+s)}\n'
    empty_hadron = hadron_code

    start = '```['
    arg_end = ']\n'
    end = '```'
    code_start = text.find(start)
    while code_start != -1:
        replace = ''
        code_arg_end = text.find(arg_end)
        code_end = text.find(end, code_start+3)
        params = text[code_start+4:code_arg_end]

        # Determine the language
        language = ''
        if params.find("javascript") != -1:
            language = "javascript"
        elif params.find("tikz") != -1:
            language = "TeX"
        elif params.find("python") != -1:
            language = "python"
        elif params.find("css") != -1:
            language = 'css'
        elif params.find("hadron") != -1:
            language = 'hadron'
            
        # Prettify code if requested
        if params.find("code") != -1:
            l = language
            if l == "hadron":
                l = "kotlin"
            replace += '```'+l+'\n' + text[code_arg_end+2:code_end] + '```'
        
        # Prepare javascript to run, provide output space
        if language == 'javascript':
            replace += "<script>"
            code = text[code_arg_end+2:code_end]
            if code.find("log(") != -1:
                id = 'script-output-' + str(output_counter)
                output_counter += 1
                code = code.replace("log(", "markdoc_javascript_logger('"+id+"',")
                replace += code + '</script><div class="script-output log-output" id="'+id+'"></div>'
            else:
                replace += text[code_arg_end+2:code_end] + "</script>"
            replace += "</script>"
        
        # Prepare tikz to be processed by render.js
        elif params.find("tikz") != -1:
            replace += '<tikz>' + text[code_arg_end+2:code_end]+'</tikz>'
        
        # Piece together python provide output
        elif language == "python":
            code = text[code_arg_end+2:code_end]
            if code.find("print(") != -1:
                id = 'script-output-' + str(output_counter)
                output_counter += 1
                code = code.replace("print(", "markdoc_python_logger('"+id+"',")
                replace += '<div class="script-output log-output" id="'+id+'"></div>'
            if code.find("plot(") != -1:
                id = 'script-output-' + str(output_counter)
                output_counter += 1
                code = code.replace("plot(", "markdoc_python_plotter('"+id+"',")
                replace += '<div class="script-output plot-output" id="'+id+'"></div>'
            python_code += code + '\n'
        
        elif language == "css":
            code = text[code_arg_end+2:code_end]
            replace += '<style>\n' + code + '\n</style>'
        
        elif language == "hadron":
            code = text[code_arg_end+2:code_end]
            id = 'script-output-' + str(output_counter)
            increment_to = output_counter + 1
            replace_with = replace + '<div class="script-output log-output" id="'+id+'"></div>'
            if code.find("print(") != -1:
                output_counter = increment_to
                code = code.replace("print(", 'markdoc_hadron_print_logger("'+id+'",')
                replace = replace_with
            if code.find("println(") != -1:
                output_counter = increment_to
                code = code.replace("println(", 'markdoc_hadron_println_logger("'+id+'",')
                replace = replace_with
            hadron_code += code + '\n'

        
        # replace text
        text = text[:code_start] + replace + text[code_end+3:]

        # search for new code blocks
        code_start = text.find(start)

    # Run the python code
    if python_code != '':
        exec(python_code, {
            'markdoc_python_logger': markdoc_python_logger,
            'markdoc_python_plotter': markdoc_python_plotter
        })

    if hadron_code != empty_hadron:
        execute_hadron(hadron_code)

    return text

def process_divs(text):
    start = text.find('||')
    while start != -1:
        end = text.find('||', start+2)
        id = text[start+2:end]
        text = text[:start] + '<div class="mdoc-div" id="'+id+'"></div>' + text[end+2:]
        start = text.find('||')
    return text

pipeline = [process_code, process_divs]

def execute_hadron(code):
    with open(".markdoc_hadron.hn", "w") as f:
        f.write(code)
    out = os.popen("hadron .markdoc_hadron.hn").read()
    id = ''
    type = ''
    for line in out.splitlines():
        colon = line.find("%%%:")
        if colon != -1:
            info = line[0:colon]
            content = line[colon+4:]
            space = info.find(' ')
            if space != -1:
                id = info[0:space]
                type = "hadron_" + info[space+1:]
            else:
                print("COLON DELIMITER BUT NO SPACE FOUND")
                exit(10)
        else:
            print("HADRON CANT HANDLE THIS SO I CANT EITHER")
            exit(10)
        dic = {'type':type, 'id':id, 'text':content}
        logs.append(dic)
    os.system("rm .markdoc_hadron.hn")