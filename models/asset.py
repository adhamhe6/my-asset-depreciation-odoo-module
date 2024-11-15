# asset_depreciation/models/asset.py
from odoo import api, fields, models, _
from datetime import date

class Asset(models.Model):
    _name = 'asset.depreciation'
    _description = 'Asset Depreciation Management'

    name = fields.Char(string="Asset Name", required=True)
    purchase_date = fields.Date(string="Purchase Date", default=fields.Date.today)
    cost = fields.Float(string="Asset Cost", required=True)
    depreciation_method = fields.Selection([
        ('straight_line', 'Straight Line'),
        ('declining_balance', 'Declining Balance')
    ], string="Depreciation Method", required=True, default='straight_line')
    useful_life = fields.Integer(string="Useful Life (Years)", required=True)
    salvage_value = fields.Float(string="Salvage Value", required=True, default=0.0)
    depreciation_value = fields.Float(string="Depreciation Value", compute='_compute_depreciation_value', store=True)
    accumulated_depreciation = fields.Float(string="Accumulated Depreciation", compute='_compute_accumulated_depreciation', store=True)
    current_value = fields.Float(string="Current Value", compute='_compute_current_value', store=True)

    @api.depends('cost', 'salvage_value', 'useful_life', 'depreciation_method')
    def _compute_depreciation_value(self):
        for asset in self:
            if asset.depreciation_method == 'straight_line':
                asset.depreciation_value = (asset.cost - asset.salvage_value) / asset.useful_life
            elif asset.depreciation_method == 'declining_balance':
                rate = 2 / asset.useful_life  # Assuming a double-declining balance method
                asset.depreciation_value = (asset.cost - asset.salvage_value) * rate

    @api.depends('purchase_date', 'depreciation_value', 'useful_life')
    def _compute_accumulated_depreciation(self):
        for asset in self:
            years_elapsed = date.today().year - asset.purchase_date.year
            if asset.depreciation_method == 'straight_line':
                asset.accumulated_depreciation = min(asset.depreciation_value * years_elapsed, asset.cost - asset.salvage_value)
            elif asset.depreciation_method == 'declining_balance':
                value = asset.cost
                for _ in range(years_elapsed):
                    value -= (value * (2 / asset.useful_life))
                asset.accumulated_depreciation = asset.cost - value

    @api.depends('cost', 'accumulated_depreciation')
    def _compute_current_value(self):
        for asset in self:
            asset.current_value = asset.cost - asset.accumulated_depreciation

    @api.onchange('depreciation_method')
    def _onchange_depreciation_method(self):
        if self.depreciation_method == 'straight_line':
            self.salvage_value = 0.0
            self.useful_life = 5  # Default useful life for straight-line
        elif self.depreciation_method == 'declining_balance':
            self.useful_life = 10  # Default useful life for declining balance
