from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from six import text_type
import threading


class AppTokenGenerator(PasswordResetTokenGenerator):
    def _make_hash_value(self, new_user, timestamp):
        return (text_type(new_user.is_email_verified)+text_type(new_user.pk)+text_type(timestamp))


token_generator = AppTokenGenerator()


class EmailThread(threading.Thread):
    ###################### send email faster #####################
    def __init__(self, email_message):
        self.email_message = email_message
        threading.Thread.__init__(self)

    def run(self):
        self.email_message.send()


def sendMessage(subject, path, messages, sender, recipient):
    email_subject = subject
    message = render_to_string(path, messages)
    text_content = strip_tags(message)
    email_message = EmailMultiAlternatives(
        email_subject,
        text_content,
        sender,
        recipient,  # email a qui on envoie le message
    )
    email_message.attach_alternative(message, "text/html")
    # email_message.send(fail_silently=False)
    EmailThread(email_message).start()


def getTotalPrice(table, request):
    bigTotal = 0
    order = table.objects.filter(
        user_id=request.user.id, complete=False)
    if order:
        allItems = order[0].items.all().order_by('date_added')
        for item in allItems:
            bigTotal += float(item.total)
        return bigTotal
    else:
        return bigTotal


def removekey(d, key):
    r = dict(d)
    del r[key]
    return r


def checkPaymentMethod(instance, mtnMoney, orangeMoney):
    if instance == 'Rammassage':
        return "Veuillez passez dans l'un de nos magasin afin d'entrer en possession de votre article"
    elif instance == 'Paypal':
        return "Veuillez suivre le lien suivant pour finaliser votre payement via PayPal"
    elif instance == 'Mobile Money':
        return f"Veuillez effectuer votre payement mobile money sur l'un de ses numéros : {mtnMoney}, {orangeMoney}"
    else:
        return "Notre assistance vous appelera afin de s'accorder sur la méthode de payement"
