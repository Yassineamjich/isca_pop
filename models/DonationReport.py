from odoo import models

class DonationReport(models.AbstractModel):
    _name = 'report.isca_pop.donation_template'

    def _render_qweb_pdf(self, report_ref, docids, data=None):
        # Call the update_field_test method in the donation model
        donations = self.env['isca_pop.donation_model'].browse(docids)
        donations.update_field_test()  # Update field_test for each donation
        # Call the super method to generate the PDF
        return super(DonationReport, self)._render_qweb_pdf(report_ref, docids, data)