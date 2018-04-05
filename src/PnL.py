from flask import Flask, make_response, request, current_app
from flask_cors import CORS
from flask import json, jsonify
from base import conn, engine, session
from datetime import date, datetime
from sqlalchemy import Column, Integer, DateTime, Date
from scipy import stats
import pandas as pd




#
# PathC = "/Users/rachelmei/Documents/WaterIslandCapital/src/data/FILES C/"



# def uploadTradingPnL():
#     result = pd.read_csv(PathC + "Trading.csv")
#
#     result['Date'] = pd.to_datetime(result['Date'], format="%m/%d/%Y")
#     result['Date'] = result['Date'].reindex(pd.date_range(result['Date'].index[0], result['Date'].index[-1], freq='D'));
#
#
#     sLength = len(result['Date'])
#     result['PnL'] = pd.Series(getPnL(), index=result.index)
#     result['AccountBalance'] = pd.Series(getBalance(), index=result.index)
#
#     print("done trading")
#     with engine.connect() as conn, conn.begin():
#         result.to_sql('Trading', conn, if_exists='replace', dtype={"Date": DateTime})
#
#
#
# def getPnL():
#     data = pd.read_sql('SELECT Date, Ticker, Action, Quantity, Price FROM Trading ', conn)
#
#     df = pd.DataFrame(data.fetchall())
#     df.columns = data.keys()
#     print(df)
#
#
#
#
# def getBalance():
#
#
#
#


#
# data = []
# with open(file) as f:
#     for row in csv.DictReader(f):
#         data.append(row)
#





#
# trade = json.load(pd.read_csv(file))
# df = pd.DataFrame(trade, columns=['Index', 'Date', 'Ticker', 'Action', 'Quantity', 'Price'])
#
#
# print(df)
#
# def ProfitAndLoss(df):
#
#     df = df.copy()
#     df = df.reset_index()
#     for index,row in df.iterrows():
#         if index == 0:
#             continue
#         if row['WinLoss'] == "NoTrade":
#             df['AccountBalance'][index] = df['AccountBalance'][index-1]
#
#         elif row['WinLoss'] in ["Win", "Loss"]:
#             df['AccountBalance'][index] = df['AccountBalance'][index-1] *  (1 + df['ProfitAndLossPofChg'][index])
#
#     return df
#
# print(ProfitAndLoss(df).set_index('D'))

if __name__ == '__main__':


    PathC = "/Users/rachelmei/Documents/WaterIslandCapital/src/data/FILES C/"
    result = pd.read_csv(PathC + "Trading.csv")

    result['Date'] = pd.to_datetime(result['Date'], format="%m/%d/%Y")
    # result['Date'] = result['Date'].reindex(pd.date_range(result['Date'] freq='D'));
    print(result['Date'])
