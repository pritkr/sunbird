// Copyright (c) 2024, T4GC and contributors
// For license information, please see license.txt


frappe.ui.form.on("Scholarship Details", {
    scholarship_start_date: function(frm) {
        var scholarship_start_date = frm.doc.scholarship_start_date;
        var currentDate = new Date();

        if (scholarship_start_date) {
            var date = new Date(scholarship_start_date);

            if (!isNaN(date.getTime())) {
                // Check if the start date is in the future
                if (date > currentDate) {
                    frappe.msgprint(__('Date of Scholarship Added cannot be in the future.'));
                    frm.set_value('scholarship_start_date', '');
                } else {
                    var year = date.getFullYear();
                    frm.set_value('current_scholarship_year', year);
                }
            } else {
                frappe.msgprint(__('Invalid date provided in Scholarship Start date.'));
            }
        } else {
            frm.set_value('current_scholarship_year', '');
        }

        // Validate the scholarship end date
        if (frm.doc.scholarship_end_date) {
            if (frm.doc.scholarship_end_date < scholarship_start_date) {
                frappe.msgprint(__('Scholarship End Date cannot be less than Scholarship Start Date.'));
                frm.set_value('scholarship_end_date', ''); // Clear the invalid value
            }
        }
    },
    scholarship_end_date: function(frm) {
        var scholarship_end_date = frm.doc.scholarship_end_date;
        var scholarship_start_date = frm.doc.scholarship_start_date;

        // Validate the scholarship end date against the start date
        if (scholarship_start_date && scholarship_end_date) {
            if (scholarship_end_date < scholarship_start_date) {
                frappe.msgprint(__('Scholarship End Date cannot be less than Scholarship Start Date.'));
                frm.set_value('scholarship_end_date', ''); // Clear the invalid value
            }
        }
    },
    after_save: function(frm) {
        frappe.call({
            method: "sunbird.sunbird.doctype.scholarship_details.custom.update_student_educational_details",  // Replace with actual path
            args: {
                scholarship_details: frm.doc
            },
            callback: function(response) {
                if (response.message) {
                    frappe.msgprint(__('Student educational details updated successfully.'));
                }
            }
        });
    }
});
