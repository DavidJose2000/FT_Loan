import django_tables2 as tables
from .models import Referral

class ReferralTable(tables.Table):
    class Meta:
        model = Referral
        template_name = "django_tables2/bootstrap4.html"
        fields = ('referred_by', 'user', 'status', 'commissions')
        attrs = {"class": "container-fluid"}