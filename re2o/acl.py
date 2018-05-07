# -*- mode: python; coding: utf-8 -*-
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

"""Handles ACL for re2o.

Here are defined some decorators that can be used in views to handle ACL.
"""
from __future__ import unicode_literals

import sys
from itertools import chain

from django.db.models import Model
from django.contrib import messages
from django.shortcuts import redirect
from django.urls import reverse


def acl_base_decorator(method_name, *targets, **kwargs):
    """Base decorator for acl. It checks if the `request.user` has the
    permission by calling model.method_name. If the flag on_instance is True,
    tries to get an instance of the model by calling
    `model.get_instance(*args, **kwargs)` and runs `instance.mehod_name`
    rather than model.method_name.

    It is not intended to be used as is. It is a base for others ACL
    decorators.

    Args:
        method_name: The name of the method which is to to be used for ACL.
            (ex: 'can_edit') WARNING: if no method called 'method_name' exists,
            then no error will be triggered, the decorator will act as if
            permission was granted. This is to allow you to run ACL tests on
            fields only. If the method exists, it has to return a 2-tuple
            `(can, reason)` with `can` being a boolean stating whether the
            access is granted and `reason` a message to be displayed if `can`
            equals `False` (can be `None`)
        *targets: The targets. Targets are specified like a sequence of models
            and fields names. As an example
            ```
                acl_base_decorator('can_edit', ModelA, 'field1', 'field2', \
ModelB, ModelC, 'field3', on_instance=False)
            ```
            will make the following calls (where `user` is the current user,
            `*args` and `**kwargs` are the arguments initially passed to the
            view):
                - `ModelA.can_edit(user, *args, **kwargs)`
                - `ModelA.can_change_field1(user, *args, **kwargs)`
                - `ModelA.can_change_field2(user, *args, **kwargs)`
                - `ModelB.can_edit(user, *args, **kwargs)`
                - `ModelC.can_edit(user, *args, **kwargs)`
                - `ModelC.can_change_field3(user, *args, **kwargs)`

            Note that
            ```
                acl_base_decorator('can_edit', 'field1', ModelA, 'field2', \
on_instance=False)
            ```
            would have the same effect that
            ```
                acl_base_decorator('can_edit', ModelA, 'field1', 'field2', \
on_instance=False)
            ```
            But don't do that, it's silly.
        **kwargs: There is only one keyword argument, `on_instance`, which
            default value is `True`. When `on_instance` equals `False`, the
            decorator runs the ACL method on the model class rather than on
            an instance. If an instance need to fetched, it is done calling the
            assumed existing method `get_instance` of the model, with the
            arguments originally passed to the view.

    Returns:
        The user is either redirected to their own page with an explanation
        message if at least one access is not granted, or to the view. In order
        to avoid duplicate DB calls, when the `on_instance` flag equals `True`,
        the instances are passed to the view. Example, with this decorator:
        ```
            acl_base_decorator('can_edit', ModelA, 'field1', 'field2', ModelB,\
ModelC)
        ```
        The view will be called like this:
        ```
            view(request, instance_of_A, instance_of_b, *args, **kwargs)
        ```
        where `*args` and `**kwargs` are the original view arguments.
    """
    on_instance = kwargs.get('on_instance', True)

    def group_targets():
        """This generator parses the targets of the decorator, yielding
        2-tuples of (model, [fields]).
        """
        current_target = None
        current_fields = []
        for target in targets:
            if isinstance(target, type) and issubclass(target, Model):
                if current_target:
                    yield (current_target, current_fields)
                current_target = target
                current_fields = []
            else:
                current_fields.append(target)
        yield (current_target, current_fields)

    def decorator(view):
        """The decorator to use on a specific view
        """
        def wrapper(request, *args, **kwargs):
            """The wrapper used for a specific request"""
            instances = []

            def process_target(target, fields):
                """This function calls the methods on the target and checks for
                the can_change_`field` method with the given fields. It also
                stores the instances of models in order to avoid duplicate DB
                calls for the view.
                """
                if on_instance:
                    try:
                        target = target.get_instance(*args, **kwargs)
                        instances.append(target)
                    except target.DoesNotExist:
                        yield False, u"Entrée inexistante"
                        return
                if hasattr(target, method_name):
                    can_fct = getattr(target, method_name)
                    yield can_fct(request.user, *args, **kwargs)
                for field in fields:
                    can_change_fct = getattr(target, 'can_change_' + field)
                    yield can_change_fct(request.user, *args, **kwargs)
            error_messages = [
                x[1] for x in chain.from_iterable(
                    process_target(x[0], x[1]) for x in group_targets()
                ) if not x[0]
            ]
            if error_messages:
                for msg in error_messages:
                    messages.error(
                        request, msg or "Vous ne pouvez pas accéder à ce menu")
                return redirect(reverse(
                    'users:profil',
                    kwargs={'userid': str(request.user.id)}
                ))
            return view(request, *chain(instances, args), **kwargs)
        return wrapper
    return decorator


def can_create(*models):
    """Decorator to check if an user can create the given models. It runs
    `acl_base_decorator` with the flag `on_instance=False` and the method
    'can_create'. See `acl_base_decorator` documentation for further details.
    """
    return acl_base_decorator('can_create', *models, on_instance=False)


def can_edit(*targets):
    """Decorator to check if an user can edit the models.
    It runs `acl_base_decorator` with the flag `on_instance=True` and the
    method 'can_edit'. See `acl_base_decorator` documentation for further
    details.
    """
    return acl_base_decorator('can_edit', *targets)


def can_change(*targets):
    """Decorator to check if an user can edit a field of a model class.
    Difference with can_edit : takes a class and not an instance
    It runs `acl_base_decorator` with the flag `on_instance=False` and the
    method 'can_change'. See `acl_base_decorator` documentation for further
    details.
    """
    return acl_base_decorator('can_change', *targets)


def can_delete(*targets):
    """Decorator to check if an user can delete a model.
    It runs `acl_base_decorator` with the flag `on_instance=True` and the
    method 'can_edit'. See `acl_base_decorator` documentation for further
    details.
    """
    return acl_base_decorator('can_delete', *targets)


def can_delete_set(model):
    """Decorator which returns a list of detable models by request user.
    If none of them, return an error"""
    def decorator(view):
        """The decorator to use on a specific view
        """
        def wrapper(request, *args, **kwargs):
            """The wrapper used for a specific request
            """
            all_objects = model.objects.all()
            instances_id = []
            for instance in all_objects:
                can, _msg = instance.can_delete(request.user)
                if can:
                    instances_id.append(instance.id)
            instances = model.objects.filter(id__in=instances_id)
            if not instances:
                messages.error(
                    request, "Vous ne pouvez pas accéder à ce menu")
                return redirect(reverse(
                    'users:profil',
                    kwargs={'userid': str(request.user.id)}
                ))
            return view(request, instances, *args, **kwargs)
        return wrapper
    return decorator


def can_view(*targets):
    """Decorator to check if an user can view a model.
    It runs `acl_base_decorator` with the flag `on_instance=True` and the
    method 'can_view'. See `acl_base_decorator` documentation for further
    details.
    """
    return acl_base_decorator('can_view', *targets)


def can_view_all(*targets):
    """Decorator to check if an user can view a class of model.
    It runs `acl_base_decorator` with the flag `on_instance=False` and the
    method 'can_view_all'. See `acl_base_decorator` documentation for further
    details.
    """
    return acl_base_decorator('can_view_all', *targets, on_instance=False)


def can_view_app(app_name):
    """Decorator to check if an user can view an application.
    """
    assert app_name in sys.modules.keys()

    def decorator(view):
        """The decorator to use on a specific view
        """
        def wrapper(request, *args, **kwargs):
            """The wrapper used for a specific request
            """
            app = sys.modules[app_name]
            can, msg = app.can_view(request.user)
            if can:
                return view(request, *args, **kwargs)
            messages.error(request, msg)
            return redirect(reverse(
                'users:profil',
                kwargs={'userid': str(request.user.id)}
            ))
        return wrapper
    return decorator


def can_edit_history(view):
    """Decorator to check if an user can edit history."""
    def wrapper(request, *args, **kwargs):
        """The wrapper used for a specific request
        """
        if request.user.has_perm('admin.change_logentry'):
            return view(request, *args, **kwargs)
        messages.error(
            request,
            "Vous ne pouvez pas éditer l'historique."
        )
        return redirect(reverse(
            'users:profil',
            kwargs={'userid': str(request.user.id)}
        ))
    return wrapper
