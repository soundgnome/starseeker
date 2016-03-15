import json
from urllib.error import HTTPError
from urllib.request import urlopen

from django.core.management.base import BaseCommand
from card.models import Card, CardBlock, CardMechanic, HeroClass, Tribe


class Command(BaseCommand):
    help = 'Pulls list of all cards from external source and updates local database'


    def add_arguments(self, parser):
        parser.add_argument('url', type=str)


    def handle(self, *args, **options):

        try:
            cards = self._get_cards_from_url(options['url'])
        except HTTPError as error:
            self._say(error)
            return

        errors = []
        for card in cards:
            success = self._add_or_update_card(card)
            if not success:
                errors.append(card['id'])

        if len(errors):
            self._say('Errors were encounered with: %s' % ', '.join(errors))


    def _add_or_update_card(self, card_dict):
        if card_dict['type'] == 'HERO':
            self._say('skipping %s' % card_dict['name'])
            return True

        refs = self._get_referenced_objects(card_dict)
        if not refs:
            return

        card = Card.objects.get_or_create(card_id = card_dict['id'])[0]
        card.name = card_dict['name']
        card.rarity = getattr(Card.Rarity, card_dict['rarity'])
        card.block = refs['block']
        card.hero_class = refs['hero_class']
        card.card_type = getattr(Card.CardType, card_dict['type'])
        card.cost = card_dict['cost']
        card.attack = self._safe_get(card_dict, 'attack')
        card.health = self._safe_get(card_dict, 'health|durability')
        card.effect = self._safe_get(card_dict, 'text', '')
        card.tribe = refs['tribe']
        card.collectible = card_dict['collectible']

        card.mechanics.clear()
        if refs['mechanics']:
            for mechanic in refs['mechanics']:
                card.mechanics.add(mechanic)

        card.save()
        self._say('refreshed %s (%s)' % (card_dict['name'], card_dict['id']))

        return True


    def _get_cards_from_url(self, url):
        response = urlopen(url)
        content = response.read().decode()
        cards = json.loads(content)
        return cards


    def _get_referenced_objects(self, card):
        refs = {}

        try:
            refs['block'] = CardBlock.objects.get(slug=card['set'])

            if 'playerClass' in card:
                refs['hero_class'] = HeroClass.objects.get(slug=card['playerClass'])
            else:
                refs['hero_class'] = None

            if 'race' in card:
                refs['tribe'] = self._get_or_create(Tribe, card['race'])
            else:
                refs['tribe'] = None

            refs['mechanics'] = []
            if 'mechanics' in card:
                for mechanic in card['mechanics']:
                    refs['mechanics'].append(self._get_or_create(CardMechanic, mechanic))

        except (CardBlock.DoesNotExist, HeroClass.DoesNotExist):
            return

        return refs


    def _get_or_create(self, klass, slug):
        try:
            instance = klass.objects.get(slug=slug)
        except klass.DoesNotExist:
            instance = klass.objects.create()
            instance.name = slug
            instance.slug = slug
            instance.save()
        return instance


    def _safe_get(self, dict, key, default=None):
        keys = key.split('|')
        for key in keys:
            if key in dict:
                return dict[key]
        return default


    def _say(self, message):
        print(message)
