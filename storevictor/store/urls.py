from django.urls import path
from .views import ( NewStoreAPIView, NewClientAPIView, NewOperatorAPIView, 
                    NewConversationPartyAPIView, NewConversationPartyDetailsAPIView,
                    NewClientChatAPIView, NewChatDetailsAPIView, NewOperatorChatAPIView
)

urlpatterns = [ 
    path('new-store/', NewStoreAPIView.as_view()),
    path('operator/new-operator/', NewOperatorAPIView.as_view()),
    path('customer/register/', NewClientAPIView.as_view()),
    path('customer/register/', NewClientAPIView.as_view()), 
    path('operations/conversation/', NewConversationPartyAPIView.as_view()), 
    path('operations/conversation/<uuid>/', NewConversationPartyDetailsAPIView.as_view()), 
    path('operations/chat/', NewClientChatAPIView.as_view()), 
    path('operations/chat/respond/', NewOperatorChatAPIView.as_view()), 
    path('operations/chat/<uuid>/', NewChatDetailsAPIView.as_view()), 
    

]