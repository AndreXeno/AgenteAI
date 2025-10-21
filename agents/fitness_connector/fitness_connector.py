# ================================
# 🌐 FITNESS CONNECTOR (modulare)
# ================================
# Questo file serve solo come interfaccia compatibile con le versioni precedenti.

from .base_utils import ensure_user_dir, save_token, append_fitness_data
from .strava import connect_strava, exchange_strava_token, is_connected as is_strava_connected, disconnect as disconnect_strava
from .myfitnesspal import connect as connect_myfitnesspal
from .sync_manager import auto_sync_user_data

__all__ = [
    "ensure_user_dir",
    "save_token",
    "append_fitness_data",
    "connect_strava",
    "exchange_strava_token",
    "is_strava_connected",
    "disconnect_strava",
    "connect_myfitnesspal",
    "auto_sync_user_data"
]