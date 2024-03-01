import os
import stripe
from django.shortcuts import get_object_or_404

from dotenv import load_dotenv
from drf_spectacular.utils import extend_schema, OpenApiResponse
from rest_framework import status
from rest_framework.exceptions import ValidationError, PermissionDenied
from rest_framework.permissions import IsAuthenticated
from rest_framework.renderers import TemplateHTMLRenderer
from rest_framework.views import APIView
from rest_framework.response import Response

from .models import Item, Order
from .serializers import ItemSerializer, OrderSerializer

load_dotenv()


class CreateItemView(APIView):
    serializer_class = ItemSerializer
    @extend_schema()
    def post(self, request):
        try:
            serializer = ItemSerializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(data={'New Item': serializer.data}, status=status.HTTP_201_CREATED)
        except ValidationError as e:
            return Response(data={'Error': str(e.args)}, status=e.status_code)


class GetAllItemView(APIView):
    serializer_class = ItemSerializer

    @extend_schema()
    def get(self, request):
        try:
            items = Item.objects.all()
            if not items:
                return Response(data={'Error': 'No items found'}, status=status.HTTP_404_NOT_FOUND)
            serializer = ItemSerializer(items, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Item.DoesNotExist as e:
            return Response(data={'Error': str(e)}, status=status.HTTP_404_NOT_FOUND)


class GetItemView(APIView):
    serializer_class = ItemSerializer
    @extend_schema()
    def get(self, request, *args, **kwargs):
        try:
            item_id = kwargs.get('id')
            if not item_id:
                return Response(data={'Error': 'Item ID required'}, status=status.HTTP_400_BAD_REQUEST)
            item = get_object_or_404(Item, id=item_id)
            serializer = ItemSerializer(item)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Item.DoesNotExist as e:
            return Response(data={'Error': str(e)}, status=status.HTTP_404_NOT_FOUND)
        except ValidationError as e:
            return Response(data={'Error': str(e.args)}, status=e.status_code)


class UpdateItemView(APIView):
    serializer_class = ItemSerializer
    @extend_schema()
    def put(self, request, *args, **kwargs):
        try:
            item_id = kwargs.get('id')
            if not item_id:
                return Response(data={'Error': 'Item ID required'}, status=status.HTTP_400_BAD_REQUEST)
            item = get_object_or_404(Item, id=item_id)
            serializer = ItemSerializer(data=request.data, instance=item)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Item.DoesNotExist as e:
            return Response(data={'Error': str(e)}, status=status.HTTP_404_NOT_FOUND)
        except ValidationError as e:
            return Response(data={'Error': str(e.args)}, status=e.status_code)


class DeleteItemView(APIView):
    serializer_class = ItemSerializer
    @extend_schema()
    def delete(self, request, *args, **kwargs):
        try:
            item_id = kwargs.get('id')
            if not item_id:
                return Response(data={'Error': 'Item ID required'}, status=status.HTTP_400_BAD_REQUEST)
            item = get_object_or_404(Item, id=item_id)
            item.delete()
            return Response(data={'Message': 'Successfully deleted item'}, status=status.HTTP_204_NO_CONTENT)
        except Item.DoesNotExist as e:
            return Response(data={'Error': str(e)}, status=status.HTTP_404_NOT_FOUND)
        except ValidationError as e:
            return Response(data={'Error': str(e.args)}, status=e.status_code)


class GetSessionAPiView(APIView):

    def get(self, request, *args, **kwargs):
        try:
            stripe.api_key = os.environ.get('API_KEY')
            buy_item = Item.objects.get(id=kwargs.get('id'))
            final_price = int(buy_item.price * 100)
            session = stripe.checkout.Session.create(
                line_items=[
                    {
                        'price_data': {
                            'currency': 'usd',
                            'product_data': {
                                'name': buy_item.name,
                            },
                            'unit_amount': final_price,
                        },
                        'quantity': 1,
                    }],
                mode='payment',
                success_url='https://example.com/success',
                cancel_url='https://example.com/cancel',
            )

            return Response(data={'session_id': session.id}, status=status.HTTP_200_OK)
        except Item.DoesNotExist:
            return Response(data={'Error': 'Item not found'}, status=status.HTTP_404_NOT_FOUND)
        except stripe.error.StripeError as e:
            return Response(data={'Error': str(e)}, status=e.http_status)


class GetItemAPiView(APIView):

    renderer_classes = [TemplateHTMLRenderer]
    template_name = 'Item.html'

    def get(self, request, *args, **kwargs):
        try:
            item = Item.objects.get(id=kwargs.get('id'))
            context = {
                'item': item,
                'publishable_key': os.environ.get('PUBLISHABLE_KEY')
            }
            return Response(data=context, status=status.HTTP_200_OK)
        except Item.DoesNotExist:
            return Response(data={'Error': 'Item not found'}, status=status.HTTP_404_NOT_FOUND)


class CreateOrderView(APIView):
    serializer_class = OrderSerializer
    permission_classes = (IsAuthenticated,)

    @extend_schema(
        description='Create a new order',
        operation_id='create_order',
        responses={
            (201, 'application/json'): OpenApiResponse(response=OrderSerializer(many=True),
                                                       description='Created'),
            403: OpenApiResponse(description="Credentials weren't provided"),
            404: OpenApiResponse(description='Order does not exist'),
        }
    )
    def post(self, request):
        try:
            serializer = OrderSerializer(data=request.data, context={'user': request.user})
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(data={'New Order': serializer.data}, status=status.HTTP_201_CREATED)
        except ValidationError as e:
            return Response(data={'Error': str(e.args)}, status=e.status_code)
        except PermissionDenied:
            return Response(data={'Error': "Credentials weren't provided"}, status=status.HTTP_403_FORBIDDEN)


class GetAllOrdersApiView(APIView):
    serializer_class = OrderSerializer
    permission_classes = (IsAuthenticated,)

    @extend_schema(
        description='Get all orders',
        operation_id='get_all_orders',
        responses={
            (200, 'application/json'): OpenApiResponse(response=OrderSerializer(many=True),
                                                       description='Success'),
            403: OpenApiResponse(description="Credentials weren't provided"),
            404: OpenApiResponse(description='Order does not exist'),
        }
    )
    def get(self, request):
        try:
            orders = Order.objects.filter(user__id=request.user.id)
            if not orders:
                return Response(data={'Error': 'No orders found'}, status=status.HTTP_404_NOT_FOUND)
            serializer = OrderSerializer(orders, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Order.DoesNotExist as e:
            return Response(data={'Error': str(e)}, status=status.HTTP_404_NOT_FOUND)
        except PermissionDenied:
            return Response(data={'Error': "Credentials weren't provided"}, status=status.HTTP_403_FORBIDDEN)


class GetOrderView(APIView):
    serializer_class = OrderSerializer
    permission_classes = (IsAuthenticated,)

    @extend_schema(
        description='Get one order',
        operation_id='get_one_order',
        responses={
            (200, 'application/json'): OpenApiResponse(response=OrderSerializer(many=True),
                                                       description='Success'),
            400: OpenApiResponse(description='No id'),
            403: OpenApiResponse(description="Credentials weren't provided"),
            404: OpenApiResponse(description='Order does not exist'),
        }
    )
    def get(self, request, *args, **kwargs):
        try:
            order_id = kwargs.get('id')
            if not order_id:
                return Response(data={'Error': 'Order ID required'}, status=status.HTTP_400_BAD_REQUEST)
            order = get_object_or_404(Order, id=order_id, user__id=request.user.id)
            serializer = OrderSerializer(order)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Order.DoesNotExist as e:
            return Response(data={'Error': str(e)}, status=status.HTTP_404_NOT_FOUND)
        except ValidationError as e:
            return Response(data={'Error': str(e.args)}, status=e.status_code)
        except PermissionDenied:
            return Response(data={'Error': "Credentials weren't provided"}, status=status.HTTP_403_FORBIDDEN)


class UpdateOrderView(APIView):
    serializer_class = OrderSerializer
    permission_classes = (IsAuthenticated,)

    @extend_schema(
        description='Update order',
        operation_id='update_order',
        responses={
            (200, 'application/json'): OpenApiResponse(response=OrderSerializer,
                                                       description='Success'),
            400: OpenApiResponse(description='No id'),
            403: OpenApiResponse(description="Credentials weren't provided"),
            404: OpenApiResponse(description='Order does not exist'),
        }
    )
    def put(self, request, *args, **kwargs):
        try:
            order_id = kwargs.get('id')
            if not order_id:
                return Response(data={'Error': 'Order ID required'}, status=status.HTTP_400_BAD_REQUEST)
            order = get_object_or_404(Order, id=order_id, user__id=request.user.id)
            serializer = OrderSerializer(data=request.data, instance=order)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Order.DoesNotExist as e:
            return Response(data={'Error': str(e)}, status=status.HTTP_404_NOT_FOUND)
        except ValidationError as e:
            return Response(data={'Error': str(e.args)}, status=e.status_code)
        except PermissionDenied:
            return Response(data={'Error': "Credentials weren't provided"}, status=status.HTTP_403_FORBIDDEN)


class DeleteOrderView(APIView):
    serializer_class = OrderSerializer
    permission_classes = (IsAuthenticated,)

    @extend_schema(
        description='Delete a order',
        operation_id='delete_order',
        responses={
            (204, 'application/json'): OpenApiResponse(response=OrderSerializer,
                                                       description='Created'),
            400: OpenApiResponse(description='No id'),
            403: OpenApiResponse(description="Credentials weren't provided"),
            404: OpenApiResponse(description='Order does not exist'),
        }
    )
    def delete(self, request, *args, **kwargs):
        try:
            order_id = kwargs.get('id')
            if not order_id:
                return Response(data={'Error': 'Order ID required'}, status=status.HTTP_400_BAD_REQUEST)
            order = get_object_or_404(Order, id=order_id, user__id=request.user.id)
            order.delete()
            return Response(data={'Message': 'Successfully deleted order'}, status=status.HTTP_204_NO_CONTENT)
        except Order.DoesNotExist as e:
            return Response(data={'Error': str(e)}, status=status.HTTP_404_NOT_FOUND)
        except ValidationError as e:
            return Response(data={'Error': str(e.args)}, status=e.status_code)
        except PermissionDenied:
            return Response(data={'Error': "Credentials weren't provided"}, status=status.HTTP_403_FORBIDDEN)
