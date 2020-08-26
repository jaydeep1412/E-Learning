from django import forms
from myapp.models import Order, Student


class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['student', 'course', 'levels', 'order_date']
        widgets = {
            'student': forms.RadioSelect,
            'order_date': forms.SelectDateWidget
        }


class InterestForm(forms.Form):
    choices = (('Yes', 'Yes'), ('No', 'No'))
    interested = forms.ChoiceField(
        choices=choices,
        widget=forms.RadioSelect
    )
    levels = forms.IntegerField(min_value=1, initial=1)
    comments = forms.CharField(
        required=False,
        widget=forms.Textarea,
        label='Additional Comments'
    )

class RegisterForm(forms.ModelForm):
    class Meta:
        model = Student
        fields = ('username','password','first_name','last_name','city','interested_in','photo')
        required = ('username','password','first_name','city')
        widgets = {
            'password': forms.PasswordInput,
            'city': forms.RadioSelect
        }

class ForgotPassword(forms.Form):
    email = forms.EmailField(label='Enter your Email address', required=True)