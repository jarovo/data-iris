from jinja2 import *

slot_params = {
		"11" :{"i2c":'9', "uart_a":1, "tty1":0, "uart_b":2, "tty2":1},
		"12" :{"i2c":'8', "uart_a":1, "tty1":0, "uart_b":4, "tty2":3},
		"21" :{"i2c":'a', "uart_a":1, "tty1":0, "uart_b":4, "tty2":3},
		"22" :{"i2c":'b', "uart_a":1, "tty1":0, "uart_b":2, "tty2":1},
		"32" :{"i2c":'c', },
		"42" :{"i2c":'d', },
		"52" :{"i2c":'e', },
}


def gener_dts(template, slots, dts):
	loader=FileSystemLoader(['.'])
	env = Environment(loader=loader)
	t = env.get_template(name=template)
	dtslist = []
	for slot in slots:
		params = slot_params[str(slot)]
		result = t.render(slot=slot, **params)
		with open('dts/%s-slot%s.dts' % (dts,slot), 'w') as f:
			f.write(result)
		dtslist.append("%s-slot%s.dts" % (dts,slot))

	return dtslist

def gener_bb(template, dts):
	loader=FileSystemLoader(['.'])
	env = Environment(loader=loader)
	t = env.get_template(name=template)
	dtslist = []
	result = t.render()
	with open('dts/%s.dts' % (dts), 'w') as f:
		f.write(result)
	dtslist.append("%s.dts" % (dts,))

	return dtslist

def gener_makefile(template, dtslist):
	loader=FileSystemLoader(['.'])
	env = Environment(loader=loader)
	t = env.get_template(name=template)
	result = t.render(dtslist=dtslist)
	with open('dts/Makefile', 'w') as f:
		f.write(result)


if __name__ == "__main__":
	dtslist = []
	dtslist += gener_dts("ic-0067.template", [11,12,21,22,32,42,52], "ic-0067")
	dtslist += gener_dts("ic-006a.template", [11,12,21,22], "ic-006a")
	dtslist += gener_dts("ic-006c.template", [11,12,21,22,32,42,52], "ic-006c")
	#dtslist += gener_dts("unipispi.template", [11,12,21,22,32,42,52], "unipispi")
	dtslist += gener_dts("ic-0074.template", [12,22,32,42], "ic-0074")

	dtslist += gener_bb("bb-010f.template", "bb-010f")
	dtslist += gener_bb("bb-020f.template", "bb-020f")
	dtslist += gener_bb("bb-030f.template", "bb-030f")

	gener_makefile("Makefile.template", dtslist)
