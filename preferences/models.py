# -*- mode: python; coding: utf-8 -*-
# Re2o un logiciel d'administration développé initiallement au rezometz. Il
# se veut agnostique au réseau considéré, de manière à être installable en
# quelques clics.
#
# Copyright © 2017  Gabriel Détraz
# Copyright © 2017  Goulven Kermarec
# Copyright © 2017  Augustin Lemesle
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License along
# with this program; if not, write to the Free Software Foundation, Inc.,
# 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301 USA.
"""
Reglages généraux, machines, utilisateurs, mail, general pour l'application.
"""
from __future__ import unicode_literals

from django.utils.functional import cached_property
from django.utils import timezone
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.cache import cache

from django.forms import ValidationError
import cotisations.models
import machines.models

from re2o.mixins import AclMixin
from re2o.aes_field import AESEncryptedField
from datetime import timedelta


class PreferencesModel(models.Model):
    """ Base object for the Preferences objects
    Defines methods to handle the cache of the settings (they should
    not change a lot) """
    @classmethod
    def set_in_cache(cls):
        """ Save the preferences in a server-side cache """
        instance, _created = cls.objects.get_or_create()
        cache.set(cls().__class__.__name__.lower(), instance, None)
        return instance

    @classmethod
    def get_cached_value(cls, key):
        """ Get the preferences from the server-side cache """
        instance = cache.get(cls().__class__.__name__.lower())
        if instance is None:
            instance = cls.set_in_cache()
        return getattr(instance, key)

    class Meta:
        abstract = True


class OptionalUser(AclMixin, PreferencesModel):
    """Options pour l'user : obligation ou nom du telephone,
    activation ou non du solde, autorisation du negatif, fingerprint etc"""
    PRETTY_NAME = "Options utilisateur"

    is_tel_mandatory = models.BooleanField(default=True)
    gpg_fingerprint = models.BooleanField(default=True)
    all_can_create_club = models.BooleanField(
        default=False,
        help_text="Les users peuvent créer un club"
    )
    all_can_create_adherent = models.BooleanField(
        default=False,
        help_text="Les users peuvent créer d'autres adhérents",
    )
    self_adhesion = models.BooleanField(
        default=False,
        help_text="Un nouvel utilisateur peut se créer son compte sur re2o"
    )
    shell_default = models.OneToOneField(
        'users.ListShell',
        on_delete=models.PROTECT,
        blank=True,
        null=True,
        help_text="Shell par default"
    )
    mail_accounts = models.BooleanField(
        default=False,
        help_text="Activation des comptes mails pour les utilisateurs"
    )
    mail_extension = models.CharField(
        max_length = 32,
        default = "@example.org",
        help_text="Extension principale pour les mails internes",
    )
    max_mail_alias = models.IntegerField(
        default = 15,
        help_text = "Nombre maximal d'alias pour un utilisateur lambda"
    )

    class Meta:
        permissions = (
            ("view_optionaluser", "Peut voir les options de l'user"),
        )

    def clean(self):
        """Clean du model:
        Creation du mode de paiement par solde
        Vérifie que l'extension mail commence bien par @
        """
        if self.user_solde:
            cotisations.models.Paiement.objects.get_or_create(is_balance=True)
        if self.mail_extension[0] != "@":
            raise ValidationError("L'extension mail doit commencer par un @")


@receiver(post_save, sender=OptionalUser)
def optionaluser_post_save(**kwargs):
    """Ecriture dans le cache"""
    user_pref = kwargs['instance']
    user_pref.set_in_cache()


class OptionalMachine(AclMixin, PreferencesModel):
    """Options pour les machines : maximum de machines ou d'alias par user
    sans droit, activation de l'ipv6"""
    PRETTY_NAME = "Options machines"

    SLAAC = 'SLAAC'
    DHCPV6 = 'DHCPV6'
    DISABLED = 'DISABLED'
    CHOICE_IPV6 = (
        (SLAAC, 'Autoconfiguration par RA'),
        (DHCPV6, 'Attribution des ip par dhcpv6'),
        (DISABLED, 'Désactivé'),
    )

    password_machine = models.BooleanField(
        default=False,
        help_text="Un mot de passe par machine activé")
    max_lambdauser_interfaces = models.IntegerField(
        default=10,
        help_text="Maximum d'interface pour un user sans droits")
    max_lambdauser_aliases = models.IntegerField(
        default=10,
        help_text="Maximum de cname pour un user sans droits")
    ipv6_mode = models.CharField(
        max_length=32,
        choices=CHOICE_IPV6,
        default='DISABLED',
        help_text="Mode ipv6"
    )
    create_machine = models.BooleanField(
        default=True,
        help_text="Permet à l'user de créer une machine"
    )

    @cached_property
    def ipv6(self):
        """ Check if the IPv6 option is activated """
        return not self.get_cached_value('ipv6_mode') == 'DISABLED'

    class Meta:
        permissions = (
            ("view_optionalmachine", "Peut voir les options de machine"),
        )


@receiver(post_save, sender=OptionalMachine)
def optionalmachine_post_save(**kwargs):
    """Synchronisation ipv6 et ecriture dans le cache"""
    machine_pref = kwargs['instance']
    machine_pref.set_in_cache()
    if machine_pref.ipv6_mode != "DISABLED":
        for interface in machines.models.Interface.objects.all():
            interface.sync_ipv6()


class OptionalTopologie(AclMixin, PreferencesModel):
    """Reglages pour la topologie : mode d'accès radius, vlan où placer
    les machines en accept ou reject"""
    PRETTY_NAME = "Options topologie"
    MACHINE = 'MACHINE'
    DEFINED = 'DEFINED'
    CHOICE_RADIUS = (
        (MACHINE, 'Sur le vlan de la plage ip machine'),
        (DEFINED, 'Prédéfini dans "Vlan où placer les machines\
            après acceptation RADIUS"'),
    )

    radius_general_policy = models.CharField(
        max_length=32,
        choices=CHOICE_RADIUS,
        default='DEFINED',
        help_text="Politique par defaut de placement de vlan avec radius"
    )
    vlan_decision_ok = models.OneToOneField(
        'machines.Vlan',
        on_delete=models.PROTECT,
        related_name='decision_ok',
        blank=True,
        null=True,
        help_text="Placement sur ce vlan par default en cas d'accès OK"
    )
    vlan_decision_nok = models.OneToOneField(
        'machines.Vlan',
        on_delete=models.PROTECT,
        related_name='decision_nok',
        blank=True,
        null=True,
        help_text="Placement par defaut sur ce vlan en cas de rejet"
    )
    switchs_web_management = models.BooleanField(
        default=False,
        help_text="Web management, activé si provision automatique"
    )
    switchs_web_management_ssl = models.BooleanField(
        default=False,
        help_text="Web management ssl. Assurez-vous que un certif est installé sur le switch !"
    )   
    switchs_rest_management = models.BooleanField(
        default=False,
        help_text="Rest management, activé si provision auto"
    )
    switchs_ip_type = models.OneToOneField(
        'machines.IpType',
        on_delete=models.PROTECT,
        blank=True,
        null=True,
        help_text="Plage d'ip de management des switchs"
    )

    @cached_property
    def provisioned_switchs(self):
        """Liste des switches provisionnés"""
        from topologie.models import Switch
        return Switch.objects.filter(automatic_provision=True)

    @cached_property
    def provision_switchs_enabled(self):
        """Return true if all settings are ok : switchs on automatic provision,
        ip_type"""
        return bool(self.provisioned_switchs and self.switchs_ip_type)

    class Meta:
        permissions = (
            ("view_optionaltopologie", "Peut voir les options de topologie"),
        )


@receiver(post_save, sender=OptionalTopologie)
def optionaltopologie_post_save(**kwargs):
    """Ecriture dans le cache"""
    topologie_pref = kwargs['instance']
    topologie_pref.set_in_cache()


class RadiusKey(AclMixin, models.Model):
    """Class of a radius key"""
    radius_key = AESEncryptedField(
        max_length=255,
        help_text="Clef radius"
    )
    comment = models.CharField(
        max_length=255,
        null=True,
        blank=True,
        help_text="Commentaire de cette clef"
    )
    default_switch = models.BooleanField(
        default=True,
        unique=True,
        help_text= "Clef par défaut des switchs"
    )

    class Meta:
        permissions = (
            ("view_radiuskey", "Peut voir un objet radiuskey"),
        )


class Reminder(AclMixin, models.Model):
    """Options pour les mails de notification de fin d'adhésion.
    Days: liste des nombres de jours pour lesquells un mail est envoyé
    optionalMessage: message additionel pour le mail
    """
    PRETTY_NAME="Options pour le mail de fin d'adhésion"

    days = models.IntegerField(
        default=7,
        unique=True,
        help_text="Délais entre le mail et la fin d'adhésion"
    )
    message = models.CharField(
        max_length=255,
        default="",
        null=True,
        blank=True,
        help_text="Message affiché spécifiquement pour ce rappel"
    )

    class Meta:
        permissions = (
            ("view_reminder", "Peut voir un objet reminder"),
        )

    def users_to_remind(self):
        from re2o.utils import all_has_access
        date = timezone.now().replace(minute=0,hour=0)
        futur_date = date + timedelta(days=self.days)
        users = all_has_access(futur_date).exclude(pk__in = all_has_access(futur_date + timedelta(days=1))) 
        return users


class GeneralOption(AclMixin, PreferencesModel):
    """Options générales : nombre de resultats par page, nom du site,
    temps où les liens sont valides"""
    PRETTY_NAME = "Options générales"

    general_message = models.TextField(
        default="",
        blank=True,
        help_text="Message général affiché sur le site (maintenance, etc)"
    )
    search_display_page = models.IntegerField(
        default=15,
        help_text="Nombre de résultats affichés dans une recherche"
    )
    pagination_number = models.IntegerField(
        default=25,
        help_text="Nombre d'item par page paginée"
    )
    pagination_large_number = models.IntegerField(
        default=8,
        help_text="Nombre d'item par page paginée, items larges"
    )
    req_expire_hrs = models.IntegerField(
        default=48,
        help_text="Delais d'expiration des token changement de mdp, en heure"
    )
    site_name = models.CharField(
        max_length=32,
        default="Re2o",
        help_text="Nom du site web, par defaut re2o"
    )
    site_url = models.CharField(
        max_length=32,
        default="re2o.example.org",
        help_text="url par défaut du site. par défaut: re2o.example.org"
    )
    email_from = models.EmailField(
        default="www-data@example.com",
        help_text="From des mails envoyés par re2o"
    )
    GTU_sum_up = models.TextField(
        default="",
        blank=True,
        help_text="Résumé des CGU à l'inscription"
    )
    GTU = models.FileField(
        upload_to='',
        default="",
        null=True,
        blank=True,
        help_text="CGU et documents réglementaires à l'inscription"
    )

    class Meta:
        permissions = (
            ("view_generaloption", "Peut voir les options générales"),
        )


@receiver(post_save, sender=GeneralOption)
def generaloption_post_save(**kwargs):
    """Ecriture dans le cache"""
    general_pref = kwargs['instance']
    general_pref.set_in_cache()


class Service(AclMixin, models.Model):
    """Liste des services affichés sur la page d'accueil : url, description,
    image et nom"""
    name = models.CharField(max_length=32)
    url = models.URLField()
    description = models.TextField()
    image = models.ImageField(upload_to='logo', blank=True)

    class Meta:
        permissions = (
            ("view_service", "Peut voir les options de service"),
        )

    def __str__(self):
        return str(self.name)

class MailContact(AclMixin, models.Model):
    """Addresse mail de contact associée à un commentaire descriptif"""

    address = models.EmailField(
        default = "contact@example.org",
        help_text = "Adresse mail de contact"
    )

    commentary = models.CharField(
        blank = True,
        null = True,
        help_text = "Description de l'utilisation de l'adresse mail associée",
        max_length = 256
    )

    @cached_property
    def get_name(self):
        return self.address.split("@")[0]

    class Meta:
        permissions = (
            ("view_mailcontact", "Peut voir les mails de contact"),
        )

    def __str__(self):
        return(self.address)


class AssoOption(AclMixin, PreferencesModel):
    """Options générales de l'asso : siret, addresse, nom, etc"""
    PRETTY_NAME = "Options de l'association"

    name = models.CharField(
        default="Association réseau école machin",
        max_length=256,
        help_text="Nom complet de l'asso"
    )
    siret = models.CharField(
        default="00000000000000",
        max_length=32,
        help_text="Numero SIRET"
    )
    adresse1 = models.CharField(
        default="1 Rue de exemple",
        max_length=128,
        help_text="Adresse"
    )
    adresse2 = models.CharField(
        default="94230 Cachan",
        max_length=128
    )
    contact = models.EmailField(
        default="contact@example.org",
        help_text="Mail de contact"
    )
    telephone = models.CharField(
        max_length=15,
        default="0000000000",
        help_text="Téléphone de contact"
    )
    pseudo = models.CharField(
        default="Asso",
        max_length=32,
        help_text="Pseudo de l'asso"
    )
    utilisateur_asso = models.OneToOneField(
        'users.User',
        on_delete=models.PROTECT,
        blank=True,
        null=True,
        help_text="Utilisateur dans la db correspondant à l'asso"
    )
    description = models.TextField(
        null=True,
        blank=True,
        help_text="Description de l'asso"
    )

    class Meta:
        permissions = (
            ("view_assooption", "Peut voir les options de l'asso"),
        )


@receiver(post_save, sender=AssoOption)
def assooption_post_save(**kwargs):
    """Ecriture dans le cache"""
    asso_pref = kwargs['instance']
    asso_pref.set_in_cache()


class HomeOption(AclMixin, PreferencesModel):
    """Settings of the home page (facebook/twitter etc)"""
    PRETTY_NAME = "Options de la page d'accueil"

    facebook_url = models.URLField(
        null=True,
        blank=True,
        help_text="Url du compte facebook"
    )
    twitter_url = models.URLField(
        null=True,
        blank=True,
        help_text="Url du compte twitter"
    )
    twitter_account_name = models.CharField(
        max_length=32,
        null=True,
        blank=True,
        help_text="Nom du compte à afficher"
    )

    class Meta:
        permissions = (
            ("view_homeoption", "Peut voir les options de l'accueil"),
        )


@receiver(post_save, sender=HomeOption)
def homeoption_post_save(**kwargs):
    """Ecriture dans le cache"""
    home_pref = kwargs['instance']
    home_pref.set_in_cache()


class MailMessageOption(AclMixin, models.Model):
    """Reglages, mail de bienvenue et autre"""
    PRETTY_NAME = "Options de corps de mail"

    welcome_mail_fr = models.TextField(default="", help_text="Mail de bienvenue en français")
    welcome_mail_en = models.TextField(default="", help_text="Mail de bienvenue en anglais")

    class Meta:
        permissions = (
            ("view_mailmessageoption", "Peut voir les options de mail"),
        )
