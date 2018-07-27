# -*- coding: UTF-8 -*-
# mypy.py

# print and input:
def show(*args):
    for k, x in enumerate(args, 1):
        print('[%d]'%k, x, ':', type(x)) 


def dictprint(dct, sep=': '):
    # print dict
    for key, val in dct.items():
        print("%s%s%s"%(key, sep , val))

    
def listinput(sep=None, postprocess=None):
    # input a list of strings
    s = input()
    if sep:
        ret = s.split(sep)
    else:
        ret = s.split()
    return list(map(postprocess, ret)) if postprocess else ret


def myinput(s):
    w = input(s)
    while w == '':
        print('make sure that input is not empty!')
        w = input(s)
    return w


#------------------------------------

def mytry(s, loc=(), show_error=False):
    locals().update(loc)
    try:
        exec(s)
        return True
    except Exception as ex:
        if show_error:
            print('Error:',ex)
        return False


# functional programming
def apply(funlist, arglist):
    '''
    [...f_i(x_i)...]
    '''
    return [f(*x) for f, x in zip(funlist, arglist)]

def applyx(funlist, arglist):
    '''
    [...f_i(x_i)...]
    '''
    return [f(*x) if isinstance(x, tuple) else f(x) for f, x in zip(funlist, arglist)]

def zip_repeat(a, b):
    L1 = len(a)
    L2 = len(b)
    if L1<L2:
        return zip(a*(L2//L1), b)
    elif L1>L2:
        return zip(a, b*(L1//L2))
    else:
        return zip(a, b)
