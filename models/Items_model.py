from odoo import models, fields, api

class IscaPopItemsModel(models.Model):
    _name = 'isca_pop.items_model'
    _description = 'My category model for my app'

    name = fields.Char(string="Name", required=True)
    photo = fields.Binary(string="Foto", required=True)
    state = fields.Selection([
        ("new", "New"), 
        ("usable", "Usable"), 
        ("broken", "Broken")
    ], string="State", default="new")
    
    category_id = fields.Many2one('isca_pop.category_model', string="Category", required=True)
    user_id = fields.Many2one(comodel_name='res.users', string='Responsible User', default=lambda self: self.env.user, required=True)
    location = fields.Many2one('isca_pop.location_model', string="Location", required=True)
    
    quantity = fields.Integer(string="Quantity", required=True)
    total_quantity = fields.Integer(string="Total Quantity", compute='_compute_total_quantity', store=True)
    
    can_be_discarded = fields.Boolean(string="Can Be Discarded", default=False)
    donated = fields.Boolean(string="Donated", default=False, readonly=True)
    canbedonated = fields.Boolean(string="Can be Donated", store=False, compute="_compute_canbedonated")
    active = fields.Boolean(string="Active", default=True)
    def action_delete_discardable_items(self):
        """ Delete all records where can_be_discarded is True """
        records_to_delete = self.search([('can_be_discarded', '=', True)])
        
        if not records_to_delete:
            raise UserError("No items found that can be discarded.") # type: ignore
        
        records_to_delete.unlink()
    @api.depends('location', 'state')
    def _compute_canbedonated(self):
        """ Determines if an item can be donated based on location type and state. """
        for record in self:
            if record.location and record.location.type == 'class' or record.state == 'broken':
                record.canbedonated = False
            else:
                record.canbedonated = True

    @api.depends('quantity', 'name')
    def _compute_total_quantity(self):
        """ Computes total quantity for all items with the same name. """
        for record in self:
            records_with_same_name = self.search([('name', '=', record.name)])
            total = sum(records_with_same_name.mapped('quantity'))
            record.total_quantity = total

    def discard_item(self):
        for record in self:
            if record.state == "broken":
                record.write({'can_be_discarded': True})
        return True

    @api.model
    def create(self, vals):
        """ Prevents duplicate items by updating the quantity if an existing record matches. """
        existing_item = self.search([
            ('name', '=', vals.get('name')),
            ('state', '=', vals.get('state')),
            ('location', '=', vals.get('location')),
            ('user_id', '=', self.env.user.id)
        ], limit=1)

        if existing_item:
            existing_item.quantity += vals.get('quantity')
            return existing_item
        else:
            return super(IscaPopItemsModel, self).create(vals)
