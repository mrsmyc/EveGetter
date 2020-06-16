from django.contrib import admin

from .models import Event
from .models import EventType
from .models import Images
from .models import GenderRestriction
from .models import Ticket
from .models import UsersTickets
from .models import EventModeration
from .models import Cities
from .models import Countries
from .models import EventComment
from .models import UsersTicketsStatus



admin.site.register(Event)

admin.site.register(Images)

admin.site.register(EventType)

admin.site.register(GenderRestriction)

admin.site.register(Ticket)

admin.site.register(UsersTickets)

admin.site.register(EventModeration)

admin.site.register(Cities)

admin.site.register(Countries)

admin.site.register(EventComment)

admin.site.register(UsersTicketsStatus)