import urllib.error
import urllib.request
import os
import datetime
from PIL import Image
import io
import numpy as np
import requests
import tempfile
import glob
import cv2


class WebImage:
    __PROJECT_DIR_PATH = os.getcwd()
    __IMAGE_DIR__PATH = "\\data\\img\\"
    __RAKUTEN_HOME_PATH = "https://image.rakuten.co.jp/asitis/cabinet"
    __DATE_PATH = datetime.datetime.now().strftime("\\%y%m%d\\")

    @classmethod
    def download_image(cls, url: str, client_name: str) -> str:
        file_name = url.split("/")[-1]
        img_dir_path = cls.__PROJECT_DIR_PATH + cls.__IMAGE_DIR__PATH + client_name + "\\"
        relative_path = cls.__DATE_PATH

        if not os.path.exists(img_dir_path + relative_path):
            os.makedirs(img_dir_path + relative_path)
        file_dir_list = os.listdir(img_dir_path + relative_path)
        dir_list = [f for f in file_dir_list if os.path.isdir(os.path.join(img_dir_path + relative_path, f))]
        amount_dir = len(dir_list)
        if amount_dir == 0:
            relative_path += "1\\"
            os.makedirs(img_dir_path + relative_path)
        else:
            file_dir_list = os.listdir(img_dir_path + relative_path + str(amount_dir))
            file_list = \
                [f for f in file_dir_list if os.path.isfile(os.path.join(img_dir_path + relative_path + str(amount_dir), f))]
            amount_file = len(file_list)
            if amount_file < 500:
                relative_path += str(amount_dir) + "\\"
            else:
                relative_path += str(amount_dir + 1) + "\\"
                os.makedirs(img_dir_path + relative_path)

        raw_img = cls.imread_web(url)
        result, encimg = cv2.imencode(".jpg", raw_img, [int(cv2.IMWRITE_JPEG_QUALITY), 70])
        cv2.imwrite(img_dir_path + relative_path + file_name, raw_img)

        return cls.__RAKUTEN_HOME_PATH + relative_path.replace("\\", "/") + file_name.replace(".png", ".jpg")

    @classmethod
    def delete_image(cls, path):
        os.remove(path)

    @classmethod
    def imread_web(cls, url):
        res = requests.get(url)
        #img = None
        tmp_name = None
        with tempfile.NamedTemporaryFile(
                dir=cls.__PROJECT_DIR_PATH + cls.__IMAGE_DIR__PATH, suffix='.jpg', delete=False) as fp:
            fp.write(res.content)
            fp.file.seek(0)
            img = cv2.imread(fp.name)
            tmp_name = fp.name
            fp.close()
        cls.delete_image(tmp_name)
        return img

