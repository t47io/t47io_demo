from datetime import datetime
import glob
import os
import pickle
import simplejson
import smtplib
import subprocess
import traceback

from django.http import HttpResponse
from django.shortcuts import render

from src.env import error400
from src.settings import *
from src.models import BackupForm, ExportForm, BotSettingForm, Publication

suffixes = ['B', 'KB', 'MB', 'GB', 'TB', 'PB']


def send_notify_slack(msg_channel, msg_content, msg_attachment):
    pass

def send_notify_emails(msg_subject, msg_content):
    # send_mail(msg_subject, msg_content, EMAIL_HOST_USER, [EMAIL_NOTIFY])
    smtpserver = smtplib.SMTP(EMAIL_HOST, EMAIL_PORT)
    smtpserver.starttls()
    smtpserver.login(EMAIL_HOST_USER, EMAIL_HOST_PASSWORD)
    msg = 'Subject: %s\n\n%s' % (msg_subject, msg_content)
    smtpserver.sendmail(EMAIL_HOST_USER, EMAIL_NOTIFY, msg)
    smtpserver.quit()

def send_error_slack(err, task='', fn='', log_file=''):
    pass

def find_slack_id(name):
    pass


def get_date_time(keyword):
    t_cron = [c[0] for c in CRONJOBS if ''.join(c[2]).find(keyword) != -1][0]
    d_cron = ['Sun', 'Mon', 'Tues', 'Wednes', 'Thurs', 'Fri', 'Satur'][int(t_cron.split(' ')[-1])]
    t_cron = datetime.strptime(' '.join(t_cron.split(' ')[0:2]),'%M %H').strftime('%I:%M%p')
    t_now = datetime.now().strftime('%b %d %Y (%a) @ %H:%M:%S')
    return (t_cron, d_cron, t_now)

def humansize(nbytes):
    if nbytes == 0: return '0 B'
    i = 0
    while nbytes >= 1024 and i < len(suffixes)-1:
        nbytes /= 1024.
        i += 1
    f = ('%.1f' % nbytes).rstrip('0').rstrip('.')
    return '%s %s' % (f, suffixes[i])

def get_folder_size(path):
    total = 0
    for f in glob.glob(path):
        if os.path.isfile(f):
            total += os.path.getsize(f)
        else:
            total += get_folder_size(f + '/*')
    return total

def get_folder_num(path):
    total = 0
    for f in glob.glob(path):
        if os.path.isfile(f):
            total += 1
        else:
            total += get_folder_num(f + '/*')
    return total

def get_backup_stat():
    pass


def refresh_settings():
    pass

def get_sys_crontab():
    pass

def set_sys_crontab():
    pass

def get_backup_form():
    env_cron = simplejson.load(open('%s/config/cron.conf' % MEDIA_ROOT))
    for cron_job in env_cron['CRONJOBS']:
        cron = cron_job[0].split(' ')
        if 'backup_weekly' in cron_job[-1]:
            set_backup = ('%s:%s' % (cron[1], cron[0]), cron[-1])
        elif 'gdrive_weekly' in cron_job[-1]:
            set_upload = ('%s:%s' % (cron[1], cron[0]), cron[-1])
    return {'day_backup': set_backup[1], 'day_upload': set_upload[1], 'time_backup': set_backup[0], 'time_upload': set_upload[0], 'keep': env_cron['KEEP_BACKUP']}


def set_backup_form(request):
    form = BackupForm(request.POST)
    if not form.is_valid(): return 1

    cron_backup = '%s * * %s' % (form.cleaned_data['time_backup'].strftime('%M %H'), form.cleaned_data['day_backup'])
    cron_upload = '%s * * %s' % (form.cleaned_data['time_upload'].strftime('%M %H'), form.cleaned_data['day_upload'])

    env_cron = simplejson.load(open('%s/config/cron.conf' % MEDIA_ROOT))
    for cron_job in env_cron['CRONJOBS']:
        if 'backup_weekly' in cron_job[-1]:
            cron_job[0] = cron_backup
        elif 'gdrive_weekly' in cron_job[-1]:
            cron_job[0] = cron_upload
        suffix = cron_job[-1]
        cron_job[-1] = '>> %s/cache/log_cron.log 2>&1 # %s' % (MEDIA_ROOT, suffix[suffix.rfind(' # ') + 3:])
    env_cron['KEEP_BACKUP'] = form.cleaned_data['keep']
    simplejson.dump(env_cron, open('%s/config/cron.conf' % MEDIA_ROOT, 'w'), sort_keys=True, indent=' ' * 4)
    return 0


def get_bot_form():
    tp = simplejson.load(open('%s/cache/schedule.json' % MEDIA_ROOT, 'r'))['weekday']

    return {'is_slack': BOT['SLACK']['IS_SLACK'], 'is_cache': BOT['CACHE']['IS_CACHE'], 'is_duty_bday': BOT['SLACK']['MSG_BDAY'], 'is_duty_breakfast': BOT['SLACK']['DUTY']['MONTH']['MSG_BDAY'], 'is_duty_aws': BOT['SLACK']['DUTY']['MONTH']['MSG_AWS'], 'is_duty_breakfast': BOT['SLACK']['DUTY']['MONTH']['MSG_BREAKFAST'], 'is_duty_schedule': BOT['SLACK']['DUTY']['MONTH']['MSG_SCHEDULE'], 'is_duty_website': BOT['SLACK']['DUTY']['MONTH']['MSG_WEBSITE'], 'is_duty_trip': BOT['SLACK']['DUTY']['QUARTER']['MSG_TRIP'], 'is_duty_git': BOT['SLACK']['DUTY']['QUARTER']['MSG_GIT'], 'is_admin_backup': BOT['SLACK']['ADMIN']['MSG_BACKUP'], 'is_admin_gdrive': BOT['SLACK']['ADMIN']['MSG_GDRIVE'], 'is_admin_version': BOT['SLACK']['ADMIN']['MSG_VERSION'], 'is_admin_report': BOT['SLACK']['ADMIN']['MSG_REPORT'], 'is_admin_aws_warn': BOT['SLACK']['ADMIN']['MSG_AWS_WARN'], 'is_version': BOT['SLACK']['IS_VERSION'], 'is_report': BOT['SLACK']['IS_REPORT'], 'is_bday': BOT['SLACK']['MSG_BDAY'], 'is_flash_slide': BOT['SLACK']['IS_FLASH_SETUP'], 'is_user_jc_1': BOT['SLACK']['REMINDER']['JC']['REMINDER_1'], 'is_user_jc_2': BOT['SLACK']['REMINDER']['JC']['REMINDER_2'], 'is_admin_jc': BOT['SLACK']['REMINDER']['JC']['REMINDER_ADMIN'], 'is_user_es_1': BOT['SLACK']['REMINDER']['ES']['REMINDER_1'], 'is_user_es_2': BOT['SLACK']['REMINDER']['ES']['REMINDER_2'], 'is_admin_es': BOT['SLACK']['REMINDER']['ES']['REMINDER_ADMIN'], 'is_user_rot_1': BOT['SLACK']['REMINDER']['ROT']['REMINDER_1'], 'is_user_rot_2': BOT['SLACK']['REMINDER']['ROT']['REMINDER_2'], 'is_admin_rot': BOT['SLACK']['REMINDER']['ROT']['REMINDER_ADMIN'], 'is_duty_mic': BOT['SLACK']['DUTY']['ETERNA']['MSG_MIC'], 'is_duty_broadcast': BOT['SLACK']['DUTY']['ETERNA']['MSG_BROADCAST'], 'is_duty_webnews': BOT['SLACK']['DUTY']['ETERNA']['MSG_NEWS'], 'day_duty_month': BOT['SLACK']['DUTY']['MONTH']['WEEK_DAY'], 'day_duty_quarter': BOT['SLACK']['DUTY']['QUARTER']['WEEK_DAY'], 'day_meeting': tp, 'day_reminder_1': BOT['SLACK']['REMINDER']['DAY_BEFORE_REMINDER_1'], 'day_reminder_2': BOT['SLACK']['REMINDER']['DAY_BEFORE_REMINDER_2'], 'cache_3': BOT['CACHE']['INTERVAL_3'], 'cache_15': BOT['CACHE']['INTERVAL_15'], 'cache_30': BOT['CACHE']['INTERVAL_30']}


def set_bot_form(request):
    form = BotSettingForm(request.POST)
    if not form.is_valid(): return 1

    BOT = {"SLACK":  {"IS_SLACK": form.cleaned_data['is_slack'], "IS_FLASH_SETUP": form.cleaned_data['is_flash_slide'], "IS_VERSION": form.cleaned_data['is_version'], "IS_REPORT": form.cleaned_data['is_report'], "MSG_BDAY": form.cleaned_data['is_bday'], "DUTY":  {"MONTH":  {"MSG_BDAY": form.cleaned_data['is_duty_bday'], "MSG_BREAKFAST": form.cleaned_data['is_duty_breakfast'], "MSG_AWS": form.cleaned_data['is_duty_aws'], "MSG_SCHEDULE": form.cleaned_data['is_duty_schedule'], "MSG_WEBSITE": form.cleaned_data['is_duty_website'], "WEEK_DAY": form.cleaned_data['day_duty_month']}, "QUARTER":  {"MSG_TRIP": form.cleaned_data['is_duty_trip'], "MSG_GIT": form.cleaned_data['is_duty_git'], "WEEK_DAY": form.cleaned_data['day_duty_quarter']}, "ETERNA":  {"MSG_MIC": form.cleaned_data['is_duty_mic'], "MSG_BROADCAST": form.cleaned_data['is_duty_broadcast'], "MSG_NEWS": form.cleaned_data['is_duty_webnews']} }, "REMINDER":  {"DAY_BEFORE_REMINDER_1":  form.cleaned_data['day_reminder_1'], "DAY_BEFORE_REMINDER_2":  form.cleaned_data['day_reminder_2'], "JC":  {"REMINDER_1": form.cleaned_data['is_user_jc_1'], "REMINDER_2": form.cleaned_data['is_user_jc_2'], "REMINDER_ADMIN": form.cleaned_data['is_admin_jc']}, "ES":  {"REMINDER_1": form.cleaned_data['is_user_es_1'], "REMINDER_2": form.cleaned_data['is_user_es_2'], "REMINDER_ADMIN": form.cleaned_data['is_admin_es']}, "ROT":  {"REMINDER_1": form.cleaned_data['is_user_rot_1'], "REMINDER_2": form.cleaned_data['is_user_rot_2'], "REMINDER_ADMIN": form.cleaned_data['is_admin_rot']} }, "ADMIN":  {"MSG_BACKUP": form.cleaned_data['is_admin_backup'], "MSG_GDRIVE": form.cleaned_data['is_admin_gdrive'], "MSG_VERSION": form.cleaned_data['is_admin_version'], "MSG_REPORT": form.cleaned_data['is_admin_report'], "MSG_AWS_WARN": form.cleaned_data['is_admin_aws_warn']} }, "CACHE":  { "IS_CACHE": form.cleaned_data['is_cache'], "INTERVAL_3": form.cleaned_data['cache_3'], "INTERVAL_15": form.cleaned_data['cache_15'], "INTERVAL_30": form.cleaned_data['cache_30']} }

    env_cron = simplejson.load(open('%s/config/cron.conf' % MEDIA_ROOT))
    for cron_job in env_cron['CRONJOBS']:
        if 'cache_03' in cron_job[-1]:
            cron_job[0] = '*/%s * * * *' % form.cleaned_data['cache_3']
        elif 'cache_15' in cron_job[-1]:
            cron_job[0] = '*/%s * * * *' % form.cleaned_data['cache_15']
        elif 'cache_30' in cron_job[-1]:
            cron_job[0] = '*/%s * * * *' % form.cleaned_data['cache_30']
        elif 'duty_monthly' in cron_job[-1]:
            cron_job[0] = '20 15 * * %s' % form.cleaned_data['day_duty_month']
        elif 'duty_quarterly' in cron_job[-1]:
            cron_job[0] = '25 15 * 1,4,7,10 %s' % form.cleaned_data['day_duty_quarter']
        suffix = cron_job[-1]
        cron_job[-1] = '>> %s/cache/log_cron.log 2>&1 # %s' % (MEDIA_ROOT, suffix[suffix.rfind(' # ') + 3:])

    simplejson.dump(env_cron, open('%s/config/cron.conf' % MEDIA_ROOT, 'w'), sort_keys=True, indent=' ' * 4)
    simplejson.dump(BOT, open('%s/config/bot.conf' % MEDIA_ROOT, 'w'), sort_keys=True, indent=' ' * 4)
    return 0


def restyle_apache():
    pass


def aws_result(results, args, req_id=None):
    pass

def aws_call(conn, args, qs, req_id=None):
    pass


def aws_stats(request):
    if 'qs' in request.GET and 'sp' in request.GET and 'tqx' in request.GET:
        qs = request.GET.get('qs')
        sp = request.GET.get('sp')
        req_id = request.GET.get('tqx').replace('reqId:', '')
        if qs == 'init':
            return simplejson.dumps(simplejson.load(open('%s/cache/aws/admin/init.json' % MEDIA_ROOT, 'r')), indent=' ' * 4, sort_keys=True)
        elif qs in ['23xx', '45xx', 'host', 'status', 'network', 'credit', 'volbytes']:
            results = pickle.load(open('%s/cache/aws/admin/%s.pickle' % (MEDIA_ROOT, qs), 'rb'))
            return results.replace('__REQ_ID__', req_id)
        elif qs in ['request', 'cpu', 'latency']:
            results = pickle.load(open('%s/cache/aws/admin/%s_%s.pickle' % (MEDIA_ROOT, qs, sp), 'rb'))
            return results.replace('__REQ_ID__', req_id)
    return error400(request)

def ga_stats(request):
    if 'qs' in request.GET and 'tqx' in request.GET:
        qs = request.GET.get('qs')
        req_id = request.GET.get('tqx').replace('reqId:', '')
        if qs == 'init':
            return simplejson.dumps(simplejson.load(open('%s/cache/ga/admin/init.json' % MEDIA_ROOT, 'r')), indent=' ' * 4, sort_keys=True)
        elif qs == 'geo':
            results = pickle.load(open('%s/cache/ga/admin/%s.pickle' % (MEDIA_ROOT, qs), 'rb'))
            return results.replace('__REQ_ID__', req_id)
        elif 'sp' in request.GET:
            sp = request.GET.get('sp')

            if (qs == 'chart' and sp in ('24h', '7d', '1m', '3m')) or (qs == 'pie' and sp in ('session', 'user', 'browser', 'pageview')):
                results = pickle.load(open('%s/cache/ga/admin/%s_%s.pickle' % (MEDIA_ROOT, qs, sp), 'rb'))
                return results.replace('__REQ_ID__', req_id)
            else:
                return error400(request)
        else:
            return error400(request)
    else:
        return error400(request)

def git_stats(request):
    if 'qs' in request.GET and 'tqx' in request.GET:
        qs = request.GET.get('qs')
        req_id = request.GET.get('tqx').replace('reqId:', '')
        if qs in ['init', 'num']:
            return simplejson.dumps(simplejson.load(open('%s/cache/git/admin/%s.json' % (MEDIA_ROOT, qs), 'r')), indent=' ' * 4, sort_keys=True)
        elif qs in ['c', 'ad', 'au']:
            results = pickle.load(open('%s/cache/git/admin/%s.pickle' % (MEDIA_ROOT, qs), 'rb'))
            return results.replace('__REQ_ID__', req_id)
        else:
            return error400(request)
    else:
        return error400(request)


def export_citation(request):
    form = ExportForm(request.POST)
    if not form.is_valid(): return render(request, PATH.HTML_PATH['admin_export'], {'form': ExportForm()})

    is_order_number = form.cleaned_data['order_number']
    is_quote_title = form.cleaned_data['quote_title']
    is_double_space = form.cleaned_data['double_space']
    is_include_preprint = form.cleaned_data['include_preprint']
    is_include_hidden = form.cleaned_data['include_hidden']

    text_type = form.cleaned_data['text_type']
    year_start = form.cleaned_data['year_start']
    number_order = form.cleaned_data['number_order'] == '1'
    sort_order = 'display_date'
    if form.cleaned_data['sort_order'] == '1': sort_order = '-' + sort_order

    publications = Publication.objects.filter(year__gte=year_start).order_by(sort_order)
    if not is_include_preprint: publications = publications.filter(is_preprint=False)
    if not is_include_hidden: publications = publications.filter(is_visible=True)

    if text_type == '0':
        txt = ''
        for i, pub in enumerate(publications):
            order = ''
            if is_order_number:
                if number_order:
                    order = '%d. ' % (len(publications) - i)
                else:
                    order = '%d. ' % (i + 1)

            title = pub.title
            if is_quote_title: title = '"%s"' % title
            number = pub.volume
            if pub.issue: number += '(%s)' % pub.issue
            page = ''
            if pub.begin_page: page += ': %s' % pub.begin_page
            if pub.end_page: page += '-%s' % pub.end_page
            double_space = ''
            if is_double_space: double_space = '\n'
            txt += '%s%s (%s) %s %s %s%s\n%s' % (order, pub.authors, pub.year, title, pub.journal, number, page, double_space)

        response = HttpResponse(txt, content_type='text/plain')
    else:
        is_bold_author = form.cleaned_data['bold_author']
        is_bold_year = form.cleaned_data['bold_year']
        is_underline_title = form.cleaned_data['underline_title']
        is_italic_journal = form.cleaned_data['italic_journal']
        is_bold_volume = form.cleaned_data['bold_volume']

        html = '<html><body>'
        for i, pub in enumerate(publications):
            order = ''
            if is_order_number:
                if number_order:
                    order = '%d. ' % (len(publications) - i)
                else:
                    order = '%d. ' % (i + 1)

            authors = pub.authors
            if is_bold_author: authors = authors.replace('Das, R.', '<b>Das, R.</b>').replace('Das R.', '<b>Das, R.</b>')
            year = pub.year
            if is_bold_year: year = '<b>%s</b>' % year
            title = pub.title
            if is_underline_title: title = '<u>%s</u>' % title
            if is_quote_title: title = '&quot;%s&quot;' % title
            journal = pub.journal
            if is_italic_journal: journal = '<i>%s</i>' % journal
            number = pub.volume
            if is_bold_volume: number = '<b>%s</b>' % number
            if pub.issue: number += '(%s)' % pub.issue
            page = ''
            if pub.begin_page: page += ': %s' % pub.begin_page
            if pub.end_page: page += '-%s' % pub.end_page
            double_space = ''
            if is_double_space: double_space = '<br/>'
            html += '<p>%s%s (%s) %s %s %s%s</p>%s' % (order, authors, year, title, journal, number, page, double_space)

        html += '</body></html>'
        response = HttpResponse(html, content_type='text/html')


    if request.POST['action'] == 'save':
        if text_type == '0':
            response["Content-Disposition"] = "attachment; filename=export_citation.txt"
        else:
            open(os.path.join(MEDIA_ROOT, 'data/export_citation.html'), 'w').write(html.encode('UTF-8'))

            try:
                subprocess.check_call('cd %s/data && pandoc -f html -t docx -o export_citation.docx export_citation.html' % MEDIA_ROOT, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
            except subprocess.CalledProcessError:
                send_error_slack(traceback.format_exc(), 'Export Citations', 'export_citation', 'log_django.log')

            lines = open(os.path.join(MEDIA_ROOT, 'data/export_citation.docx'), 'r').readlines()
            response = HttpResponse(lines, content_type='application/msword')
            response["Content-Disposition"] = "attachment; filename=export_citation.docx"
    return response


