from flask import Flask, render_template, request, jsonify
from pymongo import MongoClient
client = MongoClient('mongodb+srv://test:sparta@cluster0.87wks.mongodb.net/Cluster0?retryWrites=true&w=majority')
db = client.dbsparta
app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/guestbook')
def guestbook():
    return render_template('guestbook.html')

@app.route('/room1')
def room1():
    return render_template('room1.html')


@app.route("/homework", methods=["POST"])
def homework_post():
    nickname_receive = request.form['nickname_give']
    comment_receive = request.form['comment_give']

    doc = {'nickname': nickname_receive, 'comment': comment_receive}
    db.guest_book.insert_one(doc)
    return jsonify({'msg':'응원 완료!'})

@app.route("/homework", methods=["GET"])
def homework_get():
    guest_list = list(db.guest_book.find({}, {'_id': False}))
    return jsonify({'guests':guest_list})

if __name__ == '__main__':
    app.run('0.0.0.0', port=5000, debug=True)