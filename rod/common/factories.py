import factory

from rod.common.models import RandomModel
from rod.common.models import SimpleModel
from rod.common.utils import faker


class RandomModelFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = RandomModel

    end_date = factory.LazyAttribute(lambda self: faker.date_object())
    start_date = factory.LazyAttribute(
        lambda self: faker.date_object(end_datetime=self.end_date),
    )


class SimpleModelFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = SimpleModel

    name = factory.LazyAttribute(lambda self: faker.word())
