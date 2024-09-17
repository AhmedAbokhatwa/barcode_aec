// Copyright (c) 2024, ds and contributors
// For license information, please see license.txt
/* eslint-disable */

frappe.query_reports["design"] = {
	"filters": [
        {
            "fieldname":"company",
            "label": __("Company"),
            "fieldtype": "Link",
            "options": "Company",
            "reqd": 1,
            "default": frappe.defaults.get_user_default("Company")
        },
		{   fieldname:"custom_department",
			label:"Department",
			fieldtype:"Link",
			options:"Department",
			width:"300px"
		
		},
		{   fieldname:"branch",
			label:"Branch",
			fieldtype:"Link",
			options:"Branch",
			width:"300px"
		
		},
		{   fieldname:"custom_code_",
			label:"Code",
			fieldtype:"Data",
			width:"300px"
		
		},
		// {   fieldname:"custom_open_job_opening",
		// 	label:"custom_open_job_opening",
		// 	fieldtype:"Data",
		// 	width:"300px"
		
		// }
        
    ],
    "initial_depth": 0,
    "tree": true,
    "parent_field": "parent_designation",
    "name_field": "designation"
    };



