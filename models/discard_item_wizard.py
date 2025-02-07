from odoo import models, fields, api
from odoo.exceptions import ValidationError

class DiscardItem(models.TransientModel):
    _name = 'isca_pop.discard_item_wizard'
    _description = 'This is a model to discard items'
    
