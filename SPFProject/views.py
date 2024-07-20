from django.shortcuts import render
from formulation.models import formulations


def home(request):
    all_formulations = formulations.objects.all()
    return render(request, 'formulation_list.html', {'formulations': all_formulations})
