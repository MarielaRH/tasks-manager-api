from django.db import models
from categories.models import Category
from projects.models import Project
from users.models import User

# Create your models here.
class Task(models.Model):
    STATUS_TASKS = [('PI', 'Por inciar'),('EP', 'En proceso'),('FN', 'Finalizada')]
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='tasks')
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='tasks')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='tasks')
    name = models.CharField(max_length=100, null=False ,blank=False)
    description = models.CharField(max_length=200)
    status = models.CharField(choices=STATUS_TASKS, default='PI', max_length=2)
    creatd_at = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return self.name

    class Meta:
        db_table = 'task'
        verbose_name_plural = 'tasks'