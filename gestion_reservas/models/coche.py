from odoo import models, fields, api

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
    
    reservation_ids=fields.One2many("res.booking","coche_id",string="Reservas")
    
    @api.model
    def create(self, values):
        """ Método para crear un coche """
        # Validación para que no haya dos coches con la misma matrícula
        if 'matricula' in values:
            existing_car = self.search([('matricula', '=', values['matricula'])])
            if existing_car:
                raise KeyError('Ya existe un coche con esa matrícula.')
            
    @api.model
    def read(self, ids=None, fields=None, load='_classic_read'):
        return super(Coche, self).read(ids, fields, load)