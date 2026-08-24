import pandas as pd
import numpy as np

#1.加载商户交易原始数据
df = pd.read_csv("商户交易明细.csv")
print(f"原始数据量:{len(df)}行")

#2.数据清洗:去重、补缺失、过滤无效交易
df = df.drop_duplicates(subset="交易ID")
df["商家实收"]= df["商家实收"].fillna(df["交易金额"]*0.7)
df_valid = df[df["交易状态"]=="有效"]

#3.特征计算:衍生业务指标
df_valid["客均金额"]= df_valid["交易金额"]/ df_valid["消费人数"]
df_valid["补贴率"] = (df_valid["渠道补贴"]+ df_valid["商户补贴"])/ df_valid["交易金额"]
         
#4.商户维度聚合统计
shop_stats = df_valid.groupby("商户名称").agg(
    交易量=("交易ID","count"),
    总交易金额=("交易金额","sum"),
    实收金额=("商家实收","sum"),
    平均客均金额=("客均金额","mean")
).round(2).sort_values("总交易金额",ascending=False)
print(shop_stats.head())