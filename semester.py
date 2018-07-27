# -*- coding: utf-8 -*-

# calcute the semester according to the date

from datetime import date

today = date.today()
datelist = [today.year, today.month, today.day]


def semester():
    tlist = datelist
    if 3 < tlist[1] < 9:
        s = 2
    else:
        s = 1
    if tlist[1] < 9:
        y = tlist[0]
    else:
        y = tlist[0] + 1
    return s, y

class Semester(object):
    ''' Semester class
    propteries
    year: year
    spring_fall: spring (2) or fall (1) semester
    '''
    def __init__(self, year=None, spring_fall=None):
        if year and spring_fall:
            self.year = year
            self.spring_fall = spring_fall
        else:
            self.spring_fall, self.year = semester()

    def __str__(self):
        return "%d/%d %d"%self.toTuple()

    def toChinese(self):
        return "第 %d/%d 学年第 %d 学期"%self.toTuple()

    def totex(self):
        return "第 %d/%d 学年\\\\第 %d 学期"%self.toTuple()

    def toTuple(self):
        return (self.year-1, self.year, self.spring_fall)

    @property
    def chinese(self):
        return self.toChinese()

