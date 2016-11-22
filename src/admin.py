from django.contrib import admin
from django.utils.html import format_html
from django.shortcuts import render
from django.http import HttpResponse
# from django.contrib.admin import AdminSite
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User

from src.console import *
from src.dash import *
from src.env import error403
from src.models import *
from src.settings import *


UserAdmin.list_display = ('username', 'email', 'last_login', 'is_active', 'is_staff', 'is_superuser')
UserAdmin.ordering = ('-is_superuser', '-is_staff', 'username')
# admin.site.unregister(User)
admin.site.register(User, UserAdmin)


class NewsAdmin(admin.ModelAdmin):
    list_display = ('date', 'content', 'link',)
    ordering = ('-date',)
    # form = NewsForm
    readonly_fields = ('image_tag',)

    fieldsets = [
        (format_html('<span class="glyphicon glyphicon-comment"></span>&nbsp;Contents'), {'fields': ['date', 'content', ('image', 'image_tag')]}),
        (format_html('<span class="glyphicon glyphicon-share"></span>&nbsp;Links'), {'fields': ['link', 'video']}),
    ]
admin.site.register(News, NewsAdmin)

class MemberAdmin(admin.ModelAdmin):
    list_display = ('full_name', 'sunet_id', 'year', 'joint_lab', 'affiliation',)
    ordering = ('is_alumni', 'last_name', 'role',)
    readonly_fields = ('image_tag',)

    fieldsets = [
        (format_html('<span class="glyphicon glyphicon-user"></span>&nbsp;Personal Information'), {'fields': [('first_name', 'last_name'), 'role', ('image', 'image_tag'), 'description', 'more_info']}),
        (format_html('<span class="glyphicon glyphicon-home"></span>&nbsp;Affiliation'), {'fields': ['department', ('joint_lab', 'joint_link')]}),
        (format_html('<span class="glyphicon glyphicon-earphone"></span>&nbsp;Contact'), {'fields': [('email', 'bday'), ('sunet_id', 'phone')]}),
        (format_html('<span class="glyphicon glyphicon-road"></span>&nbsp;Alumni Information'), {'fields': [('is_alumni', 'is_visible'), ('start_year', 'finish_year')]}),
    ]
admin.site.register(Member, MemberAdmin)

class PublicationAdmin(admin.ModelAdmin):
    list_display = ('year', 'journal', 'authors', 'title', 'link',)
    ordering = ('-display_date',)
    readonly_fields = ('image_tag',)

    fieldsets = [
        (format_html('<span class="glyphicon glyphicon-book"></span>&nbsp;Citation'), {'fields': ['title', ('year', 'display_date'), 'authors', 'journal', ('volume', 'issue'), ('begin_page', 'end_page')]}),
        (format_html('<span class="glyphicon glyphicon-th-large"></span>&nbsp;Media'), {'fields': ['pdf', 'is_preprint', 'is_visible', 'is_feature', ('image', 'image_tag')]}),
        (format_html('<span class="glyphicon glyphicon-share"></span>&nbsp;Links'), {'fields': ['link', 'extra_field', 'extra_link', 'extra_field_2', 'extra_link_2', 'extra_field_3', 'extra_file']}),
    ]
admin.site.register(Publication, PublicationAdmin)


############################################################################################################################################

class FlashSlideAdmin(admin.ModelAdmin):
    list_display = ('date', 'link',)
    ordering = ('-date',)

    fieldsets = [
        (format_html('<span class="glyphicon glyphicon-share"></span>&nbsp;Links'), {'fields': ['date', 'link']}),
    ]
admin.site.register(FlashSlide, FlashSlideAdmin)

class JournalClubAdmin(admin.ModelAdmin):
    list_display = ('date', 'presenter', 'title', 'link',)
    ordering = ('-date',)

    fieldsets = [
        (format_html('<span class="glyphicon glyphicon-share"></span>&nbsp;Links'), {'fields': ['date', 'presenter', 'link', 'title', ('authors', 'year'), 'citation']}),
    ]
admin.site.register(JournalClub, JournalClubAdmin)

class RotationStudentAdmin(admin.ModelAdmin):
    list_display = ('date', 'full_name', 'title',)
    ordering = ('-date',)

    fieldsets = [
        (format_html('<span class="glyphicon glyphicon-user"></span>&nbsp;Personal Information'), {'fields': ['date', 'full_name', 'title']}),
        (format_html('<span class="glyphicon glyphicon-share"></span>&nbsp;Links'), {'fields': ['ppt', 'data']}),
    ]
admin.site.register(RotationStudent, RotationStudentAdmin)

class KhalaYoutubeAdmin(admin.ModelAdmin):
    list_display = ('date', 'presenter', 'title', 'link',)
    ordering = ('-date',)

    fieldsets = [
        (format_html('<span class="glyphicon glyphicon-share"></span>&nbsp;Links'), {'fields': ['date', 'presenter', 'title', 'link']}),
    ]
admin.site.register(KhalaYoutube, KhalaYoutubeAdmin)

class PresentationAdmin(admin.ModelAdmin):
    list_display = ('date', 'presenter', 'title',)
    ordering = ('-date',)

    fieldsets = [
        (format_html('<span class="glyphicon glyphicon-share"></span>&nbsp;Links'), {'fields': ['date', 'presenter', 'title', 'ppt', 'link']}),
    ]
admin.site.register(Presentation, PresentationAdmin)

class DefensePosterAdmin(admin.ModelAdmin):
    list_display = ('date', 'presenter', 'title',)
    ordering = ('-date',)
    readonly_fields = ('image_tag',)

    fieldsets = [
        (format_html('<span class="glyphicon glyphicon-share"></span>&nbsp;Links'), {'fields': ['date', 'presenter', 'title', 'image', 'image_tag']}),
    ]
admin.site.register(DefensePoster, DefensePosterAdmin)

class SlackMessageAdmin(admin.ModelAdmin):
    list_display = ('date', 'receiver', 'message')
    ordering = ('-date',)

    fieldsets = [
        (format_html('<span class="glyphicon glyphicon-comment"></span>&nbsp;Contents'), {'fields': ['date', 'receiver', 'content', 'attachment']}),
    ]
admin.site.register(SlackMessage, SlackMessageAdmin)


############################################################################################################################################


def apache(request):
    return render(request, PATH.HTML_PATH['admin_apache'], {'host_name': env('SSL_HOST')})

def aws(request):
    return render(request, PATH.HTML_PATH['admin_aws'], {'timezone': TIME_ZONE})

def ga(request):
    return render(request, PATH.HTML_PATH['admin_ga'], {'ga_url': GA['LINK_URL']})

def git(request):
    return render(request, PATH.HTML_PATH['admin_git'], {'timezone': TIME_ZONE})


def backup(request):
    flag = -1
    if request.method == 'POST':
        flag = set_backup_form(request)

    form = BackupForm(initial=get_backup_form())
    return render(request, PATH.HTML_PATH['admin_backup'], {'form': form, 'flag': flag, 'email': EMAIL_HOST_USER})

def backup_form(request):
    return HttpResponse(simplejson.dumps(get_backup_form(), sort_keys=True, indent=' ' * 4), content_type='application/json')

def bot(request):
    flag = -1
    if request.method == 'POST':
        flag = set_bot_form(request)

    form = BotSettingForm(initial=get_bot_form())
    return render(request, PATH.HTML_PATH['admin_bot'], {'form': form, 'flag': flag, 'BOT': BOT})

def dir(request):
    return render(request, PATH.HTML_PATH['admin_dir'], {})

def export(request):
    if request.method == 'POST':
        return export_citation(request)
    else:
        return render(request, PATH.HTML_PATH['admin_export'], {'form': ExportForm()})


def get_stat(request, keyword):
    if keyword == "pem":
        return error403(request)
    else:
        json = simplejson.load(open('%s/cache/stat_%s.json' % (MEDIA_ROOT, keyword.strip('/')), 'r'))
    return HttpResponse(simplejson.dumps(json, sort_keys=True, indent=' ' * 4), content_type='application/json')

def get_dash(request, keyword):
    if keyword == 'aws':
        json = aws_stats(request)
    elif keyword == 'ga':
        json = ga_stats(request)
    elif keyword == 'git':
        json = git_stats(request)
    elif keyword == 'group':
        json = simplejson.dumps({'admin': GROUP.ADMIN, 'group': GROUP.GROUP, 'alumni': GROUP.ALUMNI, 'roton': GROUP.ROTON, 'other': GROUP.OTHER}, sort_keys=True, indent=' ' * 4)
    elif keyword == 'dash':
        json = simplejson.dumps({'t_aws': format_dash_ts(), 't_ga': format_dash_ts(), 't_git': format_dash_ts(), 't_slack': format_dash_ts(), 't_dropbox': format_dash_ts(), 't_cal': format_dash_ts(), 't_sch': format_dash_ts(), 't_duty': format_dash_ts()}, sort_keys=True, indent=' ' * 4)

    if isinstance(json, HttpResponse): return json
    return HttpResponse(json, content_type='application/json')


def man(request):
    return render(request, PATH.HTML_PATH['admin_man'], {})

def ref(request):
    return render(request, PATH.HTML_PATH['admin_ref'], {})


admin.site.register_view('backup/', view=backup, visible=False)
admin.site.register_view('backup/form/', view=backup_form, visible=False)

admin.site.register_view('apache/', view=apache, visible=False)
admin.site.register_view('aws/', view=aws, visible=False)
admin.site.register_view('ga/', view=ga, visible=False)
admin.site.register_view('git/', view=git, visible=False)

admin.site.register_view('dir/', view=dir, visible=False)
admin.site.register_view('bot/', view=bot, visible=False)
admin.site.register_view('export/', view=export, visible=False)

admin.site.register_view('man/', view=man, visible=False)
admin.site.register_view('ref/', view=ref, visible=False)

admin.site.register_view(r'dash/(apache|aws|ga|git|group|dash)/?$', view=get_dash, visible=False)
admin.site.register_view(r'stat/(ver|sys|backup|pem)/?$', view=get_stat, visible=False)
