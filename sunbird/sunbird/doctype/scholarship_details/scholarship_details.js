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

        // Validate the scholarship end date if it exists
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
                return; // Stop further execution
            }
        }

        // Calculate tenure if valid dates are present
        if (scholarship_start_date && scholarship_end_date) {
            calculate_tenure(frm, scholarship_start_date, scholarship_end_date);
        }
    },
    after_save: function(frm) {
        frappe.call({
            method: "sunbird.sunbird.doctype.scholarship_details.custom.update_student_profile",  
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

function calculate_tenure(frm, start_date, end_date) {
    // Parse the dates
    var start = new Date(start_date);
    var end = new Date(end_date);

    // Calculate the difference in years
    var tenure_in_years = end.getFullYear() - start.getFullYear();
    var month_difference = end.getMonth() - start.getMonth();

    // Adjust tenure based on month difference
    if (month_difference < 0 || (month_difference === 0 && end.getDate() < start.getDate())) {
        tenure_in_years--;
        month_difference += 12; // Adjust month difference if the end month is earlier than the start month
    }

    // Calculate total months
    var total_months = (tenure_in_years * 12) + month_difference;

    if (total_months < 12) {
        // For less than a year, display the total months
        frappe.msgprint(__('Scholarship Duration: ') + total_months + ' ' + __('Month(s)'));
        frm.set_value('scholarship_duration', total_months + " months"); 
    } else {
        var years = Math.floor(total_months / 12); 
        var months = total_months % 12; 

        var duration_text = years + ' ' + __('Year(s)');
        if (months > 0) {
            duration_text += ' ' + months + ' ' + __('Month(s)');
        }

        frappe.msgprint(__('Scholarship Duration: ') + duration_text);
        frm.set_value('scholarship_duration', duration_text); 
    }
}

