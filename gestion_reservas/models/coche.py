from odoo import models, fields

class Coche(models.Model):
    _name = 'coche'
    _description = 'Coche Disponible para reserva'

    name = fields.Char(string='Modelo del Coche', required=True)
    marca= fields.Char(string="Marca",required=True)
    precio_por_dia=fields.Float(string="Precio por Dia", required=True)
    disponible=fields.Boolean(string="Disponible",default=True)
    matricula=fields.Char(string="matricula",required=True,unique=True)
    