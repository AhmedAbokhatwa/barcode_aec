import frappe
from frappe import _
from frappe.model.document import Document
from frappe.client import get

import frappe

@frappe.whitelist(allow_guest=True)
def get_active_customer(name, condition_of_members, committees,ignore_permission=True):
    try:
        emails = []

        # Fetch customers based on condition_of_members
        customers = frappe.get_list(
            "Customer",
            filters={"custom_customer_status": condition_of_members},
            fields=["name", "custom_email"]
        )
        

                


        # for customer in customers:
        #     customer_name = customer.get("name")
            # print("Processing customer:", customer_name)
        customer_child = get(doctype="Customer",name='1')
        # print(customer_child)
        child = customer_child.get("custom_committees_you_would_like_to_join")
        
        for row in child:
            if committees == row.committees:
                print(row.committees)
                emails.append(customer_child.get("custom_email"))
                print("Length:", len(emails))

            # child = customer.get("custom_committees_you_would_like_to_join")
            # for row in child:
            #     if committees == row.committees:
            #         print(row.committees)    
            # Fetch committees customer wants to join
            # all_committees = frappe.db.get_list(
            #     "Committees you would like to join",
            #     filters={"parent": customer_name, "committees": committees},
            #     fields=["committees"],
            #     ignore_permissions=True,
                
            # )
            
            # if all_committees:
            #     emails.append(customer.get("custom_email"))
            #     print("Email added for customer:", customer_name)
            #     print("Length:", len(emails))
    
        return emails   
    except Exception as e:
        frappe.msgprint(_("Error: ") + str(e), indicator='red')
        frappe.log_error(str(e), _("Error in custom button action"))


# def get_customers(condition_of_members):
#     try:
#         return frappe.get_list(
#             "Customer",
#             filters={"custom_customer_status": condition_of_members},
#             fields=["name"]
#         )
#     except Exception as e:
#         frappe.msgprint(_("Error: ") + str(e), indicator='red')
#         frappe.log_error(str(e), _("Error in fetching customers"))

# def get_customer_names(customers):
#     try:
#         return [customer.get("name") for customer in customers]
#     except Exception as e:
#         frappe.msgprint(_("Error: ") + str(e), indicator='red')
#         frappe.log_error(str(e), _("Error in processing customer names"))
