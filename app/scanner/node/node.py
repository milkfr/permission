from celery_worker import celery, es
import scanner.plugin
import traceback
import sys
import time
from datetime import datetime


@celery.task
def handle(target, plugin, name):
    target_uid = target.get('uid')
    target_content = target.get('target')
    plugin_name = plugin.get('name')
    plugin_option = plugin.get('option')
    try:
        result = getattr(scanner.plugin, plugin_name)(target_content, plugin_option)
    except Exception as e:
        exc, tb = sys.exc_info()[1:]
        result = str(exc.__class__, exc, ''.join(traceback.format_tb(tb)))
        traceback.clear_frames(tb)
        del tb
    es.index(
        index='node-{}-{}'.format(name, time.strftime('%Y-%m-%d', time.localtime())),
        doc_type='doc',
        body={
            'target': target,
            'plugin': plugin,
            'result': result,
            'timestamp': datetime.utcnow()
    })
    return {'uid': target_uid, 'result': result}
