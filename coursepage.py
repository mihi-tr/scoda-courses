import csv,urllib2
import itertools
import pystache


class Overview():
  def __init__(self,data,dimension,template="overview.html.tmpl",sort=None,order=None,slice=None):
    self.dimension=dimension
    self.template=template
    self.data=data
    self.sort_dim=slice
    self.sort=sort
    self.order=order
    self.dim_levels=set(
      itertools.ifilter(lambda x: x!='',
      reduce(lambda x,y: x+y,
      (i[dimension].strip().split(" ") for i in self.data),[])))
    if slice:  
      s=map(lambda x: x['tag'],slice)
      self.dim_levels=sorted([i for i in self.dim_levels], 
        key=lambda x: s.index(x))

  def modules_per_group(self,c):
    if self.sort: 
       s=map(lambda x: x['tag'],self.sort)
       data=sorted(self.data, key=lambda x: (s.index(x[self.order]), x['Title']))
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
