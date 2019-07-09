
class DeleteItemManagementEntity:
    client_id = None
    item_name = None
    managed_number = None

    def __init__(self, client_id: int, item_name: str, managed_number: str):
        self.client_id = client_id
        self.item_name = item_name
        self.managed_number = managed_number

    def get_client_id(self) -> int:
        return self.client_id

    def get_item_name(self) -> str:
        return self.item_name

    def get_managed_number(self) -> str:
        return self.managed_number
