from odoo import fields, models


class SaleOrder(models.Model):
    _inherit = 'sale.order'

    is_project = fields.Boolean(default=False, string="Is Project")

    def action_create_project(self):
        milestone_project = self.env['project.project'].create({
            'name': self.name,
            'milestone_id': self.id
        })
        milestone_list = []

        for line in self.order_line:
            str_milestone = "milestone-"+str(line.milestone)
            milestone_list.append(line.milestone)

            if (milestone_list.count(line.milestone)) > 1:
                self.env['project.task'].create({
                    'name': line.product_template_id.name,
                    'parent_id': datas.id
                })
            else:
                datas = self.env['project.task'].create({
                    'name': str_milestone,
                    'project_id': milestone_project.id,
                })
                child = self.env['project.task'].create({
                    'name': line.product_template_id.name,
                    'parent_id': datas.id
                })
        self.is_project = True

    def action_update_project(self):
        project = self.env['project.project'].search([('milestone_id', '=', self.id)])
        tasks = self.env['project.task'].search([('project_id', '=', project.id)])

        for task in tasks:
            task.unlink()

        milestone_list = []

        for line in self.order_line:
            str_milestone = "milestone-" + str(line.milestone)
            milestone_list.append(line.milestone)

            if (milestone_list.count(line.milestone)) > 1:
                self.env['project.task'].create({
                    'name': line.product_template_id.name,
                    'parent_id': datas.id
                })
            else:
                datas = self.env['project.task'].create({
                    'name': str_milestone,
                    'project_id': project.id,
                })
                child = self.env['project.task'].create({
                    'name': line.product_template_id.name,
                    'parent_id': datas.id
                })
        self.is_project = True





    # def action_update_project(self):
    #     project = self.env['project.project'].search([('milestone_id', '=', self.id)])
    #     tasks = self.env['project.task'].search([('project_id', '=', project.id)])
    #
    #     task_products = []
    #     for task in tasks:
    #         task_products.append(task.name)
    #     print("task_products>>>>>>>>>", task_products)
    #
    #     for line in self.order_line:
    #         if line.product_template_id.name not in task_products:
    #             print("line.milestone>>>>>>>>>>>>", line.milestone)
    #
    #             string_milestone = 'milestone-' + str(line.milestone)
    #             print("string_milestone>>>>>>>>>>>", string_milestone)
    #
    #             if string_milestone in task_products:
    #                 print('update')
    #
    #                 update_task = self.env['project.task'].search([('project_id', '=', project.id),
    #                                                                ('name', '=', string_milestone)])
    #                 print("update_task>>>>>>>>", update_task)
    #                 print("update_task.id>>>>>>>>", update_task.id)
    #
    #                 child = update_task.update({
    #                     'name': line.product_template_id.name,
    #                     'parent_id': update_task.id
    #                 })
    #
    #             else:
    #                 print("create ")
    #
    #                 create_task = self.env['project.task'].search([('project_id', '=', project.id)])
    #
    #                 datas = create_task.create({
    #                     'name': string_milestone,
    #                     'project_id': project.id,
    #                 })
    #                 child = create_task.create({
    #                     'name': line.product_template_id.name,
    #                     'parent_id': datas.id
    #                 })
    #
    #         else:
    #             print("nahi..")
