1. 激活开发者模式
    - 点击设置(点下左上角的四个小方块, 就能看到)
    - 点击页面右侧的激活开发者模式

2. 成为超级用户
    - 点击右上方开发者工具(小虫子按钮)
    - 点击成为超级用户

3. 创建应用
    - ` python odoo-bin scaffold example addons`
        - `python odoo-bin scaffold 模型名称 放置它的位置`
        -  执行后会发现在odoo-12.0/addons里面有个新建的文件夹example, 里面会包含`__init__.py  __manifest__.py  controllers  demo  models  security  views`这几个文件夹
        - 应用目录
            - controllers
                - 控制器 (HTTP路径)
            - data
                - 演示和数据XML
            - doc
                - 模型说明
            - models
                - 定义模型
            - report
                - 报告
            - security
                - 权限管理
            - i18n
                - 翻译
            - views
                - 视图和模型
            - static
                - CSS
                - JS
                - IMG
                - LIB
                - ...
            - tests
                - 存放 python 和 yml 测试用例
            - wizard
                - 放临时的 model 和视图 

            <summary>__manifest__.py</summary>
            <details>

            ```python
            # -*- coding: utf-8 -*-
            {
                # 模型名
                'name': "example",

                # 摘要
                'summary': """
                    Short (1 phrase/line) summary of the module's purpose, used as
                    subtitle on modules listing or apps.openerp.com""",
                # 介绍
                'description': """
                    Long description of module's purpose
                """,

                # 作者
                'author': "My Company",

                # 网址
                # 'website': "http://www.yourcompany.com",

                # Categories can be used to filter modules in modules listing
                # Check https://github.com/odoo/odoo/blob/12.0/odoo/addons/base/data/ir_module_category_data.xml
                # for the full list

                # 类别
                'category': 'Uncategorized',

                # 版本号
                'version': '0.1',

                # any module necessary for this one to work correctly
                # 依赖
                'depends': ['base'],

                # always loaded
                # 数据文件
                'data': [
                    # 'security/ir.model.access.csv',
                    'views/views.xml',
                    'views/templates.xml',
                ],
                # only loaded in demonstration mode
                    
                # 演示文件
                'demo': [
                    'demo/demo.xml',
                ],
            }
            ```
            </details>
                
4. 安装应用
    1. 重启odoo服务
    2. 点击`刷新本地模型列表`
    3. 弹出窗口点击`更新`按钮
    4. 删除搜索框内容,然后输入`example`
    5. 点击安装
        - 以后执行步骤4时, 点击三个小点点. 然后点击升级按钮

5. 新建模型 
    <summary>修改addons/example/models/models.py</summary>
    <details>

    ```python
    # -*- coding: utf-8 -*-
    import datetime

    from odoo import models, fields, api


    class example(models.Model):
        _name = 'example.example'
        name = fields.Char()
        active = fields.Boolean(default=True, string='归档', required=True)  # 系统保留变量, False时不在主页显示，需要筛选改为True才能显示
        price = fields.Float()
        note = fields.Text()
        content = fields.Html(readonly=True)
        my_datetime = fields.Datetime(default=fields.Datetime.now)
        # my_date = fields.Date(default=fields.Date.today)
        my_date = fields.Date(default=lambda self: datetime.date.today() + datetime.timedelta(days=4))
        select = fields.Selection([
            ('1', 'em'),
            ('2', 'emm'),
            ('3', 'emmm'),
        ])
        em1_mo = fields.Many2one(comodel_name='example.example1')
        em1_om = fields.One2many(comodel_name='example.example1', inverse_name='em_mo')
        em1_mm = fields.Many2many(comodel_name='example.example1', column1='name', column2='fuck_id')
        my_reference = fields.Reference(selection='_select_objects')

        @api.model
        def _select_objects(self):
            records = self.env['ir.model'].search([])
            return [(record.model, record.name) for record in records] + [('', '')]


    class em1(models.Model):
        _name = 'example.example1'
        fuck_id = fields.Integer()
        em_mo = fields.Many2one('example.example')

    ```
    </details>
    
    <summary>知识内容</summary>
    <details>

    - 模型的字段
        - 系统字段
            -  `_name`
                - 必需的
                - 定义了Odoo系统中模型的名称
            - `_description`
                - 为模型添加更为友好的描述，更新后在Settings下可发现相应的变化(需开启调试模式Database Structure>Models)
            - `_order`
                - 默认情况下Odoo使用内置的id进行排序，可以通过逗号分隔指定多个字段进行排序，desc表示降序，仅能使用数据库中存储的字段排序，外部计算后的字段不适用，_order有些类似SQL语句中的ORDER BY,但无法使用NULL FIRST之类的语句
            - 字段共同属性
                - string(unicode, 默认：字段名称)
                    - UI中字段的标签(用户可见)
                - required(bool默认：False)
                    - 如果True该字段不能为空, 则它必须具有默认值或在创建记录时始终给定值
                - help(unicode默认：'')
                    - 长格式, 在UI中为用户提供帮助工具提示
                - index(bool默认：False)
                    - 请求Odoo 在列上创建数据库索引
                - readonly(bool默认：False)
                    - 是否只读

        - Model字段类型    
            - 字段共同属性
                - string(unicode, 默认：字段名称)
                    - UI中字段的标签(用户可见)
                - required(bool默认：False)
                    - 如果True该字段不能为空, 则它必须具有默认值或在创建记录时始终给定值
                - help(unicode默认：'')
                    - 长格式, 在UI中为用户提供帮助工具提示
                - index(bool默认：False)
                    - 请求Odoo 在列上创建数据库索引
                - readonly(bool默认：False)
                    - 是否只读
            - 常用字段属性
                - default
                    - 默认值
            - Binary
                - Binary字段用于存储二进制文件，如图片或文档
                - `a = fields.Binary()`
            - Float
                - Float用于存储数值，其精度可以通过数字长度和小数长度一对值来进行指定
                ```python
                a = fields.Float(
                    string='float',
                    digits=(14, 4), # Optional precision (total, decimals)
                    )
                ```
            - Boolean
                - Boolean字段用于存储True/False布尔值
                - `a = fields.Boolean()`
            - Integer
                - Integer即为整型
                - `a = fields.Integer()`
            - Char
                - Char用于字符串
                - `a = fields.Char(string='aa', required=True)`
            - Date
                - Date字段用于存储日期，ORM中以字符串格式对其进行处理，但以日期形式存放在数据库中，该格式在odoo.fileds.DATE_FORMAT中定义
                - `my_date = fields.Date(default=fields.Date.today)`
                - `my_date = fields.Date(default=lambda self: datetime.date.today() + datetime.timedelta(days=4))`
            - Datetime
                - Datetime用于存储日期时间，在数据库中以UTC无时区时间(naive)存放，ORM中以字符串和UTC时间表示，该格式在odoo.fields.DATETIME_FORMAT中定义
                - `my_datetime = fields.Datetime(default=fields.Datetime.now)`
            - Text
                - Text用于多行字符串
                - `notes = fields.Text()`
            - Monetary
                - 货币
                - `a=fields.Monetary()`
            - Html
                - Used to store HTML, provides an HTML widget.
                - Html类似text字段，但一般用于存储富文本格式的HTML
                - strip_style=True:清除所有样式元素
                - strip_class=True:清除类属性
                - `description = fields.Html()`
            - Selection
                - Store Text in database but propose a selection widget. It induces no selection constraint in database. Selection must be set as a list of tuples or a callable that returns a list of tuples
                - Selection用于选择列表，由值和描述对组成，选择的值将存储在数据库中，可以为字符串或整型，描述默认可翻译,虽然整型的值看似简洁，但注意Odoo会把0解析为未设置(unset)，因而当存储值为0时不会显示描述
                - index: Tells Odoo to index for faster searches replaces the select kwarg

                ```python
                select = fields.Selection([
                    ('1', 'em'),
                    ('2', 'emm'),
                    ('3', 'emmm'),
                ], required=True, default='1')
                ```
            - Many2one
                - Store a relation against a co-model
                - comodel_name指定绑定多对一的模型名, 即类名
                - `em1_mo = fields.Many2one(comodel_name='example.example1')`
            - Many2many
                - Store a relation against many2many rows of co-model
                - Many2many会新建一个中间表, relation指定中间表的表名
                - 例:
                    ```python
                    _name = 'emm.a'
                    e = Many2many(
                        comodel_name='emmm.b',   # 关联的表
                        relation='emmm_a_b_rel', # 可选, 中间表名
                        column1='a_id',          # 当前表的字段名
                        column2='b_id',          # 关联的其他表的字段名
                        string='Tags') 
                    ```
            - One2many
                - Store a relation against many rows of co-model
                - 新建one2many前需要先写many2one, 并且数据库的外键会建立在many2one上
                - comodel_name: 指定绑定一对多的模型名, 即类名
                - inverse_name: 指定绑定一对多的模型的Many2one字段的名
                - domain
                    - 过滤, 例:`domain=[('id','=',1)]`

                ```python
                class em(models.Model):
                    _name = 'example.example'
                    em1_om = fields.One2many(comodel_name='example.example1', inverse_name='em_mo')

                class em1(models.Model):
                    _name = 'example.example1'
                    em_mo = fields.Many2one('example.example')
                ```
                
            - Reference
                - Store an arbitrary reference to a model and a row
                - 事先不能决定关联的目标模型时, 这种情况需要使用reference将目标模型的选择权留给用户
                
                ```python
                my_reference = fields.Reference(selection='_select_objects')

                @api.model
                def _select_objects(self):
                    records = self.env['ir.model'].search([])
                    return [(record.model, record.name) for record in records] + [('', '')]
                ```

        - 保留字段
            - Odoo在所有模型中都创建了以下几个字段,这些字段由系统管理,是系统保留的字段, 用户不应定义
                - id(Id)
                    - 模型中记录的唯一标识符
                - create_date(Datetime)
                    - 记录的创建日期
                - create_uid(Many2one)
                    - 创建记录的用户
                - write_date(Datetime)
                    - 记录的最后修改日期
                - write_uid(Many2one)
                    - 上次修改记录的用户
        - Method and decorator
            - @api.returns
                - This decorator guaranties unity of returned value. It will return a RecordSet of specified model based on original returned value:
                ```python
                @api.returns('res.partner')
                def afun(self):
                    ...
                    return x  # a RecordSet
                ```
            - @api.one
                - This decorator loops automatically on Records of RecordSet for you. Self is redefined as current record:
                ```python
                @api.one
                def afun(self):
                    self.name = 'toto'
                ```
            - @api.multi
                - Self will be the current RecordSet without iteration. It is the default behavior:
                ```python
                @api.multi
                def afun(self):
                    len(self)
                ```
            - @api.model
                - This decorator will convert old API calls to decorated function to new API signature. It allows to be polite when migrating code.
                ```python
                @api.model
                def afun(self):
                    pass
                ```
            - @api.constrains
                - This decorator will ensure that decorated function will be called on create, write, unlink operation. If a constraint is met the function should raise a openerp.exceptions.Warning with appropriate message.
            - @api.depends
                - This decorator will trigger the call to the decorated function if any of the fields specified in the decorator is altered by ORM or changed in the form
                ```python
                @api.depends('name', 'an_other_field')
                def afun(self):
                    pass
                ```
            - @api.onchange
                - This decorator will trigger the call to the decorated function if any of the fields specified in the decorator is changed in the form
                ```python
                @api.onchange('fieldx')
                def do_stuff(self):
                    if self.fieldx == x:
                        self.fieldy = 'toto'
                ```
            - @api.noguess
                - This decorator prevent new API decorators to alter the output of a method
    </details>
    
        
6. 升级应用
    1. 重启odoo服务
    2. 在搜索框输入`example`
    3. 点击升级



7. 修改数据文件
    <summary>修改addons/example/views/views.xml文件</summary>
    <details>

    ```xml
    <odoo>
        <data>
            <!-- explicit list view definition -->
            <!--选择显示哪些字段, 默认是name,即ui-->
            <record model="ir.ui.view" id="example.list">
                <field name="name">example模型表头</field>
                <field name="model">example.example</field>
                <field name="arch" type="xml">
                    <tree>
                        <field name="name"/>
                        <field name="active"/>
                        <field name="price"/>
                    </tree>
                </field>
            </record>


            <!-- actions opening views on models -->
            <!--选择哪些功能动作即action-->
            <!--res_model是目标模块的标识符 -->
            <record model="ir.actions.act_window" id="example.action_window">
                <field name="name">example act_window</field>
                <field name="res_model">example.example</field>
                <!--
                tree, 显示数据
                form, 新建数据
                默认为tree
                -->
                <field name="view_mode">tree,form</field>
            </record>


            <!-- server action to the one above -->
            <!--执行py代码-->
            <record model="ir.actions.server" id="example.action_server">
                <field name="name">example server</field>
                <field name="model_id" ref="model_example_example"/>
                <field name="state">code</field>
                <!--
                <field name="code">里面包裹的是py代码
                action将作为下一个要执行的操作返回给客户端
                -->
                <field name="code">
                    action = {
                    "type": "ir.actions.act_window",
                    "view_mode": "tree,form",
                    "res_model": "example.example",
                    }
                </field>
            </record>


            <!-- Top menu item -->
            <!--顶部菜单-->
            <menuitem name="example" id="example.menu_root"/>

            <!-- menu categories -->
            <!--分菜单-->
            <menuitem name="Menu 1" id="example.menu_1" parent="example.menu_root"/>
            <menuitem name="Menu 2" id="example.menu_2" parent="example.menu_root"/>


            <!-- actions -->
            <!--菜单绑定动作-->
            <menuitem name="List" id="example.menu_1_list" parent="example.menu_1"
                    action="example.action_window"/>
            <menuitem name="Server to list" id="example" parent="example.menu_2"
                    action="example.action_server"/>

        </data>
    </odoo>
    ```
    </details>

    重复步骤4 升级应用

    <summary>知识内容</summary>
    <details>

    - 数据文件仅在安装或更新模块时才加载数据文件的内容
    - 模块的数据通过带有`<record>`元素的数据文件, XML文件声明.每个`<record>`元素都创建或更新数据库记录
    - 数据文件必须在要manifest文件中声明数据文件, 它们可以在`data`列表(始终加载)或`demo`列表中声明(仅在演示模式下加载).
    - 属性
        - model
            - 记录的Odoo模块的名称
        - id
            - 一个外部标识符, 用于被引用
        - `<field>`
            - name标识字段名称
            - `<field>`的innnerText是`<field>`的值
    - menuitem 
        - 必须先声明相应的Action, 因为数据文件按顺序执行, 在id创建菜单之前, Action必须存在于数据库中
        - 在创建完菜单后必须成为超级用户才能正常显示新建的菜单
        - menuitem 只有绑定action， 或子menuitem绑定了action才能显示出来
        - 属性
            - id: 定义唯一标记
            - action: 绑定动作
            - parent: 父菜单
            - sequence: 优先级, 数字越小优先级越高, 显示越靠前,最小为0
            - groups: 绑定权限
            - name: 菜单名称

    - view
        - **视图定义了模块记录的显示方式(Views define the way the records of a model are displayed)**.每种类型的视图代表一种可视化模式(记录列表, 其聚合图, ......).可以通过类型(例如合作伙伴列表)或特别是通过其ID 来一般性地请求视图.对于通用请求, 将使用具有正确类型和最低优先级的视图(因此每种类型的最低优先级视图是该类型的默认视图).
        
        - 对于view 中的`<record>`的id, 会被存到数据库中, 而且当你修改`<record>`的model, 然后再次执行, 则`<record>`的model仍为修改前的model, 不报错, 且正常使用
            - 解决方法:
                - 修改`<record>`的id
                - 或将`<record>`删除, 重启服务,升级模块, 然后再写`<record>`
    </details>
    
    

8. 自定义添加数据的表单
    <summary>修改addons/example/models/models.py</summary>
    <details>

    ```python
    # -*- coding: utf-8 -*-
    import datetime

    from odoo import models, fields, api


    class example(models.Model):
        _name = 'example.example'
        name = fields.Char()
        active = fields.Boolean(default=True, string='归档',required=True)  # 系统保留变量, False时不在主页显示，需要筛选改为True才能显示
        price = fields.Float()
        note = fields.Text()
        content = fields.Html(readonly=True)
        my_datetime = fields.Datetime(default=fields.Datetime.now)
        # my_date = fields.Date(default=fields.Date.today)
        my_date = fields.Date(default=lambda self: datetime.date.today() + datetime.timedelta(days=4))
        select = fields.Selection([
            ('1', 'em'),
            ('2', 'emm'),
            ('3', 'emmm'),
        ])
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

    class em1(models.Model):
        _name = 'example.example1'
        fuck_id = fields.Integer()
        em_mo = fields.Many2one('example.example')

    ```
    </details>
    
    <summary>修改addons/example/views/views.xml文件</summary>
    <details>

    ```xml
    <odoo>
        <data>
            <record model="ir.ui.view" id="example.list">
                <field name="name">列表显示字段</field>
                <field name="model">example.example</field>
                <field name="arch" type="xml">
                    <tree>
                        <field name="name"/>
                        <field name="active"/>
                        <field name="price"/>
                        <field name="note"/>
                        <field name="content"/>
                        <field name="my_date"/>
                        <field name="my_datetime"/>
                        <field name="select"/>
                        <field name="em1_mo"/>
                        <field name="em1_om"/>
                        <field name="em1_mm"/>
                        <field name="my_reference"/>
                    </tree>
                </field>
            </record>

            <!--动作-->
            <record id="example.root_menu_action_view" model="ir.actions.act_window">
                <field name="type">ir.actions.act_window</field>
                <field name="name">我会被显示出来</field>
                <field name="res_model">example.example</field>
            </record>

            <!--自定义form表单-->
            <record id="example.example_form_view" model="ir.ui.view">
                <field name="model">example.example</field>
                <field name="arch" type="xml">
                    <form>
                        <header>
                            <!--三个按钮, 一个状态条-->
                            <!--
                            - button
                                - name: 点击时执行的函数名
                                - string: 按钮显示内容
                                - states: 当状态值为多少时, 该按钮可见, 不设置则永远可见
                            - <field name="state" widget="statusbar"/>
                                -  statusbar_visible: 根据state值确定哪些状态在状态条上显示
                            -->

                            <button states="1" name="button2" string="当前状态值为1, 点击设置为2" class="oe_highlight" type="object"/>
                            <button states="1" name="button3" string="当前状态值为1, 点击设置为3" class="oe_highlight" type="object"/>
                            <button states="2" name="button3" string="当前状态值为2, 点击设置为3" class="oe_highlight" type="object"/>
                            <button states="3" name="button1" string="当前状态值为3, 点击设置为1" class="oe_highlight" type="object"/>
                            <field name="state" widget="statusbar" statusbar_visible="1,2,3"/>

                        </header>
                        <sheet>
                            <group string="group1">
                                <field name="name"/>
                                <field name="active"/>
                                <field name="price" readonly="1"/>
                            </group>
                            <group string="group2">
                                <field name="my_datetime" attrs="{'invisible': [('active', '=', False)]}"/>
                                <!--
                                此处的required的优先级大于models中的required, 但是提交时会弹错
                                -->
                                <field name="my_date" required="1"/>
                                <field name="select" required="0"/>
                            </group>
                            <group string="group3">
                                <field name="em1_mo"/>
                                <field name="em1_om"/>
                                <field name="em1_mm"/>
                                <field name="my_reference"/>

                            </group>
                            <notebook string="notebook1">
                                <page string="page1">
                                    <field name="note"/>

                                </page>
                                <page string="page1">
                                    <field name="content"/>
                                </page>
                            </notebook>
                        </sheet>
                    </form>
                </field>
            </record>

            <menuitem id="example.root_menu" name="example" action="example.root_menu_action_view" sequence="1"/>
        </data>
    </odoo>
    ```
    </details>
    重复步骤4: 升级应用

    <summary>知识内容</summary>
    <details>
    
    - **`model="ir.ui.view"`的recoder 不需要绑定任何只要在xml文件中出现既能正常显示**
    - 视图被声明为ir.ui.view的Model的record.视图类型由arch字段的根元素声明
    

    - 表单视图
        - 属性
            - create="0": 不可新建
            - edit="0": 编辑 
            - delete="0": 删除
        - field属性
            - widget
                - statusbar
                    - 头部状态条标签
                - email
                    - 电子邮件地址标签
                - selection
                    - 下拉选择标签
                - mail_followers
                    - 关注者标签
                - mail_thread
                    - 消息标签
                - progressbar
                    - 进度条，按百分比标签
                - one2many_list 
                    - 一对多列表标签
                - many2many_tags
                    - 多对多显示标签
                - url
                    - 网站链接标签
                - image 
                    - 图片标签
                - many2many_kanban
                    - 看版标签
                - handler
                    - 触发标签
                - radio
                    - 单选标签
                - char_domain
                    - 字符域标签
                - monetary
                    - 价格（和精度位数相关）标签
                - float_time
                    - 单精度时间标签
                - html
                    - html相关标签
                - pad 
                    - pad显示相关标签
                - date
                    - 日期标签
                - monetary
                    - 金额标签
                - text 
                    - 文本标签
                - sparkline_bar
                    - 燃尽标签
                - checkbox 
                    - 复选框标签
                - reference
                    - 关联标签    
            - `required`
                - 必填
            - `readonly`
                - 只读
            - `invisible`
                - 不可见
            - 根据条件变化
                - `name='123'`时`invisible="1"`
                - `active=True`时`required="1"`
                - 当前字段不是'many2many', 'many2one'状态时`readonly="1"`
                ```xml
                attrs="{
                    'invisible':[('name','=','123')],
                    'required':[('active','=', True)],
                    'readonly':[('ttype','not in', ['many2many', 'many2one'])]    
                    }"
                ```
            - 过滤one2many, many2many, 后面的many
                - domain
                - `domain="[('id','=',1)]"`
        
        <summary>表单视图还可以使用纯HTML来实现更灵活的布局</summary>
        <details>

        ```xml
        <form string="Idea Form">
            <header>
                <button string="Confirm" type="object" name="action_confirm" states="draft" 
                class="oe_highlight" />
                <button string="Mark as done" type="object" name="action_done" 
                states="confirmed" class="oe_highlight"/>
                <button string="Reset to draft" type="object" name="action_draft" 
                states="confirmed,done" />
                <field name="state" widget="statusbar"/>
            </header>
            <sheet>
                <div class="oe_title">
                    <label for="name" class="oe_edit_only" string="Idea Name" />
                    <h1><field name="name" /></h1>
                </div>
                <separator string="General" colspan="2" />
                <group colspan="2" col="2">
                    <field name="description" placeholder="Idea description..." />
                </group>
            </sheet>
        </form>
        ```
        </details>
            
    - 树视图
        > 树视图(也称为列表视图)以表格形式显示记录.他的根元素是`<tree>`.最简单的树形视图, 即只需列出要在表中显示的所有字段(每个字段作为列)
        
        - 属性
            - create="0": 不可新建
            - edit="0": 编辑 
            - delete="0": 删除
            
            ```xml
            <tree string="Idea list">
                <field name="name"/>
                <field name="inventor_id"/>
            </tree>
            ```
    - 搜索视图
        > 搜索视图通过列表视图(以及其他聚合视图)自定义关联的搜索字段.他的根元素是`<search>`, 他包含的字段, 定义了哪些时用于搜索的字段
        
        ```xml
        <search>
            <field name="name"/>
            <field name="inventor_id"/>
        </search>
        ```
        
        <summary>例</summary>
        <details>
        
        ```xml
            </field>
        </record>

        <record model="ir.ui.view" id="course_search_view">
            <field name="name">course.search</field>
            <field name="model">openacademy.course</field>
            <field name="arch" type="xml">
                <search>
                    <field name="name"/>
                    <field name="description"/>
                </search>
            </field>
        </record>
        ```
        </details>
    
        - 如果模块不存在搜索视图, 则Odoo会生成仅允许在该name字段上搜索的视图.
    </details>

9. 权限管理
    <summary>添加文件addons/em/security/security.xml</summary>
    <details>
    
    ```xml
    <?xml version="1.0" encoding="UTF-8" ?>
    <odoo>
        <record id="example.example_category" model="ir.module.category">
            <field name="name">example.example_category</field>
            <field name="sequence" eval="1"/>
        </record>
        <record id="example.example_groups_a" model="res.groups">
            <field name="name">example.example_groups_a</field>
            <field name="category_id" ref="example.example_category"/>
            <field name="implied_ids" eval="[(4, ref('base.group_user'))]"/>
        </record>
        <record id="example.example_groups_b" model="res.groups">
            <field name="name">example.example_groups_b</field>
            <field name="category_id" ref="example.example_category"/>
            <!--example.example_groups_a和example.example_groups_b, 只能选一个-->
            <field name="implied_ids" eval="[(4, ref('example.example_groups_a'))]"/>

            <!--example.example_groups_a和example.example_groups_b, 可以同时选-->
            <!--<field name="implied_ids" eval="[(4, ref('base.group_user'))]"/>-->
        </record>
    </odoo>
    ```
    </details>

    <summary>修改addons/example/__manifest__.py</summary>
    <details>

    ```python
    ...
    # always loaded
    # 数据文件
    'data': [
        'security/security.xml',
        'views/views.xml',
        'views/templates.xml',
    ],
    ...
    ```    
    </details>
    

    - 两种方法设置字段指定用户组可见
        <summary>法一. 修改addons/example/models/models.py</summary>
        <details>

        ```python
        ...
        # 设置example.example_groups_b组的用户可见
        select = fields.Selection([
            ('1', 'em'),
            ('2', 'emm'),
            ('3', 'emmm'),
        ], groups="example.example_groups_b")
        ...
        ```
        </details>
        
        法二. 修改addons/example/views/views.xml
        ```xml
        ...
        <field name="select" required="0" groups="example.example_groups_b"/>
        ...
        ```
            

        <summary>个人推荐法一</summary>
        <details>

        ```xml
        <record model="ir.actions.act_window" id="example.action_window">
            <field name="name">example act_window</field>
            <field name="res_model">example.example</field>
            <field name="view_mode">tree,form</field>
            <!-- 在model中设置groups后, 会自动权限管理 -->
        </record>
        ```
        </details>
        
    - 重复步骤4: 升级应用
    
    - 验证权限
        1. 修改群组访问权限
            1. 设置
            2. 用户&公司
            3. 群组
            4. 点击 `example.example_category / example.example_groups_a`
                1. 编辑
                2. 访问权限
                3. 添加明细行
                    - 名称随意
                    - 对象, 点击搜索更多后搜索并选择`example.example`
                    - 读, 写, 创建, 删除权限都勾上
                4. 添加明细行
                    - 名称随意
                    - 对象, 点击搜索更多后搜索并选择`example.example1`
                    - 读, 写, 创建, 删除权限都勾上
                5. 保存
     
        2. 新建用户
            1. 设置
            2. 用户&公司
            3. 用户
            4. 创建
            5. example.example_category 选择 example.example_groups_a, 其他随意
            6. 保存
            7. 点击中间的`动作`下拉框
                - 更改密码
                    - 输入密码
                    - 更改密码
     
        3. 登录刚才新建的用户
            - 点击创建
            - 是不是发现select没有了, 哈哈哈哈哈哈


10. 给name整个sequence
    - 新建文件夹`addons/example/data`
    - 新建文件`addons/example/data/example_sequence.xml`

    <summary>修改addons/example/data/example_sequence.xml</summary>
    <details>

    ```xml
    <?xml version="1.0" encoding="utf-8"?>
    <odoo>
        <!--
        年代: %(year)s
        年份: %(y)s
        月: %(month)s
        日: %(day)s
        某年某日: %(doy)s
        某年某周: %(woy)s
        某周某天 (0:周一): %(weekday)s
        时 00->24: %(h24)s
        时 00->12: %(h12)s
        分: %(min)s
        秒: %(sec)s
        -->
        <record id="example_sequence" model="ir.sequence">
            <field name="name">example.example</field>
            <field name="code">example.example</field>
            <field name="prefix">OUT%(year)s%(month)s%(day)s</field>

            <!--序列大小-->
            <field name="padding">4</field>
            <field name="company_id" eval="False"/>
        </record>
    </odoo>
    ```    
    </details>

    - 将文件路径添加到__manifest__.py中
        ```python
        'data': [
            'data/example_sequence.xml',
        ...
        ```
        
    - 修改addons/example/models/models.py
    
        ```python
        ...
        name = fields.Char(default=lambda self: self.env['ir.sequence'].next_by_code(self._name))
        ...
        ```
    
    - 重复步骤4
    - 此时会发现新建数据时. 会自动生成name

11. 继承mail模块
    - 修改`__manifest__.py`

        ```python
        ...
        'depends': ['base', 'mail'],
        ...
        ```
    - 重启odoo后, 查看example应用信息的技术数据, 可以发现依赖多了个mail

    <summary>修改addons/example/models/models.py</summary>
    <details>
    
    ```python
    ...
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
    ...
    ```
    </details>


    <summary>修改addons/example/views/views.xml文件</summary>
    <details>
    ```xml
    ...
    <field name="arch" type="xml">
        <form>

            <div class="oe_chatter">
                <field name="message_follower_ids" widget="mail_followers"/>
                <field name="message_ids" widget="mail_thread"/>
            </div>

            <header>
    ...
        <button states="3" name="button1" string="当前状态值为3, 点击设置为1" class="oe_highlight" type="object"/>

        <button name="button4" string="老铁, 点个关注" class="oe_highlight" type="object"/>
        <button name="button5" string="emmm" class="oe_highlight" type="object"/>

        <field name="state" widget="statusbar" statusbar_visible="1,2,3"/>
    ...
    ```
    </details>
        
    - track_visibility
        > 记录到备注中
        - track_visibility='onchange' :修改该字段时记录
        - track_visibility='always': 编辑track_visibility为onchange或always对应的字段时记录
            - track_visibility='always', odoo12.0 不可用时参考: https://www.cnblogs.com/edhg/p/11434625.html
    - 重复步骤4
        - 此时会发现多了块区域显示备注啥的

12. 重载系统函数
    <summary>修改addons/example/models/models.py</summary>
    <details>

    ```python
    ...
    @api.onchange('active')
    def onchange_active(self):
        # 修改记录的active字段时, 设置note内容
        self.update(dict(note='你敢改我active, 我就敢改我自己!'))

    def unlink(self):
        # 重写系统删除记录函数
        for order in self:
            if len(order.name) > 10:
                raise UserError('这谁起的名字这么长, 俺不愿意删, 改短点!!!')
        return super().unlink()

    @api.model
    def create(self, vals):
        # 新建记录后, 点击保存后执行
        # 很奇怪的地方就是float, int类型设定的默认值, 没有获取到
        return super().create(vals)

    def write(self, vals):
        # 修改记录后, 点击保存后执行, vals包括被修改后的值
        # 修改name后: vals = {'name': 'OUT201908sa300012asooss'}
        return super().write(vals)
    ...
    ```
    </details>
        
    - onchange: 修改指定字段时执行
    - unlink: 删除数据(记录)时执行
    - create: 创建数据(记录)时执行
    - write: 修改数据(记录)`后`执行
    - 重复步骤4

13. 计算字段
    > 会自动计算的字段

    <summary>修改addons/example/models/models.py</summary>
    <details>
    
    ```python
    ...
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
    ...
    ```
    </details>
        
    <summary>修改addons/example/views/views.xml文件</summary>
    <details>

    ```xml
    ...
    <record model="ir.ui.view" id="example.list">
        <field name="name">列表显示字段</field>
        <field name="model">example.example</field>
        <field name="arch" type="xml">
        <tree>
            <field name="name_and_price"/>
    ...
                    <field name="select" required="0"/>
                    <field name="name_and_price"/>
                </group>
    ...
    ```
    </details>
        
    重复步骤4

14. 关系字段
    > 将当前字段绑定到某个字段, 值随之变化, 可选择存或不存到数据库

    <summary>修改addons/example/models/models.py</summary>
    <details>
    
    ```python
    ...
    # store: 是否把关联字段存到数据库
    my_related1 = fields.Integer(related='em1_mo.fuck_id', string='关联到em1_mo.fuck_id', store=True)
    my_related2 = fields.Date(related='my_date', string='关联到my_date', store=True)
    ...
    ```
    </details>
        
    <summary>修改addons/example/views/views.xml文件</summary>
    <details>

    ```python
    ...
    <record model="ir.ui.view" id="example.list">
        <field name="name">列表显示字段</field>
        <field name="model">example.example</field>
        <field name="arch" type="xml">
        <tree>
            <field name="my_related1"/>
            <field name="my_related2"/>
    ...
                    <field name="name_and_price"/>
                    <field name="my_related1"/>
                    <field name="my_related2"/>
                </group>
    ...
    ```    
    </details>

    重复步骤4

15. 查看模型, 菜单等
    - 点击设置
    - 点击技术
16. 项目地址:https://github.com/dhgdhg/odoo_example
