#!/usr/bin/env python3
"""
SignVerse AI - Simple Server Startup
Starts both servers in separate processes without complex health checks
"""

import os
import sys
import subprocess
from pathlib import Path

def main():
    print("\n" + "="*60)
    print("   SignVerse AI - Starting Servers")
    print("="*60 + "\n")
    
    # Get script directory
    script_dir = Path(__file__).parent
    backend_dir = script_dir / "backend"
    ml_dir = script_dir / "ml_server"
    
    # Get virtual environment python executables
    if sys.platform == "win32":
        backend_python = backend_dir / "venv" / "Scripts" / "python.exe"
        ml_python = ml_dir / "venv_infer" / "Scripts" / "python.exe"
    else:
        backend_python = backend_dir / "venv" / "bin" / "python"
        ml_python = ml_dir / "venv_infer" / "bin" / "python"
    
    # Verify venv executables exist
    if not backend_python.exists():
        print(f"❌ Backend venv not found: {backend_python}")
        return 1
    if not ml_python.exists():
        print(f"❌ ML venv not found: {ml_python}")
        return 1
    
    print(f"Backend Python: {backend_python}")
    print(f"ML Python: {ml_python}\n")
    
    # Create logs directories
    (backend_dir / "logs").mkdir(exist_ok=True)
    (ml_dir / "logs").mkdir(exist_ok=True)
    
    # Start Backend
    print("Starting Backend Server on port 8000...")
    backend_log = open(backend_dir / "logs" / "backend.log", "w", buffering=1)
    backend_process = subprocess.Popen(
        [str(backend_python), "-m", "uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000", "--log-level", "debug"],
        cwd=str(backend_dir),
        stdout=backend_log,
        stderr=subprocess.STDOUT,
        creationflags=subprocess.CREATE_NEW_PROCESS_GROUP if sys.platform == "win32" else 0
    )
    print(f"✓ Backend started (PID: {backend_process.pid})")
    
    # Start ML Server
    print("Starting ML Server on port 8001...")
    ml_log = open(ml_dir / "logs" / "ml_server.log", "w", buffering=1)
    ml_process = subprocess.Popen(
        [str(ml_python), "-m", "uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8001", "--log-level", "debug"],
        cwd=str(ml_dir),
        stdout=ml_log,
        stderr=subprocess.STDOUT,
        creationflags=subprocess.CREATE_NEW_PROCESS_GROUP if sys.platform == "win32" else 0
    )
    print(f"✓ ML Server started (PID: {ml_process.pid})\n")
    
    print("="*60)
    print("Both servers are starting...")
    print("="*60)
    print("\n✓ Backend:   http://localhost:8000")
    print("✓ ML Server: http://localhost:8001")
    print("\nPress Ctrl+C to stop both servers\n")
    
    import time
    try:
        # Keep script running, check processes periodically
        while True:
            time.sleep(1)
            # If either process died, exit
            if backend_process.poll() is not None:
                print(f"\n⚠ Backend process exited with code {backend_process.returncode}")
                break
            if ml_process.poll() is not None:
                print(f"\n⚠ ML Server process exited with code {ml_process.returncode}")
                break
    except KeyboardInterrupt:
        print("\n\nStopping servers...")
        try:
            backend_process.terminate()
            ml_process.terminate()
            backend_process.wait(timeout=3)
            ml_process.wait(timeout=3)
        except:
            backend_process.kill()
            ml_process.kill()
        print("Servers stopped.")
        sys.exit(0)

if __name__ == "__main__":
    main()
