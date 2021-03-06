from scanner.master.base import BaseHandleTask
from app.models.asset import Host
from celery_worker import celery
from app.models import db


class HostHandleTask(BaseHandleTask):

    name = 'master_host_handle'

    def get_target_list(self, target_option):
        db.session.close()
        target_list = [{'uid': host.uid, 'target': host.ip}
                       for host in Host.list_items_paginate_by_search(**target_option).items]
        return target_list

    def get_plugin_list(self, plugin_option):
        plugin_list = []
        for plugin, option in plugin_option.items():
            plugin_list.append({'name': plugin, 'option': option})
        return plugin_list

    def get_success_callback(self):
        return callback_success

    def get_error_callback(self):
        return callback_error


@celery.task
def callback_success(results):
    for result in results:
        print(result)


@celery.task
def callback_error(request, exc, traceback):
    print(request, exc, traceback)
