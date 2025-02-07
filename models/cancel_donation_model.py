from odoo import models, fields, api
from odoo.exceptions import ValidationError

class DonateItemModel(models.TransientModel):
    _name = 'isca_pop.cancel_donation_model'
    _description = 'This is a model to cancel donations of  items'

    base_location = fields.Many2one('isca_pop.location_model', string="Base Location")
    donation_id = fields.Many2one('isca_pop.donation_model', string="Donation")
    item_id = fields.Many2one('isca_pop.items_model',string="item")
    quantity_to_move = fields.Integer(string="Quantity to Move", required=True)


    def action_confirm(self):
        # Ensure valid quantity

        self.base_location=self.donation_id.location
        if self.quantity_to_move <= 0:
            raise ValidationError("Quantity must be greater than zero.")
        
        if self.quantity_to_move > self.donation_id.quantity:
            raise ValidationError("Not enough quantity in the selected source location.")
        
        remaining_quantity = self.donation_id.quantity - self.quantity_to_move

        # Check if the item already exists in the donation model
        existing_item = self.env['isca_pop.items_model'].search([
            ('name', '=', self.donation_id.name),
            ('location','=',self.donation_id.location.id),
            ('state' , '=',self.donation_id.state)
          
        ], limit=1)

        # If the item exists, update the quantity, otherwise create a new record
        if existing_item:
            existing_item.quantity += self.quantity_to_move
        else:
            self.env['isca_pop.items_model'].create({
                'name': self.donation_id.name,
                'photo': self.donation_id.photo,
                'state': self.donation_id.state,
                'location': self.base_location.id,
                'quantity': self.quantity_to_move,
                'category_id':self.donation_id.category_id.id,
                'donated': False,
                'total_quantity':self.quantity_to_move,
            })

        # Update the remaining quantity in the source item or remove it if zero
        if remaining_quantity == 0:
            self.donation_id.unlink()  # Remove the donation
        else:
            self.donation_id.quantity = remaining_quantity

        # Return to close the action window
        return {'type': 'ir.actions.act_window_close'}
