from django.shortcuts import render

# Create your views here.
from django.views.generic import DetailView
from django.views.generic import ListView

from core.Mixin.StatusWrapMixin import StatusWrapMixin
from core.Mixin.CheckMixin import CheckSiteMixin
from core.dss.Mixin import JsonResponseMixin, MultipleJsonResponseMixin
from api.models import *


class TankListInfoView(CheckSiteMixin, StatusWrapMixin, MultipleJsonResponseMixin, ListView):
    model = FuelTank

    def get_queryset(self):
        queryset = self.model.objects.filter(belong=self.site)
        return queryset
