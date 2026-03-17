from odoo import models, fields

class AcademicCourse(models.Model):
    _name = 'academic.course'
    _description = 'Academic Course'

    name = fields.Char(string='Title', required=True)
    description = fields.Text(string='Description')
    responsible_id = fields.Many2one('res.users', string='Responsible')
    
    # Relasi ke Session
    session_ids = fields.One2many('academic.session', 'course_id', string='Sessions')