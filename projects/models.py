from django.db import models
from users.models import User
# Create your models here.
class Project(models.Model):
    name = models.CharField(max_length=100, null=False, blank=False)
    participants = models.ManyToManyField(User, related_name='projects', blank=True)
    admin_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='projects_managed',blank=False, null=False)
    description = models.CharField(max_length=200)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return self.name

    class Meta:
        db_table = 'project'
        verbose_name_plural = 'projects'