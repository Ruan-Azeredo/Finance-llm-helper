"""Peewee migrations -- 001_initial.py.

Some examples (model - class or model name)::

    > Model = migrator.orm['table_name']            # Return model in current state by name
    > Model = migrator.ModelClass                   # Return model in current state by name

    > migrator.sql(sql)                             # Run custom SQL
    > migrator.run(func, *args, **kwargs)           # Run python function with the given args
    > migrator.create_model(Model)                  # Create a model (could be used as decorator)
    > migrator.remove_model(model, cascade=True)    # Remove a model
    > migrator.add_fields(model, **fields)          # Add fields to a model
    > migrator.change_fields(model, **fields)       # Change fields
    > migrator.remove_fields(model, *field_names, cascade=True)
    > migrator.rename_field(model, old_field_name, new_field_name)
    > migrator.rename_table(model, new_table_name)
    > migrator.add_index(model, *col_names, unique=False)
    > migrator.add_not_null(model, *field_names)
    > migrator.add_default(model, field_name, default)
    > migrator.add_constraint(model, name, sql)
    > migrator.drop_index(model, *col_names)
    > migrator.drop_not_null(model, *field_names)
    > migrator.drop_constraints(model, *constraints)

"""

from contextlib import suppress

import peewee as pw
from peewee_migrate import Migrator
import datetime

with suppress(ImportError):
    import playhouse.postgres_ext as pw_pext


def migrate(migrator: Migrator, database: pw.Database, *, fake=False):
    """Write your migrations here."""

    @migrator.create_model
    class User(pw.Model):
        id = pw.AutoField()
        name = pw.CharField(max_length=255)
        email = pw.CharField(max_length=255, unique=True)
        password = pw.CharField(max_length=255)
        role = pw.CharField(default='free', max_length=255)
        created_at = pw.DateTimeField(default=datetime.datetime.now())
        updated_at = pw.DateTimeField(default=datetime.datetime.now())

        class Meta:
            table_name = "users"

    @migrator.create_model
    class Transaction(pw.Model):
        id = pw.CharField(max_length=255, primary_key=True)
        date = pw.CharField(max_length=255)
        direction = pw.CharField(default='expense', max_length=255)
        amount = pw.CharField(max_length=255)
        memo = pw.CharField(max_length=255)
        user_id = pw.ForeignKeyField(column_name='user_id', field='id', model=migrator.orm['users'], on_delete='CASCADE')
        tag = pw.CharField(max_length=255, null=True)
        created_at = pw.DateTimeField(default=datetime.datetime.now())
        updated_at = pw.DateTimeField(default=datetime.datetime.now())

        class Meta:
            table_name = "transactions"


def rollback(migrator: Migrator, database: pw.Database, *, fake=False):
    """Write your rollback migrations here."""
    
    migrator.remove_model('users')

    migrator.remove_model('transactions')
