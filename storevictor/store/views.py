from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from .serializers import ( StoreSerializer, ClientSerializer, OperatorSerializer, 
                            ConversationPartySerializer, ChatSerializer, OperatorChatSerializer
)
from authmanager.serializers import UserSerializer
from .models import Client, Operator, Store, Conversation, ClientChat, OperatorChat, Discount
from utility.logger import appLogs 

from .tasks import send_notification_email_task


# Create your views here.

  
class NewOperatorChatAPIView(APIView):

    '''
        API View for New Chat from Operator to Client
    '''
    def get(self, request):
        chats = OperatorChat.objects.all()
        serializer = OperatorChatSerializer(chats, many=True)
        return Response(serializer.data)

    def post(self, request):

        serializer = OperatorChatSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        
        data = {}
        data["success"] = True
        data["message"] = "New Operator Chat Created"
        data["data"] = serializer.data

        return Response(data=data, status=status.HTTP_201_CREATED)

class NewChatDetailsAPIView(APIView):
    
    '''
        Class for detail view for both Client and Operator chats.
        GET Request is for single object fetch.
    '''
    def get_object(self, uuid):

        try:            
            chat = get_object_or_404(ClientChat, uuid=uuid, is_deleted=False)
            return chat
            
        except ClientChat.DoesNotExist:
            return HttpResponse(status=status.HTTP_404_NOT_FOUND)

    def get(self, request, uuid):
        chat = self.get_object(uuid)
        serializer = ChatSerializer(chat)
        return Response(serializer.data)

    def put(self, request, uuid):

        service = self.get_object(uuid)
        serializer = ChatSerializer(service, data=request.data)
        if serializer.is_valid():
            serializer.save()
          
            return Response(serializer.data)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self, request, uuid): 

        '''
            API View for toggling to delete a chat record. 
            Records are not deleted but marked as deleted. 
        '''
        chat = self.get_object(uuid)
        chat.is_deleted = True
        chat.save()
        return  Response(status=status.HTTP_204_NO_CONTENT)


class NewClientChatAPIView(APIView):

    '''
        API View for New Chat from  Client to Operator.
    '''

    def get(self, request):
        chats = ClientChat.objects.all()
        serializer = ChatSerializer(chats, many=True)
        return Response(serializer.data)

    def post(self, request):

        serializer = ChatSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data["user"]
        
        comm = None
        try:
            if Client.objects.get(user=user):
                comm = "receiving"

        except Client.DoesNotExist as err:
            appLogs('Error with getting client of parsed user uuid', err)

            data = {}
            data["success"] = False
            data["message"] = "New Chat not Created"
            data["error"] = str(err)
            return Response(data=data, status=status.HTTP_400_BAD_REQUEST)

        chat_obj = serializer.save()
        
        chat_obj.communication = comm
        chat_obj.save()
       
        data = {}
        data["success"] = True
        data["message"] = "New Chat Created"
        data["data"] = serializer.data

        return Response(data=data, status=status.HTTP_201_CREATED)



class NewConversationPartyAPIView(APIView):

    '''
        API View for New Conversation/COnversation-Party(Store, Operator, Client).
    '''

    def get(self, request):
        services = Conversation.objects.all()
        serializer = ConversationPartySerializer(services, many=True)
        return Response(serializer.data)

    def post(self, request):

        serializer = ConversationPartySerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
   
        serializer.save()

        data = {}

        data["success"] = True
        data["message"] = "New Client Created"
        data["data"] = serializer.data

        return Response(data=data, status=status.HTTP_201_CREATED)



class NewConversationPartyDetailsAPIView(APIView):

    '''
        API View for fetching the details of particular conversation/conversation-party
        PUT request gets updates done.
    '''

    def get_object(self, uuid):

        try:            
            convo_party = get_object_or_404(Conversation, uuid=uuid, is_deleted=False)
            return convo_party
            
        except Conversation.DoesNotExist:
            return HttpResponse(status=status.HTTP_404_NOT_FOUND)

    def get(self, request, uuid):
        convo_party = self.get_object(uuid)
        serializer = ConversationPartySerializer(convo_party)
        return Response(serializer.data)

    def put(self, request, uuid):

        service = self.get_object(uuid)
        serializer = ConversationPartySerializer(service, data=request.data)
        if serializer.is_valid():
            serializer.save()
          
            return Response(serializer.data)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self, request, uuid): 
        convo_party = self.get_object(uuid)
        convo_party.is_deleted = True
        convo_party.save()
        return  Response(status=status.HTTP_204_NO_CONTENT)


class NewOperatorAPIView(APIView):

    '''
        API View for creating/registering(POST Request) a New Operator of a Store
        and assigning to a particular department.
       
    '''
    
    def post(self, request):
        store = request.data['store']
        department = request.data['department']

        
        department = request.POST.get('department', 'operations')
        
        serializer = UserSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user_obj = serializer.save()

        store_obj = Store.objects.get(uuid=store)

        operator = Operator.objects.create(user=user_obj, store=store_obj, department=department)

        serializer = OperatorSerializer(operator)

        data = {}

        data["success"] = True
        data["message"] = "New Client Created"
        data["data"] = serializer.data

        return Response(data=data, status=status.HTTP_201_CREATED)



class NewClientAPIView(APIView):

    '''
        API View for creating/registering(POST Request) a New chat from a client/customer.
        
    '''
    
    def post(self, request):
        timezone = request.POST.get('timezone', 'UTC')
        serializer = UserSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user_obj = serializer.save()

        client = Client.objects.create(user=user_obj, timezone=timezone)

        serializer = ClientSerializer(client)

        data = {}

        data["success"] = True
        data["message"] = "New Client Created"
        data["data"] = serializer.data

        return Response(data=data, status=status.HTTP_201_CREATED)



class NewStoreAPIView(APIView):

    '''
        API View for creating/registering(POST Request) a New  Store
        GET request is for fetching all stores.
    '''

    def get(self, request):
        stores = Store.objects.all()
        serializer = StoreSerializer(stores, many=True)
        return Response(serializer.data)

    
    def post(self, request):
        serializer = StoreSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()
            data = {}
            data["success"] = True
            data["message"] = "New Store, %s, is  created"% (serializer.validated_data["name"] )
            data["data"] = serializer.data
            
            return Response(data=data, status=status.HTTP_201_CREATED)

        data = {}
        data["success"] = False
        data["error"] = serializer.errors
        data["message"] = "New Store could NOT be Created"
        
        return Response(data=data, status=status.HTTP_400_BAD_REQUEST)

