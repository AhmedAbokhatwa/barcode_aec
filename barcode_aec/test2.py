import frappe 
from datetime import datetime
from frappe import _
import time
from frappe.desk.doctype.bulk_update.bulk_update import _bulk_action
from frappe.desk.doctype.bulk_update.bulk_update import submit_cancel_or_update_docs
# Define your background function to process the data
@frappe.whitelist()
def process_data():
    all_customer = frappe.db.sql_list("""
        SELECT
            `name`,`custom_tax_id_3`
         FROM
            `tabCustomer` limit 20
        """, as_dict=1)

    n = len(all_customer)
    docnames = all_customer
    doctype = 'Customer'
    action="update"
    data = {'custom_tax_id_3': 1000}
    if n < 500 :
        # return 'yes'
        return submit_cancel_or_update_docs(doctype, docnames, action= action, data =data)
        # for i,doc in enumerate (all_customer):
        #     existing_doc = frappe.get_doc(doctype, doc["name"])
            
        # show_progress(all_customer, _("Validating Customers"), i + 1, _("Processed {0}").format(doc['name']),hide_on_completion= True)
    # show_progress(all_customer, _("Validation Complete!"), n, _("All customers processed"))
        # print(enumerate (all_customer))
        # docnames = frappe.parse_json(all_customer)
        # return docnames
        

def submit_cancel_or_update_docs(doctype, docnames, action="update", data=None):
	if isinstance(docnames, str):
		docnames = frappe.parse_json(docnames)

	if len(docnames) < 20:
		return _bulk_action(doctype, docnames, action, data)
	elif len(docnames) <= 500:
		frappe.msgprint(_("Bulk operation is enqueued in background."), alert=True, indicator="green",
		)
		frappe.enqueue(
			_bulk_action,
			doctype=doctype,
			docnames=docnames,
			action=action,
			data=data,
			queue="long",
			timeout=3000,
		)
        
	else:
		frappe.throw(_("Bulk operations only support up to 500 documents."), title=_("Too Many Documents"))


def _bulk_action(doctype, docnames, action, data):
	if data:
		data = frappe.parse_json(data)

	failed = []

	for i, d in enumerate(docnames, 1):
		doc = frappe.get_doc(doctype, d)
		try:
			message = ""
			if action == "submit" and doc.docstatus.is_draft():
				doc.submit()
				message = _("Submitting {0}").format(doctype)
			elif action == "cancel" and doc.docstatus.is_submitted():
				doc.cancel()
				message = _("Cancelling {0}").format(doctype)
			elif action == "update" and not doc.docstatus.is_cancelled():
				doc.update(data)
				doc.save()
				message = _("Updating {0}").format(doctype)
			else:
				failed.append(d)
			frappe.db.commit()
			show_progress(docnames, message, i, d)

		except Exception:
			failed.append(d)
			frappe.db.rollback()

	return failed        



def show_progress(all_customer, message, i, description, hide_on_completion= True):
    n = len(all_customer)
    frappe.publish_progress(float(i) * 100 / n, title=message, description=description, hide_on_completion= True)
 
 
    # counter = 0
    # for emp in all_customer:
    #     doc = frappe.get_doc("Customer", emp.name)
    #     counter += 1
    #     frappe.publish_progress(counter * 100 / num, title=_("Updating ..."))
    #     tax_id = emp.tax_id
    #     member_name = emp.customer_name
    #     if tax_id:
    #         vol = volume_of_member_exports_last_year(tax_id)
    #         if not vol:
    #             vol = volume_of_member_exports_two_years(tax_id)
    #             if not vol:
    #                 vol = volume_of_member_exports_three_years(tax_id)
    #                 if not vol:
    #                     frappe.msgprint("This member has no tax id {}".format(member_name))
    #         # if vol:
    #         #     # if vol[0]['total']:
    #         #     customer_group_for_last_year = get_customer_group(vol[0]['total'])
    #         #     if customer_group_for_last_year:
    #         #         customer_group_name = customer_group_for_last_year[0]['name']

    #         #         doc.customer_group = customer_group_name
    #         #         doc.custom_volume_of__exports =  vol[0]['total']
    #                 # doc.save()
    #                 # emp.customer_group = customer_group_name
    #                 # emp.custom_volume_of__exports = vol[0]['total']
    #                 # frappe.db.set_value("Customer", emp.name, "customer_group", customer_group_name)
    #                 # frappe.db.set_value("Customer", emp.name, "custom_volume_of__exports", vol[0]['total'])
    #                 # frappe.db.commit()
    #     last =volume_of_member_exports_last_year(tax_id)
    #     if tax_id and last:
    #         customer_group_for_last_year = get_customer_group(vol[0]['total'])
    #         if customer_group_for_last_year:
    #             customer_group_name = customer_group_for_last_year[0]['name']
    #             emp.customer_group = customer_group_name
    #             emp.custom_volume_of__exports = last[0]['total']

    #     # vol = volume_of_member_exports_last_year(tax_id)
    #     # if vol:
    #     #         # if vol[0]['total']:
    #     #     customer_group_for_last_year = get_customer_group(vol[0]['total'])
    #     #     if customer_group_for_last_year:
    #     #         customer_group_name = customer_group_for_last_year[0]['name']
    #     #         doc.customer_group = customer_group_name
    #     #         doc.custom_volume_of__exports = vol[0]['total']

    #             # frappe.db.set_value("Customer", emp.name, "customer_group", customer_group_name)
    #             # frappe.db.set_value("Customer", emp.name, "custom_volume_of__exports", vol[0]['total'])
    #             # doc.customer_group = customer_group_name
    #             # doc.custom_volume_of__exports =  vol[0]['total']
    #     doc.set('volume_of_member_exports_for_three_years', [])



        
    #     tot_last_year = volume_of_member_exports_last_year(tax_id)
    #     if tot_last_year != 0:
    #         doc.append("volume_of_member_exports_for_three_years" , {
    #             'season': tot_last_year[0]['season'],
    #             'value': tot_last_year[0]['total'],
    #             'season_name' :tot_last_year[0]['season_name'],
    #             'total_amount_in_usd':tot_last_year[0]['total_amount_in_usd'],
    #             'quantity_in_tons' : tot_last_year[0]['quantity_in_tons'],
    #             'total_amount_in_egp': tot_last_year[0]['total']
    #         })
    #         # customer_group_for_last_year = get_customer_group(vol[0]['total'])
    #         # if customer_group_for_last_year:
    #         #     emp.customer_group = customer_group_for_last_year[0]['name']
    #         #     emp.custom_volume_of__exports = tot_last_year[0]['total']

    #     tot_two_year = volume_of_member_exports_two_years(tax_id)
    #     if tot_two_year != 0:
    #         doc.append("volume_of_member_exports_for_three_years" , {
    #             'season': tot_two_year[0]['season'],
    #             'value': tot_two_year[0]['total'],
    #             'season_name' :tot_two_year[0]['season_name'],
    #             'total_amount_in_usd':tot_two_year[0]['total_amount_in_usd'],
    #             'quantity_in_tons' : tot_two_year[0]['quantity_in_tons'],
    #             'total_amount_in_egp': tot_two_year[0]['total']
    #         })
    #     tot_last_three_year = volume_of_member_exports_three_years(tax_id)
    #     if tot_last_three_year != 0:
    #         doc.append("volume_of_member_exports_for_three_years" , {
    #             'season': tot_last_three_year[0]['season'],
    #             'value': tot_last_three_year[0]['total'],
    #             'season_name' :tot_last_three_year[0]['season_name'],
    #             'total_amount_in_usd':tot_last_three_year[0]['total_amount_in_usd'],
    #             'quantity_in_tons' : tot_last_three_year[0]['quantity_in_tons'],
    #             'total_amount_in_egp': tot_last_three_year[0]['total']
    #         })
        
    #     # vol2 = volume_of_member_exports_last_year(tax_id)
    #     # if vol2:
    #     #         # if vol[0]['total']:
    #     #     customer_group_for_last_year = get_customer_group(vol2[0]['total'])
    #     #     if customer_group_for_last_year:
    #     #         customer_group_name = customer_group_for_last_year[0]['name']
    #     #         frappe.db.set_value("Customer", emp.name, "customer_group", customer_group_name)
    #     #         frappe.db.set_value("Customer", emp.name, "custom_volume_of__exports", vol2[0]['total'])
                
    #     #         # doc.customer_group = customer_group_name
    #     #         # doc.custom_volume_of__exports = vol2[0]['total']
    #     #         # doc.save()
    #     doc.save()
    #     frappe.db.commit()
    #     time.sleep(0.5)

# @frappe.whitelist()
# def functiongdidaa():
#     # Enqueue the background function
#     frappe.enqueue(method=process_data, queue='long')

#     # Return a message indicating that the process has started
#     return "Data processing started in the background."


        
# @frappe.whitelist()
# def update_customer(result , emp ,customer_group ):
#     for memo3 in customer_group:
#         if result['total'] > memo3.custom_from and result['total'] <= memo3.custom_to and memo3.customer_group_name != 'خدمي' :
#             frappe.db.set_value("Customer" , emp.name , "customer_group" , memo3.name)
#             frappe.db.set_value("Customer" , emp.name , "custom_volume_of__exports" , result.total)
            
# @frappe.whitelist()
# def get_customer_group(value):
#     data = frappe.db.sql("""
#         SELECT
#             `name`,
#             `custom_from`,
#             `custom_to`
#         FROM
#             `tabCustomer Group`
#         WHERE 
#             %s BETWEEN `custom_from` AND `custom_to`
#         """, (value), as_dict=1)

#     return data

# @frappe.whitelist()
# def volume_of_member_exports_three_years(tax_id):
#     data = frappe.db.sql("""
#         SELECT
#             `tax__number` AS `tax_id`,
#             `season__name` AS `season_name`,
#             `season` AS `season`,
#             SUM(`total_amount_in_egp`) AS `total`,
#             SUM(`total_amount_in_usd`) AS `total_amount_in_usd`,
#             SUM(`quantity_in_tons`) AS `quantity_in_tons`
#         FROM
#             `tabVolume Of Member Exports`
#         WHERE 
#             YEAR(`posring_date`) = YEAR(CURDATE()) - 3
#             AND tax__number = %s ;
#         """ , tax_id ,as_dict=1)
#     return data

# @frappe.whitelist()
# def volume_of_member_exports_two_years(tax_id):
#     data = frappe.db.sql("""
#         SELECT
#             `tax__number` AS `tax_id`,
#             `season__name` AS `season_name`,
#             `season` AS `season`,
#             SUM(`total_amount_in_egp`) AS `total`,
#             SUM(`total_amount_in_usd`) AS `total_amount_in_usd`,
#             SUM(`quantity_in_tons`) AS `quantity_in_tons`
#         FROM
#             `tabVolume Of Member Exports`
#         WHERE 
#             YEAR(`posring_date`) = YEAR(CURDATE()) - 2
#             AND tax__number =%s ;
#         """ , tax_id ,as_dict=1)
#     return data


# @frappe.whitelist()
# def volume_of_member_exports_last_year(tax_id):
    # data = frappe.db.sql("""
    #     SELECT
    #         `tax__number` AS `tax_id`,
    #         `season__name` AS `season_name`,
    #         `season` AS `season`,
    #         SUM(`total_amount_in_egp`) AS `total`,
    #         SUM(`total_amount_in_usd`) AS `total_amount_in_usd`,
    #         SUM(`quantity_in_tons`) AS `quantity_in_tons`
    #     FROM
    #         `tabVolume Of Member Exports`
    #     WHERE 
    #         YEAR(`posring_date`) = YEAR(CURDATE()) - 1
    #         AND tax__number =%s ;
    #     """ , tax_id ,as_dict=1)
    # return data
    
    
    
    
    
    
    
    
    
    #########################
    
@frappe.whitelist()    
def get_branch():
    branches = [
        {'name': 'جميع الفروع','currency_account':'EGP', 'parent_branch': 'none','balance': '100000', 'is_group': 1, 'indent': 0},
        {'name': 'Cairo USD', 'parent_branch': 'جميع الفروع','currency_account':'USD', 'balance': '1000', 'is_group': 0, 'indent': 0},
        {'name': 'Cairo EUR', 'parent_branch': 'جميع الفروع', 'currency_account':'EUR','balance': '1000', 'is_group': 0, 'indent': 0},
        {'name': 'tellers', 'currency_account':'EGP','parent_branch': 'جميع الفروع', 'is_group': 1, 'indent': 0},
        {'name': 'teller USD', 'parent_branch': 'tellers','currency_account':'USD', 'balance': '1000', 'is_group': 0, 'indent': 0},
        {'name': 'teller EUR', 'parent_branch': 'tellers', 'currency_account':'EUR','balance': '1000', 'is_group': 0, 'indent': 0},      
    ]
    # branch = 'جميع الفروع'
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
    return add_indent()