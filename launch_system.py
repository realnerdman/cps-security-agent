import subprocess
import sys
import time

print("==================================================")
print("🚀 INITIATING RESIDUUM_MODULUS SYSTEM ARCHITECTURE")
print("==================================================")
print("1. Starting Telemetry Pipeline...")
print("2. Booting Sentinel Daemon...")
print("3. Launching SOC Dashboard (Web UI)...")
print("Press Ctrl+C to trigger emergency shutdown.\n")

try:
    injector_process = subprocess.Popen([sys.executable, "live_injector.py"])
    time.sleep(1) 
    
    sentinel_process = subprocess.Popen([sys.executable, "sentinel.py"])
    time.sleep(1)
    
    # Launch Streamlit on port 8080 so Google Cloud Shell can web-preview it
    dashboard_process = subprocess.Popen([sys.executable, "-m", "streamlit", "run", "dashboard.py", "--server.port=8080", "--server.address=0.0.0.0", "--server.enableCORS=false", "--server.enableXsrfProtection=false"])
    injector_process.wait()
    sentinel_process.wait()
    dashboard_process.wait()

except KeyboardInterrupt:
    print("\n\n🛑 EMERGENCY OVERRIDE TRIGGERED BY OPERATOR.")
    injector_process.terminate()
    sentinel_process.terminate()
    dashboard_process.terminate()
    print("✅ System successfully powered down. All connections closed.")