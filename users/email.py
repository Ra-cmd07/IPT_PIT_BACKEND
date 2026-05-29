from djoser import email
from django.conf import settings


class CustomActivationEmail(email.ActivationEmail):
    template_name = "emails/activation.html"

    def get_context_data(self):
        context = super().get_context_data()

        # Override the url — ACTIVATION_URL in settings already has the
        # full frontend URL, so we bypass Djoser prepending the backend domain.
        activation_url = settings.DJOSER.get('ACTIVATION_URL', '')
        uid = context.get('uid')
        token = context.get('token')

        if uid and token and activation_url:
            context['url'] = activation_url.format(uid=uid, token=token)

        return context