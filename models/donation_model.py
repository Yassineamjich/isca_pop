from odoo import models, fields, api
from odoo.exceptions import UserError, ValidationError

class IscaPopDonationModel(models.Model):
     _name = 'isca_pop.donation_model'
     _description = 'my  model for donations'
     
     name = fields.Char(string="Name")
     photo=fields.Binary(string="Foto")
     donator = fields.Many2one("res.users", string="Donated by :")
     reservedby=fields.Many2one("res.users",String = "Reserved by : ")
     reserve = fields.Boolean(string = "reserved")
     confirmed = fields.Boolean(string="Confirmed", default=False)
     state = fields.Selection([("new", "New"),
                               ("usable","Usable"),
                               ("broken","Broken")],string="State",default="new")
     location=fields.Many2one('isca_pop.location_model',string="Location")
     quantity = fields.Integer(string = "Quantity")
     category_id = fields.Many2one('isca_pop.category_model', string="Category")
     
     @api.depends()
     def _compute_current_user(self):
        for record in self:
            record.currentuser = self.env.uid
     def confirm_donation(self):
        """Set 'confirmed' to True only if 'reserved' is True."""
        for record in self:
            if record.reserve and record.donator.id == self.env.uid:
                record.confirmed = True
     def write(self, vals):
        if 'reserve' in vals and vals['reserve']:  # If 'reserved' is set to True
            vals['reservedby'] = self.env.uid        # Assign the current user to 'reservedby'
        elif 'reserve' in vals and not vals['reserve']:  # If 'reserved' is set to False
            vals['reservedby'] = None      
                 # Clear the 'reservedby' field
        
        return super(IscaPopDonationModel, self).write(vals)
     
    
     def open_cancel_donation_wizard(self):
        # This method is called when the button is clicked
        return {
            'type': 'ir.actions.act_window',  # Specifies the type of action to perform (window action).
            'name': 'Cancel Donation',  # The name of the action.
            'res_model': 'isca_pop.cancel_donation_model',  # The model for the wizard.
            'view_mode': 'form',  # Specifies the view mode to open the form view.
            'target': 'new',  # Open in a new window.
             'context': {
            'default_donation_id': self.id,  # Pass the active_id to the wizard
            }
        }
     def create_item_from_donation(self):
        """
        Create a new Item record (isca_pop.items_model) using values from the donation.
        The new Item's owner (user_id) is set to the donation's reservedby.
        This method only runs if the donation is confirmed.
        Note: Location and Category are not set so that the new owner can update them.
        After successfully creating the item, the donation record is unlinked.
        """
        for donation in self:
            if donation.confirmed and donation.donator.id == self.env.uid:
                # Build the values for the new item, excluding location and category_id.
                item_vals = {
                    'name': donation.name,
                    'photo': donation.photo,
                    'state': donation.state,  # Adjust as needed.
                    'quantity': donation.quantity,
                    'user_id': donation.reservedby.id,  # Set owner to reservedby.
                }
                # Create the item record using the reservedby user as the creator.
                self.env['isca_pop.items_model'].with_user(donation.reservedby).create(item_vals)
                donation.unlink()
     def unlink(self):
        allowed = self.filtered(lambda r: r.create_uid.id == self.env.uid and (r.confirmed or not r.reserve))
        return super(IscaPopDonationModel, allowed).unlink()