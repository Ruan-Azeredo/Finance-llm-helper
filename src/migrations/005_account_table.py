"""Peewee migrations -- 005_account_table.py.

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

from datetime import datetime, timezone


with suppress(ImportError):
    import playhouse.postgres_ext as pw_pext


def migrate(migrator: Migrator, database: pw.Database, *, fake=False):
    """Write your migrations here."""
    
    @migrator.create_model
    class Month(pw.Model):
        id = pw.AutoField(unique = True, primary_key = True)
        name = pw.CharField(null = False)
        user_id = pw.ForeignKeyField(column_name='user_id', field='id', model=migrator.orm['users'], on_delete='CASCADE')
        balance = pw.FloatField(default = 0)
        balance_updated = pw.IntegerField(default = datetime.now(timezone.utc).timestamp())
        origin = pw.CharField(default = "default")
        created_at = pw.DateTimeField(default = datetime.now())
        updated_at = pw.DateTimeField(default = datetime.now())

        class Meta:
            table_name = "accounts"

    migrator.sql("""
        ALTER TABLE "transactions"
        ADD COLUMN "account_id" INTEGER REFERENCES "accounts" ("id") ON DELETE CASCADE;
    """)
    
    migrator.sql("""
        ALTER TABLE "users"
        ADD COLUMN "default_account_id" VARCHAR;
    """)


def rollback(migrator: Migrator, database: pw.Database, *, fake=False):
    """Write your rollback migrations here."""
    
    migrator.remove_model('accounts')

    migrator.sql("""
        ALTER TABLE "transactions"
        DROP COLUMN "account_id";
    """)
    
    migrator.sql("""
        ALTER TABLE "users"
        DROP COLUMN "default_account_id";
    """)

