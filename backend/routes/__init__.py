"""Routes package"""
from .health import register_health_routes
from .analysis import register_analysis_routes

__all__ = ['register_health_routes', 'register_analysis_routes']
