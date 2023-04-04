# Copyright (c) 2023, enfono and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document

class Tenant(Document):
	pass
	# def validate(self):
	# 	tenant_data=frappe.db.exists(
	# 		"Tenant",
	# 		{"tenant":self.tenant,
	# 		 "docstatus":1
				
	# 		},
	# 	)

	# 	if tenant_data:
	# 		frappe.throw("Tenant Data Already exists for this Tenant")