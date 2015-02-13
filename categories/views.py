import json
from django.core import serializers
from django.db.models.query import QuerySet
from django.http.response import HttpResponse
from django.shortcuts import render

# Create your views here.
from django.views.generic.base import TemplateView
from categories.models import Topic


def query_to_json(queryset):
    if type(queryset) is QuerySet:
        serialized = serializers.serialize('json', queryset, indent=4)
    else:
        serialized = serializers.serialize('json', [queryset, ], indent=4)
    tmp = json.loads(serialized)
    json_object = []

    for item in tmp:
        fields = item["fields"]
        fields["id"] = item["pk"]

        json_object.append(fields)

    result = json.dumps(json_object, indent=4)
    return result


class CategoryView(TemplateView):

    def get(self, request, *args, **kwargs):
        data = Topic.objects.all()
        result = query_to_json(data)
        return HttpResponse(result)
