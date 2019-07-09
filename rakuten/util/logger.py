from datetime import datetime as dt
import os


class Logger:

    @classmethod
    def write(cls, client_name: str, log_text: str):
        current_time = dt.now()
        log_time = current_time.strftime("%Y-%m-%d %H-%M-%S")
        dir_path = os.getcwd() + "\\data\\log\\" + client_name
        file_path = dir_path + "\\" + current_time.strftime("%Y-%m-%d.log")
        log_content = log_time + "," + log_text
        if not os.path.exists(dir_path):
            os.makedirs(dir_path)
        with open(file_path, mode="a") as f:
            f.write(log_content + "\n")
            f.close()

