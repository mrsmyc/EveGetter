from django.forms import ModelForm
from .models import Event,Ticket,UsersTickets, EventComment
from django import forms


class CreateEventForm(ModelForm):
   # date = DateField(input_formats=settings.DATE_INPUT_FORMATS)
  #date = forms.DateField(input_formats=['%d.%m.%y'])
    date = forms.DateField(input_formats=['%d.%m.%Y'])

    class Meta:
        model = Event   
      
        fields = ('name','description','short_description','date','dresscodevalue',
        'age_start','age_end','sex','insidespendings','event_adress',
        'event_type','if_dresscode','if_age','if_gender','time','duration',
        'country','city',
        )
   
    def __init__(self, *args, **kwargs):
       super(CreateEventForm, self).__init__(*args, **kwargs)
       self.fields['date'].widget.attrs['id'] = 'id_event_date'
       self.fields['name'].widget.attrs['id'] = 'lbl_name'
       self.fields['description'].widget.attrs['id'] = 'lbl_desc'
       self.fields['short_description'].widget.attrs['id'] = 'lbl_sh_desc'
       self.fields['event_type'].widget.attrs['id'] = 'lbl_type'
       self.fields['date'].widget.attrs['id'] = 'lbl_date id_event_date'
       self.fields['time'].widget.attrs['id'] = 'lbl_time'
       self.fields['duration'].widget.attrs['id'] = 'lbl_dur'
       self.fields['if_dresscode'].widget.attrs['id'] = 'lbl_dress'
       self.fields['if_age'].widget.attrs['id'] = 'lbl_age'
       self.fields['if_gender'].widget.attrs['id'] = 'lbl_gend'
       self.fields['insidespendings'].widget.attrs['id'] = 'lbl_spend'
       self.fields['country'].widget.attrs['id'] = 'lbl_ctry'
       self.fields['city'].widget.attrs['id'] = 'lbl_city'
       self.fields['event_adress'].widget.attrs['id'] = 'lbl_adress'
       self.fields['name'].widget.attrs['class'] = 'inp_border'
       self.fields['event_type'].widget.attrs['class'] = 'inp_border'
       self.fields['date'].widget.attrs['class'] = 'inp_border id_event_date'
       self.fields['sex'].widget.attrs['class'] = 'inp_border'
       self.fields['time'].widget.attrs['class'] = 'inp_border timepicker'
       self.fields['duration'].widget.attrs['class'] = 'inp_border timepicker'
       self.fields['dresscodevalue'].widget.attrs['class'] = 'inp_border'
       self.fields['age_start'].widget.attrs['class'] = 'inp_border'
       self.fields['age_end'].widget.attrs['class'] = 'inp_border'
       self.fields['country'].widget.attrs['class'] = 'inp_border'
       self.fields['city'].widget.attrs['class'] = 'inp_border'
       self.fields['event_adress'].widget.attrs['class'] = 'inp_border'
       self.fields['if_dresscode'].widget.attrs['class'] = 'add_form_radio'
       self.fields['if_age'].widget.attrs['class'] = 'add_form_radio'
       self.fields['if_gender'].widget.attrs['class'] = 'add_form_radio'
       self.fields['insidespendings'].widget.attrs['class'] = 'add_form_radio'

class EventwithImagesForm(CreateEventForm):
  images = forms.FileField(label='Фотография',widget=forms.ClearableFileInput(attrs={'multiple': True}))

  class Meta(CreateEventForm.Meta):
    fields = CreateEventForm.Meta.fields + ('images',)

  
class TicketReturnForm(ModelForm):
  class Meta:
    model = UsersTickets
    fields = ('status',)


class BuyTicketForm(ModelForm):
  class Meta:
    model = UsersTickets
    fields = ('count',)

class CreateTicketsForm(ModelForm):
  class Meta:
    model = Ticket
    fields = ('ticket_name','amount','price','description',)


class CommentForm(forms.ModelForm):
  class Meta:
    model = EventComment
    fields = ('text',)

class TicketGift(forms.ModelForm):
  class Meta:
    model = UsersTickets
    fields = ('ticket_owner', 'count',)

  def __init__(self, *args, **kwargs):
      super(TicketGift, self).__init__(*args, **kwargs)
      self.fields['ticket_owner'].widget.attrs['class'] = 'ch_search'