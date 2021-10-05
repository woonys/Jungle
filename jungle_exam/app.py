from flask import Flask, render_template, jsonify, request
app = Flask(__name__)


from pymongo import MongoClient
client = MongoClient('mongodb://test:test@localhost', 27017)
db = client.dbjungle

## HTML을 주는 부분
@app.route('/')
def home():
   return render_template('index.html')

@app.route('/memo/show', methods=['GET'])
def showing_card():
    all_memos = list(db.exam.find({}, {'_id': 0}))
    return jsonify({'result':'success', 'all_memos':all_memos})


@app.route('/memo/open', methods=['GET'])
def open_card():
    title_receive = request.args.get('title_give')
    this_memo_with_id = db.exam.find_one({'title':title_receive})
    this_id = str(this_memo_with_id['_id'])
    this_memo = db.exam.find_one({'title': title_receive}, {'_id':0})
    print(this_id)
    return jsonify({'result': 'success', 'this_memo': this_memo, 'id': this_id})



## API 역할을 하는 부분
@app.route('/memo/post', methods=['POST'])
def posting_card():
    title_receive = request.form['title_give']
    contents_receive = request.form['contents_give']

    doc = {'title':title_receive, 'contents':contents_receive}

    db.exam.insert_one(doc)

    return jsonify({'result':'success', 'msg':'저장 완료!'})


@app.route('/memo/update', methods=['POST'])
def update_card():
    id_receive = request.form['id_give']
    title_receive = request.form['title_give']
    contents_receive = request.form['contents_give']
    print("id_receive: ", id_receive)
    print(title_receive, contents_receive)
    db.exam.update_one({'_id': id_receive}, {'$set': {'title': title_receive}})
    db.exam.update_one({'_id': id_receive}, {'$set': {'contents': contents_receive}})
    print(db.exam.find_one({'title':title_receive}))
    return jsonify({'result': 'success', 'msg': '수정 완료'})




@app.route('/memo/delete', methods=['POST'])
def delete_card():
    title_receive = request.form['title_give']
    db.exam.delete_one({'title': title_receive})
    return jsonify({'result': 'success', 'msg': '제거되었습니다!'})

if __name__ == '__main__':
   app.run('0.0.0.0',port=5000,debug=True)