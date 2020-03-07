from io import _io
from PIL import Image
import numpy
import scipy.fftpack
from operator import itemgetter
'''
hashing = img.imhashing(img)
hashing.hash() `str`
hashing.compare(another list)
'''


class compare_result:
    def __init__(self, data):
        self.data = data
        self.hash = None
        self.judge = None
        self.score = None
        self.parse()

    def parse(self):
        if 'hash' in self.data.keys():
            self.hash = self.data['hash']
        if 'judge' in self.data.keys():
            self.judge = self.data['judge']
        if 'score' in self.data.keys():
            self.score = self.data['score']


class hashing_result(object):
    def __init__(self, binary_array):
        self.hash = binary_array

    def __str__(self):
        return self._binary_array_to_hex(self.hash.flatten())

    def __repr__(self):
        return repr(self.hash)

    def __sub__(self, other):
        if other is None:
            raise TypeError('other hash must not be None.')
        if self.hash.size != other.hash.size:
            raise TypeError('hashing must be of the same shape.',
                            self.hash.shape, other.hash.shape)
        return numpy.count_nonzero(self.hash.flatten() != other.hash.flatten())

    def __eq__(self, other):
        if other is None:
            return False
        return numpy.array_equal(self.hash.flatten(), other.hash.flatten())

    def __ne__(self, other):
        if other is None:
            return False
        return not numpy.array_equal(self.hash.flatten(), other.hash.flatten())

    def __hash__(self):
        # this returns a 8 bit integer, intentionally shortening the
        # information
        return sum([2**(i % 8)
                    for i, v in enumerate(self.hash.flatten()) if v])

    def _binary_array_to_hex(self, arr):
        bit_string = ''.join(str(b) for b in 1 * arr.flatten())
        width = int(numpy.ceil(len(bit_string) / 4))
        return '{:0>{width}x}'.format(int(bit_string, 2), width=width)


class hashing:
    def __init__(self, image=None):
        self.image = self.open_img(image)

    def open_img(self, image):
        if isinstance(image, str):
            return Image.open(image)
        elif type(image) in [bytes, _io.BufferedReader, _io.BytesIO]:
            return Image.open(image)
        else:
            raise TypeError(f'unsupported image type {image}')

    def phash(self, hash_size=8, highfreq_factor=4):
        if hash_size < 2:
            raise ValueError("hash size must be greater than or equal to 2")
        img_size = hash_size * highfreq_factor
        image = self.image.convert("L").resize(
            (img_size, img_size), Image.ANTIALIAS)
        pixels = numpy.asarray(image)
        dct = scipy.fftpack.dct(scipy.fftpack.dct(pixels, axis=0), axis=1)
        dctlowfreq = dct[:hash_size, :hash_size]
        med = numpy.median(dctlowfreq)
        diff = dctlowfreq > med
        self.hash_ = str(hashing_result(diff))
        return self.hash_

    def indexing(self):
        d = {'a': 11, 'b': 12, 'c': 13, 'd': 14, 'e': 15, 'f': 16}
        t = []
        for _ in self.hash_:
            if _.isdigit():
                t.append(int(_))
            else:
                t.append(d[_])
        return sum(t)

    def plooks_like(self, left_hash: list, right_hash=None, tolerance=75):
        """
        if right_hash got None it will using hashing target instead.
        and left_hash only accept list type
        the last one was the closest
        """
        if right_hash is None:
            right_hash = self.phash()

        tmp_list = []
        for _ in left_hash:
            judge = False
            calculator = sum(map(lambda x: 0 if x[0] == x[1] else 1, zip(
                str(_), str(right_hash))))
            result = (16 - calculator) * 6.25
            if int(result) >= tolerance:
                judge = True
            # tmp_list.append()
            tmp_list.append({'hash': _, 'judge': judge, 'score': int(result)})

        newlist = []
        for x in sorted(tmp_list, key=itemgetter('score')):
            newlist.append(compare_result(x))

        return newlist
