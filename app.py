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
    data_send = {
        "type": "text"
    }

    return jsonify(data_send)


@app.route('/message', methods=['POST'])
def Message():
    book = ''
    userinput = 'nodejs'

    dataReceive = request.get_json()
    userinput = dataReceive['content']

    keyword = quote(userinput)
    try:
        context = ssl._create_unverified_context()
        html = urlopen("https://lib.inu.ac.kr/search/tot/result?st=KWRD&si=TOTAL&q=" + keyword + "&briefType=T",
                   context=context)
        bsObj = BeautifulSoup(html, "html.parser")
    except AttributeError as e:
        return None

    result = []
    table = bsObj.find("table", {"id": "briefTable"})
    if table is None:
        return internalError()
    table_body = table.find("tbody")
    rows = table_body.findAll("tr")

    for row in rows:
        cols = row.findAll('td')
        cols = [ele.text.strip() for ele in cols]
        result.append([ele for ele in cols if ele])

    for data in result:
        if len(data) == 6:
            titles = re.sub('&nbsp;|\t|\r|\n|\xa0', '', data[1])

            if len(titles.split('학산도서관 ')) == 2:
                book +=  titles.split('학산도서관 ')[0] + '\n' + '저자 : ' + data[2] + ' / 출판사 : ' + data[3]+ ' / ' + titles.split('학산도서관 ')[1] + '\n청구기호 : ' + data[4] + '\n\n'

        data_send = {
            "message": {
                "text": book
            }
        }
    return jsonify(data_send)

def internalError():
    data_send = {
        "message": {
            "text": "검색결과가 없습니다."
        }
    }
    return jsonify(data_send)

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000, debug=True)
