#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
import logging
import json
import urllib.request


# load json object of current league table from url
en = 'http://api.football-data.org/v1/soccerseasons/445/leagueTable'
en2 = 'http://api.football-data.org/v1/soccerseasons/447/leagueTable'
de = 'http://api.football-data.org/v1/competitions/452/leagueTable'
de2= 'http://api.football-data.org/v1/competitions/453/leagueTable'
it = 'http://api.football-data.org/v1/soccerseasons/456/leagueTable'
es = 'http://api.football-data.org/v1/soccerseasons/455/leagueTable'
fr = 'http://api.football-data.org/v1/soccerseasons/450/leagueTable'
nl = 'http://api.football-data.org/v1/soccerseasons/449/leagueTable'
pt = 'http://api.football-data.org/v1/soccerseasons/457/leagueTable'
sources_available = ["en", "en2", "de", "de2", "it", "es", "fr", "nl", "pt"]

# Enable logging
"""LOG_FILENAME = 'example.log'
logging.basicConfig(filename=LOG_FILENAME,level=logging.DEBUG)
"""
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)


# Define a few command handlers. These usually take the two arguments bot and
# update. Error handlers also receive the raised TelegramError object in error.
def start(bot, update):
    update.message.reply_text('🤖 ⚽ Hello there!\n\n Use /fut <league shortcut>\n'
        "For a list of currently available leagues type /leagues 🕵️‍")

def show_leagues(bot, update):
    update.message.reply_text("🤖 ⚽ I currently offer service for \n\n"
        "🇪🇸 Spain 1 (La Liga) /fut es \n"
        "🇬🇧󠁧󠁢󠁥󠁮󠁧󠁿 England 1 (Premier League) /fut en \n"
        "🇬🇧󠁧󠁢󠁥󠁮󠁧󠁿 England 2 (League One) /fut en2 \n"
        "🇫🇷 France 1 (Ligue 1) /fut fr \n"
        "🇩🇪 Germany 1 (Bundesliga) /fut de \n"
        "🇩🇪 Germany 2 (2. Bundesliga) /fut de2 \n"
        "🇮🇹 Italy 1 (La Liga) /fut it \n"
        "🇳🇱 Netherlands 1 (Eredivisie) /fut nl \n"
        "🇵🇹 Portugal 1 (Primeira Liga) /fut pt \n")


def alarm(bot, job):
    """Send the alarm message."""
    bot.send_message(job.context, text='Beep!')

def echo(bot, update):
    """Respond to user message."""
    update.message.reply_text(
        "Hello, I am Sir James Foot\n"
        "I can provide you with the current European football tables\n"
        "type /start to get started\n"
        "Or directly get the football table by using /fut <league shortcut>")

def load_table(bot, update, args, job_queue, chat_data):
    """load table x"""
    chat_id = update.message.chat_id
    
    try:
        #args[0] should contain league shortcut
        if args[0] in sources_available:
            prepareTable(args[0], update)
    
    except (IndexError, ValueError):
        update.message.reply_text('🤖 ⚽ Usage: /fut <league shortcut>\n'
            "for a list of leagues I currently support, please type /leagues 🕵️‍")

def prepareTable(eingabe, update):
    select = ''
    greeting = ""
    if eingabe == 'en':
        select = en
        greeting = "🇬🇧 Good day, sir!\n"
    elif eingabe == 'en2':
        select = en2
        greeting = "🇬🇧 Good day, sir!\n"
    elif eingabe == 'de':
        select = de
        greeting = "🇩🇪 Guten Tag!\n"
    elif eingabe == 'it':
        select = it
    elif eingabe == 'de2':
        select = de2
        greeting = "🇩🇪 Guten Tag!\n"
    elif eingabe == 'es':
        select = es
        greeting = "🇪🇸 Hola!\n"
    elif eingabe == 'fr':
        select = fr
        greeting = "🇫🇷 Bonjour !\n"
    elif eingabe == 'pt':
        select = pt
        greeting = "🇵🇹 Olà!\n"
    elif eingabe == 'nl':
        select = nl
        greeting = "🇳🇱 Hoi!\n"

    table = urllib.request.urlopen(select)
    table_str = table.read().decode('utf-8')
    table_obj = json.loads(table_str)
    update.message.reply_text(greeting + "🤖 Opening current league table; It's matchweek {0} ⚽".
          format(table_obj['matchday']))
    long_text = ""
    for team in table_obj['standing']:
        long_text += "{:<2}) {:<15} | {} Pts {} GP {} Goals\n".format(team['position'],
            team['teamName'], team['points'],team['playedGames'], team['goals'])
    update.message.reply_text(long_text)
    #line_new = '{:>12}  {:>12}  {:>12}'.format(word[0], word[1], word[2])




def error(bot, update, error):
    """Log Errors caused by Updates."""
    logger.warning('Update "%s" caused error "%s"', update, error)


def main():
    """Run bot."""
    updater = Updater("token")

    # Get the dispatcher to register handlers
    dp = updater.dispatcher

    # on different commands - answer in Telegram
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("help", start))
    dp.add_handler(CommandHandler("leagues", show_leagues))
    dp.add_handler(CommandHandler("fut", load_table,
                                  pass_args=True,
                                  pass_job_queue=True,
                                  pass_chat_data=True))
    

    dp.add_handler(MessageHandler(Filters.text, echo))

    # log all errors
    dp.add_error_handler(error)

    # Start the Bot
    updater.start_polling()

    # Block until you press Ctrl-C or the process receives SIGINT, SIGTERM or
    # SIGABRT. This should be used most of the time, since start_polling() is
    # non-blocking and will stop the bot gracefully.
    updater.idle()


if __name__ == '__main__':
    main()
