"""
Initialize the HBnBFacade service layer.

This module creates a singleton instance of the HBnBFacade,
which provides unified access to the application's core services,
including users, places, reviews, and amenities.
"""

from app.services.facade import HBnBFacade

# Singleton instance of the application service facade
facade = HBnBFacade()
