# -*- coding: utf-8 -*-
import datetime
from email.policy import default

from dateutil.relativedelta import relativedelta
from pkg_resources import require

from odoo import models, fields, api
from odoo.addons.test_convert.tests.test_env import record
from odoo.api import ValuesType, Self, readonly
from odoo.exceptions import UserError
from odoo.fields import Datetime


class iku_tags(models.Model):
    _name = "iku_tags"
    _description = "proje tags"

    name = fields.Char(required=True)
    color = fields.Char()


class iku_milestone(models.Model):
    _name = "iku_milestone"
    _description = "proje milestone"

    name = fields.Char(required=True)
    deadline = fields.Date(required=True)
    reached = fields.Boolean()

    project_type = fields.Many2one("iku_proje")


class iku_subtask(models.Model):
    _name = "iku_subtasks"
    _description = "proje subtasks"

    tasks_id = fields.Many2one("iku_tasks")

    sequence = fields.Integer()


    is_favorite = fields.Boolean()
    title = fields.Char(required=True)
    assignees = fields.Many2many("res.users", default= lambda self: self.env.user )

    # @api.depends('tasks_id.company_name_tags')
    # def _compute_assignees(self):
    #     for record in self:
    #         record.assignees = record.tasks_id.company_name_tags

class iku_tasks(models.Model):
    _name = "iku_tasks"
    _description = "proje tasks"

    start_task_hours = fields.Datetime()
    end_task_hours = fields.Datetime()

    parent_task = fields.Many2one('iku_tasks')
    company = fields.Many2one('res.company')
    email = fields.Char(string="Email cc")
    date_assign = fields.Datetime(readonly=True, default=fields.datetime.now(),string="Assigning Date")
    date_last_stage_update = fields.Datetime(readonly=True,string="Last Stage Update")

    is_favorite = fields.Boolean()

    subtasks_ids = fields.One2many("iku_subtasks","tasks_id")

    tasks_milestone = fields.Many2one("iku_milestone")

    project_ids = fields.Many2one("iku_proje")
    company_name_tags = fields.Many2many("res.users")
    customer = fields.Many2one('res.partner')

    deadline_date = fields.Date()
    description = fields.Text(default="Lütfen açıklama giriniz.")

    status = fields.Selection(copy=False,string="Status",default="new",selection=[("new","New"),
                                                    ("in_progress","In Progress"),
                                                    ("done","Done"),
                                                    ("cancelled","Cancelled")])


    name = fields.Char(required= True)

    def write(self, vals):
        if vals.get('status'):
            vals['date_last_stage_update'] = fields.Datetime.now()
        return super().write(vals)

    def task_state_start(self):
        for record in self:
            # start_date = datetime.datetime.now().strftime("%H:%M")
            record.start_task_hours = datetime.datetime.now()
    def task_state_end(self):
        for record in self:
            record.end_task_hours = datetime.datetime.now()
            record.status = 'done'
#     BURAYA START TASK DENİLDİĞİ ZAMAN BAŞLANGIÇ VAKTİNİ ŞİMDİYE AYARLAYIP END TASK DİYENE KADAR SÜRE SAYACAK



class ikuproje(models.Model):
    _name = "iku_proje"
    _description = "okul projem"

    name = fields.Char(string="Proje Adı", required=True, copy=False)
    task_name = fields.Char()

    is_favorite = fields.Boolean()

    tag_ids = fields.Many2many("iku_tags", string="Tags")
    project_tasks = fields.One2many("iku_tasks","project_ids")

    customer = fields.Many2one('res.partner')
    company = fields.Many2one('res.company')
    company_name = fields.Many2one('res.users')

    description = fields.Text(default="Lütfen açıklama giriniz.")
    planned_date = fields.Date(default=fields.datetime.today())
    deadline_date = fields.Date(default= fields.datetime.today() + relativedelta(days=10))









