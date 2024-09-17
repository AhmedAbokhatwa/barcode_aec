

frappe.query_reports["Accounts Tree"] = {
	"filters": [

    {
        "fieldname":"company",
        "label": __("Company"),
        "fieldtype": "Link",
        "options": "Company",
        "reqd": 1,
        "default": frappe.defaults.get_user_default("Company")
    },
    
],
"initial_depth": 0,
"tree": true,
"parent_field": "parent_account",
"name_field": "account"
};
