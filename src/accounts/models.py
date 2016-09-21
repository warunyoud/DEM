from __future__ import unicode_literals
from django.db import models
from django.contrib.auth.models import (
    BaseUserManager, AbstractBaseUser
)
from django.db.models.signals import post_save
from django.utils.text import slugify
from datetime import date
from django.core.urlresolvers import reverse


class MyUserManager(BaseUserManager):
    def create_user(self, username=None, email=None, date_of_birth=None, password=None):
        """
        Creates and saves a User with the given email, date of
        birth and password.
        """
        if not username:
        	raise ValueError('Must include username')
        if not email:
            raise ValueError('Users must have an email address')

        user = self.model(
        	username = username,
            email=self.normalize_email(email),
            date_of_birth=date_of_birth,
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, email, date_of_birth, password):
        """
        Creates and saves a superuser with the given username, email, date of
        birth and password.
        """
        user = self.create_user(
        	username=username,
        	email=email,
        	date_of_birth=date_of_birth,
            password=password,
        )
        user.is_admin = True
        user.save(using=self._db)
        return user


class MyUser(AbstractBaseUser):
	username = models.CharField(
		max_length=255,
		unique=True,
	)
	email = models.EmailField(
	    verbose_name='email address',
	    max_length=255,
	    unique=True,
	)
	first_name = models.CharField(
		max_length = 120,
		null = True,
		blank = True,
	)
	last_name = models.CharField(
		max_length = 120,
		null = True,
		blank = True,
	)
	date_of_birth = models.DateField()

	is_active = models.BooleanField(default=True)
	is_admin = models.BooleanField(default=False)
	slug = models.SlugField(unique=True, blank = True, null = True)


	objects = MyUserManager()

	USERNAME_FIELD = 'username'
	REQUIRED_FIELDS = ['email', 'date_of_birth']

	def get_short_name(self):
	    # The user is identified by their email address
	    return self.email

	def __str__(self):              # __unicode__ on Python 2
	    return self.username

	def has_perm(self, perm, obj=None):
	    "Does the user have a specific permission?"
	    # Simplest possible answer: Yes, always
	    return True

	def has_module_perms(self, app_label):
	    "Does the user have permissions to view the app `app_label`?"
	    # Simplest possible answer: Yes, always
	    return True
	    
	def get_absolute_url(self):
		return reverse('account_detail', kwargs={'slug': self.slug})

	@property
	def is_staff(self):
	    "Is the user a member of staff?"
	    # Simplest possible answer: All admins are staff
	    return self.is_admin


class UserProfile(models.Model):
	user = models.OneToOneField(MyUser, related_name = 'profile')
	image = models.ImageField(null = True, upload_to = 'images/profile')
	description = models.CharField(max_length = 144, null = True, blank = True)
	connections = models.ManyToManyField('self', blank = True) 

	def __str__(self):
		return self.user.username

	@property
	def full_name(self):
		return "%s %s" %(self.user.first_name, self.user.last_name)

	@property
	def image_url(self):
		if self.image:
			return self.image.url
		else:
			return "../../static/img/avatar-dhg.png"

	@property
	def age(self):
		today = date.today()
		born = self.user.date_of_birth
		return today.year - born.year - ((today.month, today.day) < (born.month, born.day))


	def first_name(self):
		return self.user.first_name

	def last_name(self):
		return self.user.last_name


def new_user_receiver(sender, instance, created, *args, **karg):
	if created:
		new_profile = UserProfile.objects.get_or_create(user=instance)
		instance.slug = slugify(instance.username)
		instance.save()

		#merchant account 
		#send email for verifying user email

post_save.connect(new_user_receiver, sender = MyUser)