#!/usr/bin/env python
# coding: utf-8

import os
import gc
import joblib
import sqlite3
import numpy as np
import pandas as pd

from sklearn.preprocessing import MinMaxScaler

pd.set_option('precision', 4)
pd.set_option('display.max_columns', None)
pd.set_option('display.width', 5000)
np.set_printoptions(precision = 4, suppress = True, linewidth = np.inf)

def run(db_name, table_name, load_model):
    
    conn = sqlite3.connect('{}arduino_sensor.db'.format(db_name))
    conn.commit()
    
    # 先抓最新時間的 Limit 4 筆資料，後續改善成使用搜尋id的指令
    sqlDF = pd.read_sql("select * from {} ORDER BY timestamp_2 DESC LIMIT 10".format(table_name), conn)    
    sqlDF = sqlDF.set_index(pd.DatetimeIndex(sqlDF['timestamp_2']))
    sqlDF = sqlDF.drop(columns = ['id', 'timestamp_1', 'timestamp_2']).astype(float)
    #print(sqlDF)
    
    timeSample = '5min'        
    sqlDF = sqlDF.resample(rule = timeSample).mean()
    sqlDF = sqlDF.dropna() #去掉沒有收到資料的時間(NA)        
    #print(sqlDF)
    
    df_columns = sqlDF.columns
    #print('load average of last 10 records (5-mins) in DB:\n{}'.format(sqlDF))     
    infer_input = sqlDF.values    
    normalized_min = 0
    normalized_max = 1    
    
    # train data and test data do preprocessing.MinMaxScaler, respectivaly
    infer_input_scaler = MinMaxScaler(feature_range = (normalized_min, normalized_max)) #正規化到 0~1 範圍
    infer_input_scaler.fit(infer_input)
    infer_input_scaled = infer_input_scaler.transform(infer_input)
        
    pred = load_model.predict(infer_input_scaled)[-1]
    
    gc.collect()    
    return pred
    
if __name__ == "__main__":    
    
    db_name = '0823'
    table_name = 'arduino_sensor'
    model_name = 'svm_model'
    load_model = joblib.load(model_name)
    
    pred_class = run(db_name, table_name, load_model)
    if (pred_class==0):
        print('normal power enent')
        ##print('[pred_class]:{} [system-power-statud]:{}'.format(pred_class, 'solar_energy_normal'))
    else:        
        print('[pred_class]:{} [system-power-statud]:{}'.format(pred_class, 'solar_energy_abnormal'))