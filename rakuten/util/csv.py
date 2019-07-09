import pandas
import unicodedata
import numpy
import math
import re
from typing import List
from rakuten.exception.custom import CustomError


def read_sjis_csv(path: str) -> pandas.DataFrame:
    return pandas.read_csv(path, encoding='Shift_JISx0213')


def create_request_csv(requeslt_file_path: str, image_file_list):
    for index, each_file_list in enumerate(numpy.array_split(image_file_list, math.ceil(len(image_file_list)/200))):
        with open(requeslt_file_path + "request_" + str(index) + ".csv", mode="w") as f:
            f.write("\n".join(each_file_list))
            f.close()


def get_dual_price_wording_id(client_id: int):
    if client_id == 1:
        return 1


def get_color_me_number(client_id: int, item_name: str) -> str:
    if client_id == 1:
        return __get_color_me_number(item_name)


def get_managed_number(client_id: int, item_name: str) -> str:
    if client_id == 1:
        return __get_color_me_number(item_name)


def get_item_number(client_id: int, item_name: str) -> str:
    if client_id == 1:
        return __get_color_me_number(item_name)


# 商品名のみを抜き出す
def convert_item_name(client_id: int, text: str) -> str:
    if client_id == 1:
        color_me_number = __get_color_me_number(text)
        return text.replace(color_me_number, "")
        # return text


def convert_item_desc(client_id: int, text: str) -> str:
    if client_id == 1:
        tmp = text.replace("\n", "<br>").replace("㎝", "cm").replace("㎏", "kg")
        return tmp


def get_item_price(client_id: int, text: str) -> str:
    if client_id == 1:
        return text


def get_dual_price_wording_id(client_id: int) -> int:
    if client_id == 1:
        return 1


def get_consump_tax_type_id(client_id: int) -> int:
    if client_id == 1:
        return 2


def get_shipping_cost_type_id(client_id: int) -> int:
    if client_id == 1:
        return 1


def get_cod_type_id(client_id: int) -> int:
    if client_id == 1:
        return 1


def get_noshi_type_id(client_id: int) -> int:
    if client_id == 1:
        return 2


def get_order_button_type_id(client_id: int) -> int:
    if client_id == 1:
        return 1


def get_document_request_type_id(client_id: int) -> int:
    if client_id == 1:
        return 2


def get_inquiry_button_type_id(client_id: int) -> int:
    if client_id == 1:
        return 1


def get_restock_button_type_id(client_id: int) -> int:
    if client_id == 1:
        return 2


def get_reception_num_type_id(client_id: int) -> int:
    if client_id == 1:
        return 1


def get_stock_type_id(client_id: int) -> int:
    if client_id == 1:
        return 1


def get_stock_display_type_id(client_id: int) -> int:
    if client_id == 1:
        return 2


def get_delivery_info_display_id(client_id: int) -> int:
    if client_id == 1:
        return 1


def get_delivery_info_type_id_for_stock() -> int:
    return 1


def get_delivery_info_type_id_for_not_stock() -> int:
    return 2


def get_not_catalog_id_reason_id(client_id: int) -> int:
    if client_id == 1:
        return 6


def get_display_category_id(client_id: int, category_list, csv_category_l: str) -> int:
    if client_id == 1:
        for category_entity in category_list:
            if csv_category_l in category_entity.name:
                return category_entity.id
            elif category_entity.name in csv_category_l:
                return category_entity.id
        return 9


def get_not_catalog_id_flg(not_catalog_id_reason_id: int) -> bool:
    if not_catalog_id_reason_id != 1:
        return True
    else:
        return False


def get_warehouse_type_id(client_id: int) -> int:
    if client_id == 1:
        return 1


def get_display_threshold_type_id(client_id: int) -> int:
    if client_id == 1:
        return 3


def get_point_conversion_rate_id(client_id: int) -> int:
    if client_id == 1:
        return 1


def get_all_item_directory_id_id(client_id: int, csv_category_l: str) -> int:
    if client_id == 1:
        extract_word_list = __get_extract_word_kkoichan()

        for extract_word in extract_word_list:
            if csv_category_l == extract_word["csv_word"]:
                return extract_word["db_id"]

    raise CustomError("CSVのカテゴリ変換に失敗しました")


def get_item_color_choice_list(client_id: int, item_desc: str) -> List:
    if client_id == 1:
        line_list = __remove_escape_char(item_desc.split("<br>"))
        try:
            match_line = [s for s in line_list if s.startswith("カラー:")][0].replace("\r", "")
            return match_line.replace("カラー:", "").split("/")
        except IndexError:
            return None


def get_item_size_choice_list(client_id: int, item_desc: str) -> List:
    if client_id == 1:
        line_list = __remove_escape_char(item_desc.split("<br>"))
        try:
            match_line = [s for s in line_list if s.startswith("サイズ:")][0].replace("\r", "")
            return match_line.replace("サイズ:", "").split("/")
        except IndexError:
            return None


def get_item_color_client_item_choice_id(client_id: int) -> int:
    if client_id == 1:
        return 1


def get_item_size_client_item_choice_id(client_id: int) -> int:
    if client_id == 1:
        return 2


def get_item_color_item_choice_type_id(client_id: int) -> int:
    if client_id == 1:
        return 1


def get_item_size_item_choice_type_id(client_id: int) -> int:
    if client_id == 1:
        return 1


def __get_color_me_number(item_name: str) -> str:
    return item_name.split(" ")[-1]


def __get_extract_word_kkoichan() -> List:
    common_list = []
    lady_list = [{"csv_word": "Vivienne Westwood", "db_id": 5252},
                 {"csv_word": "アウター", "db_id": 5165},
                 {"csv_word": "オールインワン", "db_id": 5172},
                 {"csv_word": "シューズ、バッグ、小物", "db_id": 5252},
                 {"csv_word": "スカート", "db_id": 5166},
                 {"csv_word": "セットアップ", "db_id": 5177},
                 {"csv_word": "トップス", "db_id": 5165},
                 {"csv_word": "パンツ", "db_id": 5168},
                 {"csv_word": "パーティードレス", "db_id": 5173},
                 {"csv_word": "ビーチサンダル・ビーチアイテム", "db_id": 14561},
                 {"csv_word": "ワンピース", "db_id": 5170},
                 {"csv_word": "水着", "db_id": 5243},
                 ]

    men_list = []

    return common_list + lady_list


def __str_len_count(text):
    count = 0
    for c in text:
        if unicodedata.east_asian_width(c) in 'FWA':
            count += 2
        else:
            count += 1
    return count


def __remove_escape_char(list):
    tmp = list
    while "" in tmp:
        tmp.remove("")
    return tmp


