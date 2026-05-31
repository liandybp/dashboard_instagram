"""Exportaciones del paquete de pestañas del dashboard."""

from src.components.tabs.base_tab import BaseTab
from src.components.tabs.metrics_tab import MetricsTab
from src.components.tabs.health_tab import HealthTab
from src.components.tabs.audience_tab import AudienceTab
from src.components.tabs.posts_tab import PostsTab
from src.components.tabs.best_time_tab import BestTimeTab
from src.components.tabs.frequency_tab import FrequencyTab
from src.components.tabs.ideas_tab import IdeasTab

__all__ = [
    "BaseTab",
    "MetricsTab",
    "HealthTab",
    "AudienceTab",
    "PostsTab",
    "BestTimeTab",
    "FrequencyTab",
    "IdeasTab",
]

