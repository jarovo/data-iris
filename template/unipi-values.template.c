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

struct ptable_struct {
	int id;
	const char *name;
};

struct pstable_struct {
	int id;
	int slot;
	const char *name;
};

const struct ptable_struct ftable[] = {
{%- for f,v in platform.family.items() %}
  { .id={{ "0x%02x" % v }}, .name="{{ f|lower }}" },
{%- endfor %}
  {/* sentinel */}
};

const struct ptable_struct itable[] = {
{%- for f,v in platform.id.items() %}
  { .id={{ "0x%04x" % v }}, .name="{{ f|lower }}" },
{%- endfor %}
  {/* sentinel */}
};

const struct ptable_struct btable[] = {
{%- for f,v in board.model.items() %}
  { .id={{ "0x%04x" % v }}, .name="{{ f|lower }}" },
{%- endfor %}
  {/* sentinel */}
};

const struct ptable_struct ptable_dt[] = {
{%- for f,v in product_dt.items() %}
  { .id={{ f }}, .name="{{ v }}" },
{%- endfor %}
  {/* sentinel */}
};

const struct pstable_struct btable_dt[] = {
{%- for f,x in board_dt.items() %}
  {%- for s,v in x.items() %}
  { .id={{ f }}, .slot={{s}}, .name="{{ v }}" },
  {%- endfor %}
{%- endfor %}
{/* sentinel */}
};

static int ptable_by_name(char *name, const struct ptable_struct *table)
{
	const struct ptable_struct *p;
	for (p=table; p->name != NULL; p++) {
		if (strcasecmp(name, p->name) == 0) return p->id;
	}
	return -1;
}

static const char* ptable_by_id(int id, const struct ptable_struct *table)
{
	const struct ptable_struct *p;
	for (p=table; p->name != NULL; p++) {
		if (p->id == id) return p->name;
	}
	return NULL;
}

int unipi_family_by_name(char *name)
{
	return ptable_by_name(name, ftable);
}

const char* unipi_family_by_id(int id)
{
	return ptable_by_id(id, ftable);
}

int unipi_platform_by_name(char *name)
{
	return ptable_by_name(name, itable);
}

const char* unipi_platform_by_id(int id)
{
	return ptable_by_id(id, itable);
}

int unipi_board_by_name(char *name)
{
	return ptable_by_name(name, btable);
}

const char* unipi_board_by_id(int id)
{
	return ptable_by_id(id, btable);
}
