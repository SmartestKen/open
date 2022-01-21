import urllib.request
from xml.etree import ElementTree
from datetime import datetime, timedelta
# url = 'http://export.arxiv.org/api/query?search_query=all:math.OC&start=0&max_results=100&sortBy=submittedDate&sortOrder=descending'



feed_set1 = {"math.AC", "math.AG", "math.AT", "math.RT"
             "math.CO", "math.CT", "math.QA", "math.KT", "math.RA",
             "math.GR"}
feed_set2 = {"cs.LG", "cs.AI", "stat.ML", "eess.SY", "cs.CV", "cs.NE", "q-fin.CP"}
feed_set3 = {"math.OC"}


id_prefix = "https://arxiv.org/abs/"
scholar_prefix = "https://scholar.google.com/scholar?q="

accept_lists = [[],[],[],[]]
labels = ["algebra_app", "algebra_oc", "app_oc", "oc_self"]

prefix = '{http://www.openarchives.org/OAI/2.0/}'
prefix2 = '{http://arxiv.org/OAI/arXivRaw/}'
prefix3 = "https://arxiv.org/abs/"


for i in range(2007,2008):
    file = "/home/public/arxiv_oai_from_" + str(i) + "_to_" + str(i+1)

    for child in (ElementTree.parse(file).find(prefix + "ListRecords") or []):
        info = child.find(prefix+"metadata").find(prefix2+"arXivRaw")

        art_set = set(info.find(prefix2 + "categories").text.split())

        criteria = [0, 0, 0, 0]
        # multi criteria connection (1,2) (1,3) (2,3) (1,1)
        criteria[0] = bool(art_set & feed_set1) and bool(art_set & feed_set2)
        criteria[1] = bool(art_set & feed_set1) and bool(art_set & feed_set3)
        criteria[2] = bool(art_set & feed_set2) and bool(art_set & feed_set3)
        criteria[3] = bool(art_set & feed_set3)

        true_indices = [i for i, x in enumerate(criteria) if x]
        if len(true_indices) > 0:
            art_id = info.find(prefix2 + "id").text
            art_title = info.find(prefix2+"title").text
            print(a["id"], a["title"])

            embed_id = id_prefix + art_id
            embed_title = scholar_prefix + art_title.replace(" ", "+")


            for i in true_indices:
                accept_lists[i].append('<a href=' + embed_id + '>' + art_id + '</a>' + '&ensp;'
                               + '<a href=' + embed_title + '>' + art_title + '</a>' + "<br />\n")


for i,sublist in enumerate(accept_lists):
    with open('/home/public/arxiv_oai_'+labels[i]+'.html', 'w') as f:
        f.write("<!DOCTYPE html><head>")
        for item in sublist:
            f.write("%s" % item)
        f.write("</head>")

