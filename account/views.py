from decimal import Decimal, InvalidOperation
from django.shortcuts import get_object_or_404, redirect
from rest_framework.views import APIView
from rest_framework.response import Response
from drf_yasg.utils import swagger_auto_schema
from .serializers import RegisterUserSerializer, BillingSerializer
from rest_framework.permissions import IsAuthenticated

from .models import User


class RegisterUserView(APIView):

    @swagger_auto_schema(request_body=BillingSerializer())
    def post(self, request):
        serializer = RegisterUserSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response('Вы успешно зарегистрировались!', status=201)


class ActivateView(APIView):
    def get(self, request, activation_code):
        user = get_object_or_404(User, activation_code=activation_code)
        user.is_active = True
        user.activation_code = ''
        user.save()
        return redirect("https://google.com")
    

class TopUpBillingView(APIView):
    permission_classes = [IsAuthenticated]


    @swagger_auto_schema(request_body=BillingSerializer())
    def post(self, request):
        # ("amount":100)
        amount = request.data.get("amount")
        if not amount:
            return Response("amount is required", status=400)
        try:
            amount = Decimal(amount)
        except InvalidOperation:
            return Response("Invalid_amount", status=400)
        billing = request.user.billing
        if billing.top_up(amount):
            return Response(status=200)
        return Response("invalid amount", status=400)