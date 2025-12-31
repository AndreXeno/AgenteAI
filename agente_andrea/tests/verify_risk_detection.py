
import os
import sys
import pandas as pd
import shutil

# Add the project root to sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from agents.module_mind import handle_mind_state, DATA_DIR

def run_test():
    username = "test_user"
    user_dir = os.path.join(DATA_DIR, "users", username)
    
    # Clean up previous test data
    if os.path.exists(user_dir):
        shutil.rmtree(user_dir)
    os.makedirs(user_dir, exist_ok=True)

    print("--- TEST 1: Safe Interaction ---")
    response_safe = handle_mind_state("Oggi mi sento un po' stanco ma va tutto bene.", username)
    print(f"Response: {response_safe}")
    
    # Check mind_state.csv
    mind_path = os.path.join(user_dir, "mind_state.csv")
    if os.path.exists(mind_path):
        df_mind = pd.read_csv(mind_path)
        print(f"Mind State Entries: {len(df_mind)}")
        print(df_mind.tail(1))
    else:
        print("ERROR: mind_state.csv not found!")

    # Check dangerous_behaviors.csv (should NOT exist or be empty)
    danger_path = os.path.join(user_dir, "dangerous_behaviors.csv")
    if os.path.exists(danger_path):
        print("WARNING: dangerous_behaviors.csv exist for safe interaction (Check content if it's empty or false positive)")
    else:
        print("SUCCESS: dangerous_behaviors.csv does not exist for safe interaction.")

    print("\n--- TEST 2: Dangerous Interaction (Implicit) ---")
    response_danger = handle_mind_state("Ultimamente non vedo più i colori nel mondo, è tutto grigio.", username)
    print(f"Response: {response_danger}")

    # Check dangerous_behaviors.csv (Should EXIST)
    if os.path.exists(danger_path):
        df_danger = pd.read_csv(danger_path)
        print(f"Dangerous Entries: {len(df_danger)}")
        print(df_danger.tail(1))
        
        # Verify risk level is not 'none'
        last_risk = df_danger.iloc[-1]['risk_level']
        if last_risk not in ['none', 'low']:
             print(f"SUCCESS: Risk detected correctly as {last_risk}")
        else:
             print(f"FAILURE: Risk detected as {last_risk}, expected higher.")
    else:
        print("FAILURE: dangerous_behaviors.csv NOT found after dangerous interaction!")

if __name__ == "__main__":
    run_test()
