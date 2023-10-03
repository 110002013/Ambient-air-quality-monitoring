#!/usr/bin/env python3
# coding: utf-8
import gc
import json# 引入json庫
import time# 引入時間
from datetime import datetime
from sqlalchemy import create_engine, MetaData# 引入sqlalchemy中相關模組
from sqlalchemy import Column, Integer, String, Table
from sqlalchemy.ext.declarative import declarative_base

# 連接資料庫(有會自動忽略,無會自動創建)
engine = create_engine('sqlite:///0823arduino_sensor.db', echo = True)
# 基本類
Base = declarative_base()
#test_topic:b'"temp":25.50,"humi":61.00,"co2":400,"vis":271,"ir":331,"uv":0,"all_power":144.20,"vol":3.15'

class arduino_sensor(Base):
    # 表的名字
    __tablename__ = 'arduino_sensor'
    
    # 定義各欄位
    id = Column(Integer, primary_key = True)
    
    temp = Column(String(3))        # 濕度
    humi = Column(String(3))        # 溫度
    co2 = Column(String(3))         # co2(SGP30)
    vis = Column(String(3))         # sunlight
    ir = Column(String(3))
    uv = Column(String(3))
    all_power = Column(String(10))    # 總電功率
    vol = Column(String(10))        # 電壓
    timestamp = Column(String(10))  # 時間戳記

    def __str__(self):
        return self.id

def Handler(data_in):

    # 創建表(有表會自動忽略,無表會自動創建)
    Base.metadata.create_all(engine)
    # 綁定引擎
    metadata = MetaData(engine)
    # 連接資料表
    arduino_sensor_table = Table('arduino_sensor', metadata, autoload = True)
    # 創建 insert 對象
    ins = arduino_sensor_table.insert()
    
    
    timeout = 10
    wait_count = 0
    time.sleep(timeout)
    # 把拿到的資料轉為字串(串口接收到的資料為bytes字串類型,需要轉碼字串類型)
    #print(data_in)
    #print(type(data_in))
    strJson = str(data_in, encoding = 'utf-8')
    #print(strJson)
    # 如果有資料,則進行json轉換
    if strJson:
        # 只有當檢測到字串中含有溫濕度字元名時才進行json轉碼,其他的字串內容不作操作        
        strJson = "{" + strJson + "}"
        print("[strJson]:{}".format(strJson))
       
        if "temp" in strJson:                 
            # 字串轉為json(每個字串變數名必須為雙引號包括,而不是單引號)
            jsonData = json.loads(strJson)                
            print("轉碼成功,當前類型為->", type(jsonData))
            
            temp = jsonData["temp"]
            humi = jsonData["humi"]
            co2 = jsonData["co2"]
            vis = jsonData["vis"]
            ir = jsonData["ir"]
            uv = jsonData["uv"]
            all_power = jsonData["all_power"]
            vol = jsonData["vol"]
        
            # 亂碼 -> 時間戳記
            # timestamp = str(int(round(time.time() * 1000)))
            
            # 時間戳記
            # datetime object containing current date and time
            now = datetime.now()
            # dd/mm/YY H:M:S
            zoneTime = int(now.strftime("%S"))
            
            if zoneTime < timeout or zoneTime ==0:
                timestamp = now.strftime("%Y/%m/%d %H:%M:00")
            elif zoneTime < 2*timeout or zoneTime ==timeout:
                timestamp = now.strftime("%Y/%m/%d %H:%M:10")
            elif zoneTime < 3*timeout or zoneTime == 2*timeout:
                timestamp = now.strftime("%Y/%m/%d %H:%M:20")
            elif zoneTime < 4*timeout or zoneTime == 3*timeout:
                timestamp = now.strftime("%Y/%m/%d %H:%M:30")
            elif zoneTime < 5*timeout or zoneTime ==4*timeout:
                timestamp = now.strftime("%Y/%m/%d %H:%M:40")   
            else:
                timestamp = now.strftime("%Y/%m/%d %H:%M:50") 
      
            # 綁定要插入的資料
            ins = ins.values( 
              humi = humi, 
              temp = temp, 
              co2 = co2, 
              vis = vis, 
              ir = ir, 
              uv = uv, 
              all_power = all_power,
              vol = vol,
              timestamp = timestamp)
              
            # 連接引擎
            conn = engine.connect()
            # 執行語句
            result = conn.execute(ins)
            #執行 close 釋放 SQLite
            #conn.close()
        else:
            wait_count = wait_count + 1 
            print("[subscriber 等待資料的時間]: {} seconds".format(wait_count * 5))
    
    #執行 close 釋放 SQLite
    #engine.dispose()
    #釋放記憶體
    gc.collect()
   
#===============================================================
# Master Function to Select DB Funtion based on MQTT Topic

def sensor_Data_Handler(Topic, data_in):
   
   if Topic == "test_topic":
        print(data_in)
        Handler(data_in)

#===============================================================
