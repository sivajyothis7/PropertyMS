// Copyright (c) 2023, enfono and contributors
// For license information, please see license.txt

frappe.ui.form.on('Lease Contract', {
	// setup: function(frm) {
	// 	frm.set_query("lease_item", "lease_item", function() {
	// 		return {
	// 			"filters": [
    //                 ["item_group","=", "Lease Items"],
	// 			]
	// 		};
	// 	});

	// },
	
	// refresh: function(frm) {
	// 	cur_frm.add_custom_button(__("Make Invoice Schedule"), function() {
	// 		make_lease_payment_schedule(cur_frm);
	// 	});
	// }
});


// var make_lease_payment_schedule = function(frm){
// 	var doc = frm.doc;
// 	frappe.call({
// 		method: "pms.pms.doctype.lease_contract.lease_contract.make_lease_payment_schedule",
// 		args: {leasedoc: doc.name},
// 		callback: function(){
// 			cur_frm.reload_doc();
// 		}
// 	});
// };