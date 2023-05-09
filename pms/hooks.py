from . import __version__ as app_version

app_name = "pms"
app_title = "Pms"
app_publisher = "enfono"
app_description = "PMS"
app_icon = "octicon octicon-file-directory"
app_color = "grey"
app_email = "siva@gmail.com"
app_license = "MIT"

# Includes in <head>
# ------------------

# include js, css files in header of desk.html
# app_include_css = "/assets/pms/css/pms.css"
# app_include_js = "/assets/pms/js/pms.js"

# include js, css files in header of web template
# web_include_css = "/assets/pms/css/pms.css"
# web_include_js = "/assets/pms/js/pms.js"

# include custom scss in every website theme (without file extension ".scss")
# website_theme_scss = "pms/public/scss/website"

# include js, css files in header of web form
# webform_include_js = {"doctype": "public/js/doctype.js"}
# webform_include_css = {"doctype": "public/css/doctype.css"}

# include js in page
# page_js = {"page" : "public/js/file.js"}

# include js in doctype views
# doctype_js = {"doctype" : "public/js/doctype.js"}
# doctype_list_js = {"doctype" : "public/js/doctype_list.js"}
# doctype_tree_js = {"doctype" : "public/js/doctype_tree.js"}
# doctype_calendar_js = {"doctype" : "public/js/doctype_calendar.js"}

# Home Pages
# ----------

# application home page (will override Website Settings)
# home_page = "login"

# website user home page (by Role)
# role_home_page = {
#	"Role": "home_page"
# }

# Generators
# ----------

# automatically create page for each record of this doctype
# website_generators = ["Web Page"]

# Installation
# ------------

# before_install = "pms.install.before_install"
# after_install = "pms.install.after_install"

# Uninstallation
# ------------

# before_uninstall = "pms.uninstall.before_uninstall"
# after_uninstall = "pms.uninstall.after_uninstall"

# Desk Notifications
# ------------------
# See frappe.core.notifications.get_notification_config

# notification_config = "pms.notifications.get_notification_config"

# Permissions
# -----------
# Permissions evaluated in scripted ways

# permission_query_conditions = {
#	"Event": "frappe.desk.doctype.event.event.get_permission_query_conditions",
# }
#
# has_permission = {
#	"Event": "frappe.desk.doctype.event.event.has_permission",
# }

# DocType Class
# ---------------
# Override standard doctype classes

# override_doctype_class = {
#	"ToDo": "custom_app.overrides.CustomToDo"
# }

# Document Events
# ---------------
# Hook on document methods and events

fixtures = [
    {
        "doctype": "Custom Field",
        "filters": [
            [
                "name",
                "in",
                (
                    "Sales Invoice-lease_data",
                    "Payment Entry-column_break_qrf7w",
                    "Payment Entry-cheque_number",
                    "Payment Entry-cheque_status",
            
                ),
            ]
        ],
    }
]

# doc_events = {
#	"*": {
#		"on_update": "method",
#		"on_cancel": "method",
#		"on_trash": "method"
#	}
# }

# Scheduled Tasks
# ---------------

# scheduler_events = {
#	"all": [
#		"pms.tasks.all"
#	],
#	"daily": [
#		"pms.tasks.daily"
#	],
#	"hourly": [
#		"pms.tasks.hourly"
#	],
#	"weekly": [
#		"pms.tasks.weekly"
#	]
#	"monthly": [
#		"pms.tasks.monthly"
#	]
# }

# Testing
# -------

# before_tests = "pms.install.before_tests"

# Overriding Methods
# ------------------------------
#
# override_whitelisted_methods = {
#	"frappe.desk.doctype.event.event.get_events": "pms.event.get_events"
# }
#
# each overriding function accepts a `data` argument;
# generated from the base implementation of the doctype dashboard,
# along with any modifications made in other Frappe apps
# override_doctype_dashboards = {
#	"Task": "pms.task.get_dashboard_data"
# }

# exempt linked doctypes from being automatically cancelled
#
# auto_cancel_exempted_doctypes = ["Auto Repeat"]

# Request Events
# ----------------
# before_request = ["pms.utils.before_request"]
# after_request = ["pms.utils.after_request"]

# Job Events
# ----------
# before_job = ["pms.utils.before_job"]
# after_job = ["pms.utils.after_job"]

# User Data Protection
# --------------------

user_data_fields = [
	{
		"doctype": "{doctype_1}",
		"filter_by": "{filter_by}",
		"redact_fields": ["{field_1}", "{field_2}"],
		"partial": 1,
	},
	{
		"doctype": "{doctype_2}",
		"filter_by": "{filter_by}",
		"partial": 1,
	},
	{
		"doctype": "{doctype_3}",
		"strict": False,
	},
	{
		"doctype": "{doctype_4}"
	}
]

# Authentication and authorization
# --------------------------------

# auth_hooks = [
#	"pms.auth.validate"
# ]

