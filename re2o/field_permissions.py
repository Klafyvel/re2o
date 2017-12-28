from django.db import models
from django import forms
from functools import partial


class FieldPermissionModelMixin:
    field_permissions = {}  # {'field_name': callable}
    FIELD_PERM_CODENAME = 'can_change_{model}_{name}'
    FIELD_PERMISSION_GETTER = 'can_change_{name}'
    FIELD_PERMISSION_MISSING_DEFAULT = True

    class Meta:
        abstract = True

    def has_perm(self, user, perm):
        return user.has_perm(perm)  # Never give 'obj' argument here

    def has_field_perm(self, user, field):
        if field in self.field_permissions:
            checks = self.field_permissions[field]
            if not isinstance(checks, (list, tuple)):
                checks = [checks]
            for i, perm in enumerate(checks):
                if callable(perm):
                    checks[i] = partial(perm, field=field)

        else:
            checks = []

            # Consult the optional field-specific hook.
            getter_name = self.FIELD_PERMISSION_GETTER.format(name=field)
            if hasattr(self, getter_name):
                checks.append(getattr(self, getter_name))

            # Try to find a static permission for the field
            else:
                perm_label = self.FIELD_PERM_CODENAME.format(**{
                    'model': self._meta.model_name,
                    'name': field,
                })
                if perm_label in dict(self._meta.permissions):
                    checks.append(perm_label)

        # No requirements means no restrictions.
        if not len(checks):
            return self.FIELD_PERMISSION_MISSING_DEFAULT

        # Try to find a user setting that qualifies them for permission.
        for perm in checks:
            if callable(perm):
                result, reason = perm(self, user=user)
                if result is not None:
                    return result
            else:
                result = user.has_perm(perm)  # Don't supply 'obj', or else infinite recursion.
                if result:
                    return True

        # If no requirement can be met, then permission is denied.
        return False

class FieldPermissionModel(FieldPermissionModelMixin, models.Model):
    class Meta:
        abstract = True


class FieldPermissionFormMixin:
    """
    ModelForm logic for removing fields when a user is found not to have change permissions.
    """
    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user')

        super(FieldPermissionFormMixin, self).__init__(*args, **kwargs)

        model = self.Meta.model
        model_field_names = [f.name for f in model._meta.get_fields()]  # this might be too broad
        for name in model_field_names:
            if name in self.fields and not self.instance.has_field_perm(user, field=name):
                self.remove_unauthorized_field(name)

    def remove_unauthorized_field(self, name):
        del self.fields[name]


class FieldPermissionForm(FieldPermissionFormMixin, forms.ModelForm):
    pass

