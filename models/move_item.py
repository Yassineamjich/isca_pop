from odoo import models, fields, api
from odoo.exceptions import ValidationError

class MoveItemWizard(models.TransientModel):
    _name = 'isca_pop.move_item_model'
    _description = 'Wizard to move items between locations'

    base_location = fields.Many2one(
        'isca_pop.location_model', 
        string="Source Location", 
        required=True,
        domain="[('create_uid', '=', uid)]"  # Filter locations by current user
    )
    item_id = fields.Many2one(
        'isca_pop.items_model', 
        string="Item", 
        required=True,
        domain="[('location', '=', base_location), ('create_uid', '=', uid)]"  # Filter items by the selected source location and current user
    )
    available_quantity = fields.Integer(
        string="Available Quantity", 
        compute="_compute_available_quantity", 
        store=False
    )
    quantity_to_move = fields.Integer(string="Quantity to Move", required=True)
    target_location = fields.Many2one(
        'isca_pop.location_model', 
        string="Target Location", 
        required=True,
        domain="[('create_uid', '=', uid), ('id', '!=', base_location)]"  # Filter target locations by current user and exclude the source location
    )

    @api.depends('item_id')
    def _compute_available_quantity(self):
        for record in self:
            record.available_quantity = record.item_id.quantity if record.item_id else 0

    def action_confirm(self):
        # Ensure the quantity to move is valid (positive and not more than the available quantity)
        if self.quantity_to_move <= 0:
            raise ValidationError("Quantity must be greater than zero.")
        
        if self.quantity_to_move > self.item_id.quantity:
            raise ValidationError("Not enough quantity in the selected source location.")
        
        # Deduct quantity from the item in the source location
        remaining_quantity = self.item_id.quantity - self.quantity_to_move

        # Check if the item already exists in the target location
        existing_item_in_target_location = self.env['isca_pop.items_model'].search([
            ('name', '=', self.item_id.name),
            ('location', '=', self.target_location.id)
        ], limit=1)

        if existing_item_in_target_location:
            # If the item exists in the target location, increase its quantity
            existing_item_in_target_location.quantity += self.quantity_to_move
        else:
            # Create a new item in the target location if it doesn't exist
            self.env['isca_pop.items_model'].create({
                'name': self.item_id.name,
                'photo': self.item_id.photo,
                'state': self.item_id.state,
                'category_id': self.item_id.category_id.id,
                'location': self.target_location.id,
                'quantity': self.quantity_to_move,
                'total_quantity': self.quantity_to_move,
            })

        # After everything is done, check if the remaining quantity is zero, then delete the item
        if remaining_quantity == 0:
            self.item_id.unlink()
        else:
            self.item_id.quantity = remaining_quantity

        # Return to close the action window
        return {'type': 'ir.actions.act_window_close'}
