# -*- coding: UTF-8 -*-
# toolz_ext: extension of toolz


# def concat(x):
#     return list(itertools.chain.from_iterable(x))

import itertools
import toolz

def power(iterable, hook=set):
    # power set
    return (hook(a) for a in toolz.concat(itertools.combinations(iterable, r) for r in range(len(iterable)+1)))



def quotient(lst, key=None, rel=lambda x, y: x==y):
    '''rel is an equivalent relation
    return a partition of X, X/rel
    also see groupby in toolz
'''
    if lst==[]:
        return lst
    elif len(lst)==1:
        return [lst]
    if key:
        rel = lambda x, y: key(x)==key(y)
    #~ if rel: key = lambda x: {a for a in lst if rel(x, a)}
    p = [[lst[0]]]
    for a in lst[1:]:
        for cls in p:
            if rel(a, cls[0]):
                cls.append(a)
                break
        else:
            p.append([a])
    return p

def sortby(lst, key=None, rel=lambda x, y: x==y):
    return concat(quotient(lst, key, rel))

def repeatby(lst, nums):
    '''example:
>>> repeatby(['w','r','y'],[3,2,1,2])
['w', 'w', 'w', 'r', 'r', 'y', 'w', 'w']
'''
    new = []
    l = len(lst)
    for k, n in enumerate(nums):
        if l>k:
            new.extend([lst[k]]*n)
        else:
            new.extend([lst[k%l]]*n)
    return new


def allx(seq, key):
    return all(key(a) for a in seq)


def anyx(seq, key):
    return any(key(a) for a in seq)

