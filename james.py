#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
import logging
import json
import urllib.request


# load json object of current league table from url
en = 'http://api.football-data.org/v1/soccerseasons/445/leagueTable'
en2 = 'http://api.football-data.org/v1/soccerseasons/446/leagueTable'
de = 'http://api.football-data.org/v1/competitions/452/leagueTable'
de2= 'http://api.football-data.org/v1/competitions/453/leagueTable'
it = 'http://api.football-data.org/v1/soccerseasons/456/leagueTable'
es = 'http://api.football-data.org/v1/soccerseasons/455/leagueTable'
fr = 'http://api.football-data.org/v1/soccerseasons/450/leagueTable'
br = 'http://api.football-data.org/v1/soccerseasons/444/leagueTable'
nl = 'http://api.football-data.org/v1/soccerseasons/449/leagueTable'
pt = 'http://api.football-data.org/v1/soccerseasons/457/leagueTable'
sources_available = ["en", "en2", "de", "de2", "it", "es", "fr", "nl", "pt", "br"]

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
    update.message.reply_text("🤖 ⚽ Hello there!\n"
        "I am Sir James Foot and I provide you with the latest football tables\n"
        "Use /<league shortcut> to access the table directly\n"
        "For a list of currently available leagues type /leagues 🕵️‍\n"
        "🤖 ⚽ Enjoy my service!")

def show_leagues(bot, update):
    update.message.reply_text("🤖 ⚽ I currently offer service for \n\n"
        "🇪🇸 Spain 1 (La Liga) /es \n"
        "🇬🇧󠁧󠁢󠁥󠁮󠁧󠁿 England 1 (Premier League) /en \n"
        "🇬🇧󠁧󠁢󠁥󠁮󠁧󠁿 England 2 (Championship) /en2 \n"
        "🇫🇷 France 1 (Ligue 1) /fr \n"
        "🇩🇪 Germany 1 (Bundesliga) /de \n"
        "🇩🇪 Germany 2 (2. Bundesliga) /de2 \n"
        "🇮🇹 Italy 1 (Serie A) /it \n"
        "🇳🇱 Netherlands 1 (Eredivisie) /nl \n"
        "🇵🇹 Portugal 1 (Primeira Liga) /pt \n"
        "🇧🇷 Brazil 1 (Campeonato Brasileiro) /br \n")


def nl_shortcut(bot, update):
    """shortcut for the Eredivisie table"""
    prepareTable("nl", update)
def en_shortcut(bot, update):
    """shortcut for the Premier League table"""
    prepareTable("en", update)
def en2_shortcut(bot, update):
    """shortcut for the Championship table"""
    prepareTable("en2", update)
def es_shortcut(bot, update):
    """shortcut for the La Liga table"""
    prepareTable("es", update)
def fr_shortcut(bot, update):
    """shortcut for Ligue 1 table"""
    prepareTable("fr", update)
def de_shortcut(bot, update):
    """shortcut for the Bundesliga table"""
    prepareTable("de", update)
def de2_shortcut(bot, update):
    """shortcut for the Bundesliga 2 table"""
    prepareTable("de2", update)
def it_shortcut(bot, update):
    """shortcut for the Serie A Table"""
    prepareTable("it", update)
def pt_shortcut(bot, update):
    """shortcut for the Primeira Liga table"""
    prepareTable("pt", update)
def br_shortcut(bot, update):
    """shortcut for the Campeonato Brasileiro table"""
    prepareTable("br", update)
    

def echo(bot, update):
    """Respond to user message."""
    update.message.reply_text(
        "Hello, I am Sir James Foot\n"
        "I can provide you with the current European football tables\n"
        "type /start to get started\n"
        "You can access the football table by using /<league shortcut>\n"
        "For a list of available leagues type /leagues\n")

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
    elif eingabe == 'br':
        select = br
        greeting = "🇧🇷 Oi!\n"
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

    dp.add_handler(CommandHandler("nl", nl_shortcut))
    dp.add_handler(CommandHandler("en", en_shortcut))
    dp.add_handler(CommandHandler("en2", en2_shortcut))
    dp.add_handler(CommandHandler("de", de_shortcut))
    dp.add_handler(CommandHandler("de2", de2_shortcut))
    dp.add_handler(CommandHandler("fr", fr_shortcut))
    dp.add_handler(CommandHandler("es", es_shortcut))
    dp.add_handler(CommandHandler("it", it_shortcut))
    dp.add_handler(CommandHandler("pt", pt_shortcut))
    dp.add_handler(CommandHandler("br", br_shortcut))
    
    

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
