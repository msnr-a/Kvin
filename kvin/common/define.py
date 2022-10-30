from . import wraps

def define(name, default=None, readonly=False, validation=None, on_value_changed=None):
    def _decorator(constructor):
        @wraps(constructor)
        def _wrapper(self, *args, **kwargs):

            # __init__以外はエラー
            if not (constructor.__name__ == "__init__"):
                raise RuntimeError("This decorator only decorates __init__.")

            # "_class__name"
            field_name = "_{}__{}".format(self.__class__.__name__, name)

            # 初期値
            if (name in constructor.__args__) and not (name in kwargs):
                setattr(self, field_name, args[constructor.__args__.index(name) - 1])
            else:
                setattr(self, field_name, kwargs.get(name, default))

            # getter
            getter = lambda _: getattr(self, field_name)

            # setter
            if callable(on_value_changed):
                if callable(validation):
                    setter = lambda _, value: [setattr(self, field_name, validation(value)), on_value_changed(self, value)]
                else:
                    setter = lambda _, value: [setattr(self, field_name, value), on_value_changed(self, value)]
            else:
                if callable(validation):
                    setter = lambda _, value: setattr(self, field_name, validation(value))
                else:
                    setter = lambda _, value: setattr(self, field_name, value)

            # プロパティ作成
            if readonly:
                setattr(self.__class__, name, property(getter, None))
            else:
                setattr(self.__class__, name, property(getter, setter))

            # 処理実行
            constructor(self, *args, **kwargs)

        return _wrapper
    return _decorator
