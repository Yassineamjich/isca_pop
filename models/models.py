# -*- coding: utf-8 -*-

# from odoo import models, fields, api


# class isca_pop(models.Model):
#     _name = 'isca_pop.isca_pop'
#     _description = 'isca_pop.isca_pop'

#     name = fields.Char()
#     value = fields.Integer()
#     value2 = fields.Float(compute="_value_pc", store=True)
#     description = fields.Text()
#
#     @api.depends('value')
#     def _value_pc(self):
#         for record in self:
#             record.value2 = float(record.value) / 100

