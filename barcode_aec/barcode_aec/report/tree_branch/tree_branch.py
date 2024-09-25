# Copyright (c) 2024, ds and contributors
# For license information, please see license.txt

import frappe
from frappe import _


def execute(filters=None):
	columns = get_columns()
	data = get_branch()
	return columns, data



def get_branch():
    branches = [
        {'name': 'جميع الفروع', 'parent_branch': 'none', 'is_group': 1, 'indent': 0},
        {'name': 'Cairo USD', 'parent_branch': 'جميع الفروع', 'USD': '1000', 'is_group': 0, 'indent': 0},
        {'name': 'Cairo EUR', 'parent_branch': 'جميع الفروع', 'EUR': '1000', 'is_group': 0, 'indent': 0},
        {'name': 'tellers', 'parent_branch': 'جميع الفروع', 'is_group': 1, 'indent': 0},
        {'name': 'teller USD', 'parent_branch': 'tellers', 'USD': '1000', 'is_group': 0, 'indent': 0},
        {'name': 'teller EUR', 'parent_branch': 'tellers', 'EUR': '1000', 'is_group': 0, 'indent': 0},      
    ]
    
    def add_indent(branch, indent):
        branch['indent'] = indent
        for child in branches:
            if child['parent_branch'] == branch['name']:  # Correct the branch name access
                add_indent(child, indent + 1)

    # Loop through branches to set indentations for groups
    for branche in branches:
        if branche['is_group']:
            add_indent(branche, branche['indent'])

    # Return the modified branches for verification
    return branches



def get_columns():
	columns = [
		{
			"label": _("Accounts"),
			"fieldname": "name",
			"fieldtype": "Data",

			"width": 200,
		},
	
	]


	return columns
