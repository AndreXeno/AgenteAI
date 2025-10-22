# ============================================
# 🌐 FITNESS CONNECTOR (modulare compatibile)
# ============================================
# Questo file fa da "ponte" tra il vecchio sistema monolitico e la nuova architettura modulare.
# Permette di continuare a usare:
#     from agents.fitness_connector import connect_strava, auto_sync_user_data, ...
# anche se ora le funzioni sono divise nei rispettivi moduli.

from .base_utils import (
    ensure_user_dir,
    save_token,
    append_fitness_data
)

from .strava import (
    connect_strava,
    exchange_strava_token,
    is_connected as is_strava_connected,
    disconnect as disconnect_strava
)

from .myfitnesspal import (
    connect as connect_myfitnesspal,
    is_connected as is_myfitnesspal_connected,
    disconnect as disconnect_myfitnesspal
)

from .sync_manager import (
    auto_sync_user_data
)

__all__ = [
    # Base utils
    "ensure_user_dir",
    "save_token",
    "append_fitness_data",

    # Strava
    "connect_strava",
    "exchange_strava_token",
    "is_strava_connected",
    "disconnect_strava",

    # MyFitnessPal
    "connect_myfitnesspal",
    "is_myfitnesspal_connected",
    "disconnect_myfitnesspal",

    # Sync manager
    "auto_sync_user_data",
]


# ======================
# 🔍 Debug e verifica
# ======================
if __name__ == "__main__":
    import json
    print("✅ Fitness Connector Module Loaded")
    print(json.dumps({
        "exports": __all__,
        "status": "active"
    }, indent=2))