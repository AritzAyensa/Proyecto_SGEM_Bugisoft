from odoo import models, fields

class Coche(models.Model):
    _name = 'coche'
    _description = 'Mi gestion de reservas'

    name = fields.Char(string='Nombre', required=True)
    description = fields.Text(string='Descripción')
    active = fields.Boolean(string='Activo', default=True)
