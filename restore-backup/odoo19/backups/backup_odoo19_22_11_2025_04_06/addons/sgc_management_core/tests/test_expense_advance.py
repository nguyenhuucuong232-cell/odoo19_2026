from odoo.tests.common import TransactionCase


class TestExpenseAdvance(TransactionCase):
    def setUp(self):
        super().setUp()
        # Ensure there is at least one employee
        self.employee = self.env['hr.employee'].sudo().search([], limit=1)
        if not self.employee:
            self.employee = self.env['hr.employee'].sudo().create({'name': 'Test Employee'})

    def test_create_advance_and_expense_link(self):
        advance = self.env['sgc.expense.advance'].create({
            'name': 'TEST-ADV-TC1',
            'employee_id': self.employee.id,
            'reason': 'Test create'
        })
        expense = self.env['hr.expense'].create({
            'name': 'Test Expense',
            'employee_id': self.employee.id,
            'sgc_advance_id': advance.id,
        })
        self.assertIn(expense, advance.expense_sheet_ids)
