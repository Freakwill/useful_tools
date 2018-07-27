# -*- coding: utf-8 -*-
'''mydict

my module about dictionaries

-------------------------------
Path: mywork\mydict.py
Author: William/2015-09-05
'''

import collections                                                                                                                                                                                                                                                                       


class myDict(collections.UserDict):
    
    def __init__(self,dct={}):
        super(myDict, self).__init__(dct)

    def __call__(self,key):
        # key: key-list(set, tuple) of myDict object
        if isinstance(key, set):
            return set([self[k] for k in key])
        elif isinstance(key, list):
            return [self[k] for k in key]
        elif not isinstance(key,collections.Hashable) and isinstance(key,collections.Iterable):
            return (self[k] for k in key)
        elif key in self:
            return self[key]
        elif isinstance(key, tuple):
            return tuple(self[k] for k in key)
        elif isinstance(key,collections.Iterable):
            return (self[k] for k in key)
        else:
            print('do nothing!')

    def __or__(self, key):
        # constrain on key
        if isinstance(key, set):
            return myDict({k:self[k] for k in key})
        elif isinstance(key, list):
            return [(k, self[k]) for k in key]
        elif not isinstance(key,collections.Hashable) and isinstance([],collections.Iterable):
            return ((k, self[k]) for k in key)
        elif key in self:
            return self[key]
        elif isinstance(key, tuple):
            return tuple((k, self[k]) for k in key)
        elif isinstance(key,collections.Iterable):
            return ((k, self[k]) for k in key)
        else:
            print('do nothing!')

    def __ior__(self,key):
        return self.__or__(key)

    def apply(self,fun,*args,**kw):
        return fun(self.data, *args, **kw)
        
    def dict2dict(self,fun,*args,**kw):
        # fun : dict -> dict
        self.data = fun(self.data, *args,**kwa)

    '''def dict2dictx(self,*others,fun,*args,**kw):
        # fun : dict -> dict
        self.data=fun(self.data, *(other.data for other in others), *args, **kwa)
'''
    def __invert__(self):
        data={}
        for key, val in self.items():
            if val not in data:
                data.update({val:key})
            elif data[val] in self:
                data.update({val:(data[val], key)})
            else:
                data.update({val:data[val]+(key,)})
        return myDict(data)

    def is1_1(self):
        # is an 1-1 map
        data=[]
        for key, val in self.items():
            if val not in data:
                data.append(val)
            else:
                return False
        return True

    def torel(self):
        # dict => set of tuples (relation)
        return set((k, v) for k, v in self.items())

    def tolist(self):
        return [(k, v) for k, v in self.items()]

    def totypes(self):
        return [type(v) for k, v in self.items()]

    ''''def __iadd__(self, other):
        for k, v in self.items:
            self.data[k] = v + other.get(k, 0)'''

    def extend(self, *others):
        for other in others:
            for k, v in self.items():
                self.data[k].extend(other.get(k, []))

    def sort(self, key=None):
        pass

