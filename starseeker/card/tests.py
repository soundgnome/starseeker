from django.test import TestCase
from .models import Card, CardBlock, CardMechanic, HeroClass, StandardYear, Tribe


class CardTestCase(TestCase):

    fixtures = (
        'card/fixtures/card_cardblock.json',
        'card/fixtures/card_cardmechanic.json',
        'card/fixtures/card_heroclass.json',
        'card/fixtures/card_tribe.json',
        'card/fixtures/card_card.json',
        'card/fixtures/card_standardyear.json',
    )

    def test_minion_attributes(self):
        card = Card.objects.get(card_id='CS2_182')
        self.assertEqual(card.name, 'Chillwind Yeti')
        self.assertEqual(card.cost, 4)
        self.assertEqual(card.attack, 4)
        self.assertEqual(card.health, 5)
        self.assertEqual(card.rarity, Card.Rarity.COMMON)
        self.assertEqual(card.card_type, Card.CardType.MINION)
        self.assertEqual(card.collectible, True)
        self.assertFalse(card.effect)


    def test_minion_references(self):
        card = Card.objects.get(card_id='EX1_319')

        block = CardBlock.objects.get(name='Classic')
        self.assertEqual(card.block.pk, block.pk)

        hero_class = HeroClass.objects.get(name='Warlock')
        self.assertEqual(card.hero_class.pk, hero_class.pk)

        tribe = Tribe.objects.get(name='Demon')
        self.assertEqual(card.tribe.pk, tribe.pk)

        self.assertTrue(card.mechanics.filter(name='Battlecry').exists())
        self.assertFalse(card.mechanics.filter(name='Charge').exists())


    def test_standard_membership(self):
        standard_year = StandardYear.objects.first()
        self.assertTrue(Card.objects.get(card_id='EX1_277').is_in_standard(standard_year))
        self.assertFalse(Card.objects.get(card_id='FP1_019').is_in_standard(standard_year))


    def test_weapon_attributes(self):
        card = Card.objects.get(card_id='DS1_188')
        self.assertEqual(card.name, "Gladiator's Longbow")
        self.assertEqual(card.cost, 7)
        self.assertEqual(card.attack, 5)
        self.assertEqual(card.health, 2)
        self.assertEqual(card.rarity, Card.Rarity.EPIC)
        self.assertEqual(card.card_type, Card.CardType.WEAPON)
        self.assertEqual(card.collectible, True)
        self.assertTrue(len(card.effect) > 0)
