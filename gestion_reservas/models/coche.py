from odoo import models, fields, api

class Coche(models.Model):
    _name = 'coche'
    _description = 'Coche Disponible para reserva'

    name = fields.Char(string='Modelo del Coche', required=True)
    marca= fields.Char(string="Marca",required=True)
    precio_por_dia = fields.Float(string='Precio por Día', required=True)
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
        if 'matricula' in values:
            existing_car = self.search([('matricula', '=', values['matricula'])])
            if existing_car:
                raise KeyError('Ya existe un coche con esa matrícula.')
            
    def write(self,values):
         if 'matricula' in values:
            existing_car = self.search([('matricula', '=', values['matricula']), ('id', '!=', self.id)])
            if existing_car:
                raise KeyError('Ya existe un coche con esa matrícula.')

    def unlink(self):
        for coche in self:
            if coche.reservation_ids:
                raise KeyError('No puedes eliminar un coche que tiene reservas asociadas.')