from odoo import models, fields, api
from odoo.exceptions import UserError, ValidationError

class IscaPopItemStateChange(models.TransientModel):
    _name = 'isca_pop.item_state_change'
    _description = 'Wizard to change state and quantity of an item'

   

    item_id = fields.Many2one(
        'isca_pop.items_model',
        string="Item",
        required=True,
        domain="[('location', '=', base_location), ('create_uid', '=', uid)]",
        help="Select the item to change state and move quantity from. Only items from the selected location and created by you are shown."
    )
    
    current_state = fields.Selection(
        related="item_id.state",
        string="Current State",
        readonly=True,
        help="Displays the current state of the selected item."
    )

    available_quantity = fields.Integer(
        string="Available Quantity",
        compute="_compute_available_quantity",
        readonly=True,
        help="Displays the available quantity of the selected item."
    )

    quantity_to_move = fields.Integer(
        string="Quantity to Move",
        required=True,
        help="Enter the quantity to move to the new state."
    )

    new_state = fields.Selection(
        [("new", "New"), ("usable", "Usable"), ("broken", "Broken")],
        string="New State",
        required=True,
        help="Specify the new state for the moved quantity."
    )

    @api.depends('item_id')
    def _compute_available_quantity(self):
        for record in self:
            record.available_quantity = record.item_id.quantity if record.item_id else 0

    @api.constrains('new_state')
    def _check_new_state(self):
        for record in self:
            if record.item_id and record.new_state == record.item_id.state:
                raise ValidationError("The new state must be different from the current state.")

    def action_confirm(self):
        if self.quantity_to_move <= 0:
            raise ValidationError("Quantity must be greater than zero.")
        if self.item_id and self.quantity_to_move > self.item_id.quantity:
            raise ValidationError("Not enough quantity in the selected base location.")

        remaining_quantity = self.item_id.quantity - self.quantity_to_move

        # Instead of creating a donation record, create/update an item record with the new state.
        # The create method on isca_pop.items_model is overridden to update quantity if a duplicate exists.
        self.env['isca_pop.items_model'].create({
            'name': self.item_id.name,
            'photo': self.item_id.photo,
            'state': self.new_state,
            'user_id': self.env.user.id,
            'category_id': self.item_id.category_id.id,
            'location': self.item_id.location.id,
            'quantity': self.quantity_to_move,
        })

        # Update the source item by deducting the moved quantity.
        if remaining_quantity == 0:
            self.item_id.active = False
            self.item_id.with_context(force_unlink=True).unlink()
        else:
            self.item_id.quantity = remaining_quantity

        return {'type': 'ir.actions.act_window_close'}
