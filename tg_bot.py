#!/usr/bin/env python3

import os
import telebot
import softcalc

if os.environ.get('TG_BOT_TOKEN') is None:
    raise SystemError("Need provide env TG_BOT_TOKEN")
else:
    bot_token = os.environ.get("TG_BOT_TOKEN")


class CoordParserBot(telebot.TeleBot):
    def all_message_parser(self, message):
        res = softcalc.coord_finder(message.text)
        if len(res) > 0:
            if len(res) == 1:
                text = "`{}`".format(res[0])
            elif len(res) == 2:
                d, s = softcalc.calc_softban(*res)
                text = """Coord1: `{}`\nCoord2: `{}`\nDistance: {:.2f}km, Softban: {} min""".format(res[0], res[1], d, 2)
            else:
                text = ", ".join(["`{}`".format(elem) for elem in res])
            self.reply_to(message=message, text=text, parse_mode='Markdown')
            # print("Result: {}".format(res))
            # print("Text: {}".format(text))
        else:
            pass
            # print(message.text)


bot = CoordParserBot(bot_token)


@bot.message_handler(func=lambda message: True, content_types=['text'])
def handle_all(message):
    bot.all_message_parser(message)


if __name__ == "__main__":
    bot.remove_webhook()
    bot.polling(none_stop=True)
