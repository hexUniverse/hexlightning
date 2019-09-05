import db_tools
mongo = db_tools.use_mongo()
redis = db_tools.use_redis()


class user_list:
    def __init__(self):
        self.class_level_list = mongo.class_level.find_one({})
        self.master = 525239263

    def isdigit(self, input_str, getback=False):
        try:
            int(input_str)
        except ValueError:
            return False
        else:
            if getback:
                return str(input_str).encode()
            else:
                return True

    def refresh(self):
        self.class_level_list = mongo.class_level.find_one({})
        self.lucifer, self.michael, self.elf = [], [], []
        for class_level in self.class_level_list:
            if 'michael' in class_level:
                self.michael.extend(self.class_level_list['michael'])
            if 'lucifer' in class_level:
                self.lucifer.extend(self.class_level_list['lucifer'])
            if 'elf' in class_level:
                self.elf.extend(self.class_level_list['elf'])
        c1 = ['lucifer', 'michael', 'elf']
        c2 = [self.lucifer, self.michael, self.elf]

        for x, y in zip(c1, c2):
            redis.delete(c1)
            for data in y:
                redis.lpush(x, data)

    def is_lucifer(self, user_id: 'input telegram user id'):
        self.lucifer = redis.lrange('lucifer', 0, -1)
        user_id = self.isdigit(user_id, getback=True)
        if user_id == False:
            return False
        if user_id not in self.lucifer:
            return False
        if user_id in self.lucifer:
            return True

    def is_michael(self, user_id: 'input telegram user id'):
        self.michael = redis.lrange('michael', 0, -1)
        user_id = self.isdigit(user_id, getback=True)
        if user_id == False:
            return False
        if user_id not in self.michael:
            return False
        if user_id in self.michael:
            return True

    def is_elf(self, user_id: 'input telegram user id'):
        self.elf = redis.lrange('elf', 0, -1)
        user_id = self.isdigit(user_id, getback=True)
        if user_id == False:
            return False
        if user_id not in self.elf:
            return False
        if user_id in self.elf:
            return True

    def is_global_white(self, user_id: 'input telegram user id'):
        self.global_white = redis.lrange('global_white', 0, -1)
        user_id = self.isdigit(user_id, getback=True)
        if user_id == False:
            return False
        if user_id not in self.elf:
            return False
        if user_id in self.elf:
            return True
