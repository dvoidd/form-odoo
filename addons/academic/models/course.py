from odoo import api, fields, models
from odoo.exceptions import ValidationError


class AcademicCourse(models.Model):
    _name = 'academic.course'
    _description = 'Academic Course'

    name = fields.Char(string='Title', required=True)
    description = fields.Text(string='Description')
    responsible_id = fields.Many2one('res.users', string='Responsible')

    # Relasi ke Session
    session_ids = fields.One2many('academic.session', 'course_id', string='Sessions')

    # SQL Constraints (Section 10)
    _sql_constraints = [
        ('name_unique', 'UNIQUE(name)', 'Course name must be unique!'),
    ]

    # Python Constraint (Section 10)
    @api.constrains('name', 'description')
    def _check_name_description(self):
        for record in self:
            if record.name and record.description and record.name == record.description:
                raise ValidationError("Course name and description cannot be the same!")

    # Duplicate Record (Section 12)
    def copy(self, default=None):
        default = dict(default or {})
        default.update({
            'name': 'Copy of %s' % self.name,
        })
        return super().copy(default)