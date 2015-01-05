from itertools import imap
from django.db import models
from django.conf import settings
from django.core.urlresolvers import reverse
from django.db.models import Count
from django.db.models.query import QuerySet
from model_utils.managers import PassThroughManager
from model_utils.fields import MonitorField, StatusField
from model_utils import Choices
from .tags.models import Tag
from .permissions.models import Permission, LocalGroup
from django.db.models import Max


class CaseQuerySet(QuerySet):
    def for_user(self, user):
        print user.has_perm('cases.can_view_all')
        if user.has_perm('cases.can_view_all'):  # All rank can view own cases
            return self
        field = 'permission__user'
        return self.filter(**{field: user})

    def free(self):
        return self.exclude(permission__group__rank=LocalGroup.RANK.lawyer)

    def with_record_count(self):
        return self.annotate(Count('record'))

    def with_last_send_letter(self):
        return self.filter(record__letter__isnull=False).\
            annotate(last_send=Max('record__letter__created_on'))


class Case(models.Model):
    STATUS = Choices('open', 'closed')
    name = models.CharField(max_length=150)
    tags = models.ManyToManyField(Tag, null=True, blank=True)
    status = StatusField()
    status_changed = MonitorField(monitor='status')
    client = models.ForeignKey(settings.AUTH_USER_MODEL)
    objects = PassThroughManager.for_queryset_class(CaseQuerySet)()

    def get_absolute_url(self):
        return reverse('cases:detail', kwargs={'pk': str(self.pk)})

    def get_edit_url(self):
        return reverse('cases:edit', kwargs={'pk': str(self.pk)})

    def __unicode__(self):
        return self.name

    def get_permissions_set(self, user):
        def get_name(perm):
            return "%s.%s" % (perm.content_type.app_label, perm.codename)

        try:  # Have local priviledge
            return imap(get_name, self.permission_set.get(user=user).group.group.permissions.all())
        except Permission.DoesNotExist:  # or use global priviledge
            return user.get_all_permissions()

    def get_lawyers(self):
        group = LocalGroup.objects.get(rank=LocalGroup.RANK.lawyer)  # In one query?
        return (c.user for c in self.permission_set.filter(group=group).all())

    def save(self, *args, **kwargs):
        is_new = (True if self.pk is None else False)
        super(Case, self).save(*args, **kwargs)
        if is_new:
            self.assign(user=self.client, rank=LocalGroup.RANK.client)

    def assign(self, user, rank=LocalGroup.RANK.client):
        group = LocalGroup.objects.get(rank=rank)
        return Permission(case=self, group=group, user=user).save()

    class Meta:
        permissions = (("can_select_client", "Can select client"),
                       ('can_view_all', "Can view all cases",),
                       ('can_view_free', "Can view free", ))
