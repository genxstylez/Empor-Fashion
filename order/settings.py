from django.utils.translation import ugettext_lazy as _

ORDER_STATUS_CHOICES = (
    (0, _('Pending for payment')),
    (1, _('Paid / Ready for dispatching')),
    (2, _('Deferred / Expired')),
    (3, _('Completed')),
)

PAYMENT_METHOD_CHOICES = (
    (0, _('PayPal')),
    (1, _('COD')),
    (2, _('Card on Delivery')),
)

RECIEPT_TYPE_CHOICES = (
    (0, _('Donate')),
    (1, _('Three way reciept')),
)

DISPATCH_TIME_CHOICES = (
    (0, _('Unspecified')),
    (1, _('Before noon')),
    (2, _('12 to 17')),
    (3, _('17 to 20')),
    (4, _('20 to 21')),
)
