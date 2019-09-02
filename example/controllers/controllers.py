# -*- coding: utf-8 -*-
from odoo import http

# class Example(http.Controller):
#     @http.route('/example/example/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/example/example/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('example.listing', {
#             'root': '/example/example',
#             'objects': http.request.env['example.example'].search([]),
#         })

#     @http.route('/example/example/objects/<model("example.example"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('example.object', {
#             'object': obj
#         })