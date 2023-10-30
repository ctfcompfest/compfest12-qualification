from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP
import os
import random
import string
import sys

def generate_random_string(n):
    ASCII_CHAR = string.ascii_letters + string.digits
    
    ret = ""
    rand = random.SystemRandom()    
    for _ in range(n):
        ret = ret + rand.choice(ASCII_CHAR)
    return ret

VAR = {
    'nonroot_user': 'nonroot',
    'app_folder': '/opt/app_' + generate_random_string(16),
    'public_folder': '/usr/share/public_codebackup',
    'flag_filename': 'flag_is_here_' + generate_random_string(8) + '.txt',
    'rsakey_filename': 'codebackupRSA_' + generate_random_string(8) + '.pem',
    'flask_secret_key': generate_random_string(64),
    'flag': 'COMPFEST12{CR3aTing_Is_H4rde12_thaN_s0lv1nG_UpGraD3d_1badf416}'
}

print('Deleting old configuration files....', flush=True, end='')
file_list = os.listdir('./')
for e in file_list:
    if e.find('flag_is_here_') != -1: os.remove(e)
    elif e.find('codebackupRSA_') != -1: os.remove(e)
    elif e.find('env.yml') != -1: os.remove(e)
    elif e == 'Dockerfile': os.remove(e)
print('OK!', flush=True)

print('Genrating env.yaml...', flush=True, end='')
with open('env.yml', 'w+') as fileEnv:
    fileEnv.write("FLASK_HOST: 0.0.0.0\n")
    fileEnv.write("FLASK_PORT: 2727\n")
    fileEnv.write("FLASK_SECRET: {}\n".format(VAR['flask_secret_key']))
    fileEnv.write("FLASK_PATH: {}\n".format(VAR['public_folder']))
    fileEnv.write("FLASK_RSAKEY: /{}\n".format(VAR['rsakey_filename']))
print('OK!', flush=True)

print('Generating RSA key file...', flush=True, end='')
keyPair = RSA.generate(3072)
with open(VAR['rsakey_filename'], 'wb+') as fileKey:
    fileKey.write(keyPair.exportKey('PEM'))
print('OK!', flush=True)

print('Generating flag file...', flush=True, end='')
with open(VAR['flag_filename'], 'w+') as fileFlag:
    fileFlag.write(VAR['flag'])
print('OK!', flush=True)

print('Generating Dockerfile...', flush=True, end='')
with open('Dockerfile-template', 'r') as docker_file:
    docker_sample = docker_file.read()
    for k in VAR:
        pattern = "## {} ##".format(k)
        docker_sample = docker_sample.replace(pattern, VAR[k])
    
    with open('Dockerfile', 'w+') as docker_res:
        docker_res.write(docker_sample)    
print('OK!', flush=True)
