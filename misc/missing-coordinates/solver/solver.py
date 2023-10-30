from numpy import array
from z3 import Solver, Reals, z3types

import copy
import sys
import string
import xml.etree.ElementTree as ET

NUM_ARG = {'M': 1, 'L': 1, 'H': 1, 'V': 1, 'Z': 0, 'C': 3, 'S': 2, 'Q': 2, 'T': 1}

def tofloat(x):
    if type(x) == float:
        return x
    return float(x.numerator_as_long()) / float(x.denominator_as_long())

def solve_eq(var):
    c0, c1, c2, c3 = Reals('c0 c1 c2 c3')
    q0, q1, q2 = Reals('q0 q1 q2')
    s = Solver()

    s.add(c0 == q0, c3 == q2)
    s.add(3 * c1 - q0 == 2 * q1)
    s.add(3 * c2 - q2 == 2 * q1)

    s.add(0 <= c0, -500 <= c1, -500 <= c2, 0 <= c3)
    s.add(c0 <= 3000, c1 <= 3500, c2 <= 3500, c3 <= 3000)
    
    s.add(0 <= q0, -500 <= q1, 0 <= q2)
    s.add(q0 <= 3000, q1 <= 3500, q2 <= 3000)

    for k, v in var.items():
        exec(f's.add({k} == {v})')
    s.check()
    
    try:
        ret = s.model()
        ret_dic = dict()
        for k in ret.decls():
            ret_dic[str(k)] = ret[k]
    except z3types.Z3Exception:
        print(var)
        exit(-1)
    
    return ret_dic

def find_missing_coordinates(qcoors, ccoors):
    yaxis = dict()
    xaxis = dict()
    for i in range(3):
        if qcoors[i] == None: continue
        xaxis[f'q{i}'] = qcoors[i][0]
        yaxis[f'q{i}'] = qcoors[i][1]
    for i in range(4):
        if ccoors[i] == None: continue
        xaxis[f'c{i}'] = ccoors[i][0]
        yaxis[f'c{i}'] = ccoors[i][1]
    ret_x = solve_eq(xaxis)
    ret_y = solve_eq(yaxis)
    
    quad_ret = list()
    cub_ret = list()
    for i in range(3):
        tmp = [ret_x[f'q{i}'], ret_y[f'q{i}']]
        quad_ret.append(tmp)
    for i in range(4):
        tmp = [ret_x[f'c{i}'], ret_y[f'c{i}']]
        cub_ret.append(tmp)

    return quad_ret, cub_ret

def get_pathdata(ins):
    ret = ""
    for elm in ins:
        cmd = elm[0]

        num_arg = NUM_ARG[cmd]
        
        args = elm[-1 * num_arg:]
        if cmd == 'Z': args = list()
        args_str = ""

        for arg in args:
            if cmd == 'H':
                args_str += f'{tofloat(arg[0]):0.05f} '
            elif cmd == 'V':
                args_str += f'{tofloat(arg[1]):0.05f} '
            else:
                args_str += f'{tofloat(arg[0]):0.05f},{tofloat(arg[1]):0.05f} '

        ret += f'{cmd} {args_str}'
    
    return ret.strip()

def parse_command(cmd, pos, args):
    ret = [copy.deepcopy(pos)]

    for elm in args:
        if elm in ['?,?', '?']:
            coor = None
        elif cmd == 'H':
            coor = [float(elm), pos[1]]
        elif cmd == 'V':
            coor = [pos[0], float(elm)]
        else:
            coor = elm.split(",")
            coor[0], coor[1] = float(coor[0]), float(coor[1])
        ret.append(coor)
    return ret  


def get_real_pathdata(qs, cs):
    quad_ins = list()
    cubic_ins = list()

    qs_list = qs.split(' ')
    cs_list = cs.split(' ')

    qs_idx = 0
    cs_idx = 0
    
    last_coor = [0, 0]
    init_coor = [0, 0]

    while qs_idx < len(qs_list) and cs_idx < len(cs_list):
        qs_cmd = qs_list[qs_idx]
        cs_cmd = cs_list[cs_idx]

        if qs_cmd == 'M':
            init_coor = qs_list[qs_idx + 1].split(",")
            init_coor = [float(init_coor[0]), float(init_coor[1])]
        
        qs_n = NUM_ARG[qs_cmd]
        qs_tmp = parse_command(qs_cmd, last_coor, qs_list[qs_idx + 1:qs_idx + qs_n + 1])
        
        cs_n = NUM_ARG[cs_cmd]
        cs_tmp = parse_command(cs_cmd, last_coor, cs_list[cs_idx + 1:cs_idx + cs_n + 1])

        if qs_cmd == 'Q' and cs_cmd == 'C':
            qs_coor, cs_coor = find_missing_coordinates(qs_tmp, cs_tmp)
        else:
            qs_coor, cs_coor = qs_tmp, cs_tmp
        
        quad_ins.append([qs_cmd] + qs_coor)
        cubic_ins.append([cs_cmd] + cs_coor)

        if qs_cmd == 'Z':
            last_coor = init_coor
        else:
            last_coor = quad_ins[-1][-1]

        qs_idx += NUM_ARG[qs_cmd] + 1
        cs_idx += NUM_ARG[cs_cmd] + 1

    return get_pathdata(quad_ins), get_pathdata(cubic_ins)

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print('Usage: solver.py <SVG Quad> <SVG Cubic>')
        exit(-1)

    quad_svg = ET.parse(sys.argv[1]).getroot()
    cubic_svg = ET.parse(sys.argv[2]).getroot()

    for i in range(len(quad_svg)):
        quad_accum = dict()
        cubic_accum = dict()

        for qo, co in zip(quad_svg[i], cubic_svg[i]):
            qo_id = qo.attrib['id']
            co_id = co.attrib['id']
            if qo.tag == "path": quad_accum[qo_id] = qo.attrib['d']
            if co.tag == "path": cubic_accum[co_id] = co.attrib['d']

        for obj_id in quad_accum:
            print(obj_id)
            quad_accum[obj_id], cubic_accum[obj_id] = get_real_pathdata(quad_accum[obj_id], cubic_accum[obj_id])

        for j in range(len(quad_svg[i])):
            qo = quad_svg[i][j]
            co = cubic_svg[i][j]
            if qo.tag == "path":
                qo.attrib['d'] = quad_accum[qo.attrib['id']]
            if co.tag == "path":
                co.attrib['d'] = cubic_accum[co.attrib['id']]


    quad_str = ET.tostring(quad_svg)
    with open('solver_res1.svg', 'wb+') as f:
        f.write(quad_str)
    
    cubic_str = ET.tostring(cubic_svg)
    with open('solver_res2.svg', 'wb+') as f:
        f.write(cubic_str)