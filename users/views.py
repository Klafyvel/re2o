# Re2o est un logiciel d'administration développé initiallement au rezometz. Il
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

# App de gestion des users pour re2o
# Goulven Kermarec, Gabriel Détraz, Lemesle Augustin
# Gplv2
"""
Module des views.

On définit les vues pour l'ajout, l'edition des users : infos personnelles,
mot de passe, etc

Permet aussi l'ajout, edition et suppression des droits, des bannissements,
des whitelist, des services users et des écoles
"""

from __future__ import unicode_literals

from django.urls import reverse
from django.shortcuts import get_object_or_404, render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required, permission_required
from django.db.models import ProtectedError, Count, Max
from django.utils import timezone
from django.db import transaction
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.views.decorators.csrf import csrf_exempt

from rest_framework.renderers import JSONRenderer
from reversion import revisions as reversion

from cotisations.models import Facture, Paiement
from machines.models import Machine
from preferences.models import GeneralOption
from re2o.views import form
from re2o.utils import (
    all_has_access,
    SortTable,
    re2o_paginator
)
from re2o.acl import (
    can_create,
    can_edit,
    can_delete_set,
    can_delete,
    can_view,
    can_view_all,
    can_change
)
from cotisations.utils import find_payment_method

from .serializers import MailingSerializer, MailingMemberSerializer
from .models import (
    User,
    Ban,
    Whitelist,
    School,
    ListRight,
    Request,
    ServiceUser,
    Adherent,
    Club,
    ListShell,
)
from .forms import (
    BanForm,
    WhitelistForm,
    DelSchoolForm,
    DelListRightForm,
    NewListRightForm,
    StateForm,
    SchoolForm,
    ShellForm,
    EditServiceUserForm,
    ServiceUserForm,
    ListRightForm,
    AdherentForm,
    ClubForm,
    MassArchiveForm,
    PassForm,
    ResetPasswordForm,
    ClubAdminandMembersForm,
    GroupForm
)


@can_create(Adherent)
def new_user(request):
    """ Vue de création d'un nouvel utilisateur,
    envoie un mail pour le mot de passe"""
    user = AdherentForm(request.POST or None, user=request.user)
    GTU_sum_up = GeneralOption.get_cached_value('GTU_sum_up')
    GTU = GeneralOption.get_cached_value('GTU')
    if user.is_valid():
        user = user.save(commit=False)
        user.save()
        user.reset_passwd_mail(request)
        messages.success(request, "L'utilisateur %s a été crée, un mail\
        pour l'initialisation du mot de passe a été envoyé" % user.pseudo)
        return redirect(reverse(
            'users:profil',
            kwargs={'userid': str(user.id)}
        ))
    return form(
        {
            'userform': user,
            'GTU_sum_up': GTU_sum_up,
            'GTU': GTU,
            'showCGU': True,
            'action_name': 'Créer un utilisateur'
        },
        'users/user.html',
        request
    )


@login_required
@can_create(Club)
def new_club(request):
    """ Vue de création d'un nouveau club,
    envoie un mail pour le mot de passe"""
    club = ClubForm(request.POST or None, user=request.user)
    if club.is_valid():
        club = club.save(commit=False)
        club.save()
        club.reset_passwd_mail(request)
        messages.success(request, "L'utilisateur %s a été crée, un mail\
        pour l'initialisation du mot de passe a été envoyé" % club.pseudo)
        return redirect(reverse(
            'users:profil',
            kwargs={'userid': str(club.id)}
        ))
    return form(
        {'userform': club, 'showCGU': False, 'action_name': 'Créer un club'},
        'users/user.html',
        request
    )


@login_required
@can_edit(Club)
def edit_club_admin_members(request, club_instance, **_kwargs):
    """Vue d'edition de la liste des users administrateurs et
    membres d'un club"""
    club = ClubAdminandMembersForm(
        request.POST or None,
        instance=club_instance
    )
    if club.is_valid():
        if club.changed_data:
            club.save()
            messages.success(request, "Le club a bien été modifié")
        return redirect(reverse(
            'users:profil',
            kwargs={'userid': str(club_instance.id)}
        ))
    return form(
        {
            'userform': club,
            'showCGU': False,
            'action_name': 'Editer les admin et membres'
        },
        'users/user.html',
        request
    )


@login_required
@can_edit(User)
def edit_info(request, user, userid):
    """ Edite un utilisateur à partir de son id,
    si l'id est différent de request.user, vérifie la
    possession du droit cableur """
    if user.is_class_adherent:
        user_form = AdherentForm(
            request.POST or None,
            instance=user.adherent,
            user=request.user
        )
    else:
        user_form = ClubForm(
            request.POST or None,
            instance=user.club,
            user=request.user
        )
    if user_form.is_valid():
        if user_form.changed_data:
            user_form.save()
            messages.success(request, "L'user a bien été modifié")
        return redirect(reverse(
            'users:profil',
            kwargs={'userid': str(userid)}
        ))
    return form(
        {'userform': user_form, 'action_name': "Editer l'utilisateur"},
        'users/user.html',
        request
    )


@login_required
@can_edit(User, 'state')
def state(request, user, userid):
    """ Changer l'etat actif/desactivé/archivé d'un user,
    need droit bureau """
    state_form = StateForm(request.POST or None, instance=user)
    if state_form.is_valid():
        if state_form.changed_data:
            if state_form.cleaned_data['state'] == User.STATE_ARCHIVE:
                user.archive()
            elif state_form.cleaned_data['state'] == User.STATE_ACTIVE:
                user.unarchive()
            state_form.save()
            messages.success(request, "Etat changé avec succès")
        return redirect(reverse(
            'users:profil',
            kwargs={'userid': str(userid)}
        ))
    return form(
        {'userform': state_form, 'action_name': "Editer l'état"},
        'users/user.html',
        request
    )


@login_required
@can_edit(User, 'groups')
def groups(request, user, userid):
    """ View to edit the groups of a user """
    group_form = GroupForm(request.POST or None,
                           instance=user, user=request.user)
    if group_form.is_valid():
        if group_form.changed_data:
            group_form.save()
            messages.success(request, "Groupes changés avec succès")
        return redirect(reverse(
            'users:profil',
            kwargs={'userid': str(userid)}
        ))
    return form(
        {'userform': group_form, 'action_name': 'Editer les groupes'},
        'users/user.html',
        request
    )


@login_required
@can_edit(User, 'password')
def password(request, user, userid):
    """ Reinitialisation d'un mot de passe à partir de l'userid,
    pour self par défaut, pour tous sans droit si droit cableur,
    pour tous si droit bureau """
    u_form = PassForm(request.POST or None, instance=user, user=request.user)
    if u_form.is_valid():
        if u_form.changed_data:
            u_form.save()
            messages.success(request, "Le mot de passe a changé")
        return redirect(reverse(
            'users:profil',
            kwargs={'userid': str(userid)}
        ))
    return form(
        {'userform': u_form, 'action_name': 'Changer le mot de passe'},
        'users/user.html',
        request
    )


@login_required
@can_edit(User, 'groups')
def del_group(request, user, listrightid, **_kwargs):
    """ View used to delete a group """
    user.groups.remove(ListRight.objects.get(id=listrightid))
    user.save()
    messages.success(request, "Droit supprimé à %s" % user)
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


@login_required
@can_edit(User, 'is_superuser')
def del_superuser(request, user, **_kwargs):
    """Remove the superuser right of an user."""
    user.is_superuser = False
    user.save()
    messages.success(request, "%s n'est plus superuser" % user)
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


@login_required
@can_create(ServiceUser)
def new_serviceuser(request):
    """ Vue de création d'un nouvel utilisateur service"""
    user = ServiceUserForm(request.POST or None)
    if user.is_valid():
        user.save()
        messages.success(
            request,
            "L'utilisateur a été crée"
        )
        return redirect(reverse('users:index-serviceusers'))
    return form(
        {'userform': user, 'action_name': 'Créer un serviceuser'},
        'users/user.html',
        request
    )


@login_required
@can_edit(ServiceUser)
def edit_serviceuser(request, serviceuser, **_kwargs):
    """ Edit a ServiceUser """
    serviceuser = EditServiceUserForm(
        request.POST or None,
        instance=serviceuser
    )
    if serviceuser.is_valid():
        if serviceuser.changed_data:
            serviceuser.save()
        messages.success(request, "L'user a bien été modifié")
        return redirect(reverse('users:index-serviceusers'))
    return form(
        {'userform': serviceuser, 'action_name': 'Editer un serviceuser'},
        'users/user.html',
        request
    )


@login_required
@can_delete(ServiceUser)
def del_serviceuser(request, serviceuser, **_kwargs):
    """Suppression d'un ou plusieurs serviceusers"""
    if request.method == "POST":
        serviceuser.delete()
        messages.success(request, "L'user a été détruit")
        return redirect(reverse('users:index-serviceusers'))
    return form(
        {'objet': serviceuser, 'objet_name': 'serviceuser'},
        'users/delete.html',
        request
    )


@login_required
@can_create(Ban)
@can_edit(User)
def add_ban(request, user, userid):
    """ Ajouter un banissement, nécessite au moins le droit bofh
    (a fortiori bureau)
    Syntaxe : JJ/MM/AAAA , heure optionnelle, prend effet immédiatement"""
    ban_instance = Ban(user=user)
    ban = BanForm(request.POST or None, instance=ban_instance)
    if ban.is_valid():
        ban.save()
        messages.success(request, "Bannissement ajouté")
        return redirect(reverse(
            'users:profil',
            kwargs={'userid': str(userid)}
        ))
    if user.is_ban():
        messages.error(
            request,
            "Attention, cet utilisateur a deja un bannissement actif"
        )
    return form(
        {'userform': ban, 'action_name': 'Ajouter un ban'},
        'users/user.html',
        request
    )


@login_required
@can_edit(Ban)
def edit_ban(request, ban_instance, **_kwargs):
    """ Editer un bannissement, nécessite au moins le droit bofh
    (a fortiori bureau)
    Syntaxe : JJ/MM/AAAA , heure optionnelle, prend effet immédiatement"""
    ban = BanForm(request.POST or None, instance=ban_instance)
    if ban.is_valid():
        if ban.changed_data:
            ban.save()
            messages.success(request, "Bannissement modifié")
        return redirect(reverse('users:index'))
    return form(
        {'userform': ban, 'action_name': 'Editer un ban'},
        'users/user.html',
        request
    )


@login_required
@can_delete(Ban)
def del_ban(request, ban, **_kwargs):
    """ Supprime un banissement"""
    if request.method == "POST":
        ban.delete()
        messages.success(request, "Le banissement a été supprimé")
        return redirect(reverse(
            'users:profil',
            kwargs={'userid': str(ban.user.id)}
        ))
    return form(
        {'objet': ban, 'objet_name': 'ban'},
        'users/delete.html',
        request
    )


@login_required
@can_create(Whitelist)
@can_edit(User)
def add_whitelist(request, user, userid):
    """ Accorder un accès gracieux, temporaire ou permanent.
    Need droit cableur
    Syntaxe : JJ/MM/AAAA , heure optionnelle, prend effet immédiatement,
    raison obligatoire"""
    whitelist_instance = Whitelist(user=user)
    whitelist = WhitelistForm(
        request.POST or None,
        instance=whitelist_instance
    )
    if whitelist.is_valid():
        whitelist.save()
        messages.success(request, "Accès à titre gracieux accordé")
        return redirect(reverse(
            'users:profil',
            kwargs={'userid': str(userid)}
        ))
    if user.is_whitelisted():
        messages.error(
            request,
            "Attention, cet utilisateur a deja un accès gracieux actif"
        )
    return form(
        {'userform': whitelist, 'action_name': 'Ajouter une whitelist'},
        'users/user.html',
        request
    )


@login_required
@can_edit(Whitelist)
def edit_whitelist(request, whitelist_instance, **_kwargs):
    """ Editer un accès gracieux, temporaire ou permanent.
    Need droit cableur
    Syntaxe : JJ/MM/AAAA , heure optionnelle, prend effet immédiatement,
    raison obligatoire"""
    whitelist = WhitelistForm(
        request.POST or None,
        instance=whitelist_instance
    )
    if whitelist.is_valid():
        if whitelist.changed_data:
            whitelist.save()
            messages.success(request, "Whitelist modifiée")
        return redirect(reverse('users:index'))
    return form(
        {'userform': whitelist, 'action_name': 'Editer une whitelist'},
        'users/user.html',
        request
    )


@login_required
@can_delete(Whitelist)
def del_whitelist(request, whitelist, **_kwargs):
    """ Supprime un acces gracieux"""
    if request.method == "POST":
        whitelist.delete()
        messages.success(request, "L'accés gracieux a été supprimé")
        return redirect(reverse(
            'users:profil',
            kwargs={'userid': str(whitelist.user.id)}
        ))
    return form(
        {'objet': whitelist, 'objet_name': 'whitelist'},
        'users/delete.html',
        request
    )


@login_required
@can_create(School)
def add_school(request):
    """ Ajouter un établissement d'enseignement à la base de donnée,
    need cableur"""
    school = SchoolForm(request.POST or None)
    if school.is_valid():
        school.save()
        messages.success(request, "L'établissement a été ajouté")
        return redirect(reverse('users:index-school'))
    return form(
        {'userform': school, 'action_name': 'Ajouter'},
        'users/user.html',
        request
    )


@login_required
@can_edit(School)
def edit_school(request, school_instance, **_kwargs):
    """ Editer un établissement d'enseignement à partir du schoolid dans
    la base de donnée, need cableur"""
    school = SchoolForm(request.POST or None, instance=school_instance)
    if school.is_valid():
        if school.changed_data:
            school.save()
            messages.success(request, "Établissement modifié")
        return redirect(reverse('users:index-school'))
    return form(
        {'userform': school, 'action_name': 'Editer'},
        'users/user.html',
        request
    )


@login_required
@can_delete_set(School)
def del_school(request, instances):
    """ Supprimer un établissement d'enseignement à la base de donnée,
    need cableur
    Objet protégé, possible seulement si aucun user n'est affecté à
    l'établissement """
    school = DelSchoolForm(request.POST or None, instances=instances)
    if school.is_valid():
        school_dels = school.cleaned_data['schools']
        for school_del in school_dels:
            try:
                school_del.delete()
                messages.success(request, "L'établissement a été supprimé")
            except ProtectedError:
                messages.error(
                    request,
                    "L'établissement %s est affecté à au moins un user, \
                        vous ne pouvez pas le supprimer" % school_del)
        return redirect(reverse('users:index-school'))
    return form(
        {'userform': school, 'action_name': 'Supprimer'},
        'users/user.html',
        request
    )


@login_required
@can_create(ListShell)
def add_shell(request):
    """ Ajouter un shell à la base de donnée"""
    shell = ShellForm(request.POST or None)
    if shell.is_valid():
        shell.save()
        messages.success(request, "Le shell a été ajouté")
        return redirect(reverse('users:index-shell'))
    return form(
        {'userform': shell, 'action_name': 'Ajouter'},
        'users/user.html',
        request
    )


@login_required
@can_edit(ListShell)
def edit_shell(request, shell_instance, **_kwargs):
    """ Editer un shell à partir du listshellid"""
    shell = ShellForm(request.POST or None, instance=shell_instance)
    if shell.is_valid():
        if shell.changed_data:
            shell.save()
            messages.success(request, "Le shell a été modifié")
        return redirect(reverse('users:index-shell'))
    return form(
        {'userform': shell, 'action_name': 'Editer'},
        'users/user.html',
        request
    )


@login_required
@can_delete(ListShell)
def del_shell(request, shell, **_kwargs):
    """Destruction d'un shell"""
    if request.method == "POST":
        shell.delete()
        messages.success(request, "Le shell a été détruit")
        return redirect(reverse('users:index-shell'))
    return form(
        {'objet': shell, 'objet_name': 'shell'},
        'users/delete.html',
        request
    )


@login_required
@can_create(ListRight)
def add_listright(request):
    """ Ajouter un droit/groupe, nécessite droit bureau.
    Obligation de fournir un gid pour la synchro ldap, unique """
    listright = NewListRightForm(request.POST or None)
    if listright.is_valid():
        listright.save()
        messages.success(request, "Le droit/groupe a été ajouté")
        return redirect(reverse('users:index-listright'))
    return form(
        {'userform': listright, 'action_name': 'Ajouter'},
        'users/user.html',
        request
    )


@login_required
@can_edit(ListRight)
def edit_listright(request, listright_instance, **_kwargs):
    """ Editer un groupe/droit, necessite droit bureau,
    à partir du listright id """
    listright = ListRightForm(
        request.POST or None,
        instance=listright_instance
    )
    if listright.is_valid():
        if listright.changed_data:
            listright.save()
            messages.success(request, "Droit modifié")
        return redirect(reverse('users:index-listright'))
    return form(
        {'userform': listright, 'action_name': 'Editer'},
        'users/user.html',
        request
    )


@login_required
@can_delete_set(ListRight)
def del_listright(request, instances):
    """ Supprimer un ou plusieurs groupe, possible si il est vide, need droit
    bureau """
    listright = DelListRightForm(request.POST or None, instances=instances)
    if listright.is_valid():
        listright_dels = listright.cleaned_data['listrights']
        for listright_del in listright_dels:
            try:
                listright_del.delete()
                messages.success(request, "Le droit/groupe a été supprimé")
            except ProtectedError:
                messages.error(
                    request,
                    "Le groupe %s est affecté à au moins un user, \
                        vous ne pouvez pas le supprimer" % listright_del)
        return redirect(reverse('users:index-listright'))
    return form(
        {'userform': listright, 'action_name': 'Supprimer'},
        'users/user.html',
        request
    )


@login_required
@can_view_all(User)
@can_change(User, 'state')
def mass_archive(request):
    """ Permet l'archivage massif"""
    to_archive_date = MassArchiveForm(request.POST or None)
    to_archive_list = []
    if to_archive_date.is_valid():
        date = to_archive_date.cleaned_data['date']
        to_archive_list = [user for user in
                           User.objects.exclude(state=User.STATE_ARCHIVE)
                           if not user.end_access()
                           or user.end_access() < date]
        if "valider" in request.POST:
            for user in to_archive_list:
                with transaction.atomic(), reversion.create_revision():
                    user.archive()
                    user.save()
                    reversion.set_comment("Archivage")
            messages.success(request, "%s users ont été archivés" % len(
                to_archive_list
            ))
            return redirect(reverse('users:index'))
    return form(
        {'userform': to_archive_date, 'to_archive_list': to_archive_list},
        'users/mass_archive.html',
        request
    )


@login_required
@can_view_all(Adherent)
def index(request):
    """ Affiche l'ensemble des adherents, need droit cableur """
    pagination_number = GeneralOption.get_cached_value('pagination_number')
    users_list = Adherent.objects.select_related('room')
    users_list = SortTable.sort(
        users_list,
        request.GET.get('col'),
        request.GET.get('order'),
        SortTable.USERS_INDEX
    )
    users_list = re2o_paginator(request, users_list, pagination_number)
    return render(request, 'users/index.html', {'users_list': users_list})


@login_required
@can_view_all(Club)
def index_clubs(request):
    """ Affiche l'ensemble des clubs, need droit cableur """
    pagination_number = GeneralOption.get_cached_value('pagination_number')
    clubs_list = Club.objects.select_related('room')
    clubs_list = SortTable.sort(
        clubs_list,
        request.GET.get('col'),
        request.GET.get('order'),
        SortTable.USERS_INDEX
    )
    clubs_list = re2o_paginator(request, clubs_list, pagination_number)
    return render(
        request,
        'users/index_clubs.html',
        {'clubs_list': clubs_list}
    )


@login_required
@can_view_all(Ban)
def index_ban(request):
    """ Affiche l'ensemble des ban, need droit cableur """
    pagination_number = GeneralOption.get_cached_value('pagination_number')
    ban_list = Ban.objects.select_related('user')
    ban_list = SortTable.sort(
        ban_list,
        request.GET.get('col'),
        request.GET.get('order'),
        SortTable.USERS_INDEX_BAN
    )
    ban_list = re2o_paginator(request, ban_list, pagination_number)
    return render(request, 'users/index_ban.html', {'ban_list': ban_list})


@login_required
@can_view_all(Whitelist)
def index_white(request):
    """ Affiche l'ensemble des whitelist, need droit cableur """
    pagination_number = GeneralOption.get_cached_value('pagination_number')
    white_list = Whitelist.objects.select_related('user')
    white_list = SortTable.sort(
        white_list,
        request.GET.get('col'),
        request.GET.get('order'),
        SortTable.USERS_INDEX_BAN
    )
    white_list = re2o_paginator(request, white_list, pagination_number)
    return render(
        request,
        'users/index_whitelist.html',
        {'white_list': white_list}
    )


@login_required
@can_view_all(School)
def index_school(request):
    """ Affiche l'ensemble des établissement"""
    school_list = School.objects.order_by('name')
    pagination_number = GeneralOption.get_cached_value('pagination_number')
    school_list = SortTable.sort(
        school_list,
        request.GET.get('col'),
        request.GET.get('order'),
        SortTable.USERS_INDEX_SCHOOL
    )
    school_list = re2o_paginator(request, school_list, pagination_number)
    return render(
        request,
        'users/index_schools.html',
        {'school_list': school_list}
    )


@login_required
@can_view_all(ListShell)
def index_shell(request):
    """ Affiche l'ensemble des shells"""
    shell_list = ListShell.objects.order_by('shell')
    return render(
        request,
        'users/index_shell.html',
        {'shell_list': shell_list}
    )


@login_required
@can_view_all(ListRight)
def index_listright(request):
    """ Affiche l'ensemble des droits"""
    rights = {}
    for right in (ListRight.objects
                  .order_by('name')
                  .prefetch_related('permissions')
                  .prefetch_related('user_set')
                  .prefetch_related('user_set__facture_set__vente_set__cotisation')
                 ):
        rights[right] = (right.user_set
                         .annotate(action_number=Count('revision'),
                                   last_seen=Max('revision__date_created'),
                                   end_adhesion=Max('facture__vente__cotisation__date_end'))
                        )
    superusers = (User.objects
                  .filter(is_superuser=True)
                  .annotate(action_number=Count('revision'),
                            last_seen=Max('revision__date_created'),
                            end_adhesion=Max('facture__vente__cotisation__date_end'))
                 )
    return render(
        request,
        'users/index_listright.html',
        {
            'rights': rights,
            'superusers' : superusers,
        }
    )


@login_required
@can_view_all(ServiceUser)
def index_serviceusers(request):
    """ Affiche les users de services (pour les accès ldap)"""
    serviceusers_list = ServiceUser.objects.order_by('pseudo')
    return render(
        request,
        'users/index_serviceusers.html',
        {'serviceusers_list': serviceusers_list}
    )


@login_required
def mon_profil(request):
    """ Lien vers profil, renvoie request.id à la fonction """
    return redirect(reverse(
        'users:profil',
        kwargs={'userid': str(request.user.id)}
    ))


@login_required
@can_view(User)
def profil(request, users, **_kwargs):
    """ Affiche un profil, self or cableur, prend un userid en argument """
    machines = Machine.objects.filter(user=users).select_related('user')\
        .prefetch_related('interface_set__domain__extension')\
        .prefetch_related('interface_set__ipv4__ip_type__extension')\
        .prefetch_related('interface_set__type')\
        .prefetch_related('interface_set__domain__related_domain__extension')
    machines = SortTable.sort(
        machines,
        request.GET.get('col'),
        request.GET.get('order'),
        SortTable.MACHINES_INDEX
    )
    pagination_large_number = GeneralOption.get_cached_value(
        'pagination_large_number'
    )
    nb_machines = machines.count()
    machines = re2o_paginator(request, machines, pagination_large_number)
    factures = Facture.objects.filter(user=users)
    factures = SortTable.sort(
        factures,
        request.GET.get('col'),
        request.GET.get('order'),
        SortTable.COTISATIONS_INDEX
    )
    bans = Ban.objects.filter(user=users)
    bans = SortTable.sort(
        bans,
        request.GET.get('col'),
        request.GET.get('order'),
        SortTable.USERS_INDEX_BAN
    )
    whitelists = Whitelist.objects.filter(user=users)
    whitelists = SortTable.sort(
        whitelists,
        request.GET.get('col'),
        request.GET.get('order'),
        SortTable.USERS_INDEX_WHITE
    )
    try:
        balance = find_payment_method(Paiement.objects.get(is_balance=True))
    except Paiement.DoesNotExist:
        user_solde = False
    else:
        user_solde = (
            balance is not None
            and balance.can_credit_balance(request.user)
        )
    return render(
        request,
        'users/profil.html',
        {
            'users': users,
            'machines_list': machines,
            'nb_machines': nb_machines,
            'facture_list': factures,
            'ban_list': bans,
            'white_list': whitelists,
            'user_solde': user_solde,
        }
    )


def reset_password(request):
    """ Reintialisation du mot de passe si mdp oublié """
    userform = ResetPasswordForm(request.POST or None)
    if userform.is_valid():
        try:
            user = User.objects.get(
                pseudo=userform.cleaned_data['pseudo'],
                email=userform.cleaned_data['email']
            )
        except User.DoesNotExist:
            messages.error(request, "Cet utilisateur n'existe pas")
            return form(
                {'userform': userform, 'action_name': 'Réinitialiser'},
                'users/user.html',
                request
            )
        user.reset_passwd_mail(request)
        messages.success(request, "Un mail pour l'initialisation du mot\
        de passe a été envoyé")
        redirect(reverse('index'))
    return form(
        {'userform': userform, 'action_name': 'Réinitialiser'},
        'users/user.html',
        request
    )


def process(request, token):
    """Process, lien pour la reinitialisation du mot de passe"""
    valid_reqs = Request.objects.filter(expires_at__gt=timezone.now())
    req = get_object_or_404(valid_reqs, token=token)

    if req.type == Request.PASSWD:
        return process_passwd(request, req)
    else:
        messages.error(request, "Entrée incorrecte, contactez un admin")
        redirect(reverse('index'))


def process_passwd(request, req):
    """Process le changeemnt de mot de passe, renvoie le formulaire
    demandant le nouveau password"""
    user = req.user
    u_form = PassForm(request.POST or None, instance=user, user=request.user)
    if u_form.is_valid():
        with transaction.atomic(), reversion.create_revision():
            u_form.save()
            reversion.set_comment("Réinitialisation du mot de passe")
        req.delete()
        messages.success(request, "Le mot de passe a changé")
        return redirect(reverse('index'))
    return form(
        {'userform': u_form, 'action_name': 'Changer le mot de passe'},
        'users/user.html',
        request
    )


class JSONResponse(HttpResponse):
    """ Framework Rest """

    def __init__(self, data, **kwargs):
        content = JSONRenderer().render(data)
        kwargs['content_type'] = 'application/json'
        super(JSONResponse, self).__init__(content, **kwargs)


@csrf_exempt
@login_required
@permission_required('machines.serveur')
def ml_std_list(_request):
    """ API view sending all the available standard mailings"""
    return JSONResponse([
        {'name': 'adherents'}
    ])


@csrf_exempt
@login_required
@permission_required('machines.serveur')
def ml_std_members(request, ml_name):
    """ API view sending all the members for a standard mailing"""
    # All with active connextion
    if ml_name == 'adherents':
        members = all_has_access().values('email').distinct()
    # Unknown mailing
    else:
        messages.error(request, "Cette mailing n'existe pas")
        return redirect(reverse('index'))
    seria = MailingMemberSerializer(members, many=True)
    return JSONResponse(seria.data)


@csrf_exempt
@login_required
@permission_required('machines.serveur')
def ml_club_list(_request):
    """ API view sending all the available club mailings"""
    clubs = Club.objects.filter(mailing=True).values('pseudo')
    seria = MailingSerializer(clubs, many=True)
    return JSONResponse(seria.data)


@csrf_exempt
@login_required
@permission_required('machines.serveur')
def ml_club_admins(request, ml_name):
    """ API view sending all the administrators for a specific club mailing"""
    try:
        club = Club.objects.get(mailing=True, pseudo=ml_name)
    except Club.DoesNotExist:
        messages.error(request, "Cette mailing n'existe pas")
        return redirect(reverse('index'))
    members = club.administrators.all().values('email').distinct()
    seria = MailingMemberSerializer(members, many=True)
    return JSONResponse(seria.data)


@csrf_exempt
@login_required
@permission_required('machines.serveur')
def ml_club_members(request, ml_name):
    """ API view sending all the members for a specific club mailing"""
    try:
        club = Club.objects.get(mailing=True, pseudo=ml_name)
    except Club.DoesNotExist:
        messages.error(request, "Cette mailing n'existe pas")
        return redirect(reverse('index'))
    members = (
        club.administrators.all().values('email').distinct() |
        club.members.all().values('email').distinct()
    )
    seria = MailingMemberSerializer(members, many=True)
    return JSONResponse(seria.data)
