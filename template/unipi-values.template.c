/******************************************************************
 *
 *  {{ warning }}
 *
 * uniee_values.c
 *
 *  Created on: Jan 14, 2022
 *      Author: Miroslav Ondra <ondra@faster.cz>
 * 
 */
#include <strings.h>
#include <stddef.h>
#include "uniee.h"

struct slot_dt {
	int slot;
	const char *dt;
};

struct id_name {
	int id;
	const char *name;
	const char *dt;
	const struct slot_dt *slots;
};


struct id_slot_name {
	int id;
	int slot;
	const char *name;
	const char *dt;
};

/* board + slot --> overlays */
{%- for f,x in board_dt.items() %}
const struct slot_dt c_slot_{{f}}[] = {
  {%- for s,v in x.items() %}
  { .slot={{s}}, .dt="{{ v }}" },
  {%- endfor %}
  {/* sentinel */}
};
{%- endfor %}

/* Family names*/
const struct id_name family_table[] = {
{%- for f,v in platform.family.items() %}
  { .id={{ "0x%02x" % v }}, .name="{{ f }}" },
{%- endfor %}
  {/* sentinel */}
};

/* product --> name, overlays */
const struct id_name product_table[] = {
{%- for f,v in platform.id.items() %}
  { .id={{ "0x%04x" % v }}, .name="{{ f }}"
    {%- if v|trim in product_dt -%}
    , .dt="{{ product_dt[v|trim] }}"
    {%- endif -%}
  },
{%- endfor %}
  {/* sentinel */}
};

/* board --> name, overlays, slots */
const struct id_name board_table[] = {
{%- for f,v in board.model.items() %}
  { .id={{ "0x%04x" % v }}, .name="{{ f }}"
    {%- if v|trim in board_dt -%}
    , .slots=c_slot_{{v}}
    {%- endif -%}
    {#- %- if v|trim in board_dt -%}
    , .dt="{{ board_dt[v|trim] }}"
    {%- endif -%  -#}
  },
{%- endfor %}
  {/* sentinel */}
};

static const struct id_name* get_by_name(char *name, const struct id_name *table)
{
	const struct id_name *p;
	for (p=table; p->name != NULL; p++) {
		if (strcasecmp(name, p->name) == 0) return p;
	}
	return NULL;
}

static const struct id_name* get_by_id(int id, const struct id_name *table)
{
	const struct id_name *p;
	for (p=table; p->name != NULL; p++) {
		if (p->id == id) return p;
	}
	return NULL;
}

static const struct slot_dt* get_by_slot(int slot, const struct slot_dt *table)
{
	const struct slot_dt *p;
	for (p=table; p->dt != NULL; p++) {
		if (p->slot == slot) return p;
	}
	return NULL;
}

int unipi_family_by_name(char *name)
{
	const struct id_name *p = get_by_name(name, family_table);
	return p ? p->id : -1;
}

const char* unipi_family_name(platform_id_t id)
{
	const struct id_name *p = get_by_id(id.parsed.platform_family, family_table);
	return p ? p->name : NULL;
}

int unipi_product_by_name(char *name)
{
	const struct id_name *p = get_by_name(name, product_table);
	return p ? p->id : -1;
}

const char* unipi_product_name(platform_id_t id)
{
	const struct id_name *p = get_by_id(id.raw_id, product_table);
	return p ? p->name : NULL;
}

const char* unipi_product_dt(platform_id_t id)
{
	const struct id_name *p = get_by_id(id.raw_id, product_table);
	return p ? p->dt : NULL;
}

const char* unipi_board_name(board_model_t id)
{
	const struct id_name *p = get_by_id(id, board_table);
	return p ? p->name : NULL;
}

const char* unipi_board_dt(board_model_t id)
{
	const struct id_name *p = get_by_id(id, board_table);
	return p ? p->dt : NULL;
}

const char* unipi_slot_dt(board_model_t id, int slot)
{
	const struct id_name *p = get_by_id(id, board_table);
	const struct slot_dt *d;
	if (p == NULL )
		return NULL;
	d = get_by_slot(slot, p->slots);
	return d ? d->dt : NULL;
}
