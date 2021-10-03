from django.db import models

class Profile(models.Model):
    external_id = models.PositiveIntegerField(
        verbose_name='ID пользователя',
        unique=True,
    )

    name=models.TextField(
        verbose_name='Имя пользователя',
    )

    def __str__(self):
        return f'#{self.external_id} {self.name}'

    class Meta:
        verbose_name='Профиль'
        verbose_name_plural='Профили'

class ProfileSettings(models.Model):
    external= models.OneToOneField(
        to='Profile',
        verbose_name='ID пользователя',
        on_delete=models.PROTECT,
        to_field='external_id',
        unique=True,
    )

    api_key=models.CharField(
        verbose_name='API',
        max_length=64,
    )

    secret_key=models.CharField(
        verbose_name='SecretAPI',
        max_length=64,
    )

    subaccount_email=models.TextField(
        verbose_name='subaccount_email'
    )

    pool_username = models.TextField(
        verbose_name='pool_username'
    )

    class Meta:
        verbose_name='Настройки профиля'
        verbose_name_plural='Настройки профиля'