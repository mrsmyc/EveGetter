from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.forms import inlineformset_factory
from django.contrib.auth.forms import UserCreationForm, PasswordChangeForm
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import Http404
from .forms import CreateUserForm, PasswordChangeFormEdit, UserUpdateForm
from events import urls
from .models import Account
from events.models import Event, Ticket, UsersTickets
from django.views.generic.list import ListView
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.shortcuts import get_object_or_404
from django.utils.decorators import method_decorator
from django.template.loader import render_to_string
from django.http import JsonResponse
# Create your views here.
#####TESTSEARCH#####
# def artists_view(request):
#   ctx = {}
#   url_parameter = request.GET.get('q')

#   if url_parameter:
#     user_events = Event.objects.filter(name__icontains=url_parameter)
#   else:
#     user_events = Event.objects.all()

#   ctx['user_events'] = user_events
#   if request.is_ajax():

#     html = render_to_string(
#       # template_name='accounts/my_event_test_display.html', 
#       context={"user_events": user_events}
#     )
#     data_dict = {'html_from_view': html}
#     return JsonResponse(data=data_dict, safe=False)

#   return render(request, 'accounts/my_events_test.html', context=ctx)



def registerPage(request):
  form = CreateUserForm()

  if request.method == 'POST':
    form = CreateUserForm(request.POST)
    if form.is_valid():
      # form.cleaned_data()
      form.save()
      messages.success(request,'Вы успешно зарегестрировались!')

      return redirect('login')

  context = {'form': form}
  return render(request, 'accounts/register.html', context)


def loginPage(request):
  if request.user.is_authenticated:
    return redirect('index')
  else:
    if request.method == 'POST':
      phone = request.POST.get('phone')
      password = request.POST.get('password')
      user = authenticate(request, phone=phone, password=password)

      if user is not None:
        login(request, user)
        return redirect('index')
      
      else: 
        messages.info(request, 'Телефон или пароль неправильный')
    context = {}
    return render(request, 'accounts/login.html', context)


def logoutUser(request):
  logout(request)
  return redirect('index')



    



@login_required(login_url='login')
def accountControl(request):
  form = PasswordChangeFormEdit(user=request.user)
  if request.method == 'POST':
    form = PasswordChangeFormEdit(data=request.POST, user=request.user)

    if form.is_valid():
      # form.cleaned_data()
      form.save()
      update_session_auth_hash(request, form.user)
      return redirect('acclook')

  else:
    form = PasswordChangeFormEdit(user=request.user)    
  return render(request, 'accounts/acc_control.html', context = {'form':form})


@login_required(login_url='login')
def UpdateUser(request):
  if request.method == 'POST':
    u_form = UserUpdateForm(request.POST, request.FILES, instance=request.user)
    if u_form.is_valid():
      text = u_form
      text.user_avatar = u_form.cleaned_data['user_avatar']
      text.save()
      messages.success(request, f'Вы обновили информацию')
      return redirect('acclook')
  else:
    u_form = UserUpdateForm(instance=request.user)

  context = {
    'u_form': u_form
  }  
  return render(request, 'accounts/change_acc_info.html', context)



def UserLookUp(request,pk):
  user = get_object_or_404(Account, id=pk)
  context = {
    'user': user,
  }
  return render(request, 'accounts/user_lookup.html', context)



# @login_required(login_url='login')
class myEventsList(ListView):
  model = Event
  template_name='accounts/my_events.html'

  def get_context_data(self, **kwargs):
    context = super().get_context_data(**kwargs)

    context['user_events'] = Event.objects.filter(event_creator=self.request.user)
    paginator = Paginator(context['user_events'],4)
    page = self.request.GET.get('page')
    try:
      context['user_events'] = paginator.page(page)
    except PageNotAnInteger:
      context['user_events'] = paginator.page(1)
    except EmptyPage:
      context['user_events'] = paginator.page(paginator.num_pages)
    
    return  context

  @method_decorator(login_required(login_url='login'))
  def dispatch(self, *args, **kwargs):
    return super(myEventsList, self).dispatch(*args, **kwargs)

@login_required(login_url='login')
def myEvents(request):
  user_events = Event.objects.filter(event_creator=request.user)
  return render(request, 'accounts/my_events.html', context={'user_events':user_events})

# @login_required(login_url='login')
class myTickets(ListView):
  model = UsersTickets
  template_name = 'accounts/my_tickets.html'

  def get_context_data(self, **kwargs):
    context = super().get_context_data(**kwargs)

    context['user_tickets'] = UsersTickets.objects.filter(ticket_owner=self.request.user).filter(status=1)
    paginator = Paginator(context['user_tickets'],4)
    page = self.request.GET.get('page')
    try:
      context['user_tickets'] = paginator.page(page)
    except PageNotAnInteger:
      context['user_tickets'] = paginator.page(1)
    except EmptyPage:
      context['user_tickets'] = paginator.page(paginator.num_pages)
    
    return  context

  @method_decorator(login_required(login_url='login'))
  def dispatch(self, *args, **kwargs):
    return super(myTickets, self).dispatch(*args, **kwargs)




