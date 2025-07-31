from odoo import fields, models


class PollQuestion(models.Model):
    _name = 'poll.question'
    _description = 'Poll Question'

    name = fields.Char()
    description = fields.Text()
    answer_ids = fields.One2many(comodel_name='poll.answer', inverse_name='question_id')

class PollAnswer(models.Model):
    _name = 'poll.answer'
    _description = 'Poll Answer'

    name = fields.Char()
    count = fields.Integer()
    question_id = fields.Many2one(comodel_name='poll.question')
