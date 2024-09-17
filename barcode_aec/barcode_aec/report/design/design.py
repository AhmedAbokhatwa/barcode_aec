
import frappe
from frappe import _

def execute(filters=None):
    columns = get_columns()
    data = get_data(filters)

    return columns, data, None,

def get_columns():
    return [
        {"label": _("Designation"),"fieldname": "name","fieldtype": "Link","options": "Designation","width": 200,},
        {"label": _("Parent Designation"), "fieldname": "custom_parent_designation", "fieldtype": "Data", "width": 150},
        {"label": _("Department"), "fieldname": "custom_department", "fieldtype": "Data", "width": 150},
        {"label": _("Branch"), "fieldname": "branch", "fieldtype": "Data", "width": 150},
        {"label": _("HC"), "fieldname": "total", "fieldtype": "Int", "width": 150},
        {"label": _("Current"), "fieldname": "current", "fieldtype": "Int", "width": 150},
        {"label": _("Vacancies"), "fieldname": "vacancies", "fieldtype": "Int", "width": 150},
    ]
def get_designation():
    return frappe.get_all(
        "Designation",
        fields=["name", "custom_parent_designation", "custom_department"],
    )
    
def get_data(filters):
    name = filters.get('name')
    custom_department = filters.get('custom_department')
    # branch = filters.get('branch')
    custom_code_ = filters.get('custom_code_')

    designations = get_designation()
    # Build a dictionary for easy look-up
    designations_dict = {d['name']: {'name': d['name'],'custom_department':d['custom_department'], 'children': []} for d in designations}

    # Organize designations into a tree structure
    root_designations = []
    for designation in designations:
        name = designation['name']
        parent = designation['custom_parent_designation']
        if parent:
            # Add this designation as a child of its parent
            if parent in designations_dict:
                designations_dict[parent]['children'].append(designations_dict[name])
        else:
            # If there's no parent, it's a root designation
            root_designations.append(designations_dict[name])
    
    # Flatten the tree structure with indentation
    flattened_data = flatten_tree(root_designations)
    return flattened_data

def flatten_tree(designations, indent=0):
    data = []
    
    for designation in designations:
        items = []
        print("sssssssssss",designation)
        designation_data = {
            'name': designation['name'],
            'custom_department': designation['custom_department'],
            'branch': items,
            'indent': indent
        }
        data.append(designation_data)
        
        # Recursively add children with increased indentation
        if 'children' in designation:
            data.extend(flatten_tree(designation['children'], indent + 1))
    
    return data













###################################################################


