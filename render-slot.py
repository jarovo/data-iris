#!/usr/bin/python3

from jinja2 import *
from jinja2.exceptions import TemplateNotFound

warning = "THIS FILE IS GENERATED FROM TEMPLATE. DON'T MODIFY IT"

class EDescriptionError(Exception):
	pass

def load_yaml_values(filename):
	import yaml

	with open(filename, 'r') as stream:
		data = yaml.load(stream, Loader=yaml.Loader)
	return data

class Exporter:

	def __init__(self, dtdir, udevdir):
		self.dtdir = dtdir
		if dtdir and dtdir[-1]!='/':
			self.dtdir += '/'
		self.udevdir = udevdir
		if udevdir and udevdir[-1]!='/':
			self.udevdir += '/'
		self.dtslist = []
		self.products = {}
		self.boards = {}

	def get_name(self, id, prefix="", slot=None):
		if slot==None:
			return "%s%04x" % (prefix, id)
		return "%s%04x_slot%d" % (prefix, id, slot)
		
	def write(self, name, content):
		with open(self.dtdir+name, 'w') as f:
			f.write(content)

	def writedts(self, name, content):
		self.write(name+".dts", content)
		self.dtslist.append(name+".dts")

	def writeudev(self, name, content):
		with open(self.udevdir+name+".rules", 'w') as f:
			f.write(content)

	def add_product(self, id, **kwargs):
		product = self.products.get(str(id), {})
		def appendstr(name,value):
			try:
				product[name] += " " + value
			except KeyError:
				product[name] = value
		for k,v in kwargs.items():
			if v: appendstr(k, v)
		self.products[str(id)] = product


	def add_board(self, id, slot, **kwargs):
		subdict = self.boards.get(str(id),{})
		slotdict = subdict.get(str(slot),{})
		def appendstr(name,value):
			try:
				slotdict[name] += " " + value
			except KeyError:
				slotdict[name] = value
		for k,v in kwargs.items():
			if v: appendstr(k, v)
		subdict[str(slot)] = slotdict
		self.boards[str(id)] = subdict


def render_product_dt(p_id, p_desc, jinjaenv, exporter):
	t = jinjaenv.get_template(name=p_desc["template"])
	result = t.render(id=p_id)
	dtname = exporter.get_name(p_id, prefix="bb")
	exporter.writedts(dtname, result)
	exporter.add_product(p_id, dt=dtname)

def render_product_udev(p_id, p_desc, jinjaenv, exporter):
	t = jinjaenv.get_template(name=p_desc["udev"])
	result = t.render(id=p_id)
	udevname = exporter.get_name(p_id, prefix="bb")
	exporter.writeudev(udevname, result)
	exporter.add_product(p_id, udev=udevname)


def render_board_dt(b_id, b_desc, prefix, description, jinjaenv, exporter):
	t = jinjaenv.get_template(name=b_desc["template"])
	for slot in b_desc["slot"]:
		params = description["slot"][str(slot)]
		result = t.render(id=b_id, slot=slot, **params)
		dtname = exporter.get_name(b_id, prefix=prefix, slot=slot)
		exporter.writedts(dtname, result)
		exporter.add_board(b_id, slot, dt=dtname)

def render_board_udev(b_id, b_desc, prefix, description, jinjaenv, exporter):
	t = jinjaenv.get_template(name=b_desc["udev"])
	for slot in b_desc["slot"]:
		params = description["slot"][str(slot)]
		result = t.render(id=b_id, slot=slot, **params)
		udevname = exporter.get_name(b_id, prefix=prefix, slot=slot)
		exporter.writeudev(udevname, result)
		exporter.add_board(b_id, slot, udev=udevname)


def gener_by_desc(description, uniee_data, jinjaenv, exporter):

	data_platform = uniee_data["platform"]["id"]
	for product, p_desc in description["product"].items():
		try:
			p_id = data_platform[product]
		except KeyError as E:
			raise EDescriptionError('Invalid value for product name "%s"'% product) from None

		if not isinstance(p_desc, dict): continue
		if "template" in p_desc:
			render_product_dt(p_id, p_desc, jinjaenv, exporter)
		if "udev" in p_desc:
			render_product_udev(p_id, p_desc, jinjaenv, exporter)
		if ("options" in p_desc) and isinstance(p_desc["options"], dict):
			exporter.add_product(p_id, **p_desc["options"])

	data_board = uniee_data["board"]["model"]
	for board, b_desc in description["board"].items():
		try:
			b_id = data_board[board]
		except KeyError as E:
			raise EDescriptionError('Invalid value for board name "%s"'% board) from None
		prefix = board[:2].lower()

		if not isinstance(b_desc, dict): continue
		if "template" in b_desc:
			render_board_dt(b_id, b_desc, prefix, description, jinjaenv, exporter)
		if "udev" in b_desc:
			render_board_udev(b_id, b_desc, prefix, description, jinjaenv, exporter)
		if ("options" in b_desc) and isinstance(b_desc["options"], dict):
			for slot in b_desc["slot"]:
				exporter.add_board(b_id, slot, **b_desc["options"])


def gener_library(jinjaenv, uniee_data, exporter):
	t = jinjaenv.get_template(name="unipi-values.template.c")
	result = t.render(product_dt=exporter.products, board_dt=exporter.boards, warning=warning, **uniee_data)
	with open("unipi-values.c", 'w') as f:
		f.write(result)

def gener_pylibrary(jinjaenv, uniee_data, exporter):
	t = jinjaenv.get_template(name="unipi-values.template.py")
	result = t.render(product_dt=exporter.products, board_dt=exporter.boards, warning=warning, **uniee_data)
	with open("unipi_values.py", 'w') as f:
		f.write(result)

def gener_makefile(jinjaenv, exporter):
	t = jinjaenv.get_template(name="Makefile.template")
	result = t.render(dtslist=exporter.dtslist)
	exporter.write("Makefile", result)


if __name__ == "__main__":
	import argparse, sys
	a = argparse.ArgumentParser(prog='render-slot.py')
	a.add_argument('description', metavar="file", help='input yaml description', type=str, nargs=1)
	a.add_argument('-d','--data', metavar="file", help='uniee_values data yaml')
	a.add_argument('-t','--templates', metavar="directory", help='Template directory')
	a.add_argument('-o','--output', metavar="directory", help='Output directory')
	args = a.parse_args()
	datafile = args.data if args.data else "unipi-hardware-id/values/uniee_values.yaml"
	templates = args.templates if args.templates else "template"

	loader=FileSystemLoader(searchpath=templates)
	jinjaenv = Environment(loader=loader)

	outdir = args.output if args.output else "overlays"
	exporter = Exporter(outdir, "udev")

	uniee_data = load_yaml_values(datafile)

	description = load_yaml_values(args.description[0])
	try:
		gener_by_desc(description, uniee_data, jinjaenv, exporter)
		gener_makefile(jinjaenv, exporter)
		gener_library(jinjaenv, uniee_data, exporter)
		gener_pylibrary(jinjaenv, uniee_data, exporter)
		sys.exit(0)

	except EDescriptionError as E:
		print(str(E))
	except TemplateNotFound as E:
		print('TemplateError: %s not found' % str(E))
	sys.exit(1)
