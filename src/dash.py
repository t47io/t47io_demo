import pickle
import random
import time

from src.console import *
from src.env import error400
from src.settings import *


def cache_aws(request):
    pass

def dash_aws(request):
    if 'qs' in request.GET and 'id' in request.GET and 'tp' in request.GET and 'tqx' in request.GET:
        qs = request.GET.get('qs')
        id = request.GET.get('id')
        tp = request.GET.get('tp')
        req_id = request.GET.get('tqx').replace('reqId:', '')

        if qs == 'init':
            return simplejson.dumps(simplejson.load(open('%s/cache/aws/init.json' % MEDIA_ROOT, 'r')), indent=' ' * 4, sort_keys=True)
        elif qs in ['cpu', 'net', 'lat', 'req', 'disk']:
            results = pickle.load(open('%s/cache/aws/%s_%s_%s.pickle' % (MEDIA_ROOT, tp, id, qs), 'rb'))
            return results.replace('__REQ_ID__', req_id)
        else:
            return error400(request)
    else:
        return error400(request)


def cache_ga(request):
    pass

def dash_ga(request):
    if 'qs' in request.GET and 'id' in request.GET and 'tqx' in request.GET:
        qs = request.GET.get('qs')
        id = request.GET.get('id')
        req_id = request.GET.get('tqx').replace('reqId:', '')

        if qs == 'init':
            return simplejson.dumps(simplejson.load(open('%s/cache/ga/init.json' % MEDIA_ROOT, 'r')), indent=' ' * 4, sort_keys=True)
        elif qs in ['sessions', 'percentNewSessions']:
            results = pickle.load(open('%s/cache/ga/%s_%s.pickle' % (MEDIA_ROOT, id, qs), 'rb'))
            return results.replace('__REQ_ID__', req_id)
        else:
            return error400(request)
    else:
        return error400(request)


def cache_git(request):
    pass

def dash_git(request):
    if 'qs' in request.GET and 'repo' in request.GET and 'org' in request.GET and 'tqx' in request.GET:
        qs = request.GET.get('qs')
        repo = request.GET.get('repo')
        org = request.GET.get('org')
        req_id = request.GET.get('tqx').replace('reqId:', '')

        if qs == 'init':
            return simplejson.dumps(simplejson.load(open('%s/cache/git/init.json' % MEDIA_ROOT, 'r')), indent=' ' * 4, sort_keys=True)
        elif qs in ['c', 'ad']:
            results = pickle.load(open('%s/cache/git/%s_%s.pickle' % (MEDIA_ROOT, repo, qs), 'rb'))
            return results.replace('__REQ_ID__', req_id)
        elif qs == 'num':
            return simplejson.dumps(simplejson.load(open('%s/cache/git/%s_%s.json' % (MEDIA_ROOT, repo, qs), 'r')), indent=' ' * 4, sort_keys=True)
        else:
            return error400(request)
    else:
        return error400(request)


def cache_slack(request):
    pass

def dash_slack(request):
    if 'qs' in request.GET and 'tqx' in request.GET:
        qs = request.GET.get('qs')
        req_id = request.GET.get('tqx').replace('reqId:', '')

        if qs in ['users', 'home', 'channels', 'files']:
            return simplejson.dumps(simplejson.load(open('%s/cache/slack/%s.json' % (MEDIA_ROOT, qs), 'r')), indent=' ' * 4, sort_keys=True)
        elif qs in ['plot_files', 'plot_msgs']:
            results = pickle.load(open('%s/cache/slack/%s.pickle' % (MEDIA_ROOT, qs), 'rb'))
            return results.replace('__REQ_ID__', req_id)
        else:
            return error400(request)
    else:
        return error400(request)


def cache_dropbox(request):
    pass

def dash_dropbox(request):
    if 'qs' in request.GET and 'tqx' in request.GET:
        qs = request.GET.get('qs')
        req_id = request.GET.get('tqx').replace('reqId:', '')

        if qs in ['sizes', 'folders']:
            return simplejson.dumps(simplejson.load(open('%s/cache/dropbox/%s.json' % (MEDIA_ROOT, qs), 'r')), indent=' ' * 4, sort_keys=True)
        elif qs == 'history':
            results = pickle.load(open('%s/cache/dropbox/%s.pickle' % (MEDIA_ROOT, qs), 'rb'))
            return results.replace('__REQ_ID__', req_id)
        else:
            return error400(request)
    else:
        return error400(request)


def dash_ssl():
    pass


def get_spreadsheet(prefix, id, sufix):
    pass

def cache_schedule():
    pass

def dash_schedule(request):
    return simplejson.load(open('%s/cache/schedule.json' % MEDIA_ROOT, 'r'))

def cache_duty():
    pass

def dash_duty(request):
    return simplejson.load(open('%s/cache/duty.json' % MEDIA_ROOT, 'r'))


def get_calendar():
    pass

def cache_cal():
    pass
    
def dash_cal():
    return simplejson.dumps(simplejson.load(open('%s/cache/calendar.json' % MEDIA_ROOT, 'r')))


def format_dash_ts():
    now = datetime.fromtimestamp(time.time()).replace(minute=0, second=int(random.random()*60))
    r = random.random() * 10
    if r > 2:
        return '<span class="label label-primary">' + now.strftime('%Y-%m-%d %H:%M:%S') + '</span>'
    else:
        now = now.replace(day=now.day-1, hour=0, minute=0)
        return '<span class="label label-danger">' + now.strftime('%Y-%m-%d %H:%M:%S') + '</span>'
