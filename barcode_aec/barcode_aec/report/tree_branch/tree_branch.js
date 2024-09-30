// Copyright (c) 2024, ds and contributors
// For license information, please see license.txt
/* eslint-disable */

frappe.query_reports["tree branch"] = {
	"filters": [
		{
			"label": __("Accounts"),
			"fieldname": "name",
			"fieldtype": "Data",
			"width": 200,
		},
		{
			fieldname:'blance',
			label:__('Balance'),
			fieldtype:'Link',
			options:'Currency',
		},
	],
	// add_card_button_to_toolbar() {
	// 	if (!frappe.model.can_create("Number Card")) return;
	// 	this.page.add_inner_button(__("Create Card"), () => {
	// 		this.add_card_to_dashboard();
	// 	});
	// }
	
};
