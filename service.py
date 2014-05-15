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
        try:
            data[h]=lxml.etree.fromstring(content)
        except lxml.etree.XMLSyntaxError as ex:
            t=e.get_template("index.html")
            return t.render({"error": """Error Parsing XML: %s"""%ex})
        raise web.seeother('/file/%s'%h)

class process:
    """ process an  id """
    def GET(self, id):
        el = self.get_elements(id)

        """ redirect to done if no more elements to work on """
        if len(el) == 0:
            t=e.get_template('done.html')
            return t.render({"id":id})
        
        t=e.get_template('process.html')
        workon = el[0]
        dd = dict(((i.tag, i.text) for i in el[0].getchildren()))

        return t.render(dd)
    
    def POST(self,id):
        x = web.input()
        el = self.get_elements(id)
        
        """ add tax_nr """
        ae=lxml.etree.Element('tax_nr')
        ae.text=x['taxnr']
        el[0].append(ae)

        """ if the orgid is defined add it """
        if x['orgid']!='':
            ae=lxml.etree.Element('org_id')
            ae.text=x['orgid']
            el[0].append(ae)
        
        """ return the next element """
        return self.GET(id)

    def get_elements(self,id):
        """ get the elements to work on """
        d = data.get(id,None)
        """ redirect to index if data is not there """
        if not d:
            raise web.seeother('/')
        
        return d.xpath("//buyer[not(org_id) and not(tax_nr)]") + d.xpath(
            "//seller[not(org_id) and not(tax_nr)]")
        

class download:
    def GET(self,id):
        d = data.get(id,None)
        """ redirect to index if data is not there """
        if not d:
            raise web.seeother('/')

        web.header('Content-Type', 'application/xml')
        web.header('Content-disposition', 'attachment; filename=%s.xml'%id)
        return lxml.etree.tostring(data[id])


if __name__=="__main__":
    app = web.application(urls, globals())
    app.run()
