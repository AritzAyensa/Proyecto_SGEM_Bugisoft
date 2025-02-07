from odoo import models, fields

class Coche(models.Model):
    _name = 'coche'
    _description = 'Coche Disponible para reserva'

    name = fields.Char(string='Modelo del Coche', required=True)
    marca= fields.Char(string="Marca",required=True)
    precio_por_dia = fields.Float(string='Precio por Día', required=True)
    disponible=fields.Boolean(string="Disponible",default=True)
    matricula=fields.Char(string="matricula",required=True,unique=True)
    tipo_combustible=fields.Selection([
        ("gasolina","Gasolina"),
        ("diesel","Diesel"),
        ("hibrido","Hibrido"),
        ("electrico","Electrico"),
    ],string="Tipo de combustible",required=True)
    
    num_asientos=fields.Integer(String="Numero de asientos",default=5)
    transmision=fields.Selection([
        ("manual","Manual",)
        ("automatica","Automatica",)
    ], string="Transemision", required=True)
    
    kilometraje=fields.Float(string="Kilomentraje (km)")
    color=fields.Char(string="Color")
