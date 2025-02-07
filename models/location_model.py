from odoo import models, fields, api

class IscaPopLocationModel(models.Model):
    _name = 'isca_pop.location_model'
    _description = 'Location Model'

    name = fields.Char(string="Location Name", required=True)
    description = fields.Char(string ="Description")
    items = fields.One2many("isca_pop.items_model","location",string="Items")
    user_id = fields.Many2one(
        comodel_name='res.users',  # Links to the Users model
        string='Responsible User',  # Label for the field in the UI
        default=lambda self: self.env.user,  # Default to the current user
    )
    type = fields.Selection(
    [("class", "Class"),
     ("warehouse", "Warehouse")],
    string="Type",  
    )
   