from operator import itemgetter

from plugin import db_tools, db_parse
from plugin import sage
import pygal

chart = pygal.Pie()
mongo = db_tools.use_mongo()


# @pysnooper.snoop()
def abuser(bot, update):
    if sage.lucifer(update.message.from_user.id) != True:
        update.message.reply_text('嘻嘻 等級不夠')
        return
    angel = {}
    user = db_parse.user()
    users = mongo.user.find({"current": {'$exists': True},
                             "current.date": {'$exists': True}})
    for victim in users:
        user.parse(victim)
        if str(user.current.opid) not in angel.keys():
            try:
                angel[f"{user.current.opid}"] = 1
            except BaseException:
                raise
        else:
            try:
                angel[f"{user.current.opid}"] += 1
            except BaseException:
                raise

    ranking = sorted(angel.items(), key=itemgetter(1))
    ranking.reverse()

    text = '誰4濫權王??\n\n'
    for record in ranking:
        user = db_parse.user()
        op = mongo.user.find_one({'chat.id': int(record[0])})
        user.parse(op)
        chart.add(user.fullname, record[1])
        text += f'{user.mention_html} - {record[1]}\n'

    # bar_chart.render_to_file('pie.svg')
    chart.render_to_png('pie.png')
    # chart.render_in_browser()
    update.message.reply_html(text)
