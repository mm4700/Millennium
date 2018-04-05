from flask import Flask, make_response, request, current_app
from flask_cors import CORS
from flask import json, jsonify
from base import conn, engine, session
from datetime import date, datetime
from sqlalchemy import Column, Integer, DateTime, Date
from scipy import stats
import pandas as pd

app = Flask(__name__)
CORS(app)

PathA = "/Users/rachelmei/Documents/WaterIslandCapital/src/data/FILES A/"
PathB = "/Users/rachelmei/Documents/WaterIslandCapital/src/data/FILES B/"
PathC = "/Users/rachelmei/Documents/WaterIslandCapital/src/data/FILES C/"




@app.route('/uploadCsv', methods = ['POST'])
def uploadCsv():
    res = []
    tick = request.json["firm"]
    for record in request.json["data"]:
        res.append((datetime.strptime(record["Date"], "%m/%d/%y").date(), tick, record["PX_LAST"], record["PX_VOLUME"]))

    try:
        conn.commit()
    except:
        conn.rollback()

    return "JSON Message: " + json.dumps(request.json)

@app.route('/resetAll', methods= ['PUT'])
def reset():
    print("reset")
    session.execute('''TRUNCATE TABLE MarketData''')
    session.execute('''TRUNCATE TABLE CompanyOverview''')
    session.execute('''TRUNCATE TABLE Trading''')
    session.commit()
    session.close()
    return "Success"

@app.route('/uploadAll', methods = ['PUT'])
def uploadAll():
    print("upload")
    uploadDescription()
    uploadEquity()
    uploadTrading()
    return "Success"

def uploadEquity():
    firmList = getFirmList()
    frames = []

    for firm in firmList:
        ticker = firm
        csv = PathA + ticker + ".csv"
        df = pd.read_csv(csv)
        df['Ticker'] = ticker
        frames.append(df)

    result = pd.concat(frames)
    result['Date'] = pd.to_datetime(result['Date'], format="%m/%d/%Y")
    print("done equity")
    with engine.connect() as conn, conn.begin():
        result.to_sql('MarketData', conn, if_exists='replace', dtype={"Date": DateTime})

def uploadDescription():
    result = pd.read_csv(PathB + "Description.csv")
    result['Ticker'] = result['Ticker'].apply(lambda x: x.split(" ")[0])
    print("done des")
    with engine.connect() as conn, conn.begin():
        result.to_sql('CompanyOverview', conn, if_exists='replace')


# def uploadTrading():
#     result = pd.read_csv(PathC + "Trading.csv")
#     result['Date'] = pd.to_datetime(result['Date'], format="%m/%d/%Y")
#     sLength = len(result['Date'])
#     result['PnL'] = pd.Series(0, index=result.index)
#     result['AccountBalance'] = pd.Series(0, index=result.index)
#
#     print("done trading")
#     with engine.connect() as conn, conn.begin():
#         result.to_sql('Trading', conn, if_exists='replace', dtype={"Date": DateTime})


def uploadTrading():
    result = pd.read_csv(PathC + "Trading.csv")
    result['Date'] = pd.to_datetime(result['Date'], format="%m/%d/%Y")

    print("done trading")
    with engine.connect() as conn, conn.begin():
        result.to_sql('Trading', conn, if_exists='replace', dtype={"Date": DateTime})


def getFirmList():
    data = pd.read_sql('SELECT Ticker FROM CompanyOverview', conn)
    return [x.split(" ")[0] for x in data['Ticker'].tolist()]

@app.route('/getFirms', methods = ['GET'])
def getFirms():
    firms = {
        'firms': getFirmList()
    }

    return jsonify(firms)

@app.route('/firm_overview/<firm>', methods = ['GET'])
def getOverView(firm):

    df = pd.read_sql("SELECT * FROM CompanyOverview where Ticker = \"%s\"" %firm, conn)
    data = {
        'overview': df.to_json(orient='records')

    }
    return jsonify(data)


@app.route('/stats', methods = ['POST'])
def pairStats():
    form = request.form.to_dict()
    tick1 = form['ticker1'].split(" ")[0]
    tick2 = form['ticker2'].split(" ")[0]

    df = pd.read_sql('SELECT * FROM MarketData', conn)

    a = df[df['Ticker'] == tick1]['PX_LAST'].tolist()
    b = df[df['Ticker'] == tick2]['PX_LAST'].tolist()

    slope, intercept, r_value, p_value, std_err = stats.linregress(a, b)
    corr = stats.pearsonr(a, b)[0]
    beta = slope

    data = {
        'corr' : corr,
        'beta' : beta
    }

    return jsonify(data)

@app.route('/timeseries/<firm>')
def getTS(firm):
    df = pd.read_sql("SELECT * FROM MarketData where Ticker= \"%s\"" %firm, conn)
    data = {
        'ts': df.to_json(orient='records')
    }
    return jsonify(data)



@app.route('/add_portfolio', methods = ['POST'])
def addPortfolio():
    form = request.form.to_dict()
    data = json.loads(form["jf"])
    weights = data["weights"]
    ids = data["ids"]
    d = {'Ticker': ids, 'Weight': weights}
    df = pd.DataFrame(data=d)
    df.to_sql('Portfolio', conn, if_exists='replace')
    return jsonify(data)




if __name__ == '__main__':

    # pairStats()
    # data = pd.read_sql('SELECT * FROM MarketData', conn)
    # df.to_sql(con=conn, name='CompanyOverview', if_exists='replace', flavor='mysql')
    #
    # with engine.connect() as conn, conn.begin():
    #     df.to_sql('CompanyOverview', conn, if_exists='replace')

    # print(list(df))

    app.run(host="localhost", port=5000,  threaded=True)


    # uploadAll()
    # reset()
    # uploadDescription()