# python-telegram-bot-url-shortener-google-api
Telegram bot that shorten URL, based on Google URL Shortener goo.gl and report total clicks

https://t.me/shortenMyUrlBot

## description
The Google URL Shortener at goo.gl is a service that takes long URLs and squeezes them into fewer characters to make a link that is easier to share, tweet, or email to friends. Users can create these short links through the web interface at goo.gl, or they can programatically create them through the URL Shortener API.

## Authorizing requests and identifying your application
Every request your application sends to the Google URL Shortener API needs to identify your application to Google. There are two ways to identify your application: using an OAuth 2.0 token (which also authorizes the request) and/or using the application's API key. Here's how to determine which of those options to use:

    If the request requires authorization (such as a request for an individual's private data), then the application must provide an OAuth 2.0 token with the request. The application may also provide the API key, but it doesn't have to.
    If the request doesn't require authorization (such as a request for public data), then the application must provide either the API key or an OAuth 2.0 token, or both—whatever option is most convenient for you.

### Using OAuth 2.0 for Server to Server Applications
IMPORTANT follow this link: 
https://developers.google.com/api-client-library/python/auth/service-accounts to create new project on google and achive a json file to pass to the code.

## required package
google-api-python-client

python-telegram-bot
