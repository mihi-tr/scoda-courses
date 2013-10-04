import yaml
import pywordpress
from coursepage import Overview
import urllib2
import csv

class Bot():
  def __init__(self,configfile,wp_config="wordpress.ini"):
    self.config=yaml.safe_load(open(configfile))
    self.wp_config=wp_config
    self.data={}

  def render(self,page):
    if (page.get('order',None)):
      s=self.data[page['order']]
      sd=page['order']
    else:
      s=None
      sd=None
    slice=self.data[page['slice']]
    o=Overview(self.data[page['items']],page['slice'],
      template="templates/%s"%page['template'],
      sort=s,
      order=sd,
      slice=slice)
    f=open("_build/%s.html"%page['page'],"wb")
    f.write(o.render())
    f.close()

  def render_pages(self):
   for p in self.config['pages']:
    self.render(p)
  
  def load_data(self):
    for name,sheet in self.config['sheets'].items():
      self.load(name,sheet)
  
  def load(self,name,sheet):
    r=csv.DictReader(urllib2.urlopen(sheet))
    self.data[name]=[i for i in r]
    
  def upload_pages(self):
    for p in self.config['pages']:
      self.upload_page(p)

  def upload_page(self,p):
    pass

if __name__=="__main__":
  b=Bot("bot.yaml")
  b.load_data()
  b.render_pages()
  b.upload_pages()
