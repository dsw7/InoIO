
class Foo:

    def __init__(self):
        self.x: int

    def foo(self):
        if not hasattr(self, 'x'):
            return
        print(self.x)

Foo().foo()
