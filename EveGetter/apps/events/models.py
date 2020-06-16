from UsersProfiles.models import Account, GenderRestriction
from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from django.shortcuts import get_object_or_404
from django.urls import reverse

# Create your models here.
class Event(models.Model):
    event_creator = models.ForeignKey(Account, on_delete = models.CASCADE)
    name = models.CharField("event name", max_length=30, blank=False)
    description = models.TextField("description", blank=False)
    short_description = models.TextField("short description", blank=False)
    date = models.DateField("event date", blank=False)
    time = models.TimeField("event time", blank=True, null=True)
    duration = models.TimeField("duration of event", blank=True, null=True)
    if_dresscode = models.BooleanField("if dresscode", blank=True)
    dresscodevalue = models.CharField("dress code restriction", max_length=30, blank=True)
    if_age = models.BooleanField("if age",blank=True)
    age_start = models.IntegerField("from what age restriction", blank=True, default=0)
    age_end = models.IntegerField("till what age restriction", blank=True, default=0)
    if_gender = models.BooleanField("if gender", blank=True)
    sex = models.ForeignKey(GenderRestriction,null=True, on_delete=models.CASCADE, blank=True) 
    insidespendings = models.BooleanField("spendings restriction", blank=True)
    country = models.CharField("country", max_length=30, blank=True)
    city = models.CharField("city", max_length=30, default="", blank=True)
    event_adress = models.CharField("event adress", max_length=30, default="", blank=False)
    expected_event = models.BooleanField("if paid expectation", default=False, blank=True)
    event_type = models.ForeignKey('EventType', on_delete=models.CASCADE, blank=False)
    deposit = models.BooleanField("if deposited",default=False, blank=True)
    if_ticket_created = models.BooleanField("if it has tickets", default=False, blank=True)
    moderation = models.ForeignKey('EventModeration', on_delete=models.PROTECT, blank=True)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('event-creator-detail', kwargs={'pk': self.pk})
#@receiver(pre_save, sender=Event, dispatch_uid="set_moderate")
#def set_moderatevtion_level(sender, instance, **kwargs):
#    get_mod_ins = EventModeration.objects.get(eventstatus = 'inactive')
#    instance.moderation = get_mod_ins
#    instance.save()


class EventModeration(models.Model):
    eventstatus = models.CharField(max_length=20, default="inactive")

    def __str__(self):
        return self.eventstatus

#Фотографии
class Images(models.Model):
    event = models.ForeignKey(Event, on_delete = models.CASCADE)
    image = models.ImageField(upload_to='events_images', verbose_name='Фотография', blank=False, null=True)

    def __str__(self):
        return self.event.name + "Image"


class UsersTicketsStatus(models.Model):
    status_name = models.CharField(max_length=30)

    def __str__(self):
        return self.status_name


class Ticket(models.Model):
    ticket_name = models.CharField("ticket name", max_length=25, blank=False)
    amount = models.IntegerField("amount of ticket", blank=False) 
    price = models.IntegerField("ticket's price", blank=False)
    description = models.CharField("ticket description", max_length=100, blank=False)
    event = models.ForeignKey('Event', on_delete=models.PROTECT)
    amount_left = models.IntegerField("amount left", blank=False)
    #ticket_holder = models.ManyToManyField(Account)
    
    def __str__(self):
        return self.ticket_name
    


@receiver(post_save, sender=Ticket, dispatch_uid="update_ticket_created")
def update_ticket_created(sender, instance, **kwargs):
    instance.event.if_ticket_created = True
    instance.event.save()


class UsersTickets(models.Model):
    ticket_owner = models.ForeignKey(Account, related_name="ticketholder", on_delete=models.PROTECT)
    ticket_idpk = models.ForeignKey(Ticket, on_delete=models.PROTECT)
    count = models.IntegerField(default=1)
    date_bought = models.DateField("date of purchase", auto_now_add=True)
    if_gift = models.BooleanField("If ticket was gifted", default=False)
    status = models.ForeignKey(UsersTicketsStatus, on_delete=models.PROTECT, default=1)

    def __str__(self):
        return '{}-{}'.format(self.ticket_idpk.ticket_name, str(self.ticket_idpk))

@receiver(post_save, sender=UsersTickets, dispatch_uid="decrease_tickets_amount")
def decrease_ticket_amount(sender, instance, **kwargs):
    instance.ticket_idpk.amount_left -= instance.count
    instance.ticket_idpk.save()

class EventType(models.Model):
    name = models.CharField('name of eventtype', max_length=25)

    def __str__(self):
        return self.name

class EventComment(models.Model):
    event = models.ForeignKey(Event, on_delete = models.CASCADE)
    user = models.ForeignKey(Account, on_delete = models.CASCADE)
    text = models.TextField(max_length = 160)
    time_created = models.DateTimeField(default = timezone.now, null = True)
   # moderation = models.BooleanField(default = False)

    def __str__(self):
        return '{}-{}'.format(self.event.name, str(self.user.first_name))
     #   return self.text


class Countries(models.Model):
    country = models.CharField(max_length=30, blank=True)

    def __str__(self):
        return self.country

class Cities(models.Model):
    city = models.CharField(max_length=30, blank=True)
    countryid = models.ForeignKey(Countries, on_delete=models.CASCADE)

    def __str__(self):
        return self.city

    
