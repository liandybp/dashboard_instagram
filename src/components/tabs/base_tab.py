"""Clase base abstracta para todas las pestañas del dashboard."""

from abc import ABC, abstractmethod


class BaseTab(ABC):
    """
    Clase base abstracta que define el contrato para todas las pestañas del dashboard.
    Cada pestaña debe heredar de esta clase e implementar `label` y `render()`.
    """

    def __init__(self, data: dict):
        """
        Args:
            data: Diccionario con todos los datos cargados por load_account_data().
        """
        self.data = data

    @property
    @abstractmethod
    def label(self) -> str:
        """Texto con emoji que aparece en la pestaña, ej: '📈 Métricas'."""
        ...

    @abstractmethod
    def render(self) -> None:
        """Renderiza el contenido completo de la pestaña usando st.*"""
        ...

