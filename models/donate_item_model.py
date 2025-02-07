from odoo import models, fields, api
from odoo.exceptions import ValidationError

class DonateItemModel(models.TransientModel):
    _name = 'isca_pop.donate_item_model'
    _description = 'This is a model to donate items'
    
    base_location = fields.Many2one('isca_pop.location_model', string="Base Location")
    item_id = fields.Many2one('isca_pop.items_model', string="Item",ondelete="cascade")
    quantity_to_move = fields.Integer(string="Quantity to Move", required=True)
    donante = fields.Many2one('res.users', string="Donated by:")
    def action_confirm(self):
        # Ensure valid quantity

        self.base_location=self.item_id.location
        if self.quantity_to_move <= 0:
            raise ValidationError("Quantity must be greater than zero.")
        
        if self.quantity_to_move > self.item_id.quantity:
            raise ValidationError("Not enough quantity in the selected source location.")
        
        remaining_quantity = self.item_id.quantity - self.quantity_to_move

        # Check if the item already exists in the donation model
        existing_item_in_donation = self.env['isca_pop.donation_model'].search([
        ('name', '=', self.item_id.name),
        ('state', '=', self.item_id.state),
        ('donator', '=', self.env.user.id), 
        ], limit=1)


        # If the item exists, update the quantity, otherwise create a new record
        if existing_item_in_donation:
            existing_item_in_donation.quantity += self.quantity_to_move
        else:
            self.env['isca_pop.donation_model'].create({
                'name': self.item_id.name,
                'photo': self.item_id.photo,
                'state': self.item_id.state,
                'donator':self.donante.id,
                'category_id':self.item_id.category_id.id,
                'location': self.base_location.id,
                'quantity': self.quantity_to_move,
            })

        # Update the remaining quantity in the source item or remove it if zero
        if remaining_quantity == 0:
            self.item_id.active = False
            self.item_id.unlink()  # Remove the item from source location
        else:
            self.item_id.quantity = remaining_quantity

        # Return to close the action window
        return {'type': 'ir.actions.act_window_close'}
