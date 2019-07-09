from rakuten.util.encrypt import Encrypt
from rakuten.dao.base.dbcore import *
from rakuten.service.base.rakuten import *
import pandas
import rakuten.util.config


class ItemImageDao(DbCore):
    def __init__(self):
        super(ItemImageDao, self).__init__()

    @classmethod
    def update_item_image(cls, client_id: int, df: pandas.DataFrame) -> int:
        try:
            config = rakuten.util.config.get_image_judge_config()
            commit_num = 0
            cls.connect()
            for i, row in df.iterrows():
                item_image = cls.session.query(cls.ItemImage).join(cls.ItemImage.item).filter(
                    cls.ItemImage.image_url == row[config["image_url"]]).filter(
                    cls.Item.client_id == client_id).one()
                if not pandas.isnull(row[config["total_judge"]]):
                    item_image.total_judge = row[config["total_judge"]]
                if not pandas.isnull(row[config["text_judge"]]):
                    item_image.text_judge = row[config["text_judge"]]
                if not pandas.isnull(row[config["frame_judge"]]):
                    item_image.frame_judge = row[config["frame_judge"]]
                if not pandas.isnull(row[config["bg_judge"]]):
                    item_image.bg_judge = row[config["bg_judge"]]
                if not pandas.isnull(row[config["judge_remarks"]]):
                    item_image.judge_remarks = row[config["judge_remarks"]]
                item_image.update_date = datetime.datetime.today()
                ret = cls.session.add(item_image)
                commit_num += 1
            cls.flush()
            cls.commit()
            return commit_num
        except Exception as e:
            raise CustomError(e)
        finally:
            cls.close()
