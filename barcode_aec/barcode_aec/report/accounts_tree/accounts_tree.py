
import frappe
from frappe import _

def execute(filters=None):
	columns, data = [], []
	columns = get_columns()
	data = get_data()
	return columns, data

def get_accounts():
	return frappe.get_all(
		"Account",
		fields=["name", "parent_account", "is_group", "disabled"],
		order_by="lft",
	)


def get_data():
	accounts = get_accounts()
	update_indent(accounts)

	return accounts


def update_indent(accounts):
	for account in accounts:

		def add_indent(account, indent):
			account.indent = indent
			for child in accounts:
				if child.parent_account == account.name:
					add_indent(child, indent + 1)

		if account.is_group:
			add_indent(account, account.indent or 0)




def get_columns():
	columns = [
		{
			"label": _("Accounts"),
			"fieldname": "name",
			"fieldtype": "Link",
			"options": "Account",
			"width": 200,
		},
	
	]


	return columns