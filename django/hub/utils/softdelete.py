from django.db import models


class SoftDeleteManager(models.Manager):

    def get_queryset(self, *args, **kwargs):
        qs = super(SoftDeleteManager, self) \
            .get_queryset(*args, **kwargs)
        return qs.filter(_soft_deleted=False)


class DeletedManager(models.Manager):

    def get_queryset(self, *args, **kwargs):
        qs = super(DeletedManager, self) \
            .get_queryset(*args, **kwargs)

        return qs.filter(_soft_deleted=True)


class SoftDeleteMixin(object):
    _soft_deleted = models.BooleanField(db_index=True, default=False)

    objects = SoftDeleteManager()
    deleted = DeletedManager()

    def delete(self):
        self._soft_deleted = True
        self.save()
