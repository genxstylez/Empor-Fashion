from django.utils.translation import ugettext_lazy as _

ORDER_STATUS_CHOICES = [
    (0, _('Pending for payment')),
    (1, _('Paid / Dispatching')),
    (2, _('Deferred / Expired')),
    (3, _('Completed'))
]

PAYMENT_METHOD_CHOICES = [
    (0, _('PayPal')),
    (1, _('COD')),
]
