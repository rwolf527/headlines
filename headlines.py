import feedparser
from flask import Flask

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
    first_article = feed['entries'][0]
    return """<html>
        <body>
            <h1>{3}</h1>
            <b>{0}</b> <br/>
            <b>{1}</b> <br/>
            <b>{2}</b> <br/>

        </body>
    </html>""".format(first_article.get("title"),
                      first_article.get("author"),
                      first_article.get("published"),
                      my_title)
    return "no news is good news"

if __name__ == '__main__':
    app.run(port=5000, debug=True)
