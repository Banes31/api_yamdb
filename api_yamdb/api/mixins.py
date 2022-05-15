from rest_framework.mixins import (
    CreateModelMixin,
    DestroyModelMixin,
    ListModelMixin
)
from rest_framework.viewsets import GenericViewSet


class CustomViewSet(
    CreateModelMixin,
    ListModelMixin,
    DestroyModelMixin,
    GenericViewSet
):
    """Кастомный базовый класс вьюсета.
    Он будет создавать экземпляр объекта, получать множество объектов,
    и удалять экземпляр объекта.
    """
    pass
