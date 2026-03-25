from odoo import models, fields, api
from datetime import datetime

class FormPelatihan(models.Model):
    _name = 'form.pelatihan'
    _description = 'Formulir Pengajuan Pendidikan & Pelatihan'

    name = fields.Char('Nomor Surat', readonly=True, copy=False, default='New')
    user_id = fields.Many2one('res.users', 'Diajukan Oleh', default=lambda self: self.env.user, readonly=True)
    
    def _default_department(self):
        employee = self.env['hr.employee'].search([('user_id', '=', self.env.user.id)], limit=1)
        return employee.department_id.id if employee else False

    department_id = fields.Many2one('hr.department', 'Department', required=True, default=_default_department)
    placement_id = fields.Many2one('form.pelatihan.placement', 'Placement', required=True)
    judul = fields.Char('Judul Pelatihan', required=True)
    vendor_id = fields.Many2one('form.pelatihan.vendor', 'Vendor', required=True)
    jenis_id = fields.Many2one('form.pelatihan.jenis', 'Jenis Diklat', required=True)

    latar_belakang = fields.Text('Latar Belakang')
    tujuan = fields.Text('Tujuan')
    
    # Fungsi bantuan untuk mengecek apakah user adalah level manajerial
    def _is_manager(self):
        manager_groups = [
            'form_pelatihan.group_hod', 
            'form_pelatihan.group_hr', 
            'form_pelatihan.group_fat',
            'form_pelatihan.group_gm',
            'form_pelatihan.group_direksi'
        ]
        return any(self.env.user.has_group(g) for g in manager_groups)

    def _default_peserta(self):
        if self._is_manager():
            employee = self.env['hr.employee'].search([('user_id', '=', self.env.user.id)], limit=1)
            if employee and employee.department_id:
                employees = self.env['hr.employee'].search([('department_id', '=', employee.department_id.id)])
                return [(6, 0, employees.ids)]
        return False

    peserta_ids = fields.Many2many('hr.employee', string='Daftar Peserta', default=_default_peserta)

    state = fields.Selection([
        ('draft', 'Draft'),
        ('review_hod', 'Menunggu HOD'),
        ('review_hr', 'Menunggu HR'),
        ('review_fat', 'Menunggu FAT'),
        ('review_gm', 'Menunggu GM'),
        ('review_direksi', 'Menunggu Direksi'),
        ('approved', 'Disetujui'),
        ('rejected', 'Ditolak')
    ], string='Status', default='draft', tracking=True)

    project_ho = fields.Boolean('Project HO')
    project_site = fields.Boolean('Project Site')
    direksi_approval = fields.Boolean('Approval Direksi')

    @api.onchange('department_id')
    def _onchange_department_id(self):
        if self._is_manager() and self.department_id:
            employees = self.env['hr.employee'].search([('department_id', '=', self.department_id.id)])
            self.peserta_ids = [(6, 0, employees.ids)]
        elif not self._is_manager():
            self.peserta_ids = [(5, 0, 0)]

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if vals.get('name', 'New') == 'New':
                seq = self.env['ir.sequence'].next_by_code('form.pelatihan') or '001'
                month = datetime.now().month
                year = datetime.now().year
                roman_months = ['', 'I', 'II', 'III', 'IV', 'V', 'VI', 'VII', 'VIII', 'IX', 'X', 'XI', 'XII']
                roman = roman_months[month]
                vals['name'] = f"{seq}/PRP/GSI-HRGA/{roman}/{year}"
        return super().create(vals_list)

    def action_submit(self): self.state = 'review_hod'
    def action_hod_approve(self): self.state = 'review_hr'
    def action_hr_approve(self): self.state = 'review_fat'
    def action_fat_approve(self): self.state = 'review_gm'
    def action_gm_approve(self): self.state = 'review_direksi'
    def action_direksi_approve(self):
        self.direksi_approval = True
        self.state = 'approved'
    def action_reject(self): self.state = 'rejected'