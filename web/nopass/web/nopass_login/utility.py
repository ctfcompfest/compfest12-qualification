import random
import string

def get_html_context():
    html_context = {
        "token": "",
        "username": "",
        "is_admin": False,
        "tab_index": "",
        "tab_login": "",
        "tab_flag": "",
        "error_msg": ""
    }
    return html_context

def generate_random_string(n):
    ASCII_CHAR = string.ascii_letters + string.digits
    ret = ""
    rand = random.SystemRandom()
    for _ in range(n):
        ret = ret + rand.choice(ASCII_CHAR)
    return ret