from odoo import models, fields, api
from odoo.exceptions import ValidationError

class IscaPopCategoryModel(models.Model):
    _name = 'isca_pop.category_model'
    _description = 'My category model for my app'
    _rec_name = 'full_name'  # Set the full_name field as the record's display name

    name = fields.Char(string="Category Name", required=True)
    full_name = fields.Char(string="Full Category Path", compute="_compute_full_name", store=True)
    description = fields.Text(string="Category Description")
    
    # Only show parent categories created by the current user.
    cat_father = fields.Many2one(
        "isca_pop.category_model", 
        string="Parent Category", 
        domain="[('create_uid', '=', uid)]"
    )
    
    category_childs = fields.One2many(
        "isca_pop.category_model", 
        "cat_father", 
        string="Subcategories"
    )
    
    # Optionally, only show items created by the current user.
    items = fields.One2many(
        "isca_pop.items_model", 
        "category_id", 
        string="Items", 
        domain="[('create_uid', '=', uid)]"
    )

    @api.depends('name', 'cat_father.full_name')
    def _compute_full_name(self):
        for record in self:
            if record.cat_father:
                record.full_name = "%s / %s" % (record.cat_father.full_name, record.name)
            else:
                record.full_name = record.name

    @api.constrains('cat_father')
    def _check_cat_father(self):
        for record in self:
            if record.cat_father and record.cat_father.id == record.id:
                raise ValidationError("A category cannot be its own parent.")
