import html
import json

logs = []
def markdoc_logger(id, text):
    logs.append({'id':id, 'text':str(text)})

def generate_html(path):
    paste = ''
    template = ''
    logs.clear()
    with open(path, mode='r') as file:
        paste = file.read()
    with open('template.html', mode='r') as file:
        template = file.read()
    paste = process_code(paste)
    paste = process_divs(paste)
    paste = paste.replace("\\", "\\\\").replace('"', r'\"').replace('<','<"+"').replace('\n', r'\n')
    text = template.replace("%%%paste%%%", paste)
    text = text.replace("%%%server_side_logs%%%", json.dumps(logs))
    encoded = text.encode("utf-8", 'surrogateescape')
    return encoded

def process_code(text):

    output_counter = 0

    python_code = ''

    start = '```['
    arg_end = ']\n'
    end = '```'
    code_start = text.find(start)
    while code_start != -1:
        replace = ''
        code_arg_end = text.find(arg_end)
        code_end = text.find(end, code_start+3)
        params = text[code_start+4:code_arg_end]

        language = ''
        if params.find("javascript") != -1:
            language = "javascript"
        elif params.find("tikz") != -1:
            language = "TeX"
        elif params.find("python") != -1:
            language = "python"
            
        
        if params.find("code") != -1:
            replace += '```'+language+'\n' + text[code_arg_end+2:code_end] + '```'
        
        if language == 'javascript':
            replace += "<script>"
            code = text[code_arg_end+2:code_end]
            if code.find("mdout") != -1:
                id = 'script-output-' + str(output_counter)
                output_counter += 1
                code = code.replace("mdout(", "markdoc_logger('"+id+"',")
                replace += code + '</script><div class="script-output log-output" id="'+id+'"></div>'
            else:
                replace += text[code_arg_end+2:code_end] + "</script>"
            replace += "</script>"
        elif params.find("tikz") != -1:
            replace += '<tikz>' + text[code_arg_end+2:code_end]+'</tikz>'
        elif language == "python":
            code = text[code_arg_end+2:code_end]
            if code.find("print(") != -1:
                id = 'script-output-' + str(output_counter)
                output_counter += 1
                code = code.replace("print(", "markdoc_logger('"+id+"',")
                replace += '<div class="script-output log-output" id="'+id+'"></div>'
            python_code += code + '\n'
        text = text[:code_start] + replace + text[code_end+3:]
        code_start = text.find(start)
    exec(python_code, {}, {'markdoc_logger': markdoc_logger})
    return text

def process_divs(text):
    start = text.find('||')
    while start != -1:
        end = text.find('||', start+2)
        id = text[start+2:end]
        text = text[:start] + '<div class="mdoc-div" id="'+id+'"></div>' + text[end+2:]
        start = text.find('||')
    return text
