# -*- coding: utf-8 -*-
from g import *
from f_print import *
import time

####################################### READ FILE ######################################################################

def write_to_file(file_name, s):
    str_s = '\n' + time.strftime("%d.%m.%Y %H:%M:%S") + s
    try:
       with open(file_name, 'a+') as file:
           file.write(str_s)
    except:
        f_print.print_exception(sys._getframe().f_code.co_name)

def read_file(file_name):
    global PAIRS_NR
    with open(file_name) as file:
        # read_data = f.read()
        data_file = [row.strip() for row in file]
        i = 0
        id_line = {}
        id_line[0]={}
        id_line[1]={}
        #key_line = {}
        lineArr = {}
        for line in data_file:
            if line.find(':') == 0:
                lineArr = line.split(':')
                id_line[0][i] = lineArr[1].strip()
                id_line[1][i] = lineArr[2].strip().upper()
                i = i + 1
    return id_line

def get_field_str(id_line, str):
    for id in id_line[0]:
        if id_line[0][id] == str:
            info = get_pairs_nr(id_line[1][id])
    return info

def get_field_flt(id_line, str):
    for id in id_line[0]:
        if id_line[0][id] == str:
            info = (float)(id_line[1][id])
    return info


########################################################################################################################