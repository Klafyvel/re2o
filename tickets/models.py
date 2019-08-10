from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.core.mail import send_mail
from django.template import Context, loader
from django.db.models.signals import post_save
from django.dispatch import receiver

import users.models

class Ticket(models.Model):
    """Class définissant un ticket"""

    user = models.ForeignKey(
        'users.User', 
        on_delete=models.CASCADE,
        related_name="tickets",
        blank=True,
        null=True)
    title = models.CharField(
        max_length=255,
        help_text=_("Nom du ticket"),
        blank=False,
        null=False,)
    description = models.TextField(
        max_length=3000,
        help_text=_("Description du ticket"),
        blank=False,
        null=False)
    date = models.DateTimeField(auto_now_add=True)
    email = models.EmailField(
        help_text = _("Une adresse mail pour vous recontacter"),
        max_length=100, 
        null=True)
    assigned_staff = models.ForeignKey(
        'users.User',
        on_delete=models.PROTECT,
        related_name="tickets_assigned",
        blank=True,
        null=True)
    #categories = models.OneToManyFiled('Category')
    solved = models.BooleanField(default=False)

    class Meta:
        verbose_name = _("Ticket")
        verbose_name_plural = _("Tickets")

    def __str__(self):
        return "Ticket de {} date: {}".format(self.user.surname,self.date)

    def publish_mail(self):
        to_addr = Preferences.objects.first().publish_address
        template = loader.get_template('tickets/publication_mail')
        context = Context({'ticket':self})
        send_mail(
            'Nouvelle ouverture de ticket',
            template.render(context),
            'grisel-davy@crans.org',
            [to_addr],
            fail_silently = False)

class Preferences(models.Model):
    """ Class cannonique définissants les préférences des tickets """
    
    publish_address = models.EmailField(
        help_text = _("Adresse mail pour annoncer les nouveau tickets (laisser vide pour ne rien annoncer)"),
        max_length = 1000,
        null = True)
    class Meta:
        verbose_name = _("Préférences des tickets")


@receiver(post_save, sender=Ticket)
def ticket_post_save(**kwargs):
    """Envoit du mail de publication du ticket"""
    if Preferences.objects.first().publish_address:
        ticket = kwargs['instance']
        ticket.publish_mail()
