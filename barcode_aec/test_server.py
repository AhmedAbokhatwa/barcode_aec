import frappe 
from datetime import datetime
from frappe.utils import now,today
from frappe import _
import time

# Define your background function to process the data
@frappe.whitelist()
def test():
    current_date = today()
    frappe.msgprint(_('Today ssis: {0} and my second is ').format(current_date))