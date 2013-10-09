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
    wp=pywordpress.Wordpress.init_from_config(self.wp_config)
    pages=dict((("%s%s"%(self.config['bot']['prefix'],
      p['page']),
        self.prepare_page(p)) for p in self.config['pages']))
    wp.create_many_pages(pages)

  def prepare_page(self,page):
    with open("_build/%s.html"%page['page']) as f:
      return {"title": page['name'],
          'description': f.read(),
        'mt_allow_comments': 'open'}


if __name__=="__main__":
  b=Bot("bot.yaml")
  b.load_data()
  b.render_pages()
  b.upload_pages()
