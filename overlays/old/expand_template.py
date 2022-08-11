from jinja2 import *

uarts = {
		"11":{"uart1":1, "tty1":0, "uart2":2, "tty2":1},
		"12":{"uart1":1, "tty1":0, "uart2":4, "tty2":3},
		"21":{"uart1":1, "tty1":0, "uart2":4, "tty2":3},
		"22":{"uart1":1, "tty1":0, "uart2":2, "tty2":1},
		"32" :{},
		"42" :{},
		"52" :{},
}


def gener_dts(template, slots, dts):
	loader=FileSystemLoader(['.'])
	env = Environment(loader=loader)
	t = env.get_template(name=template)

	for slot in slots:
		uart = uarts[str(slot)]
		result = t.render(slot=slot, **uart)
		with open(dts+'-slot%s.dts' % slot, 'w') as f:
			f.write(result)
	


if __name__ == "__main__":
	gener_dts("ic-0067.template", [11,12,21,22,32,42,52], "ic-0067")
	gener_dts("ic-006a.template", [11,12,21,22], "ic-006a")
	gener_dts("ic-006c.template", [11,12,21,22,32,42,52], "ic-006c")
	gener_dts("unipispi.template", [11,12,21,22,32,42,52], "unipispi")
