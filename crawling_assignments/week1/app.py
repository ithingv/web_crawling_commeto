from ssl import _PasswordType
from flask import Flask, jsonify
import os
from crawler import crawler

app = Flask(__name__)
url = "https://www.daangn.com/hot_articles"

# 로컬서버(브라우저) <-> 당근서버
@app.route('/', methods=['GET',''])
def home():
    
    # 중고마켓 컨텐츠 목록
    contents = crawler(url)
    return jsonify(contents)

if __name__ == "__main__":
    os.system("./run_sever.sh")