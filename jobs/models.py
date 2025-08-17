from django.db import models
# Create your models here.
from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _

User = get_user_model()


class Category(models.Model):
    name = models.CharField(max_length=100, unique=True, verbose_name=_("Category Name"))
    description = models.TextField(blank=True, verbose_name=_("Category Description"))

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _("Category")
        verbose_name_plural = _("Categories")

class GenderChoices(models.TextChoices):
    MALE = 'M', _("Male")
    FEMALE = 'F', _("Female")
    BOTH = 'B', _("Both")

class Job(models.Model):
    recruiter = models.ForeignKey(User, on_delete=models.CASCADE, related_name='jobs')
    title = models.CharField(max_length=255, verbose_name=_("Job Title"))
    description = models.TextField(verbose_name=_("Job Description"))
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='jobs', verbose_name=_("Job Category"))
    location = models.CharField(max_length=255, blank=True, verbose_name=_("Job Location"))
    salary = models.DecimalField(max_digits=10, decimal_places=2, blank=True, verbose_name=_("Job Salary"))
    gender = models.CharField(
        max_length=1,
        choices=GenderChoices.choices,
        default=GenderChoices.BOTH,
        verbose_name=_("Job Gender")
    )
    responsibilities = models.TextField(blank=True, verbose_name=_("Job Responsibilities"))

    class Meta:
        verbose_name = _("Job")
        verbose_name_plural = _("Jobs")
        ordering = ['-id']

    def __str__(self):
        return f"{self.title} - {self.category.name} ({self.recruiter.username})"

