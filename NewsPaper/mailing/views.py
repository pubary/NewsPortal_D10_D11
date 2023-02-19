from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, reverse, redirect
from django.template.loader import render_to_string
from django.views import View
from django.core.mail import EmailMultiAlternatives

from NewsPaper.settings import MY_MAIL, ADMIN1
from mailing.models import FeedbackMail


class FeedbackMailView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        return render(request, 'make_feedback_mail.html', {})

    def post(self, request, *args, **kwargs):
        mail = FeedbackMail(
            reader_name=request.POST['reader_name'],
            message=request.POST['message'],
        )
        mail.save()
        html_content = render_to_string(
            'feedback_answer_mail.html',
            {
                'mail': mail,
            }
        )
        msg = EmailMultiAlternatives(
            subject=f'Уведомление для {mail.reader_name}',
            body=mail.message,
            from_email=MY_MAIL,
            to=[request.user.email, ],
        )
        msg.attach_alternative(html_content, "text/html")
        msg.send()
        return redirect('user_home')


# function to test the view of the feedback email
def feedback_answer_mailview(request):
    mail = {'reader_name': 'имя_читателя',
            'message': 'текст сообщения от читателя',
            }
    return render(request, 'feedback_answer_mail.html', {'mail': mail, })

# function to test the view of the signup email
def signup_mailview(request):
    user = request.user
    return render(request, 'account/email/email_confirmation_signup_message.html', {'user': user})
