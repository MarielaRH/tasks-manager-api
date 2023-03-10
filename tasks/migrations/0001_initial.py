# Generated by Django 4.1.7 on 2023-02-20 21:28

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('projects', '0002_alter_project_participants'),
        ('categories', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Tasks',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('description', models.CharField(max_length=200)),
                ('status', models.CharField(choices=[('PI', 'Por inciar'), ('EP', 'En proceso'), ('FN', 'Finalizada')], default='PI', max_length=2)),
                ('creatd_at', models.DateTimeField(auto_now_add=True)),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='tasks', to='categories.category')),
                ('project', models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, related_name='tasks', to='projects.project')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='tasks', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name_plural': 'tasks',
                'db_table': 'task',
            },
        ),
    ]
