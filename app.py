from flask import Flask, render_template, request, jsonify, Response
from pymongo import MongoClient
import neural_style_transfer
import tensorflow
import numpy as np
import cv2
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


@app.route('/gen_frame')
def gen_frame():
    cap = cv2.VideoCapture(0)
    while cap.isOpened():
        ret, img = cap.read()
        if not ret:
            break

        # h, w, _ = img.shape
        # cx = h / 2
        # img = img[:, 200:200 + img.shape[0]]
        img = cv2.flip(img, 1)

        if cv2.waitKey(1) == ord('q'):
            break

        ret, buffer = cv2.imencode('.jpg', img)
        frame = buffer.tobytes()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

@app.route('/video_feed')
def video_feed():
    """Video streaming route. Put this in the src attribute of an img tag."""

    return Response(gen_frame(),
                    mimetype='multipart/x-mixed-replace; boundary=frame')

# @app.route("/nst", methods=["POST"])
# def nst_post():
#     ref_img = 'static/img/ref/nst_reference1.jpg'
#     cus_img = 'static/img/cow.jpg'
#     transfer_img_path = neural_style_transfer.main(ref_img,cus_img)
#     print('transfer img = '+transfer_img_path)
#
#     return transfer_img_path


@app.route("/room1/nst", methods=["GET"])
def nst():
    # ref_img = 'static/img/ref/nst_reference1.jpg'
    # cus_img = 'static/img/dog.jpg'
    # transfer_img_path = neural_style_transfer.main(ref_img,cus_img)
    # print('transfer img = ' + transfer_img_path)
    # return render_template('room1.html',nst_result=transfer_img_path)
    # ref_img = 'static/img/ref/nst_reference1.jpg'
    cus_img = 'img/cow.jpg'
    print('here is get')
    return render_template('room1.html', filename=cus_img)

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