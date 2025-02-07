from odoo import models, fields, api
from odoo.exceptions import ValidationError

class IscaPopCategoryModel(models.Model):
     _name = 'isca_pop.category_model'
     _description = 'my category model for my app'

     name=fields.Char(string="Category_Name")
     description = fields.Text(string="Category_Description")   
     cat_father = fields.Many2one("isca_pop.category_model",string="Category_Father")
     category_childs=fields.One2many("isca_pop.category_model","cat_father",string="Category_childs")
     items = fields.One2many("isca_pop.items_model","category_id",string="Items")
   
     
     @api.constrains('cat_father')
     def _check_cat_father(self):
        for record in self:
            if record.cat_father and record.cat_father.id == record.id:
                raise ValidationError("A category cannot be its own parent.")