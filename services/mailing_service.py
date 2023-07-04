from django.core.mail import send_mail

from pages.models import Subscribe
from server.celery import app

from server.settings import EMAIL_HOST_USER

@app.task()
def notificate(author_id):
    subscribers = Subscribe.objects.filter(author__pk=author_id).select_related()
    for sub in  subscribers:
        send_mail(
        "New post from your favorite author!",
        f"Your author {sub.author.username} publicated new post! Check his profile!",
        EMAIL_HOST_USER,
        [str(sub.subscriber.email)],
        fail_silently=True,)

    return {'successful': True}