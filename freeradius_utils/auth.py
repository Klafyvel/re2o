# ⁻*- mode: python; coding: utf-8 -*-
# Re2o est un logiciel d'administration développé initiallement au rezometz. Il
# se veut agnostique au réseau considéré, de manière à être installable en
# quelques clics.
#
# Copyirght © 2017  Daniel Stan 
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
Backend python pour freeradius.

Ce fichier contient la définition de plusieurs fonctions d'interface à
freeradius qui peuvent être appelées (suivant les configurations) à certains
moment de l'authentification, en WiFi, filaire, ou par les NAS eux-mêmes.

Inspirés d'autres exemples trouvés ici :
https://github.com/FreeRADIUS/freeradius-server/blob/master/src/modules/rlm_python/

Inspiré du travail de Daniel Stan au Crans
"""

import logging
import netaddr
import radiusd # Module magique freeradius (radiusd.py is dummy)
import binascii
import hashlib
import os, sys


proj_path = "/var/www/re2o/"
# This is so Django knows where to find stuff.
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "re2o.settings")
sys.path.append(proj_path)

# This is so my local_settings.py gets loaded.
os.chdir(proj_path)

# This is so models get loaded.
from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()

import argparse

from django.db.models import Q
from machines.models import Interface, IpList, Nas, Domain
from topologie.models import Room, Port, Switch
from users.models import User
from preferences.models import OptionalTopologie

options, created = OptionalTopologie.objects.get_or_create()
VLAN_NOK = options.vlan_decision_nok.vlan_id
VLAN_OK = options.vlan_decision_ok.vlan_id


#: Serveur radius de test (pas la prod)
TEST_SERVER = bool(os.getenv('DBG_FREERADIUS', False))


## -*- Logging -*-

class RadiusdHandler(logging.Handler):
    """Handler de logs pour freeradius"""

    def emit(self, record):
        """Process un message de log, en convertissant les niveaux"""
        if record.levelno >= logging.WARN:
            rad_sig = radiusd.L_ERR
        elif record.levelno >= logging.INFO:
            rad_sig = radiusd.L_INFO
        else:
            rad_sig = radiusd.L_DBG
        radiusd.radlog(rad_sig, record.msg)

# Initialisation d'un logger (pour logguer unifié)
logger = logging.getLogger('auth.py')
logger.setLevel(logging.DEBUG)
formatter = logging.Formatter('%(name)s: [%(levelname)s] %(message)s')
handler = RadiusdHandler()
handler.setFormatter(formatter)
logger.addHandler(handler)

def radius_event(fun):
    """Décorateur pour les fonctions d'interfaces avec radius.
    Une telle fonction prend un uniquement argument, qui est une liste de tuples
    (clé, valeur) et renvoie un triplet dont les composantes sont :
     * le code de retour (voir radiusd.RLM_MODULE_* )
     * un tuple de couples (clé, valeur) pour les valeurs de réponse (accès ok
       et autres trucs du genre)
     * un tuple de couples (clé, valeur) pour les valeurs internes à mettre à
       jour (mot de passe par exemple)

    On se contente avec ce décorateur (pour l'instant) de convertir la liste de
    tuples en entrée en un dictionnaire."""

    def new_f(auth_data):
        if type(auth_data) == dict:
            data = auth_data
        else:
            data = dict()
            for (key, value) in auth_data or []:
                # Beware: les valeurs scalaires sont entre guillemets
                # Ex: Calling-Station-Id: "une_adresse_mac"
                data[key] = value.replace('"', '')
        try:
            # TODO s'assurer ici que les tuples renvoyés sont bien des (str,str)
            # rlm_python ne digère PAS les unicodes
            return fun(data)
        except Exception as err:
            logger.error('Failed %r on data %r' % (err, auth_data))
            raise

    return new_f

   

@radius_event
def instantiate(*_):
    """Utile pour initialiser les connexions ldap une première fois (otherwise,
    do nothing)"""
    logger.info('Instantiation')
    if TEST_SERVER:
        logger.info(u'DBG_FREERADIUS is enabled')

@radius_event
def authorize(data):
    # Pour les requetes proxifiees, on split
    nas = data.get('NAS-IP-Address', data.get('NAS-Identifier', None))
    nas_instance = find_nas_from_request(nas)
    # Toutes les reuquètes non proxifiées
    if nas != '127.0.0.1':
        if not nas_instance:
            logger.info(u"Nas inconnu")
            return radiusd.RLM_MODULE_REJECT
        nas_type = Nas.objects.filter(nas_type=nas_instance.type).first()
        if not nas_type:
            logger.info(u"Type de nas non enregistré dans la bdd!".encode('utf-8'))
            return radiusd.RLM_MODULE_REJECT
    else:
        nas_type = None
    if not nas_type or nas_type.port_access_mode == '802.1X':
        user = data.get('User-Name', '')
        user = user.split('@', 1)[0]
        mac = data.get('Calling-Station-Id', '')
        result, log, password = check_user_machine_and_register(nas_type, user, mac) 
        logger.info(log.encode('utf-8'))
        
        if not result:
            return radiusd.RLM_MODULE_REJECT
        else:
            return (radiusd.RLM_MODULE_UPDATED,
            (),
            (
            (str("NT-Password"), str(password)),
            ),
            )

    else:
        return (radiusd.RLM_MODULE_UPDATED,
	(),
        (
          ("Auth-Type", "Accept"),
        ),
        )

@radius_event
def post_auth(data):
    nas = data.get('NAS-IP-Address', data.get('NAS-Identifier', None))
    nas_instance = find_nas_from_request(nas)
    # Toutes les reuquètes non proxifiées
    if nas == '127.0.0.1':
        logger.info(u"Requète proxifiée".encode('utf-8'))
        return radiusd.RLM_MODULE_OK
    nas_type = Nas.objects.filter(nas_type=nas_instance.type).first()
    if not nas_type:
        logger.info(u"Type de nas non enregistré dans la bdd!".encode('utf-8'))
        return radiusd.RLM_MODULE_OK
    
    mac = data.get('Calling-Station-Id', None)
    
    # Si il s'agit d'un switch
    if hasattr(nas_instance, 'switch'):
        port = data.get('NAS-Port-Id', data.get('NAS-Port', None))
        # Hack, à cause d'une numérotation cisco baroque
        port = port.split(".")[0].split('/')[-1][-2:]
        out = decide_vlan_and_register_switch(nas_instance, nas_type, port, mac)
        sw_name, reason, vlan_id = out

        log_message = '(fil) %s -> %s [%s%s]' % \
          (sw_name + u":" + port, mac, vlan_id, (reason and u': ' + reason).encode('utf-8'))
        logger.info(log_message)

        # Filaire
        return (radiusd.RLM_MODULE_UPDATED,
            (
                ("Tunnel-Type", "VLAN"),
                ("Tunnel-Medium-Type", "IEEE-802"),
                ("Tunnel-Private-Group-Id", '%d' % int(vlan_id)),
            ),
            ()
            )

    else:
        return radiusd.RLM_MODULE_OK

@radius_event
def dummy_fun(_):
    """Do nothing, successfully. (C'est pour avoir un truc à mettre)"""
    return radiusd.RLM_MODULE_OK

def detach(_=None):
    """Appelé lors du déchargement du module (enfin, normalement)"""
    print "*** goodbye from auth.py ***"
    return radiusd.RLM_MODULE_OK

def find_nas_from_request(nas_id):
    nas = Interface.objects.filter(Q(domain=Domain.objects.filter(name=nas_id)) | Q(ipv4=IpList.objects.filter(ipv4=nas_id)))
    return nas.first()

def check_user_machine_and_register(nas_type, username, mac_address):
    """ Verifie le username et la mac renseignee. L'enregistre si elle est inconnue.
    Renvoie le mot de passe ntlm de l'user si tout est ok
    Utilise pour les authentifications en 802.1X"""
    interface = Interface.objects.filter(mac_address=mac_address).first()
    user = User.objects.filter(pseudo=username).first()
    if not user:
        return (False, u"User inconnu", '')
    if not user.has_access():
        return (False, u"Adhérent non cotisant", '')
    if interface:
        if interface.machine.user != user:
            return (False, u"Machine enregistrée sur le compte d'un autre user...", '')
        elif not interface.is_active:
            return (False, u"Machine desactivée", '')
        else:
            return (True, u"Access ok", user.pwd_ntlm)
    elif nas_type:
        if nas_type.autocapture_mac:
            result, reason = user.autoregister_machine(mac_address, nas_type)
            if result:
                return (True, u'Access Ok, Capture de la mac...', user.pwd_ntlm)
            else:
                return (False, u'Erreur dans le register mac %s' % reason, '')        
        else:
            return (False, u'Machine inconnue', '')
    else:
        return (False, u"Machine inconnue", '')


def decide_vlan_and_register_switch(nas, nas_type, port_number, mac_address):
    # Get port from switch and port number
    extra_log = ""
    if not nas:
        return ('?', u'Nas inconnu', VLAN_OK)

    sw_name = str(nas)

    port = Port.objects.filter(switch=Switch.objects.filter(switch_interface=nas), port=port_number)
    if not port:
        return (sw_name, u'Port inconnu', VLAN_OK)

    port = port.first()
    # Si un vlan a été précisé, on l'utilise pour VLAN_OK
    if port.vlan_force:
        DECISION_VLAN = int(port.vlan_force.vlan_id)
        extra_log = u"Force sur vlan " + str(DECISION_VLAN)
    else:
        DECISION_VLAN = VLAN_OK

    if port.radius == 'NO':
        return (sw_name, u"Pas d'authentification sur ce port" + extra_log, DECISION_VLAN)

    if port.radius == 'BLOQ':
        return (sw_name, u'Port desactive', VLAN_NOK)

    if port.radius == 'STRICT':
        if not port.room:
            return (sw_name, u'Chambre inconnue', VLAN_NOK)

        room_user = User.objects.filter(room=port.room)
        if not room_user:
            return (sw_name, u'Chambre non cotisante', VLAN_NOK)
        elif not room_user.first().has_access():
            return (sw_name, u'Chambre resident desactive', VLAN_NOK)
        # else: user OK, on passe à la verif MAC

    if port.radius == 'COMMON' or port.radius == 'STRICT':
        # Authentification par mac
        interface = Interface.objects.filter(mac_address=mac_address)
        if not interface:
            # On essaye de register la mac
            if not nas_type.autocapture_mac:
                return (sw_name, u'Machine inconnue', VLAN_NOK)
            elif not port.room:
                return (sw_name, u'Chambre et machine inconnues', VLAN_NOK)
            else:
                room_user = User.objects.filter(room=Room.objects.filter(name=port.room))
                if not room_user:
                    return (sw_name, u'Machine et propriétaire de la chambre inconnus', VLAN_NOK)
                elif not room_user.first().has_access():
                    return (sw_name, u'Machine inconnue et adhérent non cotisant', VLAN_NOK)
                else:
                    result, reason = room_user.first().autoregister_machine(mac_address, nas_type)
                    if result:
                        return (sw_name, u'Access Ok, Capture de la mac...' + extra_log, DECISION_VLAN)
                    else:
                        return (sw_name, u'Erreur dans le register mac %s' % reason + unicode(mac_address), VLAN_NOK) 
        elif not interface.first().is_active:
            return (sw_name, u'Machine non active / adherent non cotisant', VLAN_NOK)
        else:
            return (sw_name, u'Machine OK' + extra_log, DECISION_VLAN)


