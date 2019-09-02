# -*- coding: utf-8 -*-
import datetime

from odoo import models, fields, api


class example(models.Model):
    _name = 'example.example'
    name = fields.Char(default=lambda self: self.env['ir.sequence'].next_by_code(self._name))
    active = fields.Boolean(default=True, string='归档', required=True)  # 系统保留变量, False时不在主页显示，需要筛选改为True才能显示
    price = fields.Float()
    note = fields.Text()
    content = fields.Html(readonly=True)

    select = fields.Selection([
        ('1', 'em'),
        ('2', 'emm'),
        ('3', 'emmm'),
    ], groups="example.example_groups_b")
    em1_mo = fields.Many2one(comodel_name='example.example1')
    em1_om = fields.One2many(comodel_name='example.example1', inverse_name='em_mo')
    em1_mm = fields.Many2many(comodel_name='example.example1', column1='name', column2='fuck_id')
    my_reference = fields.Reference(selection='_select_objects')

    @api.model
    def _select_objects(self):
        records = self.env['ir.model'].search([])
        return [(record.model, record.name) for record in records] + [('', '')]

    # 添加状态值和, 按钮事件
    state = fields.Selection(
        [('1', '状态1'), ('2', '状态2'), ('3', '状态3')],
        readonly=True,
        default='1'
    )
    """
    [(状态值, 状态条中显示的内容), ('1', '状态1'),...]
    """

    def button1(self):
        return self.write({'state': '1'})

    def button2(self):
        return self.write({'state': '2'})

    def button3(self):
        return self.write({'state': '3'})

    _inherit = ['mail.thread']
    my_datetime = fields.Datetime(default=fields.Datetime.now, track_visibility='onchange')
    # my_date = fields.Date(default=fields.Date.today)

    my_date = fields.Date(default=lambda self: datetime.date.today() + datetime.timedelta(days=4),
                          track_visibility='always'
                          )

    def button4(self):
        # 通过用户test的id, 实现点击关注用户test,
        # 获取id方法设置->用户&公司->test->相关的业务伙伴->test 查看当前URL id
        self.message_subscribe(partner_ids=[7])

    def button5(self):
        # 点击添加备注
        self.message_post(body='emmm')

    name_and_price = fields.Char(
        compute='_compute_price_add_state_value'
    )

    @api.depends('price', 'name')
    def _compute_price_add_state_value(self):
        # 添加计算字段
        for order in self:
            order.name_and_price = '{} {}'.format(order.name, order.price)

    @api.onchange('price', 'name')
    def change_price_add_state_value(self):
        # 修改时,自动更新计算字段
        self.update(dict(
            name_and_price='{} {}'.format(self.name, self.price)
        ))

    my_related1 = fields.Integer(related='em1_mo.fuck_id', string='关联到em1_mo.fuck_id', store=True)
    my_related2 = fields.Date(related='my_date', string='关联到my_date', store=True)


class em1(models.Model):
    _name = 'example.example1'
    fuck_id = fields.Integer()
    em_mo = fields.Many2one('example.example')
