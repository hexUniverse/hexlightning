'''
Todo:
 - emotion call
 - emotion call with random `emotion.happy`
'''
import random


class kaomoji:
    def __init__(self):
        self.emotion = self.emotion_()

    class emotion_:
        def __init__(self, listing=False):
            self.happy = self.happy_(listing)
            self.angry_(listing)

        def happy_(self, listing):
            self.happy_list = [
                '(ﾟ∀ﾟ)',
                '(*ﾟ∀ﾟ*)',
                '(*´▽`*)',
                'ヽ(●´∀`●)ﾉ',
                '(*´艸`*)',
                '(*‘ v`*)',
                '(^u^)',
                '(^y^)',
                '(ﾉ>ω<)ﾉ',
                '(｡A｡)',
                '(ﾉ∀`*)',
                '(*’ｰ’*)',
                'd(`･∀･)b',
                '(,,・ω・,,)',
                '(((ﾟдﾟ)))',
                '(｡◕∀◕｡)',
                'ヽ(✿ﾟ▽ﾟ)ノ',
                '(」・ω・)」うー！(／・ω・)／にゃー！',
                '｡:.ﾟヽ(*´∀`)ﾉﾟ.:｡',
                'ξ( ✿＞◡❛)▄︻▇▇〓▄︻┻┳═一',
                '(✪ω✪)',
                '(⁰▿⁰)',
                '(๑´ㅂ`๑)',
                'ヽ(・×・´)ゞ',
                '(o´罒`o)',
                '☆⌒(*^-゜)v',
                '(灬ºωº灬)',
                '(´///☁///`)',
                '(❛◡❛✿)',
                '(๑• . •๑)',
                '(ㅅ˘ㅂ˘)',
                '٩(｡・ω・｡)و',
                '(*ˇωˇ*人)',
                '☆^(ｏ´Ф∇Ф)o',
                '(,,ﾟДﾟ)',
                '(ﾉ◕ヮ◕)ﾉ*:･ﾟ✧',
                'o(☆Ф∇Ф☆)o',
                '( • ̀ω•́ )',
                '(ﾟω´)',
                '(●｀ 艸 ´)',
                'ヽ(㊤V㊤*)ﾉ',
                '＼(●´ϖ`●)／',
                '(•ㅂ•)/',
                '( *´◒`*)',
                '(((o(*ﾟ▽ﾟ*)o)))',
                '٩(๑•̀ω•́๑)۶',
                '(＊゜ー゜)b',
                '(๑¯∀¯๑)',
                'ヽ(●´ε｀●)ノ',
                'ヽ( ° ▽°)ノ',
                '(ゝ∀･)⌒☆',
                '(╯°▽°)╯ ┻━┻',
                '(｡・ω・｡)',
                ' (•‾⌣‾•)',
                '✧*｡٩(ˊᗜˋ*)و✧*｡',
                '⁽⁽ ◟(∗ ˊωˋ ∗)◞ ⁾⁾',
                "＼＼٩( 'ω' )و／／",
                '（๑ • ‿ • ๑ ）',
                'ヽ( ^ω^ ゞ )',
                '(๑ ^ ₃•๑) ',
                '⁽⁽٩(๑˃̶͈̀ ᗨ ˂̶͈́)۶⁾⁾']
            if listing:
                return self.happy_list
            else:
                return random.choice(self.happy_list)

        def angry_(self, listing):
            self.angry_list = [
                '(ﾟ皿ﾟﾒ)',
                '(ﾒ ﾟ皿ﾟ)ﾒ',
                '(#`Д´)ﾉ',
                '(#`皿´)',
                '(-`ェ´-╬)',
                '(╬ﾟдﾟ)',
                '(`д´)',
                'ヽ(#`Д´)ﾉ',
                '(╬☉д⊙)',
                '(／‵Д′)／~ ╧╧',
                '(╯‵□′)╯︵┴─┴',
                '⊙谷⊙',
                'ヽ(`Д´)ノ',
                '◢▆▅▄▃崩╰(〒皿〒)╯潰▃▄▅▇◣',
                '(╬ﾟдﾟ)▄︻┻┳═一',
                '٩(ŏ﹏ŏ、)۶',
                '（ ´ﾟ,_」ﾟ）ﾊﾞｶｼﾞｬﾈｰﾉ',
                '(╬ﾟ ◣ ﾟ)',
                '(☄◣ω◢)☄',
                '(ಠ益ಠ)',
                '(ﾒﾟДﾟ)ﾒ',
                '(`へ´≠)',
                '(・`ω´・)',
                '(#ﾟ⊿`)凸',
                '╯-____-)╯~═╩════╩═',
                '(*≥▽≤)ツ┏━┓',
                '(๑•ૅω•´๑)',
                '눈言눈',
                '(╯ŏ益ŏ)╯︵(ヽo□o)ヽ',
                '曉美焰 ル||☛_☚|リ',
                '(╬▼дﾟ)▄︻┻┳═一',
                '(╯•̀ὤ•́)╯',
                '(； ･`д･´)',
                '•_ゝ•',
                '( ･᷄ὢ･᷅ )',
                '●｀ε´●)爻(●｀ε´● )',
                '(༼•̀ɷ•́༽)',
                '(╬ﾟдﾟ)╭∩╮',
                '٩(◦`꒳´◦)۶ ',
                '(ノ▼Д▼)ノ',
                '(ꐦ°᷄д°᷅)']
            if listing:
                return self.angry_list
            else:
                return random.choice(self.angry_list)
