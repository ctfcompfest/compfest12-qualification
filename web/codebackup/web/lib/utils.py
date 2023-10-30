import os
import random
import string

def generate_user_id(n):
    ASCII_CHAR = string.ascii_letters + string.digits
    
    ret = ""
    rand = random.SystemRandom()
    
    for _ in range(n):
        ret = ret + rand.choice(ASCII_CHAR)
    return ret


def get_dir_info(path):
    file_list = next(os.walk(path))[2]
    total_size = 0
    num_file = len(file_list)

    for e in file_list:
        file_path = os.path.join(path, e)
        total_size += os.stat(file_path).st_size
   
    return {
        'size' : total_size,
        'num_file': num_file
    }


def init_user_dir(user_dir):
    welcome_filepath = os.path.join(user_dir, 'welcome.txt')

    os.mkdir(user_dir)
    with open(welcome_filepath, 'w+') as welcome_file:
        welcome_file.write('Welcome to codeBackup! You upload, we kept it secret.')