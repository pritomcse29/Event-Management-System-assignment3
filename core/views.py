from django.shortcuts import render
from django.shortcuts import render,HttpResponse,redirect
from events.models import *
from events.forms import *
from datetime import date
from django.db.models import Q, Count, Max,Min,Avg
from django.urls import reverse
from django.shortcuts import get_object_or_404
from django.http import HttpResponse

from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from django.conf import settings
from django.contrib import messages
from django.utils import timezone
from events.models import Event,RSVP
from django.contrib.auth.decorators import user_passes_test,login_required,permission_required

from django.contrib.auth import get_user_model
from django.views.generic import DeleteView,ListView,DetailView,TemplateView,View
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.http import HttpResponseForbidden

# Create your views here.
# def home(request):
#     return render(request,'home.html')
def no_permission(request):
    return render(request,'no_permission.html')

    
def home_event_data(request):
    categories = Category.objects.all()  
    event = Event.objects.all()
    print(event)

    type = request.GET.get('type', 'all')
    today = date.today()
    all_events = Event.objects.all()  
    # today_events = Event.objects.filter(date=today)
    # past_events = Event.objects.filter(date__lt=today).order_by('-date')
    # upcoming_events = Event.objects.filter(date__gt=today).order_by('date')

    pubs = User.objects.aggregate(unique_count=Count('id', distinct=True))['unique_count']
    print("pubs",pubs)
  
    counts = Event.objects.aggregate(
        total=Count('id'),
        today_events=Count('id', filter=Q(date=today)),
        upcoming_events=Count('id', filter=Q(date__gt=today)),
        past_events=Count('id', filter=Q(date__lt=today))
    )

    base_query = Event.objects.prefetch_related('participants').select_related('category')
    
    if type == 'today_events':
        events = base_query.filter(date=today)
    elif type == 'upcoming_events':
        events = base_query.filter(date__gt=today)
    elif type == 'past_events':
        events = base_query.filter(date__lt=today)
    elif type == 'pubs':
          events = User.objects.filter(rsvp_events__isnull=False).distinct()
    else:
        events = base_query.all()
   

    context = {
        'events': events,
        'counts': counts,
        'pubs':pubs,
        'all_events': all_events, 
        'today': today,
        'categories': categories,
        'event':event,
        
    }

    return render(request, 'home.html', context)