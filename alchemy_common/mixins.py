import django
import json
import base64
import pickle
from django.conf.urls import url
from alchemy_common.form import CustomerSegmentForm
from django.db import connection
from django.utils.safestring import mark_safe
from alchemy_common.models import Segment
from django.urls import reverse
from django.template.response import TemplateResponse
from django.http import HttpResponseRedirect
from django.utils.html import format_html
from django.utils.translation import gettext_lazy as _
from import_export.admin import (ImportMixin, ExportMixin)


def admin_change_url(obj):
    app_label = obj._meta.app_label
    model_name = obj._meta.model.__name__.lower()
    return reverse('admin:{}_{}_change'.format(app_label, model_name), args=(obj.pk,))


def admin_change_url_link(obj):
    url = admin_change_url(obj)
    return format_html('<a href="{}">{}</a>', url, obj)


class SegmentMixin:
    change_list_template = 'admin/segment/change_list_segment.html'
    field_name = 'customer'

    def get_urls(self):
        urls = super().get_urls()
        my_urls = [
            url(r'^segment/$',
                self.admin_site.admin_view(self.segment_action),
                name='%s_%s_segment' % self.get_model_info()),
        ]
        return my_urls + urls

    def get_model_info(self):
        app_label = self.model._meta.app_label
        return (app_label, self.model._meta.model_name)

    def get_segment_queryset(self, request):
        list_display = self.get_list_display(request)
        list_display_links = self.get_list_display_links(request, list_display)
        list_filter = self.get_list_filter(request)
        search_fields = self.get_search_fields(request)
        if self.get_actions(request):
            list_display = ['action_checkbox'] + list(list_display)

        ChangeList = self.get_changelist(request)
        changelist_kwargs = {
            'request': request,
            'model': self.model,
            'list_display': list_display,
            'list_display_links': list_display_links,
            'list_filter': list_filter,
            'date_hierarchy': self.date_hierarchy,
            'search_fields': search_fields,
            'list_select_related': self.list_select_related,
            'list_per_page': self.list_per_page,
            'list_max_show_all': self.list_max_show_all,
            'list_editable': self.list_editable,
            'model_admin': self,
        }

        if django.VERSION >= (2, 1):
            changelist_kwargs['sortable_by'] = self.sortable_by

        cl = ChangeList(**changelist_kwargs)

        return cl.get_queryset(request)

    def create_segment(self, request, queryset, name, desc):
        sql, sql_params = queryset.query.get_compiler(using=queryset.db).as_sql()
        cursor = connection.cursor()
        cursor.execute('EXPLAIN ' + sql, sql_params)
        # 1
        sql_query = cursor.db.ops.last_executed_query(cursor, sql, sql_params)[8:]
        # 2
        app_label = self.model._meta.app_label
        # 3
        model_name = self.model.__name__
        # 4
        qs = base64.b64encode(pickle.dumps(queryset.query)).decode("utf-8", "ignore")
        # 5
        filter_params = json.dumps(request.GET)

        segment = Segment.objects.create(
            name=name,
            description=desc,
            queryset=qs,
            sql_query=sql_query,
            url=request.build_absolute_uri().replace('/segment', ''),
            filter_params=filter_params,
            field_name=self.field_name,
            model_name=model_name,
            app_label=app_label
        )

        return segment

    def segment_action(self, request, *args, **kwargs):
        form = CustomerSegmentForm(request.POST or None)
        if form.is_valid():
            queryset = self.get_segment_queryset(request)
            segment = self.create_segment(request, queryset, form.cleaned_data['name'], form.cleaned_data['description'])

            self.message_user(request, mark_safe("Created Segment {} targetting {} Customers".format(
                admin_change_url_link(segment),
                segment.num_customers
            )))

            post_url_continue = '/admin/{}/{}/{}'.format(
                self.model._meta.app_label,
                self.model._meta.model_name,
                request.get_full_path().replace(request.path, '')
            )

            return HttpResponseRedirect(post_url_continue)

        context = {'filter_params': request.GET}
        context.update(self.admin_site.each_context(request))

        context['title'] = _("Create a customer segment")
        context['form'] = form
        context['opts'] = self.model._meta
        request.current_app = self.admin_site.name

        return TemplateResponse(request, ['admin/segment/segment.html'], context)


class SegmentImportExportMixin(SegmentMixin, ImportMixin, ExportMixin):
    change_list_template = 'admin/segment/change_list_segment_import_export.html'
