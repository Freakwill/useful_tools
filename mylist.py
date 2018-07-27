# -*- coding: UTF-8 -*-
'''mylist

list processing
------------------
Path: mywork\mylist.py
William/2015-06-26
'''

'''
notation:
dct: dictionary
elm: element
lst: list
rel: relation
s: string
k, l: index
a: element in a list
'''


def str2pair(s, ch=":", strip=False):
    ret = s.split(ch, 1)
    if strip:
        return [ret[0].strip(), ret[1].strip()]
    else:
        return ret

# list processing
## print list

def enumprint(lst, no='(1)'):
    for k, a in enumerate(lst,1):
        print(no.replace('1',str(k)), a)

def treeprint(lst,indent=0):
    # print a list as a tree
    for a in lst:
        if not isinstance(a, list):
            if indent==0:print(a)
            else:
                print(' '*(indent-4)+'+'+'-'*3+str(a))
        else:
            treeprint(a,indent=indent+4)

# transform of lists
def list2dict(lst, strip=False):
    ''' lst is a list of strings
example:  ['1:a','2:b'] ==> {'1':'a','2':'b'}
'''
    return dict(str2pair(s, ":" , strip) for s in lst)


# list operating
def list_split(lst, ch=""):
    # split a list to (a list of) lists by ch
    if lst == []:
        return []
    k = 0
    newlst = [[]]
    for elm in lst:
        if elm == ch:
            k += 1
            newlst.append([])
        else:
            newlst[k].append(elm)
    return newlst


def list_splitx(lst,ch=""):
    '''It is powerful than list_split. For example,
>>> list_splitx(["","","my python","","","hello world","I love you"])
[['my python'], ['hello world', 'I love you']]
'''
    if lst==[]:
        return []
    newlst=[[]]
    k=0
    i=0
    for elm in lst:
        if elm != ch:
            break
        else:
            i+=1

    while i<len(lst)-1:
        if lst[i]==ch:
            if lst[i+1] != ch:
                k+=1
                newlst.append([lst[i+1]])
                i+=2
            else:
                i+=1
        else:
            newlst[k].append(lst[i])
            i+=1

    if i<len(lst) and lst[i]!=[]:
        newlst[k].append(lst[i])
    return newlst

def flatten(lst):
    # lst is a list (or list of lists)
    # list => list (1-order)
    flat = []
    for a in lst:
        if isinstance(a, list):
            flat.extend(flatten(a))
        else:
            flat.append(a)
    return flat


def join2(lst, ch1=', ', ch2='\n'):
    # lst: list of lists (2-order list)
    r = len(lst)
    return ch2.join(ch1.join(str(a) for a in lst[k]) for k in range(r))

def exclude_append(lst,a):
    # union for list
    if a not in lst:
        lst.append(a)
    return lst

def exclude_extend(lst1,lst2):
    for a in lst2:
        lst1=exclude_append(lst1,a)
    return lst1


# toolz.itertoolz.unique
'''def unique(lst):
    newlst=[]
    for a in lst:
        exclude_append(newlst,a)
    return newlst'''


def move(lst, j, k):
    # move j-th element to position k
    moved = lst[j]
    del self[j]
    lst.insert(k, moved)


def shift(lst, k=1):
    # shift a list k times right (left when k<0)
    L = len(lst)
    if L<=1 or k==0:
        return lst
    kk = k%L
    return lst[-kk:]+lst[:-kk]


# bool-valued functions about lists
def allx(lst, key=lambda x: x != 0):
    '''all elements in lst make key(x) = true
    example:
    allx(['1','2','3'],lambda x:isinstance(x,str))
    '''
    return all(map(key, lst))


def anyx(lst, key=lambda x: x != 0):
    '''at least one of the elements in lst make key(x) = true
    '''
    return any(map(key,lst))


def allin(lst, S):
    return allx(lst, lambda x: x in S)


def anyin(lst, S):
    return anyx(lst, lambda x: x in S)


def allbe(lst, typ):
    return allx(lst, lambda x: isinstance(x,typ))


def anybe(lst, typ):
    return anyx(lst, lambda x: isinstance(x,typ))


def alleq(lst, val=1):
    return allx(lst, lambda x: x == val)


def anyeq(lst, val=1):
    return anyx(lst, lambda x: x == val)

def allsame(lst, val=1):
    if lst == []:
        return True
    return alleq(lst, lst[0])

def isunique(lst, val=1):
    # set-like, each element in lst is unique
    if lst == []:
        return True
    for k, a in enumerate(lst[:-1]):
        for b in lst[k+1:]:
            if a == b:
                return False
    return True

# counting
def count(lst):
    '''
>>> count([1,2,3,1,2])
{1: 2, 2: 2, 3: 1}
'''
    d={}
    for a in lst:
        if a in d:
            d[a]+=1
        else:
            d[a]=1
    return d

def countx(lst, order=2):
    # extension of count
    d={}
    L=len(lst)  # L>=order>=1
    for k in range(L-order+1):
        a=tuple(lst[k:k+order])
        if a in d:
            d[a]+=1
        else:
            d[a]=1
    return d

def inversion(lst):
    L = len(lst)
    n = 0
    for k in range(L-1):
        for l in range(k+1, L):
            if lst[k] > lst[l]:
                n += 1
    return n

# operate a list as a set
def listminus(lst,*lsts):
    '''listminus works like setminus
'''
    if lsts==():
        return lst
    elif lst==[]:
        return []
    else:
        lst0=[]
        for a in lst:
            if a not in lsts[0]:
                lst0.append(a)
        lst=listminus(lst0,*lsts[1:])
        return lst


def partition(lst, key=None, rel=lambda x, y: x==y):
    # rel is an equivalent relation
    if lst == []:
        return []
    elif len(lst) == 1:
        return [lst]
    if key:
        sim = lambda x, y: key(x) == key(y)
    #~ if rel: key = lambda x: {a for a in lst if rel(x, a)}
    p = [[lst[0]]]
    for a in lst[1:]:
        for cls in p:
            if rel(a, cls[0]):
                cls.add(a)
                break
        else:
            p.append([a])
    return p


def union(lst):
    if lst==[]:
        return []
    u=lst[0]
    for a in lst[1:]:
        u+=a
    return u


def sort_rel(lst, **kw):
    return union(partition(lst, **kw))


# relation: list (set) of tuples
def isrel(lst):
    return allbe(lst,(tuple,list))

def isreln(lst,n=2):
    return allx(lst,(tuple,list)) and alleq([len(a) for a in lst], n)

def rel2dict(lst, k=-1):
    dct={}
    for a in lst:
        b, c=a[:k], a[k:]
        if len(b)==1:
            b=b[0]
        if len(c)==1:
            c=c[0]
        dct.setdefault(b,[]).append(c)
        #x=dct.get(b,[]);x.append(c);dct.update({b:x})
    return dct

def rel22dict(lst):
    dct = {}
    for a in lst:
        b, c = a[0], a[1]
        dct.setdefault(b,[]).append(c)
    return dct

def dict2rel2(dct):
    lst=[]
    for a, bs in dct.items():
        lst.extend([(a, b) for b in bs])
    return lst

'''
def dict2rel(d):
     return [(key, value) for key, value in d.items()]
'''

# others
def repeatby(lst, nums):
    '''
>>> repeatby([1,2,3], [3,2,5,3])
[1, 1, 1, 2, 2, 3, 3, 3, 3, 3, 1, 1, 1]
'''
    new = []
    l = len(lst)
    for k, n in enumerate(nums):
        if l > k:
            new.extend([lst[k]]*n)
        else:
            new.extend([lst[k%l]]*n)
    return new


def search(lst, x, rate=0.5):
    # len(lst) >= 2 and elements in lst are increasing
    # rate is near o.5
    L = len(lst) - 1
    if L == 0:
        return lst[0], 0
    r = round(L*rate)
    a = lst[r]
    b = lst[r+1]
    m = (b+a) / 2
    if a <= x < m:
        return a, r
    elif m <= x <= b:
        return b, r+1
    elif x < a:
        return search(lst[0:r+1], x, rate)
    else: # x > b
        a, R = search(lst[r+1:], x, rate)
        return a, R+r+1

def comb(string, N=1):
    '''comb('string',2)
    itertools.product
    ['ss', 'st', 'sr', ... , 'gg']
    '''
    if N==1:
        return list(string)
    L=[]
    for a in string:
        for s in comb(string,N-1):
            L.append(a+s)
    return L

def indexes(lst, x):
    '''find the all indexes of x in lst
    example:
    >>> lst=list('www.baidu.com')
    >>> x='.'
    >>> indexes(lst,x)
    [3, 9]
    '''
    try:
        y = lst.index(x)
    except:
        return []
    ind = [y]
    lst = lst[y+1:]
    while x in lst:
        y0 = lst.index(x)
        y = y+1+y0
        ind.append(y)               
        lst = lst[y0+1:]
    return ind


# UserList
import collections
class myList(collections.UserList):

    def __init__(self,lst=[]):
        super(myList, self).__init__(lst)

    def __getitem__(self,ind):
        if isinstance(ind, (tuple,list)):
            return myList(self.data[k] for k in ind)
        elif isinstance(ind,int):
            return self.data[ind]
        else:
            print('indices must be int, list or tuple')

    def insert(self, ind, elm):
        if ind>=0:
            super(myList, self).insert(ind, elm)
        elif ind<-1:
            super(myList, self).insert(ind+1, elm)
        else: # ind==-1
            self.append(elm)

    def isempty(self):
        return self.data == []

    def move(self, j, k):
        moved = self[j]
        del self[j]
        self.insert(k, moved)

    def max(self, key=lambda x:x, default=0):
        if self.isempty():
            return default
        x = self[0]
        y = key(x)
        ind = [0]
        xs=[x]
        for k, x in enumerate(self.data):
            z = key(x)
            if y < z:
                ind = [k]
                y = z
                xs = [x]
            elif y == z:
                ind.append(k)
                xs.append(x)
        return ind, xs, y

    def treeprint(self):
        treeprint(self.data)

    def apply(self, fun, *args, **kw):
        return fun(self.data, *args, **kw)

    def list2list(self, fun, *args,**kw):
        self.data = fun(self.data, *args,**kw)

    def match(self, pattern, flag=0):
        if isinstance(pattern, str):
            pattern = re.compile(pattern, flag)
        return pattern.match(self.data)

if __name__ == "__main__":
    print(inversion('1534726'))