from django.dispatch import receiver
from allauth.account.signals import user_signed_up
from allauth.exceptions import ImmediateHttpResponse
from allauth.socialaccount.adapter import DefaultSocialAccountAdapter


class HubAccountAdapter(DefaultSocialAccountAdapter):

    def pre_social_login(self, request, sociallogin):
        u = sociallogin.account.user

        if not u.email.split('@')[1] in ['luizalabs.com', 'magazineluiza.com.br']:
            raise ImmediateHttpResponse('Invalid domain')


@receiver(user_signed_up)
def user_signed_up_(request, user, sociallogin=None, **kwargs):
    '''
    When a social account is created successfully and this signal
    is received, django-allauth passes in the sociallogin param,
    giving access to metadata on the remote account, e.g.:

    sociallogin.account.provider  # e.g. 'twitter'
    sociallogin.account.get_avatar_url()
    sociallogin.account.get_profile_url()
    sociallogin.account.extra_data['screen_name']

    See the socialaccount_socialaccount table for more in the 'extra_data' field.
    '''
    if sociallogin:
        if sociallogin.account.provider == 'google':
            user.name = sociallogin.account.extra_data['name']

        user.save()
