import pymongo
import time
import datetime
import sys

connection = pymongo.MongoClient('172.17.0.2')
db = connection[f'{int(time.time())}']


def func_time(func):
    def _wrapper(*args, **kwargs):
        start = time.time()
        func(*args, **kwargs)
        print(func.__name__, 'run:', time.time()-start)
    return _wrapper


@func_time
def ainsert(num):
    posts = db.userinfo
    for x in range(num):
        post = {'_id': str(x),
                'author': str(x)+'tdc',
                'text': f'{int(time.time())}',
                'tags': ['tdc', 'dct', 'cdt'],
                'date': datetime.datetime.utcnow()}
        posts.insert(post)


if __name__ == '__main__':
    num = sys.argv[1]
    ainsert(int(num))
