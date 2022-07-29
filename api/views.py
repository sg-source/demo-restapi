
import datetime
import pytz
from django.conf.global_settings import TIME_ZONE
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from .serializers import GetReceiptSerializer, PostReceiptSerializer, \
    GetProductSerializer, UserShopsSerializer, SumPerTimeSerializer, ReceiptsPerTimeSerializer
from .models import Receipt, User, Shop, Product


class APIReceiptView(APIView):
    """
    Get all receipts
    """
    def get(self, request):
        receipts = Receipt.objects.all()
        serializer = GetReceiptSerializer(receipts, many=True)
        return Response(serializer.data)
    
    def post(self, request):
        if request.method == 'POST':
            if type(request.data) == dict:
                # print(request.data['total_sum'])
                serializer = PostReceiptSerializer(data=request.data)
                if serializer.is_valid():
                    serializer.save()
                    return Response(serializer.data,
                                    status=status.HTTP_201_CREATED)
                print(serializer.errors)
                return Response(serializer.data,
                                status=status.HTTP_400_BAD_REQUEST)
            elif type(request.data) == list:
                for receipt in request.data:
                    serializer = PostReceiptSerializer(data=receipt)
                    if serializer.is_valid():
                        pass
                        serializer.save()
                return Response(request.data,
                                status=status.HTTP_201_CREATED)
            return Response(status=status.HTTP_400_BAD_REQUEST)
        
        else:
            return Response(status=status.HTTP_200_OK)
        
        
class UserProductsView(APIView):
    
    def get(self, request, user):
        receipts = Product.objects.select_related('receipt').filter(receipt__user__iexact=user)
        serializer = GetProductSerializer(receipts, many=True)
        return Response(serializer.data,
                        status=status.HTTP_200_OK)


class UserShopsView(APIView):
    """
    Get user infarmaton about products
    """
    def get(self, request, user):
        receipts = Receipt.objects.all().filter(user__iexact=user).values_list('shop').distinct()
        shops_map = {str(number): str(shop[0]) for number, shop in enumerate(receipts, start=1)}
        data = {key: val for key, val in zip(['name', 'shops'], [str(user), shops_map])}
        serializer = UserShopsSerializer(data=data)
        
        if serializer.is_valid():
            return Response(serializer.data,
                            status=status.HTTP_200_OK)
        else:
            print(serializer.errors)
            return Response(status=status.HTTP_400_BAD_REQUEST)


class SumPerTimeView(APIView):
    """
    Get total sum of receipts for a certain time
    """
    def get(self, request, time_from, time_to):
        
        try:
            tz = pytz.timezone(TIME_ZONE)
            date_from = datetime.datetime.strptime(str(time_from), '%Y%m%d').replace(tzinfo=tz)
            date_to = datetime.datetime.strptime(str(time_to), '%Y%m%d').replace(tzinfo=tz)
        except ValueError:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        
        receipts = Receipt.objects.all().filter(date_of_issue__range=(date_from, date_to)).values_list('total_sum')
        result = [item[0] for item in receipts]
        data = {key: val for key, val in zip(['date_from', 'date_to', 'total_sum'],
                                             [date_from, date_to, sum(result)])}
        serializer = SumPerTimeSerializer(data=data)
        
        if serializer.is_valid():
            return Response(serializer.data,
                            status=status.HTTP_200_OK)
        else:
            print(serializer.errors)
            return Response(status=status.HTTP_400_BAD_REQUEST)
        
class ReceiptsPerTimeView(APIView):
    """
    Get receipts for a certain time
    """
    def get(self, request, time_from, time_to):
        
        try:
            tz = pytz.timezone(TIME_ZONE)
            date_from = datetime.datetime.strptime(str(time_from), '%Y%m%d').replace(tzinfo=tz)
            date_to = datetime.datetime.strptime(str(time_to), '%Y%m%d').replace(tzinfo=tz)
        except ValueError:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        
        receipts = Receipt.objects.all().filter(date_of_issue__range=(date_from, date_to)).values()
        data = {key: val for key, val in zip(['date_from', 'date_to', 'receipts'],
                                             [date_from, date_to, list(receipts)])}
        serializer = ReceiptsPerTimeSerializer(data=data)

        if serializer.is_valid():
            return Response(serializer.data,
                            status=status.HTTP_200_OK)
        else:
            print(serializer.errors)
            return Response(status=status.HTTP_400_BAD_REQUEST)
