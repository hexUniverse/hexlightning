
#qtype, qact, qdata = query.data.split()


class callback_parse:
    def __init__(self, data):
        self.qtype = None
        self.qact = None
        self.qdata = None

        self.data = data
        self.parse()

    def parse(self):
        tmp = self.data.split()
        self.qtype = tmp[0]
        self.qact = tmp[1]
        self.qdata = ' '.join(tmp[2:])
        self.qdata_list = tmp[2:]
