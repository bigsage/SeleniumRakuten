from rakuten.dao.base.dbcore import *
from rakuten.service.base.rakuten import *
from rakuten.entity.delete_item_management_entity import DeleteItemManagementEntity


class DeleteItemManagementDao(DbCore):
    def __init__(self):
        super(DeleteItemManagementDao, self).__init__()

    @classmethod
    def create_list(cls, delete_item_management_list: List):
        try:
            cls.connect()
            for dim_entity in delete_item_management_list:
                new_data = cls.DeleteItemManagement(client_id=dim_entity.get_client_id(),
                                                    item_name=dim_entity.get_item_name(),
                                                    managed_number=dim_entity.get_managed_number())
                ret = cls.session.add(new_data)
            cls.flush()
            cls.commit()
        except Exception as e:
            raise CustomError(e)
        finally:
            cls.close()

    @classmethod
    def update_delete_flg_list(cls, delete_item_management_list: List):
        try:
            cls.connect()
            update_date = datetime.datetime.now()
            for dim_entity in delete_item_management_list:
                data = cls.session.query(cls.DeleteItemManagement).filter(
                    cls.DeleteItemManagement.client_id == dim_entity.get_client_id(),
                    cls.DeleteItemManagement.managed_number == dim_entity.get_managed_number(),
                    cls.DeleteItemManagement.delete_flg == False).first()
                data.delete_flg = True
                data.update_date = update_date
                cls.session.add(data)
            cls.flush()
            cls.commit()
        except Exception as e:
            raise CustomError(e)
        finally:
            cls.close()

    @classmethod
    def get_not_deleted_list(cls, client_id: int) -> List:
        try:
            cls.connect()
            result_list = []
            data_list = cls.session.query(cls.DeleteItemManagement).filter(
                    cls.DeleteItemManagement.client_id == client_id, cls.DeleteItemManagement.delete_flg == False).all()
            for data in data_list:
                result_list.append(DeleteItemManagementEntity(client_id, data.item_name, data.managed_number))
            cls.flush()
            cls.commit()
        except Exception as e:
            raise CustomError(e)
        finally:
            cls.close()
            return result_list
