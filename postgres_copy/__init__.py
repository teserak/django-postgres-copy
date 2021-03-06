#!/usr/bin/env python
# -*- coding: utf-8 -*-
from django.db import models
from django.db import connection
from .copy_from import CopyMapping
from .copy_to import SQLCopyToCompiler, CopyToQuery
__version__ = '2.0.0'


class CopyQuerySet(models.QuerySet):
    """
    Subclass of QuerySet that adds from_csv and to_csv methods.
    """
    def from_csv(self, csv_path, mapping, **kwargs):
        """
        Copy CSV file from the provided path to the current model using the provided mapping.
        """
        mapping = CopyMapping(self.model, csv_path, mapping, **kwargs)
        mapping.save(silent=True)

    def to_csv(self, csv_path, *fields):
        """
        Copy current QuerySet to CSV at provided path.
        """
        query = self.query.clone(CopyToQuery)
        query.copy_to_fields = fields
        compiler = query.get_compiler(self.db, connection=connection)
        compiler.execute_sql(csv_path)


CopyManager = models.Manager.from_queryset(CopyQuerySet)


__all__ = (
    'CopyManager',
    'CopyMapping',
    'CopyQuerySet',
    'CopyToQuery',
    'SQLCopyToCompiler',
)
