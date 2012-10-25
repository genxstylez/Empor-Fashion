# -*-coding: utf-8 -*-
from django.conf import settings
from django.template.loader import render_to_string
from order.models import OrderItem
from xhtml2pdf import pisa
import cStringIO as StringIO

def generate_order_pdf(request, order):
    """
    產生ORDER PDF
    """
    items = OrderItem.objects.filter(order=order)
    html = render_to_string('order/email-pdf.html', {
            'order': order,
            'items': items,
            'host': request.get_host(),
            'STATIC_URL': settings.STATIC_URL
    })
    result = StringIO.StringIO()
    pdf = pisa.pisaDocument(StringIO.StringIO(html.encode("utf8")), result, encoding='utf8')

    if pdf.err:
        pass

    return result.getvalue()
