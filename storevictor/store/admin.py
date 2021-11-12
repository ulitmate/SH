from django.contrib import admin
from .models import Store, Discount, Operator, Client, Conversation, ClientChat


# Register your models here.
admin.site.register(Store)
admin.site.register(Discount)
admin.site.register(Operator)
admin.site.register(Client)
admin.site.register(Conversation)
admin.site.register(ClientChat)

