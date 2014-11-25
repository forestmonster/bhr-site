from django.views.generic import View, FormView, TemplateView, DetailView
from django.core.urlresolvers import reverse
from django.shortcuts import render, redirect
from django.http import HttpResponse

from bhr.models import WhitelistEntry, Block, BlockEntry, BHRDB
from bhr.forms import AddBlockForm, QueryBlockForm, UnblockForm

from django.db import transaction
from django.db.models import Q
from django.utils import timezone
import datetime

from django.db import transaction



class IndexView(TemplateView):
    template_name = "bhr/index.html"

class AddView(FormView):
    template_name = "bhr/add.html"
    form_class = AddBlockForm

    def form_valid(self, form):
        block_request = form.cleaned_data
        block_request['cidr'] = str(block_request['cidr'])
        BHRDB().add_block(who=self.request.user, source='web', **block_request)
        return redirect(reverse("query") + "?cidr=" +  block_request["cidr"])

class QueryView(View):
    def get(self, request):
        if self.request.GET:
            form = QueryBlockForm(self.request.GET)
        else:
            form = QueryBlockForm()

        if not form.is_valid():
            return render(self.request, "bhr/query.html", {"form": form})

        query = form.cleaned_data['cidr']
        blocks = BHRDB().get_history(query).prefetch_related("blockentry_set")
        return render(self.request, "bhr/query_result.html", {"query": query, "form": form, "blocks": blocks})

class UnblockView(View):
    def post(self, request):
        query = self.request.POST.get("query")
        block_ids = self.request.POST.getlist("block_id")
        blocks = Block.objects.filter(id__in=block_ids).all()
        block_str = " ".join(block_ids)
        form = UnblockForm(initial={"block_ids": block_str, "query": query})
        return render(self.request, "bhr/unblock.html", {"form": form, "blocks": blocks})

class DoUnblockView(FormView):
    template_name = "bhr/unblock.html"
    form_class = UnblockForm

    def form_valid(self, form):
        query = form.cleaned_data['query']
        block_ids = form.cleaned_data['block_ids'].split()
        why = form.cleaned_data['why']

        block_ids = map(int, block_ids)
        blocks = Block.objects.filter(id__in=block_ids).all()
        for b in blocks:
            b.unblock_now(self.request.user, why)
        return redirect(reverse("query") + "?cidr=" + query)

class StatsView(TemplateView):
    template_name = "bhr/stats.html"
    def get_context_data(self, *args):
        db = BHRDB()
        return {
            'stats': db.stats(),
            'source_stats': db.source_stats(),
        }
