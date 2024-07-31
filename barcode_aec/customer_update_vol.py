import frappe


@frappe.whitelist()
def update():
    try:    
        # Fetch data from the query into ahmed_query
        ahmed = """
            SELECT
                tc.name AS customer_name,
                tc.tax_id,
                tvme.season AS season,
                tvme.season_name AS season_name,
                tvme.year,
                tvme.value,
                SUM(tvme.total_amount_in_egp) AS total_amount_in_egp,
                SUM(tvme.total_amount_in_usd) AS total_amount_in_usd,
                SUM(tvme.quantity_in_tons) AS quantity_in_tons
            FROM
                `tabCustomer` tc
            INNER JOIN
                `tabVolume Of Member Exports` tvme ON (tc.tax_id = tvme.tax_id)
            WHERE
                tvme.year = YEAR(CURDATE()) - 4
            GROUP BY
                tc.tax_id     
        """
        ahmed_query = frappe.db.sql(ahmed, as_dict=True)
        print(ahmed_query)

        # Update tabVolume Of Member Exports for Three Years table with the fetched data
        for data in ahmed_query:
            # print(data)
            query = """
               UPDATE `tabVolume Of Member Exports for Three Years` ti
                INNER JOIN `tabCustomer` tc ON tc.name = ti.parent
                SET ti.season = %s,
                    ti.season_name = %s,
                    ti.total_amount_in_egp = %s,
                    ti.total_amount_in_usd = %s,
                    ti.quantity_in_tons = %s,
                    ti.value = %s
                WHERE tc.name = %s;
            """
            # Execute the update query with parameters
            d = frappe.db.sql(query, (data['season'], data['season_name'], data['total_amount_in_egp'], data['total_amount_in_usd'],data['quantity_in_tons'], data['value'], data['customer_name']),as_dict=True)
            frappe.db.commit()
            print("ssssssssssss",ahmed_query)
            return ahmed_query
    
    except Exception as e:
        frappe.log_error(f"Error in update function: {str(e)}")
        return "Error occurred, check logs for details"