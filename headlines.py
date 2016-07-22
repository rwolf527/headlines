import feedparser
import json
import urllib2
import urllib
import datetime

from flask import Flask
from flask import render_template
from flask import request
from flask import make_response

app = Flask(__name__)

RSS_FEEDS = {'bbc': ['http://feeds.bbci.co.uk/news/rss.xml', 'BBC'],
             'cnn': ['http://rss.cnn.com/rss/edition.rss', 'CNN'],
             'fox': ['http://feeds.foxnews.com/foxnews/latest', 'Fox News'],
             'iol': ['http://www.iol.co.za/cmlink/1.640', 'IOL'],
             'nyt': ['http://rss.nytimes.com/services/xml/rss/nyt/HomePage.xml', 'New York Times']}

DEFAULTS = {'publication': 'bbc',
            'city': 'Apex,US',
            'currency_from': 'GBP',
            'currency_to': 'USD'}

WEATHER_URL = "http://api.openweathermap.org/data/2.5/weather?q={}&units=imperial&appid=8acf0981b06d1edbb12527f2c7cdfa86"
CURRENCY_URL = "https://openexchangerates.org/api/latest.json?app_id=b067697202db446ea3026d30ac66fc40"


def get_value_with_fallback(key):
    if request.args.get(key):
        return request.args.get(key)
    if request.cookies.get(key):
        return request.cookies.get(key)
    return DEFAULTS[key]


@app.route("/")
def home():
    # get customized headlines, based on user input or default
    publication = get_value_with_fallback("publication")
    articles, title = get_news(publication)

    # get customized weather based on user input or default
    city = get_value_with_fallback("city")
    weather = get_weather(city)

    # get customized currency based on user input or default
    currency_from = get_value_with_fallback("currency_from")
    currency_to = get_value_with_fallback("currency_to")
    rate, currencies = get_rate(currency_from, currency_to)

    response = make_response(render_template("home.html", title=title, articles=articles, weather=weather,
                                             currency_from=currency_from, currency_to=currency_to, rate=rate,
                                             currencies=sorted(currencies)))
    expires = datetime.datetime.now() + datetime.timedelta(days=365)
    response.set_cookie("publication", publication, expires=expires)
    response.set_cookie("city", city, expires=expires)
    response.set_cookie("currency_from", currency_from, expires=expires)
    response.set_cookie("currency_to", currency_to, expires=expires)
    return response


def get_news(query):
    if not query or query.lower() not in RSS_FEEDS:
        publication = DEFAULTS['publication']
    else:
        publication = query.lower()

    feed = feedparser.parse(RSS_FEEDS[publication][0])
    my_title = RSS_FEEDS[publication][1]
    return tuple((feed['entries'], my_title))


def get_weather(query):
    query = urllib.quote(query)
    url = WEATHER_URL.format(query)
    data = urllib2.urlopen(url).read()
    parsed = json.loads(data)
    weather = None
    if parsed.get("weather"):
        weather = {"description": parsed["weather"][0]["description"],
                   "temperature": parsed["main"]["temp"],
                   "city": parsed["name"], 'country': parsed['sys']['country']}
    return weather


def get_rate(frm, to):
    all_currency = urllib2.urlopen(CURRENCY_URL).read()

    parsed = json.loads(all_currency).get('rates')
    frm_rate = parsed.get(frm.upper())
    to_rate = parsed.get(to.upper())
    return tuple((to_rate / frm_rate, parsed.keys()))


if __name__ == '__main__':
    app.run(port=5000, debug=True)
