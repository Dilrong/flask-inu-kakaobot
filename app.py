import os
import re
import ssl
from flask import Flask, request, jsonify
from urllib.request import urlopen
from urllib.parse import quote
from bs4 import BeautifulSoup

app = Flask(__name__)


@app.route("/")
def hello():
    return "INU Haksan kakao bot! with flask"


@app.route("/keyboard")
def Keyboard():
    dataSend = {
        "type": "buttons",
        "buttons": ["도서검색"]
    }

    return jsonify(dataSend)


@app.route('/message', methods=['POST'])
def Message():
    book=''
    keyword = quote("파이썬")
    try:
        context = ssl._create_unverified_context()
        html = urlopen("https://lib.inu.ac.kr/search/tot/result?st=KWRD&si=TOTAL&q=" + keyword + "&briefType=T",
                       context=context)
        bsObj = BeautifulSoup(html, "html.parser")
    except AttributeError as e:
        return None
    
    result = []
    table = bsObj.find("table", {"id": "briefTable"})
    table_body = table.find("tbody")
    rows = table_body.findAll("tr")

    for row in rows:
        cols = row.findAll('td')
        cols = [ele.text.strip() for ele in cols]
        result.append([ele for ele in cols if ele])

    for data in result:
        if len(data) == 6:
            titles = re.sub('&nbsp;|\t|\r|\n|\xa0', '', data[1])

            # if len(titles.split('학산도서관 ')) == 2:
            #     data_list = {
            #         'title': titles.splite('학산도서관 ')[0],
            #         'author': data[2],
            #         'publisher': data[3],
            #         'place': data[4],
            #         'year': data[5],
            #         'state': titles.split('학산도서관 ')[1]
            #     }
            book = str(data)
    
    dataReceive = request.get_json()
    content = dataReceive['content']
    
    if content == u"test1":
        dataSend = {
            "message": {
                "text": book
            }
        }
    return jsonify(dataSend)


if __name__ == "__main__":
    # app.run(host='0.0.0.0', port=5000, debug=True)
    app.run(debug=True)
