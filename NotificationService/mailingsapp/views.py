import requests
from django.shortcuts import get_object_or_404
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from .serializers import *


class ClientViewSet(viewsets.ModelViewSet):
    serializer_class = ClientSerializer
    queryset = Client.objects.all()


class MessageViewSet(viewsets.ModelViewSet):
    serializer_class = MessageSerializer
    queryset = Message.objects.all()


class MailingViewSet(viewsets.ModelViewSet):
    serializer_class = MailingSerializer
    queryset = Mailing.objects.all()

    @action(detail=True, methods=['GET'])
    def info(self, request, pk=None):
        queryset_mailing = Mailing.objects.all()
        get_object_or_404(queryset_mailing, pk=pk)
        queryset = Message.objects.filter(message_mailing_id=pk).all()
        serializer = MessageSerializer(queryset, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['GET'])
    def fullinfo(self, request):
        total_count = Mailing.objects.count()
        mailing = Mailing.objects.values('id')
        content = {'Mailings count': total_count,
                   'Messages send': ''}
        result = {}

        for row in mailing:
            res = {'Total messages': 0, 'Send': 0, 'Not send': 0}
            mail = Message.objects.filter(message_mailing_id=row['id']).all()
            group_send = mail.filter(status='send').count()
            group_not_send = mail.filter(status='not send').count()
            res['Total messages'] = len(mail)
            res['Send'] = group_send
            res['Not send'] = group_not_send
            result[row['id']] = res

        content['Messages send'] = result
        return Response(content)
