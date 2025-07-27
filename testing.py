from event_signal import signaler


class XTest(object):
    def __init__(self, x=0):
        self._x = x

    def get_x(self):
        return self._x

    @signaler
    def set_x(self, x):
        self._x = x

    @set_x.on("before_change")
    def x_changing(self, x):
        print("x is changing")

    @set_x.on("change")
    def x_changed(self, x):
        print("x changed", x)

t = XTest()
t.set_x(1)
# x is changing
# x changed 1
t.set_x.on("change", lambda x: print("new signal"))
t.set_x(2)
# x is changing
# x changed 2
# new signal
t.set_x.off("before_change", t.x_changing)
t.set_x(3)
# x changed 3
# new signal

t.set_x.block()
t.set_x(4)

t.set_x.block(block=False)
t.set_x(5)
# x changed 3
# new signal

t.set_x.block('change', True)
t.set_x(6)