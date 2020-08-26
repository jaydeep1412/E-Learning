from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
import datetime
from django.contrib.auth.models import User
from django.utils import timezone


# Create your models here.

class Topic(models.Model):
    name = models.CharField(max_length=200)
    category = models.CharField(max_length=200, blank=False, default='Dev')

    def __str__(self):
        return '%s' % self.name


class Course(models.Model):
    topic = models.ForeignKey(Topic, related_name='courses', on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    price = models.DecimalField(max_digits=10, decimal_places=2, validators=[MaxValueValidator(200), MinValueValidator(100)])
    for_everyone = models.BooleanField(default=True)
    interested = models.PositiveIntegerField(default=0)
    stages = models.PositiveIntegerField(default=3)
    description = models.TextField(max_length=300, null=True, blank=True)

    def __str__(self):
        return '%s %s' % (self.name, self.description)

    def discount(self):
        self.price -= (0.1 * self.price)
        return self.price


class Student(User):
    CITY_CHOICES = [('WS', 'Windsor'), ('CG', 'Calgery'), ('MR', 'Montreal'), ('VC', 'Vancouver')]
    school = models.CharField(max_length=50, null=True, blank=True)
    city = models.CharField(max_length=2, choices=CITY_CHOICES, default='WS')
    interested_in = models.ManyToManyField(Topic)
    photo = models.ImageField(upload_to='images/')

    def __str__(self):
        return '%s %s' % (self.first_name, self.last_name)


class Order(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    levels = models.PositiveIntegerField()
    order_choice = [(0, 'Cancelled'), (1, 'Order Confirmed')]
    order_status = models.IntegerField(choices=order_choice, default=1)
    order_date = models.DateField()

    def total_cost(self):
        return '%s' % (sum(item for item in self.course.price))

    def __str__(self):
        return '%s %s' % (self.course, self.student)
