blacklist = ["javascript", "script", "system", "join", "self", "attr", "document", "get", "post", "alert", "onclick",
             "onafterprint", "onbeforeprint", "onbeforeunload", "onhaschange", "onmessage", "onoffline", "onload",
             "onerror", "ononline", "onpagehide", "onpageshow", "onpopstate", "onresize", "onstorage", "onunload", "_"]

def html_encode(text):
    out = ""
    for char in text:
        out += "&#" + str(ord(char)) + ";"
    return out

def filterText(text):
    for string in blacklist:
        text.replace(string, html_encode(string))
        text.replace(string.upper(), html_encode(string.upper()))
    return text if len(text) <= 5000 else text[:5000]
