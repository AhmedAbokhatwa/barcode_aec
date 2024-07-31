# import frappe
# from frappe import _



# def execute(filters=None):
#     columns =get_columns()
#     data = get_data(filters)    
#     return columns, data



# def get_columns():
#     columns = [  
#     {"label": _("Member code"), "fieldname": "code_customer", "fieldtype": "Link", "options": "Customer", "width": 150},
    
#     {"label": _("Member"), "fieldname": "member", "fieldtype": "Link", "options": "Customer", "width": 150},
#       {"label": _("last invoice name"), "fieldname": "last_invoice_name", "fieldtype": "Link", "options": "Sales Invoice", "width": 200},
#     {"label": _("last invoice total "), "fieldname": "last_invoice_total", "fieldtype": "Data", "width": 200},
#     {"label": _("member group last inv "), "fieldname": "last_invoice_custom_customer_group", "fieldtype": "Data", "width": 200},
#     {"label": _("Rate Category for Invoice"), "fieldname": "price_list_rate_for_inv", "fieldtype": "Data", "width": 200},
#     {"label": _("TAX ID"), "fieldname": "tax__number", "fieldtype": "Data", "width": 80},
#     {"label": _("Year"), "fieldname": "year", "fieldtype": "Data", "width": 200},
#     {"label": _("EGY"), "fieldname": "total_amount_in_egp", "fieldtype": "Data", "width": 200},
#     {"label": _("Category for Exports Volume"), "fieldname": "price", "fieldtype": "Data", "width": 200}, 
#     {"label": _("rate"), "fieldname": "rate", "fieldtype": "Data", "width": 200},    
#     {"label": _("USD"), "fieldname": "total_amount_in_usd", "fieldtype": "Data", "width": 200},
#     {"label": _("Tons"), "fieldname": "quantity_in_tons", "fieldtype": "Data", "width": 200},
  
#     ]
#     return columns

# def get_data(filters):
#     conditions = []
#     params = {}

#     code_customer = filters.get("code_customer")

#     if code_customer:
#         conditions.append("tc.`name` = %(code_customer)s")
#         params["code_customer"] = code_customer

#     # product_name = filters.get("product_name")
#     # salutation_type = filters.get("salutation_type")
#     # custom_customer_status = filters.get("custom_customer_status")
#     # custom_company_type_ = filters.get("custom_company_type_")
#     # custom_customer_activity_type = filters.get("custom_customer_activity_type")
#     # custom_company_code = filters.get("custom_company_code")
#     # customer_name = filters.get("customer_name")
#     # territory = filters.get("territory")
#     # custom_joining_date = filters.get("custom_joining_date")
    

   


    
# ###3##################################################################3
#     sql =  """
#         SELECT 
#             tc.`name` AS code_customer,
#             tc.`customer_name` AS `member`,
#             COALESCE(tvme.`tax__number`, 'No Export') AS `tax__number`,
#             YEAR(CURDATE()) - 1 AS `year`,
#             SUM(tvme.`total_amount_in_egp`) AS `total_amount_in_egp`,
#             SUM(COALESCE(tvme.`total_amount_in_usd`, 0)) AS `total_amount_in_usd`,
#             SUM(COALESCE(tvme.`quantity_in_tons`, 0)) AS `quantity_in_tons`,
#             COALESCE(last_invoice.`last_invoice_name`, 'No Last Invoice') AS `last_invoice_name`,
#             COALESCE(last_invoice.`posting_date`, 'No Last Invoice') AS `last_invoice_posting_date`,
#             COALESCE(last_invoice.`custom_customer_group`, 'No Last Invoice') AS `last_invoice_custom_customer_group`,
#             COALESCE(last_invoice.`total`, 0) AS `last_invoice_total`,
#             COALESCE(last_invoice.`price_list_rate_for_inv`, 0) AS `price_list_rate_for_inv`,
#             CASE
#                 WHEN SUM(tvme.`total_amount_in_egp`) BETWEEN (
#                     SELECT MIN(tcg.custom_from) FROM `tabCustomer Group` AS tcg
#                 ) AND (
#                     SELECT MAX(tcg.custom_to) FROM `tabCustomer Group` AS tcg
#                 ) THEN (
#                     SELECT tcg.name
#                     FROM `tabCustomer Group` AS tcg
#                     WHERE SUM(tvme.total_amount_in_egp) BETWEEN tcg.custom_from AND tcg.custom_to
#                     LIMIT 1
#                 )
#                 ELSE ''
#             END AS `price`,
#             (
#                 SELECT tip.price_list_rate
#                 FROM `tabItem Price` AS tip
#                 JOIN `tabCustomer Group` AS tcg ON tcg.name = tip.custom_member_categories
#                 WHERE SUM(tvme.total_amount_in_egp) BETWEEN tcg.custom_from AND tcg.custom_to
#                 LIMIT 1
#             ) AS rate    


#         FROM
#             `tabCustomer` AS tc 
#         LEFT JOIN (
#             SELECT 
#                 tvme.`tax__number`,
#                 SUM(tvme.`total_amount_in_egp`) AS total_amount_in_egp,
#                 SUM(tvme.`total_amount_in_usd`) AS total_amount_in_usd,
#                 SUM(tvme.`quantity_in_tons`) AS quantity_in_tons,
#                 (
#                 SELECT 
#                     tip.price_list_rate
#                 FROM 
#                     `tabItem Price` AS tip
#                 JOIN 
#                     `tabCustomer Group` AS tcg ON tcg.name = tip.custom_member_categories
#                 WHERE 
#                     SUM(tvme.total_amount_in_egp) BETWEEN tcg.custom_from AND tcg.custom_to
#                 LIMIT 1
#             ) AS rate
#             FROM 
#                 `tabVolume Of Member Exports` AS tvme
#             WHERE 
#                 `year` = YEAR(CURDATE()) - 1
#             GROUP BY 
#                 tax__number
#         ) AS tvme ON tc.`tax_id` = tvme.`tax__number`
#         LEFT JOIN (
#             SELECT 
#                 tsi.name AS last_invoice_name,
#                 tsi.customer,
#                 tcg.name AS customer_group_name,
#                 tip.`price_list_rate` AS price_list_rate_for_inv,
#                 tcg.`custom_from` AS customer_group_from,
#                 tcg.`custom_to` AS customer_group_to, 
#                 tsi.posting_date,
#                 tsi.total,
#                 tsi.custom_customer_group,
#                 ROW_NUMBER() OVER (PARTITION BY tsi.customer ORDER BY tsi.creation DESC) AS rn
#             FROM 
#                 `tabSales Invoice` AS tsi 
#             LEFT JOIN
#                 `tabCustomer Group` AS tcg ON tcg.name = tsi.custom_customer_group
#             LEFT JOIN 
#                 `tabItem Price` AS tip ON tip.custom_member_categories = tcg.name
#            )    AS last_invoice ON tc.`name` = last_invoice.`customer` AND last_invoice.rn = 1
#            GROUP BY tc.`name`;
#                     """    
#          # Apply the conditions to the SQL query
#     if conditions:
#         sql += " WHERE " + " AND ".join(conditions)
    
#     # sql += ""

#     # Execute the query with the filter values
#     mydata = frappe.db.sql(sql, as_dict=True)
# #
#     return mydata

import frappe
from frappe import _

def execute(filters=None):
    columns = get_columns()
    data = get_data(filters)    
    return columns, data

def get_columns():
    columns = [
        {"label": _("Member code"), "fieldname": "code_customer", "fieldtype": "Link", "options": "Customer", "width": 150},
        {"label": _("Member"), "fieldname": "member", "fieldtype": "Link", "options": "Customer", "width": 150},
        {"label": _("Last Invoice Name"), "fieldname": "last_invoice_name", "fieldtype": "Link", "options": "Sales Invoice", "width": 200},
        {"label": _("Last Invoice Total"), "fieldname": "last_invoice_total", "fieldtype": "Data", "width": 150},
        {"label": _("Member Group Last Invoice"), "fieldname": "last_invoice_custom_customer_group", "fieldtype": "Data", "width": 200},
        {"label": _("Rate Category for Invoice"), "fieldname": "price_list_rate_for_inv", "fieldtype": "Data", "width": 200},
        {"label": _("TAX ID"), "fieldname": "tax__number", "fieldtype": "Data", "width": 80},
        {"label": _("Year"), "fieldname": "year", "fieldtype": "Data", "width": 80},
        {"label": _("EGY"), "fieldname": "total_amount_in_egp", "fieldtype": "Data", "width": 150},
        {"label": _("Category for Exports Volume"), "fieldname": "price", "fieldtype": "Data", "width": 200},
        {"label": _("Rate of member export "), "fieldname": "rate", "fieldtype": "Data", "width": 100},
        {"label": _("USD"), "fieldname": "total_amount_in_usd", "fieldtype": "Data", "width": 150},
        {"label": _("Tons"), "fieldname": "quantity_in_tons", "fieldtype": "Data", "width": 100},
        {"label": _("Membership Rate Difference"), "fieldname": "m_r_d", "fieldtype": "Data", "width": 100},

    ]
    return columns

def get_data(filters):
    conditions = []
    params = {}

    code_customer = filters.get("code_customer")

    if code_customer:
        conditions.append("tc.`name` = %(code_customer)s")
        params["code_customer"] = code_customer

    sql = """
        SELECT 
            tc.`name` AS code_customer,
            tc.`customer_name` AS member,
            COALESCE(tvme.`tax__number`, '') AS tax__number,
            YEAR(CURDATE()) - 1 AS year,
            SUM(tvme.`total_amount_in_egp`) AS total_amount_in_egp,
            SUM(COALESCE(tvme.`total_amount_in_usd`, 0)) AS total_amount_in_usd,
            SUM(COALESCE(tvme.`quantity_in_tons`, 0)) AS quantity_in_tons,
            COALESCE(last_invoice.`last_invoice_name`, 'No Last Invoice') AS last_invoice_name,
            COALESCE(last_invoice.`custom_customer_group`, '') AS last_invoice_custom_customer_group,
            COALESCE(last_invoice.`total`, 0) AS last_invoice_total,
            COALESCE(last_invoice.`price_list_rate_for_inv`, 0) AS price_list_rate_for_inv,
            CASE
                WHEN SUM(tvme.`total_amount_in_egp`) BETWEEN (
                    SELECT MIN(tcg.custom_from) FROM `tabCustomer Group` AS tcg
                ) AND (
                    SELECT MAX(tcg.custom_to) FROM `tabCustomer Group` AS tcg
                ) THEN (
                    SELECT tcg.name
                    FROM `tabCustomer Group` AS tcg
                    WHERE SUM(tvme.total_amount_in_egp) BETWEEN tcg.custom_from AND tcg.custom_to
                    LIMIT 1
                )
                ELSE ''
            END AS price,
            (
                SELECT tip.price_list_rate
                FROM `tabItem Price` AS tip
                JOIN `tabCustomer Group` AS tcg ON tcg.name = tip.custom_member_categories
                WHERE SUM(tvme.total_amount_in_egp) BETWEEN tcg.custom_from AND tcg.custom_to
                LIMIT 1
            ) AS rate,
            (COALESCE(last_invoice.`price_list_rate_for_inv`, 0) - COALESCE((SELECT tip.price_list_rate
            FROM `tabItem Price` AS tip
            JOIN `tabCustomer Group` AS tcg ON tcg.name = tip.custom_member_categories
            WHERE SUM(tvme.total_amount_in_egp) BETWEEN tcg.custom_from AND tcg.custom_to
            LIMIT 1), 0)) AS m_r_d
        FROM
            `tabCustomer` AS tc
        LEFT JOIN (
            SELECT 
                tvme.`tax__number`,
                SUM(tvme.`total_amount_in_egp`) AS total_amount_in_egp,
                SUM(tvme.`total_amount_in_usd`) AS total_amount_in_usd,
                SUM(tvme.`quantity_in_tons`) AS quantity_in_tons
            FROM 
                `tabVolume Of Member Exports` AS tvme
            WHERE 
                tvme.`year` = YEAR(CURDATE()) - 1
            GROUP BY 
                tvme.`tax__number`
        ) AS tvme ON tc.`tax_id` = tvme.`tax__number`
        LEFT JOIN (
            SELECT 
                tsi.customer,
                tsi.name AS last_invoice_name,
                tcg.`custom_from` AS customer_group_from,
                tcg.`custom_to` AS customer_group_to,
                tcg.name AS custom_customer_group,
                tsi.total,
                tip.`price_list_rate` AS price_list_rate_for_inv,
                ROW_NUMBER() OVER (PARTITION BY tsi.customer ORDER BY tsi.posting_date DESC) AS rn
            FROM 
                `tabSales Invoice` AS tsi
            LEFT JOIN 
                `tabCustomer Group` AS tcg ON tcg.name = tsi.`custom_customer_group`
            LEFT JOIN 
                `tabItem Price` AS tip ON tip.`custom_member_categories` = tcg.`name`
        ) AS last_invoice ON tc.`name` = last_invoice.`customer`
    """

    if conditions:
        sql += " WHERE " + " AND ".join(conditions)

    sql += " GROUP BY tc.`name`"

    # Execute the query with the filter values
    mydata = frappe.db.sql(sql, params, as_dict=True)

    return mydata
