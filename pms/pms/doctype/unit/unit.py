# Copyright (c) 2023, enfono and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document

class Unit(Document):
	def validate(self):
		if self.status=="Available":

			property_add=frappe.get_doc("Properties",self.property)
			property_add.append("property_units",{"unit_name":self.name,
												"unit_status":self.status

			})
			property_add.save(ignore_version=True)
