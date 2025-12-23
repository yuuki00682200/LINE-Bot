class Callback:
    def __init__(self, func=print, func2=print):
        self.func = func
        self.func2 = func2

    def output(self, url):
        self.func(url)

    def output_pin(self, pin):
        self.func2(pin)

