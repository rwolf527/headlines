import feedparser
from flask import Flask
from flask import render_template

app = Flask(__name__)

RSS_FEEDS = {'bbc': ['http://feeds.bbci.co.uk/news/rss.xml', 'BBC'],
             'cnn': ['http://rss.cnn.com/rss/edition.rss', 'CNN'],
             'fox': ['http://feeds.foxnews.com/foxnews/latest', 'Fox News'],
             'iol': ['http://www.iol.co.za/cmlink/1.640', 'IOL'],
             'nyt': ['http://rss.nytimes.com/services/xml/rss/nyt/HomePage.xml', 'New York Times']}


@app.route("/")
@app.route("/<publication>/")
def get_news(publication="bbc"):
    feed = feedparser.parse(RSS_FEEDS[publication][0])
    my_title = RSS_FEEDS[publication][1]
    return render_template("home.html", title=my_title, articles=feed['entries'])

if __name__ == '__main__':
    app.run(port=5000, debug=True)
