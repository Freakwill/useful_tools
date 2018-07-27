# -*- coding: utf-8 -*-
'''
string operation
'''

import re

'''notation:
b: bracket brace
dct: dictionary
lst: list
s: string
ch: charactor
rx: regular expression
'''

# string

def split2(s, ch1='.',ch2=','):
    '''double split
>>> split2('hello,world.I love you forever, my python')
[['hello', 'world'], ['I love you forever', ' my python']]
'''
    lst=s.split(ch1)
    return [_.split(ch2) for _ in lst]


def endadd(s, ch='.'):
    # add ch at the end of s
    if not s.endswith(ch):
        s += ch
    return s


def searchcb(s, b='{}'):
    '''search close brace ignoring a complete brace
'''
    left, right = b
    flag = 0
    for k, a in enumerate(s):
        if a == left:
            flag += 1
        elif a == right:
            if flag == 0:
                return k
            flag -= 1
    return None

def findbrace(s, b='{}'):
    '''find the content in braces
>>> findbrace('aaa{bbb{ccc}ddd}eee{fff}')
['{bbb{ccc}ddd}', '{fff}']
'''
    left,right=b
    flag=0
    lst=[]
    for k,a in enumerate(s):
        if a==left:
            flag+=1
            if flag==1:  # first {
                L=k
        elif a==right:
            if flag==1:  # last }
                lst.append(s[L:k+1])
            flag-=1
    return lst


def caesar(s, n):
    newstr=''
    for a in s:
        if a.isalpha():
            if 97<=ord(a)<=122:
                b=chr((ord(a)+n-97)%26+97)
            elif 65<=ord(a)<=90:
                b=chr((ord(a)+n-65)%26+65)
            newstr+=b
        else:
            newstr+=a
    return newstr

# regular expression
IDEN = '[a-zA-Z_]\w*'
IDENX = '{0}(?:\.{0})*'.format(IDEN)
IDENS = '{0}(?:,{0})'.format(IDEN)
STR = '"([^"]|(?<!\\\\)(\\\\\\\\)*\\\\")*"|\'([^\']|(?<!\\\\)(\\\\\\\\)*\\\\\')*\''
RAW = 'r"[^"]*"|r\'[^\']*\''
DIGIT = '\d+'
ALPHA = '[a-zA-Z]'
WORD = ALPHA+'+'
PM = '\+|\-'
INT = '(\-|\+)?\d+'
NUM = '(?:\-|\+)?(?:\d*\.\d+|\d+)(?:[eE](?:\-|\+)?\d+)?'
CMP = '<=|==|>=|!=|<|>'
IN = 'in|not +in'
MATHOP = '\+|\-|\*|/|\*\*|//'
SHIFTOP = '<<|>>'
BINOP = '\||\^|&'
LOGOP = 'not|and|or'
ESC = '\\\\'
SLASH = '\\\\\\\\'
SLASHES = '(\\\\\\\\)+'
BLANK = '\s*'
TITLE = '[A-Z][a-z]*'
LIST = '\[.*\]'
TUPLE = '\(.*\)'
ENDWHITE = '[ \t]+(?=\n)|[ \n\t]+\Z'
CAMEL = '(?:[A-Z][a-z]*)(?:[A-Z][a-z]*)'


def or_(*pattern):
    return '('+')|('.join(pattern)+')'


def endwith(s, pattern, flags=0):
    # like endswith
    rx=re.compile('(?:'+pattern+')\Z',flags)
    if rx.search(s):
        return True
    else:
        return False

def beginwith(s,pattern,flags=0):
    # like startswith
    rx=re.compile('\A(?:'+pattern+')',flags)
    if rx.search(s):
        return True
    else:
        return False

def mymatch(pattern,string, flags=0):
    rx=re.compile('\A('+pattern+')\Z', flags)
    return rx.match(string)

def mymatchi(pattern,string):
    rx=re.compile('\A('+pattern+')\Z',re.IGNORECASE)
    return rx.match(string, flags)

def ismatched(pattern,string, flags=0):
    # more restrict matching method
    rx=re.compile('\A(?:'+pattern+')\Z', flags)
    if rx.search(string):
        return True
    else:
        return False

def isblank(s):
    # s is a blank string
    return ismatched('\s*',s)

def isname(name):
    '''recognize a name as F. Name
'''
    return ismatched('([A-Z]. ){1,2}[A-Z][a-z]+',name)


def istitle(title):
    return ismatched('[A-Z][a-z]*( ([A-Z][a-z]*|a|an|and|at|for|in|on|of|the|to))+',title)

def istitle_simple(title):
    return ismatched('[A-Z][a-z]*( [a-z]+)+',title)


def isvar(s):
    return ismatched(IDEN,s)

def isnum(s):
    return ismatched(NUM,s)

def isstr(s):
    return ismatched(STR,s)

def tagfind(string, tag='', left='<', right='>', flags=re.DOTALL):
    # find all tags in HTML
    rx=re.compile(left+'\s*'+tag+'.*?'+right, flags)
    return rx.findall(string)

def delrx(s, pattern, flags=0):
    # delete pattern in s
    #example: a=delrx('def  \ndef', ENDWHITE) deletes the whitespaces at the end of line
    rx=re.compile(pattern, flags)
    return rx.sub("",s)

def delvowel(s,flags=re.I):
    return delrx(s,r'[aeiou]',flags)

def shortset(s, N=3):
    '''
>>> shortset('expression')
{'xpr', 'x', 'expression', 'exp', 'e', 'xpression'}
>>> shortset('expression',4)
{'expr', 'xpre', 'x', 'xprs', 'expression', 'e', 'xpression'}
'''
    # N>=3 generally
    # each element in set is short for s or equal to s
    if 1<=len(s)<=N:
        return {s[0],s}
    elif len(s)>N:
        short=delvowel(s[1:])
        L=len(short)
        if L<=N-1:
            SL={s[0],s[0]+short,s[:N],s}
        else: # L>N
            SL={s[0],s[0]+short[:N-1],s[:N],s}
        if s.startswith('ex'):
            SL |= shortset(s[1:],N)
        return SL
    else:
        return {''}

def striprx(s,pattern1="\s",pattern2="\s",flags=0):
    # strip s with pattern1 and pattern2
    if pattern2==None:
        pattern2=pattern1
    return delrx(s,'\A('+pattern1+')+|('+pattern2+')+\Z')

def lstriprx(s,pattern="\s",flags=0):
    # lstrip s with pattern
    return delrx(s,'\A('+pattern+')+')

def rstriprx(s,pattern="\s",flags=0):
    # rstrip s with pattern
    return delrx(s,'('+pattern+')+\Z')

def mysub(s,pattern,repl):
    '''example:
>>> mysub('||x||=norm{x}_{xinX}','x','t')
'||t||=norm{t}_{xinX}'
'''
    rx=re.compile(r'\b'+pattern+r'\b')
    return rx.sub(repl,s)

def mysubx(s,patterns,repls):
    for k,pattern in enumerate(patterns):
        # s=mysub(s,pattern,repls[k])
        rx=re.compile(r'\b'+pattern+r'\b')
        s=rx.sub(repls[k],s)
    return s

def myfind(s,pattern=IDENX):
    rx=re.compile(r'\b('+pattern+r')\b')
    return set(rx.findall(s))

def between(pattern,left='<',right='>'):
    return re.compile('(?<=%s)'%left+pattern+'(?=%s)'%right)

def search_between(s,pattern,left='<',right='>'):
    rx=between(pattern,left,right)
    return rx.search(s)


# others

def ischinese(ch):
    return '\u4e00'<=ch<='\u9fa5'

def col(loc, s):
    return 1 if loc < len(s) and s[loc] == '\n' else loc - s.rfind("\n", 0, loc)   #

def lineno(loc, s):
    return s.count("\n", 0, loc) + 1

def line(loc, s):
    lastCR = s.rfind("\n", 0, loc)
    nextCR = s.find("\n", loc)
    if nextCR >= 0:
        return s[lastCR+1:nextCR]
    else:
        return s[lastCR+1:]


# user string object
import collections

def ind2iter(ind, N):
    # slice to range, int and list to list
    if isinstance(ind, list):
        return ind
    elif isinstance(ind, slice): # slc is a slice
        a=0 if ind.start is None else ind.start
        b=N if ind.stop is None else ind.stop # b <= N
        if ind.step is None:
            return range(a, b)
        else:
            return range(a, b, c)
    else:
        return [ind]

class myString(collections.UserString):

    def __init__(self,s=''):
        UserString.__init__(self,s)

    def __setitem__(self,key,val):
        if isinstance(key,int):
            newdata=''
            for k,a in enumerate(self.data):
                if k==key:
                    newdata+=val
                else:
                    newdata+=a
            self.data=newdata
        elif isinstance(key,(list,slice)):
            newdata=''
            if isinstance(val, str):
                for k,a in enumerate(self.data):
                    if k in key:
                        newdata+=val
                    else:
                        newdata+=a
                self.data=newdata
            else: # list of strings
                kk=0
                for k,a in enumerate(self.data):
                    if k in ind2iter(key,len(self)):
                        newdata+=val[kk]
                        kk+=1
                    else:
                        newdata+=a
                self.data=newdata

    def apply(self,fun, *args, **kwargs):
        return fun(self.data, *args, **kwargs)

    def str2str(self, fun, *args, **kwargs):
        self.data=fun(self.data, *args, **kwargs)
        return self

    def str2strx(self,*others,fun):
        self.data=fun(*((self.data,)+tuple(other.data if isinstance(other, myString) else str(other) for other in others)))
        return self


if __name__ == '__main__':

    rx = re.compile(NUM)
    m = rx.match('12.3')
    print(m.group())