#!/usr/bin/env python3

import os
import sys
from time import sleep
import telebot
import softcalc
import threading
from bottle import route, run, template, static_file, request

if os.environ.get('TG_BOT_TOKEN') is None:
    raise SystemError("Need provide env TG_BOT_TOKEN")
else:
    bot_token = os.environ.get("TG_BOT_TOKEN")

web_port = sys.argv[1]


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


@route("/")
def web_parse_root():
    return "Hello World"


def run_web():
    run(host='0.0.0.0', port=web_port, quiet=True)


def run_bot_poller():
    while True:
        try:
            bot.remove_webhook()
            bot.polling(none_stop=True)
        except Exception as polling_err:
            sleep(15)


if __name__ == "__main__":
    w = threading.Thread(target=run_web, daemon=True)
    w.name = "WebThread"
    b = threading.Thread(target=run_bot_poller, daemon=True)
    b.name = "BotThread"
    try:
        w.start()
        b.start()
        w.join()
        b.join()
    except KeyboardInterrupt:
        raise SystemExit("CTRL+C pressed, exiting...")
