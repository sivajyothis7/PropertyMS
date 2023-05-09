# Copyright (c) 2023, enfono and contributors
# For license information, please see license.txt

import frappe


from frappe import _

def execute(filters=None):
    columns = [
        _("Name") + ":Link/Payment Entry:120",
        _("Posting Date") + ":Date:90",
        _("Party Type") + "::100",
        _("Party") + ":Dynamic Link/Payment Entry:150",
        _("Payment Type") + "::150",
        _("Mode of Payment") + "::150",
        _("Cheque Number") + "::120",
        _("Cheque Status") + "::120",
        _("Paid Amount") + ":Currency/currency:120",
        # _("Allocated Amount") + ":Currency/currency:120",
        # _("Unallocated Amount") + ":Currency/currency:120",
        # _("Remarks") + "::200",
    ]

    conditions = ""
    if filters.get("from_date"):
        conditions += " and posting_date >= %(from_date)s"
    if filters.get("to_date"):
        conditions += " and posting_date <= %(to_date)s"
    if filters.get("payment_type"):
        conditions += " and payment_type = %(payment_type)s"
    if filters.get("mode_of_payment"):
        conditions += " and mode_of_payment = %(mode_of_payment)s"
    if filters.get("cheque_status"):
        conditions += " and cheque_status = %(cheque_status)s"

    data = frappe.db.sql(
        """
        select name, posting_date, party_type, party, payment_type, mode_of_payment, cheque_number,
        cheque_status, paid_amount
        from `tabPayment Entry`
        where docstatus = 0{0}
        order by posting_date desc
        """.format(conditions),
        filters,
        as_dict=True,
    )

    return columns, data
