from django_admin_multiple_choice_list_filter.list_filters import MultipleChoiceListFilter
from alchemy_common.models import Customer


class GenderFilter(MultipleChoiceListFilter):
    title = 'gender'
    parameter_name = 'gender__in'

    def lookups(self, request, model_admin):
        qs = Customer.objects.values_list('gender').distinct()

        return [(i[0], i[0]) for i in qs if i[0] is not None and i[0] != '']


class AgeFilter(MultipleChoiceListFilter):

    title = "age"
    parameter_name = "age__in"

    def lookups(self, request, model_admin):
        qs = Customer.objects.values_list('age').distinct()

        return [(i[0], i[0]) for i in qs if i[0] is not None and i[0] != '']
