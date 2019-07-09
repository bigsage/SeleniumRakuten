import configparser
import os


def get_csv_config() -> configparser.ConfigParser:
    config = configparser.ConfigParser()
    config.read(os.getcwd() + "\\config\\config.txt", encoding='utf-8')
    return config['color_me_csv_column']


def get_image_judge_config() -> configparser.ConfigParser:
    config = configparser.ConfigParser()
    config.read(os.getcwd() + "\\config\\config.txt", encoding='utf-8')
    return config['rakuten_image_judge']
