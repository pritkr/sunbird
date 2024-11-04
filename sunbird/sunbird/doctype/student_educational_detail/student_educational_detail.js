// Copyright (c) 2024, T4GC and contributors
// For license information, please see license.txt

frappe.ui.form.on("Student Educational Detail", {
    date_of_student_added: function(frm) {
        var dateOfStudentAdded = frm.doc.date_of_student_added;

        if (dateOfStudentAdded) {
            var date = new Date(dateOfStudentAdded);
            var currentDate = new Date();

            if (!isNaN(date.getTime())) {
                if (date > currentDate) {
                    frappe.msgprint(__('Date of Student Added cannot be in the future.'));
                    frm.set_value('date_of_student_added', '');
                } else {
                    var year = date.getFullYear();
                    frm.set_value('year', year);
                }
            } else {
                frappe.msgprint(__('Invalid date provided in Date of Student Added.'));
            }
        } else {
            frm.set_value('year', '');
        }
    },
    overall_percent_in_previous_year: function(frm) {
        var overallPercent = frm.doc.overall_percent_in_previous_year;

        if (overallPercent !== undefined && overallPercent > 100) {
            frappe.msgprint(__('Overall Percent in Previous Year cannot be more than 100.'));
            frm.set_value('overall_percent_in_previous_year', ''); // Clear the invalid value
        }
    },
    }
);

frappe.ui.form.on('Subject Scores', {
    percent_score: function(frm, cdt, cdn) {
        var child = locals[cdt][cdn];
        var percentScore = child.percent_score;

        if (percentScore !== undefined && percentScore > 100) {
            frappe.msgprint(__('Percent Score cannot be more than 100.'));
            frappe.model.set_value(cdt, cdn, 'percent_score', ''); // Clear the invalid value
        }
    }
});