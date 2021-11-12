from rest_framework import serializers
from . models import Store, Client, Operator, Conversation, ClientChat, OperatorChat
from authmanager.serializers import UserSerializer
from itertools import chain


class StoreSerializer(serializers.ModelSerializer):

    created_by_details = UserSerializer(source='created_by', read_only=True)

    class Meta:
        model = Store
        fields = [ 'name', 'uuid' ,'created_by', 'created_by_details', 'timezone', 'telephone']
        extra_kwargs = {
            'created_by': {'write_only': True} 
        }


class OperatorSerializer(serializers.ModelSerializer):
    
    operator = UserSerializer(source='user', read_only=True)
    store_detail = StoreSerializer(source='store', read_only=True)

    class Meta:
        model = Operator
        dept = 1
        fields = [ 'user', 'uuid', 'store', 'store_detail', 'operator', 'department' ]
        extra_kwargs = {
            'store': {'write_only': True} 
        }

class ClientSerializer(serializers.ModelSerializer):
    
    client_detail = UserSerializer(source='user', read_only=True)

    class Meta:
        model = Client
        dept = 1
        fields = [ 'user', 'uuid', 'client_detail', 'timezone', 'address']


class ConversationPartySerializer(serializers.ModelSerializer):

    
    client_detail = ClientSerializer(source='client', read_only=True)
    operator = OperatorSerializer(source='operator_uuid', read_only=True)
    chats = serializers.SerializerMethodField('get_chats_from_conversation')


    class Meta:
        model = Conversation
        dept = 1
        fields = [ 'store', 'uuid', 'client','client_detail', 'operator_uuid', 'operator', 'status', 'chats']
        extra_kwargs = {
            'store': {'write_only': True}, 
            'client': {'write_only': True},
            'operator_uuid': {'write_only': True} 
        }

    def get_chats_from_conversation(self, conversation):

        opchat = OperatorChat.objects.filter(conversation_party=conversation).values_list('message', flat=True)
        clichat = ClientChat.objects.filter(conversation_party=conversation).values_list('message', flat=True)
        combined_list = list(chain(clichat, opchat))

        return combined_list

class ChatSerializer(serializers.ModelSerializer):
    
    convo_party = ConversationPartySerializer(source='conversation_party', read_only=True)

    class Meta:
        model = ClientChat
        dept = 1
        fields = [ 'uuid', 'conversation_party', 'user', 'convo_party', 'message', 'status']


class OperatorChatSerializer(serializers.ModelSerializer):
    
    convo_party = ConversationPartySerializer(source='conversation_party', read_only=True)

    class Meta:
        model = OperatorChat
        dept = 1
        fields = [ 'uuid', 'conversation_party', 'operator', 'convo_party', 'message', 'chat']
