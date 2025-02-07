# -*- coding: utf-8 -*-
# from odoo import http


# class IscaPop(http.Controller):
#     @http.route('/isca_pop/isca_pop', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/isca_pop/isca_pop/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('isca_pop.listing', {
#             'root': '/isca_pop/isca_pop',
#             'objects': http.request.env['isca_pop.isca_pop'].search([]),
#         })

#     @http.route('/isca_pop/isca_pop/objects/<model("isca_pop.isca_pop"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('isca_pop.object', {
#             'object': obj
#         })

