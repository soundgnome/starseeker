from enumfields import Enum, EnumIntegerField
from django.db import models


class CardBlock(models.Model):

    class BlockType(Enum):
        CORE = 0
        EXPANSION = 1
        ADVENTURE = 2
        SPECIAL = 3

    name = models.CharField(max_length=255, unique=True)
    slug = models.CharField(max_length=255, unique=True)
    block_type = EnumIntegerField(BlockType)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ('name',)


class CardMechanic(models.Model):
    name = models.CharField(max_length=255, unique=True)
    slug = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ('name',)


class HeroClass(models.Model):
    name = models.CharField(max_length=255, unique=True)
    slug = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = 'Hero classes'
        ordering = ('name',)


class Tribe(models.Model):
    name = models.CharField(max_length=255, unique=True)
    slug = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ('name',)


class Card(models.Model):

    class Rarity(Enum):
        FREE = 0
        COMMON = 1
        RARE = 2
        EPIC = 3
        LEGENDARY = 4

    class CardType(Enum):
        MINION = 0
        SPELL = 1
        WEAPON = 2

    card_id = models.CharField(max_length=255, unique=True)
    name = models.CharField(max_length=255)
    rarity = EnumIntegerField(Rarity)
    block = models.ForeignKey(CardBlock, on_delete=models.CASCADE)
    hero_class = models.ForeignKey(HeroClass, on_delete=models.CASCADE, blank=True, null=True)
    card_type = EnumIntegerField(CardType)
    cost = models.IntegerField()
    attack = models.IntegerField(blank=True, null=True)
    health = models.IntegerField(blank=True, null=True)
    effect = models.CharField(max_length=255, blank=True, default='')
    tribe = models.ForeignKey(Tribe, blank=True, null=True)
    mechanics = models.ManyToManyField(CardMechanic)
    collectible = models.BooleanField(default=True)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ('name',)
