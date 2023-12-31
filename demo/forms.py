from django import forms


class LoginForm(forms.Form):
    input_tailwind_classes = "text-gray-700 w-full rounded py-3 px-2 border border-gray-200"

    username = forms.CharField(max_length=65, widget=forms.TextInput(
        attrs={"class": input_tailwind_classes}))
    password = forms.CharField(max_length=65, widget=forms.PasswordInput(
        attrs={"class": input_tailwind_classes}))
