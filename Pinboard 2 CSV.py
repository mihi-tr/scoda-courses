# -*- coding: utf-8 -*-
# <nbformat>3.0</nbformat>

# <markdowncell>

# # Converting Pinboard.in to CSV
# 
# Tony has saved tons of stuff on Pinboard.in, let's convert this to a csv so we can all categorize stuff using a spreadsheet.

# <codecell>

import urllib2, lxml.etree,re

# <codecell>

u=urllib2.urlopen("https://feeds.pinboard.in/rss/t:scodamd/")
data=u.read()
u.close()

# <codecell>

root=lxml.etree.fromstring(data)

# <codecell>

ns=[("rss","http://purl.org/rss/1.0/"),("rdf","http://www.w3.org/1999/02/22-rdf-syntax-ns#"),("taxo","http://purl.org/rss/1.0/modules/taxonomy/")]

# <codecell>

items=root.xpath("//rss:item",namespaces=ns)

# <codecell>

items

# <codecell>

def tagdict(x,y):
    x[y[0]]=x.get(y[0],"")+y[1]+" "
    return x

def process_item(i):
    link=i.xpath("./rss:link",namespaces=ns)[0].text
    title=i.xpath("./rss:title",namespaces=ns)[0].text.split("|")[0].strip().encode("utf-8")
    tags=[re.search("/t:([a-zA-Z0-9:]+)$",n.attrib["{http://www.w3.org/1999/02/22-rdf-syntax-ns#}resource"]).group(1) for n in i.xpath("./taxo:topics/rdf:Bag/rdf:li",namespaces=ns)]
    r=reduce(tagdict,[(j[0],j[1]) for j in filter(lambda x: len(x)>1, [i.split(":") for i in tags])],{})
    r["link"]=link
    r["title"]=title
    return r

# <codecell>

courses=[process_item(i) for i in items]

# <codecell>

import csv
f=open("tagged-courses.csv","wb")
w=csv.DictWriter(f,delimiter=",",fieldnames=["title","link","course","theme","level","skill","skilll","tool","topic","media","audience","meta"])
for c in courses:
    w.writerow(c)
f.close()

# <codecell>



# <codecell>

courses

# <codecell>


