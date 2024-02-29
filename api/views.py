import os
import stripe

from dotenv import load_dotenv
from rest_framework import status
from rest_framework.exceptions import ValidationError
from rest_framework.permissions import IsAuthenticated
from rest_framework.renderers import TemplateHTMLRenderer
from rest_framework.views import APIView
from rest_framework.response import Response

from api.models import Item
from api.serializers import ItemSerializer

load_dotenv()


class CreateItemView(APIView):

    def post(self, request):
        try:
            serializer = ItemSerializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(data={'New Item': serializer.data}, status=status.HTTP_201_CREATED)
        except ValidationError as e:
            return Response(data={'Error': str(e.args)}, status=e.status_code)


class GetAllItemView(APIView):

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

    def get(self, request, *args, **kwargs):
        try:
            item_id = kwargs.get('item_id')
            if not item_id:
                return Response(data={'Error': 'Item ID required'}, status=status.HTTP_400_BAD_REQUEST)
            item = Item.objects.get(id=item_id)
            if not item:
                return Response(data={'Error': 'item not found'}, status=status.HTTP_404_NOT_FOUND)
            serializer = ItemSerializer(item)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Item.DoesNotExist as e:
            return Response(data={'Error': str(e)}, status=status.HTTP_404_NOT_FOUND)
        except ValidationError as e:
            return Response(data={'Error': str(e.args)}, status=e.status_code)


class UpdateItemView(APIView):

    def put(self, request, *args, **kwargs):
        try:
            item_id = kwargs.get('item_id')
            if not item_id:
                return Response(data={'Error': 'Item ID required'}, status=status.HTTP_400_BAD_REQUEST)
            item = Item.objects.get(id=item_id)
            if not item:
                return Response(data={'Error': 'item not found'}, status=status.HTTP_404_NOT_FOUND)
            serializer = ItemSerializer(data=request.data, instance=item)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Item.DoesNotExist as e:
            return Response(data={'Error': str(e)}, status=status.HTTP_404_NOT_FOUND)
        except ValidationError as e:
            return Response(data={'Error': str(e.args)}, status=e.status_code)


class DeleteItemView(APIView):

    def delete(self, request, *args, **kwargs):
        item_id = kwargs.get('item_id')
        if not item_id:
            return Response(data={'Error': 'Item ID required'}, status=status.HTTP_400_BAD_REQUEST)
        item = Item.objects.get(id=item_id)
        if not item:
            return Response(data={'Error': 'item not found'}, status=status.HTTP_404_NOT_FOUND)
        item.delete()
        return Response(data={'Message': 'Successfully deleted item'}, status=status.HTTP_204_NO_CONTENT)


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
