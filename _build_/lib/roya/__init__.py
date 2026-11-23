"""Roya — Material Design 3 component library for Django."""
import logging

__version__ = "0.2.0"
__author__ = "Roya Team"
__all__ = ["__version__"]

default_app_config = "roya.apps.RoyaConfig"

logging.getLogger(__name__).addHandler(logging.NullHandler())