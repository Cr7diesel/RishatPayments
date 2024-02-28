import os
import stripe

from dotenv import load_dotenv
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.renderers import TemplateHTMLRenderer
from rest_framework.views import APIView
from rest_framework.response import Response

from api.models import Item


load_dotenv()
stripe.api_key = os.environ.get('API_KEY')


class GetSessionAPiView(APIView):

    def get(self, request, *args, **kwargs):
        try:
            buy_item = Item.objects.get(id=kwargs.get('id'))
            session = stripe.checkout.Session.create(
                line_items=[
                    {
                        'price_data': {
                            'currency': 'usd',
                            'product_data': {
                                'name': buy_item.name,
                            },
                            'unit_amount': int(buy_item.price),
                        },
                        'quantity': 1,
                    }],
                mode='payment',
                success_url='http://localhost:4242/success',
                cancel_url='http://localhost:4242/cancel',
            )

            return Response(data={'session_id': session.id}, status=status.HTTP_200_OK)
        except Item.DoesNotExist:
            return Response(data={'Error': 'Item not found'}, status=status.HTTP_404_NOT_FOUND)
        except stripe.error.StripeError as e:
            return Response(data={'Error': str(e)}, status=e.http_status)


class GetItemAPiView(APIView):

    renderer_classes = [TemplateHTMLRenderer]
    template_name = 'item.html'

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



