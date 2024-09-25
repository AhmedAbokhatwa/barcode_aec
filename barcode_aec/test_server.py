import frappe
from frappe import _

@frappe.whitelist()
def test(number, name):
    # root = TreeNode(number, name)
    
    # # Fetch children from the database
    # children = get_children(number)  # Function to retrieve children based on the number
    # for child in children:
    #     child_node = TreeNode(child.account_number, child.name)
    #     root.add_child(child_node)

    # # Serialize the tree structure
    # return root.serialize()
    return frappe.get_all('Account', filters={'parent_account': name}, fields=['account_number', 'name'])

def get_children(name):
    # Replace 'Account' and 'parent_field' with your actual doctype and field names
    return frappe.get_all('Account', filters={'parent_account': name}, fields=['is_group', 'account_number', 'name'])
    
class TreeNode:
    def __init__(self, number, name):
        self.number = number
        self.name = name
        self.children = []
    
    def add_child(self, child):
        self.children.append(child)
    
    def serialize(self):
        s = {
            "number": self.number,
            "name": self.name,
            "children": {}
        }
        for child in self.children:
            s["children"][child.name] = child.serialize()
        return s




################################################
################################################
################################################
################################################



@frappe.whitelist()
def get_data():
	accounts = get_accounts()
	update_indent(accounts)

	return accounts

def get_accounts():
	return frappe.get_all(
		"Account",
		fields=["name", "parent_account", "is_group", "disabled"],
		order_by="lft",
	)
 
@frappe.whitelist()
def get_data1():
    # Call the function to update indentation and return the result
    acc = update_indent()
    return acc

def update_indent():
    # , "is_group", "disabled"
    accounts = frappe.get_all(
        "Account",
        fields=["name", "parent_account"],
        order_by="lft"
    )

    # Define the inner function to add indentation
    def add_indent(account, indent):
        account.indent = indent
        for child in accounts:
            if child.parent_account == account.name:
                add_indent(child, indent + 1)

    # Loop through accounts to set indentations for groups
    for account in accounts:
        if account.is_group:
            add_indent(account, account.indent or 0)

    # Return the modified accounts for verification
    return accounts

        



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


################################################
################################################
################################################
################################################

@frappe.whitelist()
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
