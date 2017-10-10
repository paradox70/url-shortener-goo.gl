#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Simple Bot to short link and report clicks.
# This program is dedicated to the public domain under the CC0 license.
"""
This Bot uses the Updater class to handle the bot.

First, a few callback functions are defined. Then, those functions are passed to
the Dispatcher and registered at their respective places.
Then, the bot is started and runs until we press Ctrl-C on the command line.

Usage:
Send /start to initiate.
Send a valid url to shorten it, and counter clicks.
Press Ctrl-C on the command line or send a signal to the process to stop the
bot.
"""

from telegram import Bot, MessageEntity, ParseMode, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (Updater, CommandHandler, MessageHandler, Filters,
						  Dispatcher, CallbackQueryHandler)
import logging
import json

from httplib2 import Http
from oauth2client.service_account import ServiceAccountCredentials
from apiclient.discovery import build

#telegram bot token
TOKEN = "XXXXXXX:XXXXXXXXXXXXXXXXXXXXXXXXX"

# Enable logging
logging.basicConfig(filename='pvChat_bot.log', format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
					level=logging.INFO)
logger = logging.getLogger(__name__)

# Using OAuth 2.0 for Server to Server Applications 
# Read more: https://developers.google.com/api-client-library/python/auth/service-accounts
scopes = ['https://www.googleapis.com/auth/urlshortener'] 
credentials = ServiceAccountCredentials.from_json_keyfile_name('/path/to/googleProject.json', scopes)
service = build('urlshortener', 'v1', credentials=credentials, cache_discovery=False)

def start(bot, update):
	user = update.message.from_user
	update.message.reply_text('Just send me a link and I\'ll shorten it.')

def insert(bot, update):
	user = update.message.from_user
	longUrl = update.message.text
	body = {'longUrl': longUrl}

  response = service.url().insert(body=body).execute()

  keyboard = [[InlineKeyboardButton("Refresh total clicks", callback_data=response['id'])]]
	reply_markup = InlineKeyboardMarkup(keyboard)
	update.message.reply_text('Long url: {}\n\nShort url: {}\n\nTotal clicks: 0\n'.format(response['longUrl'], response['id']), reply_markup=reply_markup)

def get(bot, update):
	query = update.callback_query
	user = update.callback_query.from_user
	shortUrl = query.data

	response = service.url().get(shortUrl=shortUrl, projection='ANALYTICS_CLICKS').execute()

	keyboard = [[InlineKeyboardButton("Refresh total clicks", callback_data=response['id'])]]
	reply_markup = InlineKeyboardMarkup(keyboard)
	bot.edit_message_text('Long url: {}\n\nShort url: {}\n\nTotal clicks: {}\n'.format(response['longUrl'], response['id'], response['analytics']['allTime']['shortUrlClicks']),
						chat_id=query.message.chat_id, message_id=query.message.message_id, reply_markup=reply_markup)

def send_text(bot, update):
	user = update.message.from_user
	update.message.reply_text('Oops! Your message seems not a regular Link...!!! 🙄')
	#return SEND_TEXT

def error(bot, update, error):
	logger.warn('Update "%s" caused error "%s"' % (update, error))

def main(webhook_url=None):
	# Get the dispatcher to register handlers
	if webhook_url:
		bot = Bot(TOKEN)
		dp = Dispatcher(bot, None, workers=0)
	else:
		updater = Updater(TOKEN)
		bot = updater.bot
		dp = updater.dispatcher

	start_handler = CommandHandler('start', start, allow_edited=False)
	insert_handler = MessageHandler((Filters.text & Filters.entity(MessageEntity.URL)), insert, allow_edited=False)
	send_text_handler = MessageHandler(Filters.all, send_text)
	dp.add_handler(start_handler)
	dp.add_handler(insert_handler)
	dp.add_handler(send_text_handler)
	dp.add_handler(CallbackQueryHandler(get))
	dp.add_error_handler(error)

	# Start the Bot
	if webhook_url:
		bot.set_webhook(url=webhook_url)
		return dp, bot
	else:
		bot.set_webhook()
		updater.start_polling()
		updater.idle()

if __name__ == '__main__':
	main()
