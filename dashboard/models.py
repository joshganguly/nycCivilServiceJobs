from django.db import models
from register.models import User
from examresults.models import CivilServicesTitle
from django.core.validators import MaxValueValidator, MinValueValidator

# Create your models here.

"""We are using Civil Service title as means of subscription for Exam results in DB
That is a user can subscribe to an exam result by selecting civil service title"""


class ExamSubscription(models.Model):
    civil_service_title = models.ForeignKey(
        CivilServicesTitle, on_delete=models.CASCADE
    )
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    is_notified = models.BooleanField("is_notified", default=False)

    class Meta:
        unique_together = ("civil_service_title", "user")


class ExamResultsSubscription(models.Model):
    exam_number = models.IntegerField(
        validators=[MaxValueValidator(999999), MinValueValidator(1000)]
    )
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    is_notified = models.BooleanField("is_notified", default=False)

    class Meta:
        unique_together = ("exam_number", "user")
