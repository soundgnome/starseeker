from django.test import TestCase
from .models import Card, CardBlock, CardMechanic, HeroClass, Tribe


class CardTestCase(TestCase):

    fixtures = (
        'card/fixtures/card_cardblock.json',
    )

    def test_minion_attributes(self):
        card = Card.objects.get(card_id='CS2_182')
        self.assertEqual(card.name, 'Chillwind Yeti')
        self.assertEqual(card.cost, 4)
        self.assertEqual(card.attack, 4)
        self.assertEqual(card.health, 5)
        self.assertEqual(card.rarity, Card.Rarity.COMMON)
        self.assertEqual(card.card_type, Card.Type.MINION)
        self.assertEqual(card.collectible, True)
        self.assertIsNone(card.effect)


    def test_minion_references(self):
        card = Card.objects.get(card_id='EX1_319')

        block = Block.objects.get(name='Classic')
        self.assertEqual(card.block.pk, block.pk)

        hero_class = HeroClass.objects.get(name='Warlock')
        self.assertEqual(card.hero_class.pk, hero_class.pk)

        tribe = Tribe.objects.get(name='Demon')
        self.assertEqual(card.tribe.pk, tribe.pk)

        has_mechanic = False
        card_mechanic = CardMechanic.objects.get(name='Battlecry')
        for mechanic in card.mechanics:
            if mechanic.pk == card_mechanic.pk:
                has_mechanic = True
                break
        self.assertTrue(has_mechanic)


    def test_weapon_attributes(self):
        card = Card.objects.get(card_id='DS1_188')
        self.assertEqual(card.name, "Gladiator's Longbow")
        self.assertEqual(card.cost, 7)
        self.assertEqual(card.attack, 5)
        self.assertEqual(card.health, 2)
        self.assertEqual(card.rarity, Card.Rarity.EPIC)
        self.assertEqual(card.type, Card.Type.WEAPON)
        self.assertEqual(card.collectible, True)
        self.assertTrue(len(card.effect) > 0)
