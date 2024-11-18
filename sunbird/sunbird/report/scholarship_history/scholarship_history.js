frappe.query_reports["Scholarship History"] = {
    "filters": [
        {
            "fieldname": "student_id",
            "label": __("Student ID"),
            "fieldtype": "Link",
            "options": "Student Profile",  // Link to the "Student Profile" DocType
            "reqd": 0
        },
        {
            "fieldname": "institute_id",
            "label": __("Institute ID"),
            "fieldtype": "Link",
            "options": "Institute Profile",  // Link to the "Institute Profile" DocType
            "reqd": 0
        },
        {
            "fieldname": "year",
            "label": __("Year"),
            "fieldtype": "Int",
            "default": new Date().getFullYear(),  // Default to the current year
            "reqd": 0
        },
		{
			"fieldname": "status",
			"label": __("Scholarship Status"),
			"fieldtype": "Select",
			"options" : ["","Active", "Tenure Completed", "Cancelled"]
				
			
		}
    ]
};
