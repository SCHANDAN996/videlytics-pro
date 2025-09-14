from allauth.account.forms import LoginForm, SignupForm
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit

class CustomLoginForm(LoginForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_class = 'space-y-6'
        # यहाँ हम इस फ़ॉर्म को बता रहे हैं कि Tailwind का इस्तेमाल करो
        self.helper.template_pack = "tailwind" 
        self.helper.form_show_labels = False
        self.helper.layout = Layout(
            'login',
            'password',
            'remember'
        )

class CustomSignupForm(SignupForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_class = 'space-y-6'
         # यहाँ हम इस फ़ॉर्म को बता रहे हैं कि Tailwind का इस्तेमाल करो
        self.helper.template_pack = "tailwind"
        self.helper.form_show_labels = False
        self.helper.layout = Layout(
            'email',
            'password',
            'password2'
        )
