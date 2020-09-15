from __future__ import unicode_literals
from django.contrib.auth.models import User, BaseUserManager, AbstractBaseUser
from django.db import models
from django.db.models.signals import pre_save
from django.urls import reverse
from django.utils import timezone
from django.utils.text import slugify

from .utils import unique_slug_generator


class MyUserManager(BaseUserManager):
    def create_user(self, username, email, password):
        if not username:
            raise ValueError('Users must have a user name')
        if not email:
            raise ValueError('User must have a valid email address')
        user = self.model(
            username=username,
            email=self.normalize_email(email),
        )
        user.is_admin = False
        user.is_employee = False
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, email, password):
        user = self.create_user(username, email, password=password)
        user.is_admin = True
        user.is_employee = True
        user.save(using=self._db)
        return user


class MyUser(AbstractBaseUser):
    username = models.CharField(verbose_name='username', max_length=100, unique=True, )
    email = models.EmailField()
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)
    is_employee = models.BooleanField(default=False)
    objects = MyUserManager()
    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email']

    def __str__(self):
        return self.username

    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, app_label):
        return True

    @property
    def is_staff(self):
        return self.is_admin


class Team(models.Model):
    name = models.CharField(verbose_name='team_name', max_length=30, unique=True, )
    description = models.TextField()
    added_by = models.ForeignKey(MyUser, on_delete=models.CASCADE)
    slug = models.SlugField(blank=True)

    def __str__(self):
        return self.name

    def delete(self, *args, **kwargs):
        super(Team, self).delete(*args, **kwargs)


def pre_save_team_slug(sender, instance, *args, **kwargs):
    if not instance.slug:
        slug = slugify(instance.name)
        instance.slug = slug


pre_save.connect(pre_save_team_slug, sender=Team)


class PlayedGames(models.Manager):
    def all(self, *args, **kwargs):
        return super(PlayedGames, self).get_queryset().filter(game_is_played=True)


class Contest(models.Model):
    contest_date = models.DateField(blank=True)
    contest_started = models.BooleanField(default=False)
    contest_completed = models.BooleanField(default=False)
    slug = models.SlugField(max_length=32, unique=True, editable=True)
    start_time = models.TimeField(default="09:00:00")
    game_length = models.IntegerField(default=10)
    pauza_length = models.IntegerField(default=5)

    def __str__(self):
        return "Contest date: " + (self.contest_date).__str__()

    def delete(self, *args, **kwargs):
        super(Contest, self).delete(*args, **kwargs)


def pre_save_contest_slug(sender, instance, *args, **kwargs):
    if not instance.slug:
        slug = unique_slug_generator(sender, instance)
        instance.slug = slug


pre_save.connect(pre_save_contest_slug, sender=Contest)


class PlayedGames(models.Manager):
    def all(self, *args, **kwargs):
        # return super(PlayedGames, self).get_queryset().filter(game_is_played=False)
        return super(PlayedGames, self).get_queryset().filter(game_is_played=False)


class Game(models.Model):
    contest = models.ForeignKey(Contest, on_delete=models.CASCADE)
    team_a = models.ForeignKey(Team, related_name='name_a', on_delete=models.CASCADE)
    team_b = models.ForeignKey(Team, related_name='name_b', on_delete=models.CASCADE)
    score_team_a = models.IntegerField(default=0)
    score_team_b = models.IntegerField(default=0)
    game_is_started = models.BooleanField(default=False)
    game_is_played = models.BooleanField(default=False)
    # in game_result field following values are possible:
    # 1: team_a is a winner
    # 2: team_b is a winner
    # 3: draw
    game_result = models.IntegerField(null=True, blank=True)
    slug = models.SlugField(max_length=32, unique=True, editable=True)
    game_time = models.TimeField(default=timezone.now().time(), blank=False)

    # objects = PlayedGames()

    def __str__(self):
        return self.contest.contest_date.__str__() + " " + (self.game_time).__str__() + " " \
               + self.team_a.name + " vs " + self.team_b.name

    def delete(self, *args, **kwargs):
        super(Game, self).delete(*args, **kwargs)


def pre_save_game_slug(sender, instance, *args, **kwargs):
    if not instance.slug:
        slug = unique_slug_generator(sender, instance)
        instance.slug = slug


pre_save.connect(pre_save_game_slug, sender=Game)


class Bet(models.Model):
    game = models.ForeignKey(Game, on_delete=models.CASCADE)
    user = models.ForeignKey(MyUser, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    team_a_win = models.BooleanField(default=False, blank=True)
    team_b_win = models.BooleanField(default=False, blank=True)
    draw = models.BooleanField(default=False, blank=True)

    def __str__(self):
        return self.game.contest.contest_date.__str__() + " @" + self.game.game_time.__str__() \
               + " " + self.game.team_a.name + " play against " + self.game.team_b.name \
               + " Bet amount: EUR " + self.amount.__str__()

    def delete(self, *args, **kwargs):
        super(Bet, self).delete(*args, **kwargs)
