def function(*args, **kwargs):
    return None


def _empty_decorator(x):
    return x


def clocals(**arg_types):
    return _empty_decorator


class _EmptyDecoratorAndManager(object):
    def __call__(self, x):
        return x

    def __enter__(self):
        pass

    def __exit__(self, exc_type, exc_value, traceback):
        pass


class FakeAttr(object):
    def __getattr__(self, name):
        return FakeAttr()

    def __call__(self, *args, **kwargs):
        return FakeAttr()

    def __getitem__(self, *args, **kwargs):
        return FakeAttr()


class FakeCython(object):

    def __init__(self):
        self.declare = function
        self.int = FakeAttr()
        self.void = FakeAttr()
        self.locals = clocals
        self.cclass = _EmptyDecoratorAndManager()
        self.ccall = _EmptyDecoratorAndManager()
        self.cfunc = _EmptyDecoratorAndManager()
        self.compiled = False
        self.returns = lambda type_arg: _EmptyDecoratorAndManager()

cython = FakeCython()
