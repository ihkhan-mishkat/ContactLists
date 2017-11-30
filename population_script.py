import os

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings.dev")

import django
django.setup()

from django.contrib.auth import get_user_model

from apps.contacts.models import Contact

User = get_user_model()


def populate():
    user = add_user('I.H.', 'Khan', 'ihkhan',
                    'ihkhan.mishkat@gmail.com', 'password')
    add_contact('abc', user, 'abc@abc.com', '+880170000000',
                'Mirpur, Dhaka')
    add_contact('zxc', user)

    user = add_user('Mishkat', 'Khan', 'mkhan',
                    'mkhan@mkhan.com', 'password')
    add_contact('qwe', user, 'qwe@qwe.com', '+880190000000',
                'Dhanmondi, Dhaka')
    add_contact('jkl', user)


def add_user(first_name, last_name, username, email, password):
    user = User.objects.get_or_create(
        first_name=first_name, last_name=last_name,
        username=username, email=email)[0]
    user.set_password(password)
    user.save()
    return user


def add_contact(name, user, email='', phone='', address=''):
    contact = Contact.objects.get_or_create(
        name=name, email=email, phone=phone,
        address=address, user=user)[0]
    contact.save()
    return contact


def print_db():
    """
    Print what we have
    """
    for user in User.objects.all():
        for contact in user.contact_set.all():
            print("User: {} -- Contact: {}".format(user, contact))


if __name__ == '__main__':
    print("Starting to populate DB...\n")
    populate()
    print_db()
