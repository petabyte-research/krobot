import os
import hashlib
import web
import lxml.etree
import jinja2
import re
import datetime

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
		files = []
		for id in data:
			files.append({
				"id": id,
				"filename": id.split('::')[0],
				"uploaded": id.split('::')[1],
				"elcount": len(process().get_elements(id))
			})
		return t.render({ "active": 0,"files": list(reversed(files)) })

	def POST(self):
		x = web.input(file={})
		content = x['file'].file.read()
		h = x['file'].filename.split('/')[-1] + '::' + datetime.datetime.now().strftime("%Y.%m.%d. %H:%M.%S")
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
			return t.render({ "id": id, "active": 2, "filename": id.split("::")[0] })

		t=e.get_template('process.html')
		dd = dict(((i.tag, i.text) for i in el[0].getchildren()))
		dd['active'] = 1
		dd['count'] = len(el)
		dd['filename'] = id.split("::")[0]
		return t.render(dd)

	def POST(self,id):
		x = web.input()
		el = self.get_elements(id)

		""" if taxnr is defined well add it """
		if re.match("[0-9\\-]{8,}", x['taxnr']):
			ae=lxml.etree.Element('tax_nr')
			ae.text=x['taxnr']
			el[0].append(ae)

		""" if the orgid is defined add it """
		if re.match("\\d+", x['orgid']):
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

		return d.xpath(
			"//buyer[not(org_id) and not(tax_nr)]") + d.xpath(
			"//seller[not(org_id) and not(tax_nr)]") + d.xpath(
			"//tender[not(org_id) and not(tax_nr)]")


class download:
	def GET(self,id):
		d = data.get(id,None)
		""" redirect to index if data is not there """
		if not d:
			raise web.seeother('/')

		web.header('Content-Type', 'application/xml')
		web.header('Content-disposition', 'attachment; filename=%s'%id.split("::")[0])
		return lxml.etree.tostring(data[id])


if __name__=="__main__":
	app = web.application(urls, globals())
	app.run()
