# -*- coding: utf-8 -*-
# description for predict

import numpy as np

import pandas as pd
# from sklearn.model_selection import train_test_split
from neupy import algorithms, estimators, environment, storage

import pytseries
from statsmodels.tsa import stattools


class Predictor(object):
    '''Predictor: a wrapper of predicting model
    name: name
    model: model'''
    def __init__(self, name='predictor', model=None):
        self.name = name
        self.model = model

    def __getstate__(self): 
        return (self.name, self.model)
        
    def __setstate__(self, state):
        self.name, self.model = state

    def __call__(self, data):
        # input -> output
        return self.model.predict(data)


class ANNPredictor(Predictor):
    '''ANN Predictor
    model: ann
    step: array
    '''
    def __init__(self, name='predictor', model=None, step=2):
        super(ANNPredictor, self).__init__(name='predictor', model=model)
        self.step = step

    def get_step(self):
        d = pd.Series(data).diff()
        acf = stattools.pacf(d.fillna(0), nlags=200)
        return np.array([k for k, a in enumerate(acf) if k>0 and 0.3>a>0.11])

    @classmethod
    def fromTimeSeries(cls, ts, model, step, back=None):
        '''train a predictor from
        ts: Time Series
        model: ann or ts model'''
        datax, datat = cls.generate_data(ts, step)
        if back is None:       
            model.train(datax, datat)
        else:
            model.train(datax[:-back], datat[:-back])
        annp = ANNPredictor(model=model, step=step)
        annp.datax = datax
        annp.datat = datat
        annp.datay = annp(datax)
        return annp

    @classmethod
    def fromNDTimeSeries(cls, ndts, model, step, back=None):
        '''train a predictor from
        df: n dim-Time Series
        model: ann or ts model
        '''

        datax, datat = cls.generate_data(ndts, step)
        if back is None:
            model.train(datax, datat)
        else:
            model.train(datax[:-back], datat[:-back])
        annp = ANNPredictor(model=model, step=step)
        annp.datax = datax
        annp.datat = datat
        annp.datay = annp(datax)
        return annp

    @classmethod
    def fromDataFrame(cls, df, model, step, back=None):

        datax, datat = cls.generate_data(df, step)
        if back is None:
            cls.train(model, datax, datat)
        else:
            model.train(datax[:-back], datat[:-back])
        annp = ANNPredictor(model=model, step=step)
        annp.datax = datax
        annp.datat = datat
        annp.datay = annp(datax)
        return annp

    def get_error(self, ts, h=1):
        pass

    def predict(self, ts, n=20, back=0):
        '''ts: time series
        n: the number of predictions
        back: from when'''
        ts = ts.values
        if isinstance(self.step, int):
            if back == 0:
                a = ts[-self.step:]
                a = a.ravel()
                data0 = a[np.newaxis,:]
            else:
                data0 = ts[-self.step-back:-back][np.newaxis,:]
            ys = self(data0)
            y = ys.copy()
            for _ in range(n+back-1):
                data0 = np.hstack((data0[:,1:], y))
                y = self(data0)
                ys = np.vstack((ys, y))
        else:
            stepmax = np.max(self.step)
            if back == 0:
                data0 = ts[-stepmax:][np.newaxis,:]
            else:
                data0 = ts[-stepmax-back:-back][np.newaxis,:]
            index = [stepmax - a for a in self.step]
            ys = self(data0[:, index])
            y = ys.copy()
            for _ in range(n+back-1):
                data0 = np.hstack((data0[:,1:], y))
                y = self(data0[:,index])
                ys = np.vstack((ys, y))
        return ys

    def ndpredict(self, ndts, n=20, back=0):
        '''ndts: time series
        n: the number of predictions
        back: from when'''
        ts = ndts.values
        if isinstance(self.step, int):
            if back == 0:
                a = ts[-self.step:]
                data0 = a.ravel()[np.newaxis,:]
            else:
                a = ts[-self.step-back:-back]
                data0 = a.ravel()[np.newaxis,:]
            ys = self(data0)
            y = ys.copy()
            for _ in range(n+back-1):
                a = np.vstack((a[1:, :], y))
                data0 = a.ravel()[np.newaxis,:]
                y = self(data0)
                ys = np.vstack((ys, y))
        else:
            stepmax = np.max(self.step)
            if back == 0:
                a = ts[-self.step:]
                a = a.ravel()
                data0 = a[np.newaxis,:]
            else:
                a = ts[-stepmax-back:-back]
                a = a.ravel()
                data0 = a[np.newaxis,:]
            index = [stepmax - a for a in self.step]
            ys = self(data0[:, index])
            y = ys.copy()
            for _ in range(n+back-1):
                data0 = np.hstack((data0[:,1:], y))
                y = self(data0[:,index])
                ys = np.vstack((ys, y))
        return ys
    
    @staticmethod
    def generate_data(ts, step):
        return ts.generate_Xy(step=step, style='row')

    @staticmethod
    def train(model, datax, datat):
        return model.train(datax, datat)



