from django import forms

class LoginForm(forms.Form):
    input_tailwind_classes = "text-black bg-neutral-200 dark:text-white dark:bg-neutral-600 w-full rounded"

    username = forms.CharField(max_length=65, widget=forms.TextInput(attrs={"class": input_tailwind_classes}))
    password = forms.CharField(max_length=65, widget=forms.PasswordInput(attrs={"class": input_tailwind_classes}))