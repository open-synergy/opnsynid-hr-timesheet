import setuptools

with open('VERSION.txt', 'r') as f:
    version = f.read().strip()

setuptools.setup(
    name="odoo14-addons-open-synergy-opnsynid-hr-timesheet",
    description="Meta package for open-synergy-opnsynid-hr-timesheet Odoo addons",
    version=version,
    install_requires=[
        'odoo14-addon-ssi_holiday_state_change_constrain',
        'odoo14-addon-ssi_hr_holiday',
        'odoo14-addon-ssi_hr_leave_allocation_request_batch',
        'odoo14-addon-ssi_hr_leave_request_batch',
        'odoo14-addon-ssi_hr_overtime',
        'odoo14-addon-ssi_hr_overtime_account',
        'odoo14-addon-ssi_hr_overtime_batch',
        'odoo14-addon-ssi_hr_overtime_state_change_constrain',
        'odoo14-addon-ssi_timesheet',
        'odoo14-addon-ssi_timesheet_attendance',
        'odoo14-addon-ssi_timesheet_attendance_work_log',
        'odoo14-addon-ssi_timesheet_state_change_constrain',
        'odoo14-addon-ssi_work_log_cost',
        'odoo14-addon-ssi_work_log_expense',
        'odoo14-addon-ssi_work_log_mixin',
        'odoo14-addon-ssi_work_log_state_change_constrain',
        'odoo14-addon-test_ssi_work_log_mixin',
    ],
    classifiers=[
        'Programming Language :: Python',
        'Framework :: Odoo',
        'Framework :: Odoo :: 14.0',
    ]
)
