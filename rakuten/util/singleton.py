class Singleton(object):
    __instance = None

    # __new__は__init__の前に実行されるのでここでインスタンスが生成されているか確認する
    def __new__(cls, *args, **kwargs):
        if cls.__instance is None:
            cls.__instance = object.__new__(cls)
        return cls.__instance

