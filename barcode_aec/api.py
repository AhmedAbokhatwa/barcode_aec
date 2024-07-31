import frappe
from frappe import _


@frappe.whitelist()
def get_items_per_department(department):
    item = frappe.qb.DocType("Item")
    item_department = frappe.qb.DocType("Item Department")
    item_default = frappe.qb.DocType("Item Default")
    items = frappe.qb.from_(item).join(item_department).on(
        item_department.parent == item.name).join(item_default).on(
            item.name == item_default.parent).select(
                item.name, item_default.expense_account).where(
                    item_department.department == department).where(
                        item.custom_is_budget == 1).distinct().run(
                            as_dict=True)

    return items


@frappe.whitelist()
def get_expected_price(item_name, price_list):
    expected = frappe.get_doc("")