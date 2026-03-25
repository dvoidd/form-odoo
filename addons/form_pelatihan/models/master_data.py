from odoo import models, fields

class MasterPlacement(models.Model):
    _name = 'form.pelatihan.placement'
    _description = 'Master Data Placement'
    name = fields.Char('Placement', required=True)

class MasterVendor(models.Model):
    _name = 'form.pelatihan.vendor'
    _description = 'Master Data Vendor'
    name = fields.Char('Nama Vendor', required=True)

class MasterJenisDiklat(models.Model):
    _name = 'form.pelatihan.jenis'
    _description = 'Master Data Jenis Diklat'
    name = fields.Char('Jenis Diklat', required=True)