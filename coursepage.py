import csv,urllib2
import pystache

key="0Aq9agjil66PydG9yelI0clFPMFJMaVE3M1gxMk9hV1E"

sort={"theme":["scoping","finding","getting","cleaning",
  "analyzing","visualizing","communicating","managing"],
    "level":["basic","advanced","pro"],
    "course":["DataFundamentals","IntroDataCleaning","IntroExploringData",
      "GentleIntroGeocoding","GentleIntroExtractingData",
      "SchoolOfDataJourn","WorkingWithBudgetAndSpendingData"],
     }

template="overview.html.tmpl"
outfile="courses.html"


url="https://docs.google.com/spreadsheet/pub?key=%s&single=true&gid=0&output=csv"%key


class Overview():
  def __init__(self,dimension,template="overview.html.tmpl",url=url):
    self.dimension=dimension
    self.template=template
    self.url=url
    u=urllib2.urlopen(url)
    r=csv.DictReader(u)
    self.data=[i for i in r]
    self.dim_levels=set(
      reduce(lambda x,y: x+y,
      (i[dimension].strip().split(" ") for i in self.data),[]))
    if dimension in sort.keys():
      s=sort[dimension]
      self.dim_levels=sorted([i for i in self.dim_levels],
        lambda x,y: s.index(x)-s.index(y))

  def modules_per_group(self,c):
    return {'name':c,
      'modules':[{"link":i['Link'], "title":i["Title"].decode("utf-8")} for i in
      filter(lambda x: c in x[self.dimension].split(), self.data)]
      }
  
  def render(self):
    groups=[self.modules_per_group(i) for i in self.dim_levels]
    f=open(self.template)
    return pystache.render(f.read(),{"groups":groups}).encode("utf-8")

if __name__=="__main__":
  import sys
  dimension=sys.argv[1]
  o=Overview(dimension)
  f=open(outfile,"wb")
  f.write(o.render())
  f.close()
