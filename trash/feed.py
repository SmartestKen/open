with open("/home/public/arxiv_feed") as f:
    content = f.readlines()

import datetime
date_obj = datetime.datetime.today()
weekday_list = ["Monday", "Tuesday", "Wednesday", "Thursday",
                "Friday", "Saturday", "Sunday"]
today_date = str(date_obj.date()) + " " + str(weekday_list[date_obj.weekday()])

if content[-1].strip() == "--------end of " + today_date + "--------":
    print("feed already updated")
else:

    import feedparser
    url_set1 = set()
    feed_list1 = ["math.AC", "math.AG", "math.AT", "math.RT"
             "math.CO", "math.CT", "math.QA", "math.KT", "math.RA",
             "math.GR"]
    for category in feed_list1:
        feed = feedparser.parse("http://arxiv.org/rss/" + category).entries
        url_set1.update([x.id + '\n' + x.title for x in feed])

    url_set2 = set()
    feed_list2 = ["cs.LG", "cs.AI", "stat.ML", "eess.SY", "cs.CV", "cs.NE", "q-fin.CP"]
    for category in feed_list2:
        feed = feedparser.parse("http://arxiv.org/rss/" + category).entries
        url_set2.update([x.id + '\n' + x.title for x in feed])

    url_set3 = set()
    feed = feedparser.parse("http://arxiv.org/rss/" + "math.OC").entries
    url_set3.update([x.id + '\n' + x.title for x in feed])

    id_prefix = "https://arxiv.org/abs/"
    scholar_prefix = "https://scholar.google.com/scholar?q="



    with open('/home/public/arxiv_feed', 'a') as f:
        set.intersection(url_set1, url_set2)

        set.intersection(url_set1, url_set3)

        set.intersection(url_set2, url_set3)


        for item in list(url_set.difference({x.strip() for x in content})):
            f.write("%s\n\n" % item)
        f.write("--------end of " + today_date + "--------\n")






