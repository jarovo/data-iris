##########################################################################
#
#  {{ warning }}
#
#  uniee_values.py
#
#  Created on: Jan 14, 2022
#      Author: Miroslav Ondra <ondra@faster.cz>
# 
{% include "sss" ignore missing %}

class Product:
	def __init__(self, id, name, **kwargs):
		self.id = id
		self.name = name
		self.vars = kwargs

class Board:
	def __init__(self, id, name, slots, **kwargs):
		self.id = id
		self.name = name
		self.slots = slots
		self.vars = kwargs

class Slot:
	def __init__(self, slot, **kwargs):
		self.slot = slot
		self.vars = kwargs

products = {
{%- for pname,pid in platform.id.items() %}
  '{{ pid|int }}': Product({{ pid|int }}, '{{ pname }}'
    {%- if pid|trim in product_dt -%}
             {%- for k,v in product_dt[pid|trim].items() -%}, {{ k }}='{{ v }}' {% endfor -%}
    {%- endif -%}
    ),
{%- endfor %}
}

boards = {
{%- for bname,b_id in board.model.items() %}
  '{{ b_id|int }}': Board({{ b_id|int }}, '{{ bname }}'
    {%- if b_id|trim in board_dt -%}
    ,{
        {%- for s,sv in board_dt[b_id|trim].items() %}
             '{{s|int}}': Slot({{s|int}}
             {%- for k,v in sv.items() -%}, {{ k }}='{{ v }}' {% endfor -%}),
        {%- endfor %}
    }
    {#- %- if b_id|trim in board_dt -%}
    , dt="{{ board_dt[v|trim] }}"
    {%- endif -%  -#}
    {%- else -%}
    , None
    {%- endif -%}
           ),
{%- endfor %}
}

# Family names
family = {
{%- for f,v in platform.family.items() %}
  '{{ v|int }}': '{{ f }}',
{%- endfor %}
}

def unipi_product_info(product_id, version=None):
	''' return product_info or none '''
	return products.get(str(product_id), None)

def unipi_product_info_by_name(product_name, version=None):
	''' return product_info or none '''
	for k,v in products.items():
		if v.name.lower() == product_name.lower(): 
			return v
	return None

def unipi_board_info(board_id, slot=None, version=None):
	''' return board_info or None '''
	board_info = boards.get(str(board_id), None)
	if slot == None or board_info == None:
		return board_info
	if board_info.slots is None:
		return None
	return board_info.slots.get(str(slot), None)


def unipi_family_name(product_id):
	''' return family name or none '''
	return family.get(str(product_id & 0xff), None)

