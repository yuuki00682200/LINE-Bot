class TextConv:
    def __init__(self, cl, op, text):
        self.client = cl
        self.op = op
        self.text = self.conv(text)

    def conv(self, text):
        op = self.op
        if "%1" in text:
            con = self.client.run(self.client.getContact(op.param2))
            text = text.replace("%1", con.displayName)
        if "%2" in text:
            gro = self.client.run(self.client.getGroup(op.param1))
            text = text.replace("%2", gro.name)
        return text

