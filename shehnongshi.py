from flask import Flask, request, render_template, jsonify
from PIL import Image
from yolo import YOLO
from PIL import Image
from flask_sqlalchemy import SQLAlchemy
import sqlalchemy
app = Flask(__name__)
labels = []
def return_img_stream(img_local_path):
  """
  工具函数:
  获取本地图片流
  :param img_local_path:文件单张图片的本地绝对路径
  :return: 图片流
  """
  import base64
  img_stream = ''
  with open(img_local_path, 'rb') as img_f:
    img_stream = img_f.read()
    img_stream = base64.b64encode(img_stream)
  return img_stream

@app.route('/')
def index():
    return "123"

#用户名、密码、主机名、端口和数据库名
app.config['SQLALCHEMY_DATABASE_URI'] = "mysql+pymysql://root:921499@127.0.0.1:3306/baicaoshi"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
#创建数据库对象
db = SQLAlchemy(app)
db.reflect()
    # 获取所有表名
    # 获取所有表名
all_table = {table_obj.name: table_obj for table_obj in db.get_tables_for_bind()}
    # 获取demo表的所有数据
all_data = db.session.query(all_table['caoyao'])
@app.route('/submit', methods=['GET','POST'])

def send_img():
    f = request.files['content']
    f.save('1.jpg')
    yolo = YOLO()

    img = f

    try:
        image = Image.open(img)
    except:
        print('Open Error! Try again!')
    else:
        r_image, label = yolo.detect_image(image)
        labels.clear()
        for i in label:
            labels.append(i)
        r_image.save("img.jpg")
    img_path = "img.jpg"
    img_stream = return_img_stream(img_path)
    return img_stream

@app.route('/label', methods=['GET'])
def label():
    lables = {}
    j = 0
    for i in labels:
        lables[j] = i
        j = j + 1
        print(i)
    name={}
    for data in all_data:
        key=data[0]
        
        labelname=lables
        for t in range(j):
            if key==lables[t]:
                name[t]=data[1]
    return jsonify(name)

if __name__ == '__main__':
    app.run()