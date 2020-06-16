from django.shortcuts import render, redirect
from django.utils import timezone
from .models import Event, Images, Ticket, EventModeration, EventComment, UsersTickets
from django.forms import inlineformset_factory
from django.forms import modelformset_factory
from django.contrib.auth.decorators import login_required
from .forms import CreateEventForm, CreateTicketsForm, BuyTicketForm, EventwithImagesForm, CommentForm, TicketGift, TicketReturnForm
from django.contrib import messages
from django import forms
from django.urls import reverse
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from django.views.generic.edit import FormMixin
from django.views.generic import (
    ListView,
    DetailView,
    CreateView,
    UpdateView,
    DeleteView
)
from django.template import loader
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.http import JsonResponse
from el_pagination.views import AjaxListView
from el_pagination.decorators import page_template
from django.db.models import Q
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.utils.decorators import method_decorator
import datetime

  ####################TEST_FILTER########################
#from django.http import JsonResponse
#from rest_framework.generics import ListAPIView
#from .serializers import EventSerializers
#from .pagination import StandardResultsSetPagination
  ####################TEST_FILTER########################

###########ОСТАВИТЬ
def EventDetailView_true(request, pk):
  event_detail = get_object_or_404(Event, id=pk)
  comments = EventComment.objects.filter(event = event_detail).order_by('-id')
  if request.method == 'POST':
    comment_form = CommentForm(request.POST or None)
    if comment_form.is_valid():
      text = comment_form.save(commit = False)
      text.user = request.user
      text.event = event_detail
      text.save()

  else:
    comment_form = CommentForm()
    paginator = Paginator(comments, 4)
    page = request.GET.get('page')
    try:
      comments = paginator.page(page)
    except PageNotAnInteger:
      comments = paginator.page(1)
    except EmptyPage:
      comments = paginator.page(paginator.num_pages)

  context = {
    'event_detail': event_detail,
    'comments': comments,
    'comment_form': comment_form,
  }
  return render(request, 'events/event_detail2.html', context)


####################УДАЛИТЬ ОТОБРАЖЕНИЕ ИВЕНТА
class EventDetailView(DetailView):
  model = Event

  def get_context_data(self, **kwargs):
    context = super().get_context_data(**kwargs)
    context['event_detail'] = Event.objects.filter(id=id)
    #get_object_or_404(Event, id=id)
    #Event.objects.all().order_by()
    return context
  
  @method_decorator(login_required(login_url='login'))
  def dispatch(self, *args, **kwargs):
    return super(EventDetailView, self).dispatch(*args, **kwargs)


##########ОСТАВИТЬ
def EventLookUpCreator(request, pk):
  event_detail = get_object_or_404(Event, id=pk)
  comments = EventComment.objects.filter(event = event_detail).order_by('-id')

  paginator = Paginator(comments, 4)
  page = request.GET.get('page')
  try:
    comments = paginator.page(page)
  except PageNotAnInteger:
    comments = paginator.page(1)
  except EmptyPage:
    comments = paginator.page(paginator.num_pages)

  context = {
    'event_detail': event_detail,
    'comments': comments,
    # 'comment_form': comment_form,
  }
  return render(request, 'events/event_lookup_creator.html', context)



############ОСТАВИТЬ
def TicketAll (request, pk):
  event = get_object_or_404(Event, id=pk)
  AllEventTickets = Ticket.objects.filter(event = event)
  return render(request, 'events/event_tickets_creator.html', context={'AllEventTickets': AllEventTickets, 'event': event})



###############ОСТАВИТЬ
def TicketReturn(request, pk):
  ticket_to_return = UsersTickets.objects.filter(id=pk)
  ticket_to_return.update(status=3)
  return redirect('mytickets')
  # return HttpResponse('<h1>Все отлично</h1>')


##########ОСТАВИТЬ
class EventDetailTicketGift(FormMixin, DetailView):
  model = Event
  template_name='events/ticket_gift_pre.html'
  form_class = BuyTicketForm

  def get_success_url(self):
    return reverse('mytickets', kwargs={'pk': self.object.pk})


  def post(self, request, *args, **kwargs):    
    self.object = self.get_object()
    form = self.get_form()  
    if form.is_valid():
      return self.form_valid(form)
    else:
      return self.form_invalid(form)

  def form_valid(self, form):
    text = form.save(commit=False)
    text.ticket_holder = request.user
    text.save()
    form.save_m2m()
    return super(BuyTicketForm, self).form_valid(form)
  
  @method_decorator(login_required(login_url='login'))
  def dispatch(self, *args, **kwargs):
    return super(EventDetailTicketGift, self).dispatch(*args, **kwargs)




############ОСТАВИТЬ
class EventDetailTicketBuy(FormMixin, DetailView):
  model = Event
  template_name='events/ticket_buy.html'
  form_class = BuyTicketForm

  def get_success_url(self):
    return reverse('mytickets', kwargs={'pk': self.object.pk})


  def post(self, request, *args, **kwargs):    
    self.object = self.get_object()
    form = self.get_form()  
    if form.is_valid():
      return self.form_valid(form)
    else:
      return self.form_invalid(form)

  def form_valid(self, form):
    text = form.save(commit=False)
    text.ticket_holder = request.user
    text.save()
    form.save_m2m()
    return super(BuyTicketForm, self).form_valid(form)

  @method_decorator(login_required(login_url='login'))
  def dispatch(self, *args, **kwargs):
    return super(EventDetailTicketBuy, self).dispatch(*args, **kwargs)







#########ОСТАВИТЬ
######привязка билета к покупател
@login_required(login_url='login')
def TicketBuy(request, pk):
  form = BuyTicketForm()
  ticket_id = Ticket.objects.filter(id = pk)
  if request.method == 'POST':
    form = BuyTicketForm(request.POST)
    print(request.method)
    if form.is_valid():
      print(request.method)
      text = form.save(commit=False)
      text.ticket_idpk = ticket_id.first()
      text.ticket_owner = request.user
      text.save()
      return redirect('mytickets')
  else:
    form = BuyTicketForm()
    
  return render(request,'events/ticket_save.html', context={'ticket_id':ticket_id, 'form':form})



###########ОСТАВИТЬ
###############Ппдарить билет 
@login_required(login_url='login')
def TicketGiftDone(request, pk):
  form = TicketGift()
  ticket_id = Ticket.objects.filter(id = pk)
  if request.method == 'POST':
    form = TicketGift(request.POST)
    if form.is_valid():
      text = form.save(commit=False)
      text.ticket_idpk = ticket_id.first()
      text.if_gift = True
      #text.ticket_owner = request.form.ticket_owner
      text.save()
      return redirect('mytickets')
  else:
    form = TicketGift()
    
  return render(request,'events/ticket_gift_save.html', context={'ticket_id':ticket_id, 'form':form})


########ОТСАВИТЬ
####создание билетов
@login_required(login_url='login')
def EventCreateTickets(request, pk):
  form = CreateTicketsForm()
  event_id = get_object_or_404(Event, id = pk)
  if request.method == 'POST':
    form = CreateTicketsForm(request.POST)
    if form.is_valid():
      text = form.save(commit=False)
      #text.instance.event = pk
      text.event = event_id
      text.amount_left = text.amount
      text.save()
      return redirect('myevents')
  else:
    form = CreateTicketsForm
  context = {'form':form, 'event_id': event_id,}
  return render(request,'events/ticket_create2.html', context)
#############ОСТАВИТЬ
@login_required(login_url='login')
def EventLookReport(request, pk):
  event = get_object_or_404(Event, id = pk)
  cur_date = datetime.date.today()
  tickets = Ticket.objects.filter(event = event.id)
  user_tickets = UsersTickets.objects.filter(ticket_idpk = tickets)
  all_profit = 0
  all_tickets = 0
  all_tickets_left = 0 
  for ticket in tickets:
    cur_profit = (ticket.amount-ticket.amount_left)*ticket.price
    all_profit += cur_profit
    all_tickets += ticket.amount
    all_tickets_left += ticket.amount_left
  context = {'event':event, 'all_tickets_left':all_tickets_left, 'all_tickets':all_tickets, 'cur_date': cur_date, 'all_profit': all_profit,}
  return render(request, 'events/my_event_report.html', context)


#############ОСТАВИТЬ
@login_required(login_url='login')
def EventUpdateTickets(request, pk):
  event_id = get_object_or_404(Event, id = pk)
  cur_ticket = get_object_or_404(Ticket, event = event_id)
  #cur_ticket = Ticket.objects.filter(event = event_id)
  form = CreateTicketsForm()
  if request.method == 'POST':
    form = CreateTicketsForm(request.POST, instance=cur_ticket)
    if form.is_valid():
      cur_ticket = form.save(commit = False)
      cur_ticket.save()
      #text = form.save(commit=False)
      #text.instance.event = pk
      #text.event = event_id
      #text.amount_left = text.amount
      #text.save()
      return redirect('myevents')
  else:
    form = CreateTicketsForm(instance=cur_ticket)
  context = {'form':form}
  return render(request,'events/ticket_redact2.html', context)

########ОСТАВИТЬ
####создание мероприятия
@login_required(login_url='login')
def createEvent(request):
  ImageFormset = modelformset_factory(Images, fields=('image',), extra=4)
  allEvents = Event.objects.all()
  form = CreateEventForm()
  get_mod_ins = EventModeration.objects.get(eventstatus = 'inactive')
  #formset = ImageFormset(request.POST or None, request.FILES or None)
  
  if request.method == 'POST':
    form = CreateEventForm(request.POST)
    formset = ImageFormset(request.POST or None, request.FILES or None)
    if form.is_valid() and formset.is_valid(): 
      text = form.save(commit=False)
      text.event_creator = request.user
      text.moderation = get_mod_ins
      text.save()

      for f in formset:
        try:
          photo = Images(event=text, image=f.cleaned_data['image'])
          photo.save()
        except Exception as e:
          break
      return redirect('myevents')
  else:
    print(form.errors)
   # print(formset.errors)
   # print("ОШИБКА В ВАЛИДАЦИИ")
    form = CreateEventForm()
    formset = ImageFormset(queryset=Images.objects.none())       


  context = {'form': form, 'allEvents':allEvents, 'formset': formset}
  return render(request, 'events/event_create2.html', context)


#############ОСТАВИТЬ
def MainPageListView(request,
    template='events/index.html',
    page_template='events/event_mainpage.html'):
    latest_events_list = Event.objects.filter(moderation = 2)
    
    context = {
        'latest_events_list': latest_events_list,
        # 'latest_events_list': Event.objects.filter(moderation = 2),
        'expected_events_list': Event.objects.filter(expected_event=True),
        'page_template': page_template,
    }
    if request.is_ajax():
        template = page_template
    return render(request, template, context)

##################ОСТАВИТЬ
def AllEventsDisplay(request):
  search_query = request.GET.get('search', '')  
  if search_query:
    all_allowed_events_list = Event.objects.filter(Q(name__icontains=search_query) |
    Q(description__icontains=search_query) | Q(short_description__icontains=search_query))
  else:
    all_allowed_events_list = Event.objects.filter(moderation=2)

  paginator = Paginator(all_allowed_events_list,9)
  page = request.GET.get('page')
  try:
    all_allowed_events_list = paginator.page(page)
  except PageNotAnInteger:
    all_allowed_events_list = paginator.page(1)
  except EmptyPage:
    all_allowed_events_list = paginator.page(paginator.num_pages)

  return render(request, 'events/all_filter_events.html', context={'all_allowed_events_list':all_allowed_events_list})



###########ОСТАВИТЬ
@login_required
def UpdateEvent(request, pk):
  ImageFormset = modelformset_factory(Images, fields=('image',), extra=4)
  #form = CreateEventForm()
  event_cur = get_object_or_404(Event, pk=pk)
  
  get_mod_ins = EventModeration.objects.get(eventstatus = 'inactive')
  #formset = ImageFormset(request.POST or None, request.FILES or None)

  if request.method == 'POST':
    form = CreateEventForm(request.POST, instance=event_cur)
    formset = ImageFormset(request.POST or None, request.FILES or None)
    if form.is_valid() and formset.is_valid(): 
      event_cur = form.save(commit=False)
      #event_cur.event_creator = request.user
      #event_cur.moderation = get_mod_ins
      event_cur.save()
      #text = form.save(commit=False)
      #text.event_creator = request.user
     # text.moderation = get_mod_ins
      #text.save()

      for f in formset:
        try:
          photo = Images(event=text, image=f.cleaned_data['image'])
          photo.save()
        except Exception as e:
          break
      return redirect('myevents')
  else:
   # print(form.errors)
   # print(formset.errors)
   # print("ОШИБКА В ВАЛИДАЦИИ")
    form = CreateEventForm(instance=event_cur)
   # formset = ImageFormset(queryset=Images.objects.none())
    formset = ImageFormset(queryset=Images.objects.filter(event=event_cur))       


  context = {'form': form,'formset': formset,}
  return render(request, 'events/event_redact2.html', context)


