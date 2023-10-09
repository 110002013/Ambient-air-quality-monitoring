# Ambient-air-quality-monitoring
# 研究背景/動機
- 火力發電為臺灣最主要的電力來源。  
- 溫室氣體中二氧化碳(CO2)約占95.28%,其中 90.13%來自於能源燃料燃燒。  
- 二氧化碳(CO2)為造成空氣汙染與溫室效應之主要因素。   
- 提出以太陽能作為主要供電能源之微型空品感測器系統。  

### Q : 再生能源是否會有供電不穩定的問題 ? 供電異常資料集不平衡怎麼辦 ?  
本組利用SMOTE改善資料不平衡的問題,再使用SVM分類演算法,偵測系統是否有供電異常的情形。


# 實驗方法
#### Publisher
- PM2.5感測器
- 溫溼度感測器
- 太陽能轉換板
- 太陽光感測器
- 電壓電流感測器
- 二氧化碳感測器

#### Broker
- 溫度TEM  
- 溼度HUM
- 二氧化碳CO2
- 懸浮微粒PM2.5  
- 可見光VIS
- 紅外光IR
- 紫外光UV
- 系統耗電功率TPC
- 太陽能總電壓SPV

#### Subscriber
- Raspberry Pi 4  
- 網頁平台  
- 資料庫

#### 輸入特徵 :  
溫度、溼度、二氧化碳、懸浮微粒、可見光、紅外光、紫外光、系統耗電功率、太陽能總電壓

#### 輸出 : 1 ( 異常事件 ) 、0 ( 正常事件 )
$\Rightarrow$ MQTT  傳輸資料至Raspberry Pi 4 ( Database )  
$\Rightarrow$ SMOTE  解決不平衡數據集  
$\Rightarrow$ SVM  偵測系統供電情形是否有異常事件  
$\Rightarrow$ Node - RED  結果於網頁平台呈現  

# 結論
研究結果顯示透過 SMOTE 進行資料前處理,並使用Polynomial SVM進行分類之分類性能較好。

# 資料庫
![image](https://github.com/110002013/Ambient-air-quality-monitoring/assets/93826901/c0af0f6d-fdd8-47da-bb86-c7d899761bfa)

# 網頁呈現
#### 即時感測資料
<img width="898" alt="image" src="https://github.com/110002013/Ambient-air-quality-monitoring/assets/93826901/9c5ea3cf-9823-49af-9a84-3cb536a3d1d9">

#### 歷史感測資料
<img width="149" alt="image" src="https://github.com/110002013/Ambient-air-quality-monitoring/assets/93826901/6a42de30-21d2-48a1-8fc4-e48b47d8e968">  




