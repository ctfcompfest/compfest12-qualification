from multipledispatch import dispatch 
from numpy import array, ndarray

import copy
import random
import sys
import string
import xml.etree.ElementTree as ET

CMD = {'M': 1, 'L': 1, 'H': 1, 'V': 1, 'Z': 0, 'C': 3, 'S': 2, 'Q': 2, 'T': 1}
K = 6

def get_new_coordinate(cmd, old, nxt):
    if cmd.isupper(): return nxt
    else: return old + nxt

def parse_command(cmd, pos, args):
    ret = [cmd.upper(), copy.deepcopy(pos)]
    nxt_pos = copy.deepcopy(pos)

    for elm in args:
        if cmd.islower():
            if cmd == 'h':
                tmp = array([float(elm), 0])
                nxt_pos = pos + tmp
            elif cmd == 'v':
                tmp = array([0, float(elm)])
                nxt_pos = pos + tmp
            else:
                tmp = list(map(float, elm.split(",")))
                nxt_pos = pos + array(tmp)
        else:
            if cmd == 'H':
                nxt_pos[0] = float(elm)
            elif cmd == 'V':
                nxt_pos[1] = float(elm)
            else:
                tmp = list(map(float, elm.split(",")))
                nxt_pos = array(tmp)
        ret.append(copy.deepcopy(nxt_pos))
    return ret, nxt_pos        

def parse_pathdata(s):
    s_list = s.split(' ')
    ins_list = list()
    
    last_cmd = ''
    last_coor = array([0, 0])
    init_coor = array([0, 0])

    idx = 0
    sz = len(s_list)
    while idx < sz:
        if s_list[idx].isalpha():
            if s_list[idx] in ['Z', 'z']:
                res, last_coor = parse_command(s_list[idx], last_coor, [])
                ins_list.append(res)
                last_coor = init_coor
            elif s_list[idx] in ['M', 'm']:
                tmp = list(map(float, s_list[idx + 1].split(",")))
                init_coor = get_new_coordinate(last_cmd, last_coor, tmp)

            last_cmd = s_list[idx]
            idx += 1
        else:
            # The subsequent pairs are treated as implicit lineto commands.
            if len(ins_list) > 0 and last_cmd in ['M', 'm'] and ins_list[-1][0] == 'M':
                last_cmd = chr(ord(last_cmd) - 1)

            num_arg = CMD[last_cmd.upper()]
            args = [s_list[i] for i in range(idx, idx + num_arg)]
            res, last_coor = parse_command(last_cmd, last_coor, args)
            ins_list.append(res)
            idx += num_arg
    return ins_list


def get_pathdata(ins):
    ret = ""
    for elm in ins:
        cmd = elm[0]

        num_arg = CMD[cmd]
        
        args = elm[-1 * num_arg:]
        if cmd == 'Z': args = list()
        args_str = ""

        for arg in args:
            if type(arg) == type(None):
                if args_str in ['H', 'V']: args_str += "? "
                else: args_str += "?,? "
                continue

            if cmd == 'H':
                args_str += f'{arg[0]:0.7f} '
            elif cmd == 'V':
                args_str += f'{arg[1]:0.7f} '
            else:
                args_str += f'{arg[0]:0.7f},{arg[1]:0.7f} '

        ret += f'{cmd} {args_str}'
    
    return ret.strip()

@dispatch(ndarray,ndarray,ndarray,ndarray) 
def cubic_to_quadratic_bezier(c0, c1, c2, c3):
    q0 = c0
    q2 = c3
    q1 = (3 * (c1 + c2) - q0 - q2) / 4
    return [q0, q1, q2]

@dispatch(list) 
def cubic_to_quadratic_bezier(c):
    return cubic_to_quadratic_bezier(c[0], c[1], c[2], c[3])

@dispatch(ndarray,ndarray,ndarray) 
def quadratic_to_cubic_bezier(q0, q1, q2):
    c0 = q0
    c1 = (q0 + 2 * q1) / 3
    c2 = (q2 + 2 * q1) / 3
    c3 = q2
    return [c0, c1, c2, c3]

@dispatch(list) 
def quadratic_to_cubic_bezier(q):
    return quadratic_to_cubic_bezier(q[0], q[1], q[2])

# Splitting to homogen quadratic and cubic instruction list
def split_ins_bezier(ins_list):
    quad, cubic = list(), list()
    for i in range(len(ins_list)):
        e = ins_list[i]

        for j in range(1, len(e)):
            ins_list[i][j] *= K
        
        if e[0] in ['C']:
            tmp = cubic_to_quadratic_bezier(e[1:])
            qtmp = quadratic_to_cubic_bezier(tmp)
            quad.append(['Q'] + tmp)
            cubic.append(['C'] + qtmp)
        elif e[0] in ['Q']:
            quad.append(copy.deepcopy(e))
            cubic.append(['C'] + quadratic_to_cubic_bezier(e[1:]))
        else:
            quad.append(copy.deepcopy(e))
            cubic.append(copy.deepcopy(e))
    return [quad, cubic]

# Nilai variabel yang diketahui
HINT = [
    {'q1', 'c1', 'c2'},
    {'q0', 'q2', 'c1'}, {'c0', 'q2', 'c1'}, {'q0', 'c3', 'c1'},
    {'q0', 'q2', 'c2'}, {'c0', 'q2', 'c2'}, {'q0', 'c3', 'c2'},
    {'q0', 'q1', 'c2'}, {'q1', 'c0', 'c2'},
    {'q1', 'q2', 'c1'}, {'q1', 'c3', 'c1'}
]

def remove_variables(hint, quad, cubic):
    unknown_var = {'q0', 'q1', 'q2', 'c0', 'c1', 'c2', 'c3'} - hint
    chall_quad = copy.deepcopy(quad)
    chall_cubic = copy.deepcopy(cubic)

    for i in range(4):
        if f'q{i}' in unknown_var:
            chall_quad[i] = None
        if f'c{i}' in unknown_var:
            chall_cubic[i] = None    

    return [chall_quad, chall_cubic]

def convert_to_chall(quad_ins, cubic_ins):
    ret_q = list()
    ret_c = list()
    for q, c in zip(quad_ins, cubic_ins):
        if q[0] == 'Q':
            chall_q, chall_c = remove_variables(random.choice(HINT), q[1:], c[1:])
            ret_q.append(['Q'] + chall_q)
            ret_c.append(['C'] + chall_c)
        else:
            ret_c.append(copy.deepcopy(c))
            ret_q.append(copy.deepcopy(q))
    return [ret_q, ret_c]


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print('Usage: generate_chall.py <SVG file>')
        exit(-1)

    svg_tree = ET.parse(sys.argv[1])
    svg_root = svg_tree.getroot()

    svg_ins_list = list()
    chall_ins_list = list()
    for layer in svg_root:
        accum = dict()
        accum_chall = dict()

        for obj in layer:
            obj_id = obj.attrib['id']
            if obj.tag == 'path':
                obj_ins_list = parse_pathdata(obj.attrib['d'])
                quad_ins, cubic_ins = split_ins_bezier(obj_ins_list)
                quad_chall, cubic_chall = convert_to_chall(quad_ins, cubic_ins)
                
                accum[obj_id] = {
                    'cubic': cubic_ins,
                    'quad': quad_ins
                }
                accum_chall[obj_id] = {
                    'cubic': cubic_chall,
                    'quad': quad_chall
                }
        svg_ins_list.append(accum)
        chall_ins_list.append(accum_chall)
    
    svg_root.attrib['viewBox'] = '0 0 3000 3000'
    cubic_svg = copy.deepcopy(svg_root)
    quad_svg = copy.deepcopy(svg_root)

    for i in range(len(svg_root)):
        random.shuffle(cubic_svg[i])
        random.shuffle(quad_svg[i])
        for j in range(len(svg_root[i])):
            if cubic_svg[i][j].tag == 'path':
                obj_id = cubic_svg[i][j].attrib['id']
                cubic_pathdata = get_pathdata(chall_ins_list[i][obj_id]['cubic'])
                cubic_svg[i][j].attrib['d'] = cubic_pathdata

            if quad_svg[i][j].tag == 'path':
                obj_id = quad_svg[i][j].attrib['id']
                quad_pathdata = get_pathdata(chall_ins_list[i][obj_id]['quad'])
                quad_svg[i][j].attrib['d'] = quad_pathdata
                
    quad_str = ET.tostring(quad_svg)
    with open('share/missing_coor1.svg', 'wb+') as f:
        f.write(quad_str)
    
    cubic_str = ET.tostring(cubic_svg)
    with open('share/missing_coor2.svg', 'wb+') as f:
        f.write(cubic_str)