# -*- coding: utf-8 -*-
import requests

from odoo import models, fields, api, _


class LaravelInheritProductCategory(models.Model):
    _inherit = "product.category"
    unique_id = fields.Char(required=False)


class LaravelInheritProductBrand(models.Model):
    _inherit = "product.brand"
    unique_id = fields.Char(required=False)


class LaravelConnectorOperations(models.TransientModel):
    _name = 'laravel.connector.operations'

    name = fields.Selection(string="Select Operation",
                            selection=[('p_category', 'Product Category'), ('p_brand', 'Product Brand'), ],
                            required=True, )

    def create_product_category(self, *data):
        if data:
            for li in data:
                for rec in li:
                    unique_id = self.env['product.category'].search([]).mapped('unique_id')
                    if not rec['unique_id'] in unique_id:
                        self.env['product.category'].create({
                            'name': rec['name'],
                            'unique_id': rec['unique_id']
                        })

    def create_product_brand(self, *data):
        if data:
            for li in data:
                for rec in li:
                    unique_id = self.env['product.brand'].search([]).mapped('unique_id')
                    if not str(rec['id']) in unique_id:
                        self.env['product.brand'].create({
                            'name': rec['name'],
                            'unique_id': rec['id']
                        })
    def sync_action(self):
        for rec in self:
            if rec.name == 'p_category':
                try:
                    request_data = requests.post(url='https://mastbeauty.com/api/get-category/')
                    collected_data = request_data.json().get('data')
                    rec.create_product_category(collected_data)
                except Exception as e:
                    print(e)

            if rec.name == 'p_brand':
                try:
                    request_data = requests.post(url='https://mastbeauty.com/api/get-brand/')
                    collected_data = request_data.json().get('data')
                    rec.create_product_brand(collected_data)
                except Exception as e:
                    print(e)
