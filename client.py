import requests
import os
import time
import argparse
from PIL import Image
from io import BytesIO
import base64
# 加载图片地址
# 图片文件夹，可以修改为自己的路径
path = r'C:\Users\lenovo\Desktop\pic1'
# 连接地址，服务部署的地址，默认本机ip，端口5000
url = "http://127.0.0.1:5000/photo"
file_path = os.listdir(path)
s = len(file_path)
t1 = time.time()
for i in file_path:
    img_path = os.path.join(path + '/' + i)
    path1 = img_path.replace("\\", "/")
    # 路径拼接
    file_name = img_path.split('/')[-1]
    # 图片名分割
    # 二进制打开图片
    file = open(img_path, 'rb')
    # # 拼接参数，False为不返回图片，True为返回图片
    data = {'download_image': False}
    files = {'image': file}
    # 发送post请求到服务器端
    r = requests.post(url, files=files, data=data)
    file.close()
    # # 获取服务器返回的图片，字节流返回
    result = r.json()
    try:
        # 对图片进行解码并打开
        img = Image.open(BytesIO(base64.b64decode(result['image'])))
        # 结果删除图片编码进行打印
        result.pop('image')
        print(result)
        # 储存图片，在本项目目录，需要建立一个名字为1的文件夹
        img.save('1/' + 'result' + file_name)
        img.show()#展示图片
        img.close()
    except KeyError:
        result['path'] = path1
        print(result)
t2 = time.time()
t3 = t2 - t1
print('耗费时间', t3)
print('图片总数', s)
print('平均时间', t3 / s)