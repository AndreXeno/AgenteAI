import xml.etree.ElementTree as ET
import pandas as pd
import os

def import_health_data(xml_path="data/export.xml"):
    """
    Legge il file export.xml di Apple Health e estrae gli allenamenti.
    """
    if not os.path.exists(xml_path):
        return "Nessun file export.xml trovato in /data"

    tree = ET.parse(xml_path)
    root = tree.getroot()

    workouts = []
    for workout in root.findall("Workout"):
        type_ = workout.get("workoutActivityType", "Unknown").split("Type")[1] if "Type" in workout.get("workoutActivityType", "") else "Unknown"
        duration = workout.get("duration", "0")
        duration_unit = workout.get("durationUnit", "")
        total_energy = workout.get("totalEnergyBurned", "0")
        distance = workout.get("totalDistance", "0")

        workouts.append({
            "tipo": type_,
            "durata": duration + " " + duration_unit,
            "distanza_km": distance,
            "calorie": total_energy
        })

    df = pd.DataFrame(workouts)
    df.to_csv("data/allenamenti_importati.csv", index=False)
    return f"Importati {len(df)} allenamenti da Apple Health ✅"