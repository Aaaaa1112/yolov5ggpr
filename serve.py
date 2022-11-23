from flask import Flask, request,render_template
import torch
import io
from io import BytesIO
import base64
import json
from PIL import Image
import client
# 加载模型,'ultralytics/yolov5'为yolov5源码路径，下载存在本地。'custom'：通过这个设置可以加载自己的模型。path = 'yolov5s.pt':权重地址，source='local'：从本地加载yolov5源码，如果不设置默认为github，force_reload=True是否强制更新代码
model = torch.hub.load('G:\keti111\yolov5\yolov5gpr', 'custom', path='best.pt', force_reload=False, source='local')

# 设置允许上传的文件格式
ALLOW_EXTENSIONS = ['png', 'jpg', 'jpeg', 'gif']


# 判断文件后缀是否存在
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[-1] in ALLOW_EXTENSIONS


# 定义路由
app = Flask(__name__)


@app.route("/photo", methods=['POST', 'GET'])    #后端代码能做的事情
def uploads():
    if not request.method == "POST":
        return
    if request.files.get("image"):
        image_file = request.files["image"]
        file_name = image_file.filename
        if allowed_file(file_name) == True:
            image_bytes = image_file.read()
            img = Image.open(io.BytesIO(image_bytes))
            if img.mode != 'RGB':
                img = img.convert('RGB')
            results = model(img, size=640)
            str = results.pandas().xyxy[0].to_json(orient="records")
            im = request.values.to_dict()
            # 判断是否返回图片，这里的True和False都是字符串，只有True返回，其他字符串都不返回图片
            value = im['download_image']
            if value == 'True':
                # results.imgs  # array of original images (as np array) passed to model for inference
                results.render()  # updates results.imgs with boxes and labels
                image_str = []
                for img in results.ims:
                    buffered = BytesIO()
                    img_base64 = Image.fromarray(img)
                    img_base64.save(buffered, format="JPEG")
                    image = base64.b64encode(buffered.getvalue()).decode('utf-8')  # base64 encoded image with results
                    image_str.append(image)
                s = {'result': str, 'image': image_str[0], "name": file_name}
            else:
                s = {'result': str, "name": file_name}
        else:
            s = {file_name: "格式错误，无法正常打开", 'error': 'error', }
            s = json.dumps(s)
        return s

@app.route('/')                                              #导入前端文件
def upload_file():
   return render_template('index1.html')

#导入前端文件

if __name__ == "__main__":
    app.run(host='127.0.0.1', port=5000)