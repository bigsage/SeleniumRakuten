from rakuten.dao.base.dbcore import *
from rakuten.service.base.rakuten import *


class ClientItemChoiceDao(DbCore):
    def __init__(self):
        super(ClientItemChoiceDao, self).__init__()

    @classmethod
    def get_client_item_choice_list(cls, client_id):
        try:
            cls.connect()
            result = cls.session.query(cls.ClientItemChoice).filter_by(client_id=client_id).options(
                    eagerload_all("item_choice_type")).all()
            return result
        except Exception as e:
            raise CustomError(e)
        finally:
            cls.close()

