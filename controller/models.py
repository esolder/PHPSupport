from django.db import models
from django.db.models.signals import pre_save, pre_delete
from django.dispatch import receiver
from django.utils import timezone

class Client(models.Model):
    username = models.CharField('Уникальное имя пользователя telegram',
                                max_length=32,
                                unique=True)
    subscription_end = models.DateField('Дата окончания подписки')

    def __str__(self):
        return self.username
    
    class Meta:
        verbose_name = 'Клиент'
        verbose_name_plural = 'Клиенты'
    

class Executor(models.Model):
    username = models.CharField('Уникальное имя пользователя telegram',
                                max_length=32,
                                unique=True)
    
    def delete(self, *args, **kwargs):
        orders = Order.objects.filter(executor=self)
        orders.update(
            executor=None,
            executor_tg_id=None,
            questions='',
            answers='',
            is_taken=False,
            estimate=None,
        )
        super(Executor, self).delete(*args, **kwargs)
    
    def __str__(self):
        return self.username
    
    class Meta:
        verbose_name = 'Подрядчик'
        verbose_name_plural = 'Подрядчики'


class Rate(models.Model):
    rate = models.DecimalField('Ставка за заказ в рублях', max_digits=10, decimal_places=2)
    when_set = models.DateTimeField('Когда установлена ставка', auto_now_add=True)

    def __str__(self):
        return f'{self.rate} р.'
    
    class Meta:
        verbose_name = 'Ставка за заказ'
        verbose_name_plural = 'Ставки за заказы'
        ordering = ['-when_set']


class Order(models.Model):
    client = models.ForeignKey(Client, 
                               on_delete=models.CASCADE,
                               related_name='orders',
                               verbose_name='Клиент')
    client_tg_id = models.IntegerField('ID клиента в telegram',
                                        blank=True,
                                        null=True)
    creation_date = models.DateField('Дата создания заказа', auto_now_add=True)
    executor = models.ForeignKey(Executor, 
                                 on_delete=models.SET_NULL,
                                 null=True,
                                 blank=True,
                                 related_name='orders',
                                 verbose_name='Подрядчик')
    executor_tg_id = models.IntegerField('ID подрядчика в telegram',
                                        blank=True,
                                        null=True)
    is_taken = models.BooleanField('Заказ взят',
                                   default=False)
    is_complete = models.BooleanField('Заказ выполнен',
                                      default=False)
    rate = models.ForeignKey(Rate, 
                             on_delete=models.PROTECT,
                             blank=True,
                             verbose_name='Ставка за заказ',
                             related_name='orders')
    estimate = models.CharField('Оценка времени выполнения заказа',
                                max_length=100,
                                blank=True,
                                null=True)
    complete_date = models.DateField('Дата закрытия заказа',
                                     blank=True,
                                     null=True)
    
    text = models.TextField('Текст заказа')
    credentials = models.TextField('Данные от админки', blank=True, null=True)
    questions = models.TextField('Вопросы от подрядчика', blank=True, null=True)
    answers = models.TextField('Ответы от клиента', blank=True, null=True)

    def save(self, *args, **kwargs):
        if not self.pk:
            latest_rate = Rate.objects.latest('when_set')
            self.rate = latest_rate
        super().save(*args, **kwargs)

    def __str__(self):
        return f'Заказ {self.id} от {self.client}'
    
    class Meta:
        verbose_name = 'Заказ'
        verbose_name_plural = 'Заказы'


@receiver(pre_save, sender=Order)
def set_complete_date(sender, instance, **kwqrgs):
    if instance.is_complete:
        instance.complete_date = timezone.now().date()


@receiver(pre_delete, sender=Executor)
def executor_delete_handler(sender, instance, **kwargs):
    orders = instance.orders.filter(is_taken=True)
    orders.update(is_taken=False, estimate='')
