from odoo.addons.web.controllers.dataset import DataSet
from odoo.http import request
from odoo import http


class ResequenceEnhanced(DataSet):
    """
    In kanban views, "default_order" attr's field name is expected to be 'sequence'; if not, you can't sort columns in kanban view.
    There are 2 solutions:
    1) You can define a field like
        default_order_field_name = fields.Integer(related='sequence')
    2) Or enable the code below to break 'sequence' name forcing.
    """
    @http.route('/web/dataset/resequence', type='json', auth="user")
    def resequence(self, model, ids, field='sequence', offset=0):
        if 'skts' in model:
            m = request.env[model]
            if not m.fields_get([field]):
                return super(ResequenceEnhanced, self).resequence(model, ids, 'sequence', offset)
        return super(ResequenceEnhanced, self).resequence(model, ids, field, offset)
