class Singleton:
    obj = None

    def __new__(cls, *args, **kwargs):
        if not isinstance(cls.obj, cls):
            cls.obj = object.__new__(cls)
        return cls.obj
