# Generated by Django 3.1.2 on 2020-10-24 23:32

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="ExamResultsActive",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("exam_number", models.IntegerField(null=True)),
                ("list_number", models.FloatField(null=True)),
                ("first_name", models.CharField(max_length=30)),
                ("last_name", models.CharField(max_length=30)),
                (
                    "middle_initial",
                    models.CharField(blank=True, max_length=30, null=True),
                ),
                ("adjust_final_average", models.FloatField(null=True)),
                ("list_title_code", models.IntegerField(null=True)),
                (
                    "list_title_desc",
                    models.CharField(blank=True, max_length=250, null=True),
                ),
                ("group_number", models.IntegerField(null=True)),
                ("list_agency_code_promo", models.IntegerField(null=True)),
                (
                    "list_agency_code_promo_desc",
                    models.CharField(blank=True, max_length=250, null=True),
                ),
                (
                    "list_div_code_promo",
                    models.CharField(blank=True, max_length=30, null=True),
                ),
                ("published_date", models.DateTimeField(null=True)),
                ("established_date", models.DateTimeField(null=True)),
                ("anniversary_date", models.DateTimeField(null=True)),
                ("extention_date", models.DateTimeField(null=True)),
                (
                    "veteran_credit",
                    models.CharField(blank=True, max_length=100, null=True),
                ),
                (
                    "parent_legacy_credit",
                    models.CharField(blank=True, max_length=100, null=True),
                ),
                (
                    "sibling_legacy_credit",
                    models.CharField(blank=True, max_length=100, null=True),
                ),
                (
                    "residency_credit",
                    models.CharField(blank=True, max_length=100, null=True),
                ),
            ],
            options={
                "verbose_name_plural": "Exam Results(Active)",
            },
        ),
        migrations.CreateModel(
            name="ExamResultsTerminated",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("exam_number", models.IntegerField(null=True)),
                ("list_title_code", models.IntegerField(null=True)),
                (
                    "list_title_desc",
                    models.CharField(blank=True, max_length=250, null=True),
                ),
            ],
            options={
                "verbose_name_plural": "Exam Results(Terminated)",
            },
        ),
    ]