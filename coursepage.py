import csv,urllib2
import pystache

key="0Aq9agjil66PydG9yelI0clFPMFJMaVE3M1gxMk9hV1E"

sort_default={"theme":["scoping","finding","getting","cleaning",
  "analyzing","visualizing","communicating","managing"],
    "level":["basic","advanced","pro"],
    "course":["DataFundamentals","IntroDataCleaning","IntroExploringData",
      "GentleIntroGeocoding","GentleIntroExtractingData",
      "SchoolOfDataJourn","WorkingWithBudgetAndSpendingData"],
     }

template="templates/overview.html"
outfile="courses.html"


url="https://docs.google.com/spreadsheet/pub?key=%s&single=true&gid=0&output=csv"%key


class Overview():
  def __init__(self,dimension,template="overview.html.tmpl",sort=None,sort_dim=None,url=url):
    self.dimension=dimension
    self.template=template
    self.url=url
    u=urllib2.urlopen(url)
    r=csv.DictReader(u)
    self.data=[i for i in r]
    self.sort_dim=sort_dim
    if sort:
      self.sort=sort
    else:
      self.sort=sort_default
    self.dim_levels=set(
      reduce(lambda x,y: x+y,
      (i[dimension].strip().split(" ") for i in self.data),[]))
    if dimension in self.sort.keys():
      s=self.sort[dimension]
      self.dim_levels=sorted([i for i in self.dim_levels], 
        key=lambda x: s.index(x))

  def modules_per_group(self,c):
    if self.sort_dim and self.sort_dim in self.sort.keys():
       s=self.sort[self.sort_dim]
       data=sorted(self.data, key=lambda x: (s.index(x[self.sort_dim]), x['Title']))
    else:    
      data=self.data
    return {'name':c,
      'modules':[{"link":i['Link'], "title":i["Title"].decode("utf-8")} for i in
      filter(lambda x: c in x[self.dimension].split(), data)]
      }
  
  def render(self):
    groups=[self.modules_per_group(i) for i in self.dim_levels]
    f=open(self.template)
    return pystache.render(f.read(),{"groups":groups}).encode("utf-8")

if __name__=="__main__":
  import sys
  dimension=sys.argv[1]
  o=Overview(dimension,sort_dim="theme")
  f=open(outfile,"wb")
  f.write(o.render())
  f.close()
