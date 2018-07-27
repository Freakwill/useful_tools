# -*- coding: utf-8 -*-
'''mydeco

my decorator
-------------------------------
Path: mywork\mydeco.py
Author: William/2015-07-29
'''

import functools
import inspect

import toolz

def currying2(f):
    '''Currying: f(x,*y)  =>  f(*y)(x)
'''
    def g(*y):
        def h(x):
            return f(x,*y)
        return h
    return g

def show(f):
    '''wrapper == f as a function, but prints a string when calling it
'''
    @functools.wraps(f)
    def wrapper(*args):
        argspec=inspect.getargspec(f)
        narg=len(args)
        fnarg=len(argspec.args)
        # 0<=fnarg-narg<=len(argspec.defaults)
        print("Call: %s: arguments: "%f.__name__,end='')
        for arg in args:
            print('%s, '%arg,end='')
        if fnarg>narg:
            print('['+', '.join(map(str,argspec.defaults[-fnarg+narg:]))+']', end='')
        # print('\b')
        print(" = %s"%str(f(*args)))
        return f(*args)
    return wrapper


'''
@toolz.curry
def showx(arg, f):
    @functools.wraps(f)
    def wrapper(*args):
        print("Call:(%s) %s,"%(arg,f.__name__),'argument tuple: %r'%(args,))
        return f(*args)
    return wrapper

@currying2
def showx(f,*args):
    @functools.wraps(f)
    def wrapper(*args):
        print("Call:(%s) %s,"%(arg,f.__name__),'argument tuple: %r'%(args,))
        return f(*args)
    return wrapper
'''

'''@show
def foo(x,y,z=0,w=0):
    return x*y+z+w'''


def extend(f):
    def g(F):
        def h(x):
            return f(F(x))
        return h
    return g

def extend2(f):
    def g(F,G):
        def h(x):
            return f(F(x),G(x))
        return h
    return g

def extendn(f):
    def g(*Fs):
        def h(x):
            return f(*tuple(F(x) for F in Fs))
        return h
    return g

'''
@extend
def double(x):
    return x*2

@extendn
def add(x,y):
    return x+y
'''

def flatten(tup):
    flat=()
    for a in tup:
        if isinstance(a, tuple):
            flat+=flatten(a)
        else:
            flat+=(a,)
    return flat

def pack(f):
    def g(*p):
        return f(flatten(p))
    return g

def unpack(f):
    def g(*p):
        return f(*flatten(p))
    return g

@pack
def m(x):
    return x[0]+x[1]


@currying2
def add_callback(f, *callbacks):
    def g(*args, **kwargs):
        ret = f(*args, **kwargs)
        for callback in callbacks:
            callback(*args, **kwargs)
        return ret
    return g

@currying2
def insert_callback(f, *callbacks):
    def g(*args, **kwargs):
        for callback in callbacks:
            callback(*args, **kwargs)
        return f(*args, **kwargs)
    return g


@add_callback(lambda : print('hello'))
def f():
    print('come on')


# class decorator
optrans = {'+':'__add__','-':'__sub__','*':'__mul__','/':'__truediv__','**':'__pow__','&':'__and__','|':'__or__','^':'__xor__', \
'<<':'__lshift__','>>':'__rshift__','//':'__floordiv__','%':'__mod__','==':'__eq__','<':'__lt__','>':'__gt__','<=':'__le__','>=':'__ge__'}
ioptrans = {'i+':'__iadd__','i-':'__isub__','i*':'__imul__','i/':'__itruediv__','i**':'__ipow__','i&':'__iand__','i|':'__ior__','i^':'__ixor__', \
'i<<':'__ilshift__','i>>':'__irshift__','i//':'__ifloordiv__','i%':'__mod__'}


class FillMissingMethod:
    '''fill missing method form a special method
    properties:
        givenMethods: tuple of strings, the names of given methods
        convert: dict as {method name: function (base on given methods)}
    example:
    fill methods a+b a-b a-=b from a+=b and -a
    def divmethod(mul='__mul__', inv='inv'):
        def f(self, other):
            return getattr(self, mul)(getattr(other,inv)())
        return f

    def rdivmethod(mul='__mul__', inv='inv'):
        def f(self, other):
            return getattr(getattr(other,inv)(), mul)(other)
        return f

    def opmethod(iop='__iadd__'):
        def f(self, other):
            cpy = self.copy()
            return getattr(cpy, iop)(other)
        return f

    @FillMissingMethod(('__add__','__neg__'), {'__sub__':divmethod, '__rsub__':rdivmethod})
    @FillMissingMethod(('__iadd__','__neg__'), {'__isub__':divmethod})
    @FillMissingMethod(('__iadd__',), {'__add__':opmethod,'__radd__':opmethod})
    class MyClass:
        def copy(self):
            ...
        def __neg__(self):
            ...
        def __iadd__(self,other):
            ...
    '''
    def __init__(self, givenMethods, convert):
        self.givenMethods = givenMethods
        self.convert = convert

    def check(self, cls):
        for mth in self.givenMethods:
            if not hasattr(cls, mth):
                raise ValueError('must define all methods: %s in class %s'%(mth, cls.__name__))
        return True

    def __call__(self, cls):
        if self.check(cls):
            for opname, opfunc in self.convert.items():
                #opname = optrans.get(opname, opname)
                #opname = ioptrans.get(opname, opname)
                if not hasattr(cls, opname):    # opname is not defined explictively in cls
                    opfunc.__name__ = opname
                    if isinstance(opfunc, str):
                        setattr(cls, opname, getattr(cls, opfunc))
                    else:
                        setattr(cls, opname, opfunc(*self.givenMethods))
        return cls


def divmethod(mul='__mul__', inv='inv'):
    def f(self, other):
        return getattr(self, mul)(getattr(other,inv)())
    return f

def rdivmethod(mul='__mul__', inv='inv'):
    def f(self, other):
        return getattr(getattr(other,inv)(), mul)(other)
    return f

def opmethod(iop='__iadd__'):
    def f(self, other):
        cpy = self.copy()
        return getattr(cpy, iop)(other)
    return f

def fillarith(cls):
    return FillMissingMethod(('__mul__','inv'), {'__truediv__':divmethod, '__rtruediv__':rdivmethod})(
    FillMissingMethod(('__imul__','inv'), {'__itruediv__':divmethod})(
    FillMissingMethod(('__imul__',), {'__mul__':opmethod,'__rmul__':opmethod})(
    FillMissingMethod(('__add__','__neg__'), {'__sub__':divmethod, '__rsub__':rdivmethod})(
    FillMissingMethod(('__iadd__','__neg__'), {'__isub__':divmethod})(
    FillMissingMethod(('__iadd__',), {'__add__':opmethod,'__radd__':opmethod})(
    cls))))))
