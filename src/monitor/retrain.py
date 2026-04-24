import subprocess
import time
from drift import check_data_drift

def main():
    print("Starting continuous monitoring for data drift...")
    try:
        while True:
            # Check every 60 seconds
            time.sleep(60)
            
            is_drifting = check_data_drift()
            if is_drifting:
                print("Drift detected. Running DVC reproduction pipeline...")
                # Run dvc repro to retrain the model
                result = subprocess.run(["dvc", "repro"], capture_output=True, text=True)
                
                if result.returncode == 0:
                    print("Retraining successful.")
                    print(result.stdout)
                else:
                    print("Retraining failed!")
                    print(result.stderr)
                    
    except KeyboardInterrupt:
        print("Monitoring stopped.")

if __name__ == "__main__":
    main()
