from django.contrib import admin
from alchemy_common.models import Customer, Segment
from alchemy_common.mixins import SegmentImportExportMixin
from alchemy_common.filters import GenderFilter, AgeFilter
from rangefilter.filter import DateRangeFilter, DateTimeRangeFilter
from import_export import resources
from import_export.admin import ImportExportActionModelAdmin
from admin_numeric_filter.admin import (
    NumericFilterModelAdmin,
    SingleNumericFilter,
    RangeNumericFilter,
    SliderNumericFilter
)


class CustomerResource(resources.ModelResource):

    class Meta:
        model = Customer
        import_id_fields = ('clearbridge_appuser_id')
        skip_unchanged = True
        report_skipped = False


class CustomerAdminMixin(SegmentImportExportMixin):
    field_name = '_uid'


@admin.register(Customer)
class CustomerAdmin(NumericFilterModelAdmin, ImportExportActionModelAdmin, CustomerAdminMixin):
    resource_class = CustomerResource
    list_filter = (
        GenderFilter,
        AgeFilter,
        ('created_at', DateRangeFilter),
        ('updated_at', DateTimeRangeFilter),
        ('user_selected_level', SliderNumericFilter),
        ('age', SliderNumericFilter),
    )


admin.site.register(Segment)
