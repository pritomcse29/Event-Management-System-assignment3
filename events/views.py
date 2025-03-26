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
from .models import  Event, RSVP
from django.contrib.auth.decorators import user_passes_test,login_required,permission_required
from users.views import is_admin
from django.contrib.auth import get_user_model
from django.views.generic import DeleteView,ListView,DetailView,TemplateView,View
from django.urls import reverse_lazy

User = get_user_model()
def is_organizer(user):
    return user.groups.filter(name='Organizer').exists()
def is_participant(user):
    return user.groups.filter(name='User').exists()

class Organizer_Dashboard(TemplateView):
    template_name = 'dashboard/organizer_dashboard.html'
    def get_context_data(self, **kwargs):
        context =  super().get_context_data(**kwargs)
        categories = Category.objects.all()  
        event = Event.objects.all()

        type = self.request.GET.get('type', 'all')
        today = date.today()
        all_events = Event.objects.all()  
        pubs = User.objects.aggregate(unique_count=Count('id', distinct=True))['unique_count']
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

        return context
    
@user_passes_test(is_organizer,login_url='no-permission')
def organizer_dashboard(request):
    categories = Category.objects.all()  
    event = Event.objects.all()

    type = request.GET.get('type', 'all')
    today = date.today()
    all_events = Event.objects.all()  
    # today_events = Event.objects.filter(date=today)
    # past_events = Event.objects.filter(date__lt=today).order_by('-date')
    # upcoming_events = Event.objects.filter(date__gt=today).order_by('date')

    pubs = User.objects.aggregate(unique_count=Count('id', distinct=True))['unique_count']

  
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

    return render(request, 'dashboard/organizer_dashboard.html', context)

class CreateEventView(View):
    template_name = 'dashboard/create_event.html'

    def get(self, request):
        event_e = EventModelForm()
        return render(request, self.template_name, {"event_e": event_e})

    def post(self, request):
        event_e = EventModelForm(request.POST, request.FILES)
        if event_e.is_valid():
            event_e.save()
            return redirect('create-event')
        return render(request, self.template_name, {"event_e": event_e})
     
@login_required
@permission_required("events.add_event",login_url='no-permission')
def create_event(request):
     event_e = EventModelForm()

     if request.method == "POST":
        event_e  = EventModelForm(request.POST, request.FILES)
        if event_e.is_valid():
                event_e.save()
                return redirect('create-event')
    
        else:
            event_e =  EventModelForm()
            
     return render(request,'dashboard/create_event.html',{"event_e": event_e})
@login_required
@permission_required("events.add_category",login_url='no-permission')
def create_category(request):
     event_form = CategoryModelForm()
     if request.method == "POST":
        event_form = CategoryModelForm(request.POST)
        if event_form.is_valid():
                event_form.save()
               
                return render(request,'dashboard/create_category.html',{"event_form":event_form,"message": "added successfully"})  
    
        else:
           event_form = CategoryModelForm()

     return render(request,'dashboard/create_category.html',{"event_form": event_form})
@login_required
def add_participant(request):
    if request.method == 'POST':
        form = ParticipantForm(request.POST)
        if form.is_valid():
            # Create a new user
            username = form.cleaned_data['username']
            email = form.cleaned_data['email']
            first_name = form.cleaned_data['first_name']
            last_name = form.cleaned_data['last_name']
            events = form.cleaned_data['events']
            try:
                user = User.objects.get(email=email)
            except User.DoesNotExist:
                user = User.objects.create_user(
                    username=username,
                    email=email,
                    password='default_password', 
                    first_name=first_name,
                    last_name=last_name
                )

            for event in events:
                event.participants.add(user)

            return redirect('organizer-dashboard')  
    else:
        form = ParticipantForm()

    return render(request, 'dashboard/add_participant.html', {'form': form})

@login_required
def update_participant(request, user_id):
    user = get_object_or_404(User, id=user_id)
    events = Event.objects.filter(participants=user)

    if request.method == 'POST':
        form = ParticipantForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
            new_events = form.cleaned_data['events']
            for event in events:
                event.participants.remove(user)
            for event in new_events:
                event.participants.add(user)

            return redirect('organizer_dashboard')  
    else:
        form = ParticipantForm(instance=user, initial={
            'events': events
        })

    return render(request, 'dashboard/update_participant.html', {'form': form, 'user': user})

@user_passes_test(is_participant,login_url='no-permission')
def participant_dashboard(request):
    user_id = request.user.id
    user = get_object_or_404(User, id=user_id)  
    if not request.user.is_authenticated or request.user.id != user.id:
        messages.error(request, 'You do not have permission to access this page.')
        return redirect('login')
    today = timezone.now().date()
    today_events = Event.objects.filter(date=today)
    past_events = Event.objects.filter(date__lt=today).order_by('-date')
    upcoming_events = Event.objects.filter(date__gt=today).order_by('date')
    if request.method == 'POST':
        event_id = request.POST.get('event_id')
        event = get_object_or_404(Event, id=event_id)
        if not RSVP.objects.filter(user=user, event=event).exists():
           
            RSVP.objects.create(user=user, event=event, is_active=True)
            messages.success(request, f'You have successfully registered for the event: {event.name}')
        else:
            messages.warning(request, 'You are already registered for this event.')

    
        return redirect('participant-dashboard')

    return render(request, 'dashboard/participant_dashboard.html', {
        'upcoming_events': upcoming_events,
        'today_events': today_events,
        'past_events': past_events,
        'user': user,
    })

@login_required
@permission_required("events.add_category",login_url='no-permission')
def update_event(request,id):
     event = Event.objects.get(id=id)
     event_e = EventModelForm(instance=event)
     if request.method == "POST":
        event_e  = EventModelForm(request.POST,instance=event)
        if event_e.is_valid():
                event_e.save()
                return redirect(reverse('update-event', args=[id]),{"message": "updated successfully"})
        
            
     return render(request,'dashboard/create_event.html',{"event_e": event_e})
     

@login_required
@permission_required("events.change_event",login_url='no-permission')
def update_category(request,id):
     category = Category.objects.get(id=id)
     event_form = CategoryModelForm(instance=category)
     if request.method == "POST":
        event_form = CategoryModelForm(request.POST,instance = category)
        if event_form.is_valid():
                event_form.save()
               
                return redirect(reverse('dashboard'))
   
    

     return render(request,'dashboard/create_category.html',{"event_form": event_form})
     

def detail_page(request,id):
     event = Event.objects.get(id=id)

     return render(request,'detail_page.html',{'event':event})

class Detail_Page(ListView):
    model = Event
    template_name = 'detail_page.html'
    context_object_name = 'event'
    def get_queryset(self):
        return Event.objects.filter(id=self.kwargs['id'])

@login_required
@permission_required("events.delete_event",login_url='no-permission')
def delete_event(request,id):
    if request.method == 'POST':
      event = Event.objects.get(id=id)
      event.delete()
      return redirect('dashboard')
    else:
      return redirect('dashboard')
    
class Delete_Event_View(DeleteView):
    model = Event
    def get_success_url(self):
        return reverse_lazy(dashboard)
    pk_url_kwarg = 'id'

    def post(self,request,*args,**kwargs):
        event_id = self.kwargs.get('id')
        try:
            event = Event.objects.get(id=event_id)
            event.delete()
            messages.success(request,'Event Deleted Successfully')
        except Event.DoesNotExist:
            messages.error(request,'Event not found')
        return redirect(self.get_success_url())

def event_details(request):
    search_query = request.GET.get('q', '').strip()  
    

    if search_query:
        events = Event.objects.filter(name__icontains=search_query)
    else:
        events = Event.objects.all()  

    context = {
        'events': events,
        'search_query': search_query,  
    }
    return render(request, 'event_details.html', context)
class EventDetailsView(ListView):
    model = Event
    template_name = 'event_details.html'
    context_object_name = 'events'

    def get_queryset(self):
        search_query = self.request.GET.get('q', '').strip()
        if search_query:
            return Event.objects.filter(name__icontains=search_query)
        return Event.objects.all()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['search_query'] = self.request.GET.get('q', '').strip()
        return context


User = get_user_model()
@login_required
@user_passes_test(is_participant)

def rsvp_event(request, event_id):
    event = get_object_or_404(Event, id=event_id)
    user = request.user


    RSVP.objects.create(user=user, event=event)




    return redirect('participant-dashboard')


def activate_user(request, user_id, token):
    user = get_object_or_404(User, id=user_id)
    
    if default_token_generator.check_token(user, token):
        user.is_active = True
        user.save()
   
        event = get_object_or_404(Event, id=request.session.get('event_id'))
        event.participants.add(user)
        
        return redirect('profile') 
    


@login_required
@permission_required("events.view_event",login_url='no-permission')

def participant_page(request, event_id):
    event = get_object_or_404(Event, id=event_id)
    participants = event.participants.all()
    return render(request, 'events/participant_page.html', {'event': event, 'participants': participants})
@login_required
@user_passes_test(is_participant)
def user_registered_events(request):
    user = request.user
    registered_events = RSVP.objects.filter(user=user).select_related('event')

    return render(request, 'dashboard/user_registered_events.html', {
        'registered_events': registered_events,
    })
@login_required
@user_passes_test(is_organizer)
def event_detail(request,event_id):
    event = Event.objects.get(id=event_id)
    return render (request,'dashboard/event_detail.html',{'event':event})

@login_required
def dashboard(request):
    if is_participant(request.user):
        return redirect('participant-dashboard')
    elif is_organizer(request.user):
        return redirect('organizer-dashboard')
    elif is_admin(request.user):
        return redirect('admin-dashboard')

    return redirect('no-permission')
def all_event(request):
    eventList = Event.objects.all()
    return render(request,'dashboard/all_event.html',{'eventList':eventList})


def all_category(request):
    categories = Category.objects.all()
    return render(request,'dashboard/all_category.html',{'categories':categories})

