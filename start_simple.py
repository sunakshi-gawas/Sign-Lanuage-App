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
    
    # Get python executable
    python_exe = sys.executable
    
    print(f"Using Python: {python_exe}\n")
    
    # Create logs directories
    (backend_dir / "logs").mkdir(exist_ok=True)
    (ml_dir / "logs").mkdir(exist_ok=True)
    
    # Start Backend
    print("Starting Backend Server on port 8000...")
    backend_log = open(backend_dir / "logs" / "backend.log", "w")
    backend_process = subprocess.Popen(
        [python_exe, "-m", "uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"],
        cwd=str(backend_dir),
        stdout=backend_log,
        stderr=subprocess.STDOUT,
        creationflags=subprocess.CREATE_NEW_PROCESS_GROUP if sys.platform == "win32" else 0
    )
    print(f"✓ Backend started (PID: {backend_process.pid})")
    
    # Start ML Server
    print("Starting ML Server on port 8001...")
    ml_log = open(ml_dir / "logs" / "ml_server.log", "w")
    ml_process = subprocess.Popen(
        [python_exe, "-m", "uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8001"],
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
    
    try:
        # Keep script running
        backend_process.wait()
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
