import frappe
from frappe.utils import add_days, today, date_diff, getdate, add_months


@frappe.whitelist()
def invoice_schedule(
    date,
    item,
    paid_by,
    item_name,
    name,
    qty,
    rate,
    idx,
    # currency=None,
    document_type="Sales Invoice"
):
    date_to_invoice = add_days(date, -1 * (0))
    payment_schedule=frappe.get_doc(
        dict(
            idx=idx,
            doctype="Lease Payment Schedule",
            parent=name,
            parentfield="lease_payment_schedule",
            parenttype="lease_contract",
            date_to_invoice=date_to_invoice,
            # schedule_start_date=date,
            lease_item=item,
            paid_by=paid_by,
            lease_item_name=item_name,
            qty=qty,
            rate=rate,
            # currency=currency,
            document_type=document_type
        )
    )
    payment_schedule.insert(ignore_permissions=True)
    # frappe.msgprint("Orientation meeting created")