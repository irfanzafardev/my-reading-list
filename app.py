from flask import Flask, render_template, request, jsonify
from pymongo import MongoClient

import certifi
client = MongoClient(
    'mongodb+srv://test:sparta@cluster0.tmmsx79.mongodb.net/?retryWrites=true&w=majority', tlsCAFile=certifi.where())
db = client.dbsparta
app = Flask(__name__)


@app.route('/')
def home():
    return render_template('index.html')


@app.route("/book", methods=["POST"])
def book_post():
    title_receive = request.form["title_give"]
    author_receive = request.form["author_give"]
    count = db.book.count_documents({})
    num = count + 1
    doc = {
        'num': num,
        'title': title_receive,
        'author': author_receive,
        'done': 0
    }
    db.book.insert_one(doc)
    return jsonify({'msg': 'data saved!'})


@app.route("/book/done", methods=["POST"])
def book_done():
    num_receive = request.form["num_give"]
    db.book.update_one(
        {'num': int(num_receive)},
        {'$set': {'done': 1}}
    )
    return jsonify({'msg': 'Update done!'})


@app.route("/book/undone", methods=["POST"])
def book_undone():
    num_receive = request.form["num_give"]
    db.book.update_one(
        {'num': int(num_receive)},
        {'$set': {'done': 0}}
    )
    return jsonify({'msg': 'Update done!'})


@app.route("/delete", methods=["POST"])
def delete_book():
    num_receive = request.form['num_give']
    db.book.delete_one({'num': int(num_receive)})
    return jsonify({'msg': 'delete done!'})


@app.route("/book", methods=["GET"])
def book_get():
    book_list = list(db.book.find({}, {'_id': False}))
    return jsonify({'book': book_list})


if __name__ == '__main__':
    app.run('0.0.0.0', port=5000, debug=True)
