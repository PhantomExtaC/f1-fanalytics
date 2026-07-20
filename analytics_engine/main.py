import subprocess
from pathlib import Path
import sys

def run_script(script_path):
    """Helper function to execute a python script and stream its output."""
    print(f"\n{'='*50}")
    print(f"▶️ RUNNING: {script_path.name}")
    print(f"{'='*50}")
    
    try:
        # We use subprocess to run the script exactly as if you typed it in the terminal
        result = subprocess.run([sys.executable, str(script_path)], check=True, text=True)
    except subprocess.CalledProcessError as e:
        print(f"\n❌ PIPELINE HALTED: Error executing {script_path.name}")
        sys.exit(1)

def execute_pipeline():
    print("🏁 INITIALIZING FANALYTICS DATA PIPELINE 🏁")
    
    BASE_DIR = Path(__file__).resolve().parent
    SRC_DIR = BASE_DIR / "src"
    
    # Define the exact execution order
    # Note: We omit bootstrap.py because that is a one-time setup, not a weekly task.
    # When we write update.py, it will go here in index 0.
    pipeline_steps = [
        SRC_DIR / "ingestion" / "update.py",
        SRC_DIR / "features" / "track_profile.py",
        SRC_DIR / "features" / "power_rating.py",
        SRC_DIR / "features" / "mastery.py",
        SRC_DIR / "features" / "generate_standings.py",
        SRC_DIR / "export" / "json_builder.py"

    ]
    
    for script in pipeline_steps:
        if not script.exists():
            print(f"❌ CRITICAL ERROR: Could not find {script}")
            sys.exit(1)
        run_script(script)
        
    print(f"\n{'='*50}")
    print("🏆 PIPELINE EXECUTED SUCCESSFULLY")
    print(f"{'='*50}")

if __name__ == "__main__":
    execute_pipeline()
   