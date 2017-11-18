from __future__ import unicode_literals
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.core.urlresolvers import reverse
from .models import *
from .forms import *

@login_required()
def calendar(request):
    context = {}
    band = request.session['band']
    context['bandid'] = band
    return render(request, 'user_calendar.html', context)