from odoo import models, fields, api
from odoo.exceptions import ValidationError

class IscaPopDonationModel(models.Model):
     _name = 'isca_pop.donation_model'
     _description = 'my  model for donations'

     name = fields.Char(string="Name")
     photo=fields.Binary(string="Foto")
     donator = fields.Many2one("res.users",String ="Donated by : ",default=lambda self: self)
     reservedby=fields.Many2one("res.users",String = "Reserved by : ")
     reserve = fields.Boolean(string = "reserved")
     field_test = fields.Char(String= "test",default = "I am the best")
     state = fields.Selection([("new", "New"),
                               ("usable","Usable"),
                               ("broken","Broken")],string="State",default="new")
     location=fields.Many2one('isca_pop.location_model',string="Location")
     quantity = fields.Integer(string = "Quantity")
     category_id = fields.Many2one('isca_pop.category_model', string="Category")
     
     
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
     @api.model
     def _render_qweb_pdf(self, docids, data=None):
    # Fetch the records for which the PDF is being generated.
        docs = self.env[self.model].browse(docids)
    
    # Iterate over each record in docs.
        for doc in docs:
            # Retrieve the donation name; if it's empty, default to an empty string.
            
            
            # Concatenate the donation name and the donator's name.
            
            
            # Update the 'field_test' field with the concatenated string.
            doc.write({'field_test': "it works"})
        
    # Call the original _render_qweb_pdf method to continue generating the PDF.
        return super(IscaPopDonationModel, self)._render_qweb_pdf(docids, data)