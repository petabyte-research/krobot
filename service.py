import os
import hashlib
import web
import lxml.etree
import jinja2

e=jinja2.Environment(loader=jinja2.FileSystemLoader('templates'));

urls= ( 
    '/', 'index',
    '/file/(.+)', 'process',
    '/download/(.+)', 'download',
    )

data= {}

class index:
    """ handle requests to the page """
    def GET(self):
        t=e.get_template("index.html")
        return t.render()

    def POST(self):
        x = web.input(file={})
        content = x['file'].file.read()
        h = hashlib.md5(content).hexdigest()
        data[h]=lxml.etree.fromstring(content)
        raise web.seeother('/file/%s'%h)

class process:
    """ process an  id """
    def GET(self, id):
        d = data.get(id,None)
        if not d:
            raise web.seeother('/')
        
        el = self.get_elements(id)
        if len(el) == 0:
            t=e.get_template('done.html')
            return t.render({"id":id})
        
        t=e.get_template('process.html')
        workon = el[0]
        dd = dict(((i.tag, i.text) for i in el[0].getchildren()))

        return t.render(dd)
    
    def POST(self,id):
        x = web.input()
        d = data.get(id,None)
        if not d:
            raise web.seeother('/')
        
        el = self.get_elements(id)
        ae=lxml.etree.Element('tax_nr')
        ae.text=x['taxnr']
        el[0].append(ae)
        if x['orgid']!='':
            ae=lxml.etree.Element('org_id')
            ae.text=x['orgid']
            el[0].append(ae)
        return self.GET(id)

    def get_elements(self,id):
        d = data.get(id,None)
        if not d:
            raise web.seeother('/')
        
        return d.xpath("//buyer[not(org_id) and not(tax_nr)]") + d.xpath(
            "//seller[not(org_id) and not(tax_nr)]")
        

class download:
    def GET(self,id):
        d = data.get(id,None)
        if not d:
            raise web.seeother('/')

        web.header('Content-Type', 'application/xml')
        return lxml.etree.tostring(data[id])


if __name__=="__main__":
    app = web.application(urls, globals())
    app.run()
