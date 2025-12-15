#!/usr/bin/env python3
"""
SignVerse AI - Start Backend and ML Server simultaneously
Runs both servers in parallel with proper process management
"""

import os
import sys
import subprocess
import time
import signal
import socket
from pathlib import Path

# Color codes
class Colors:
    BLUE = '\033[94m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    BOLD = '\033[1m'
    END = '\033[0m'

def print_header():
    print(f"\n{Colors.BLUE}{'='*60}")
    print(f"   SignVerse AI - Backend & ML Server Startup")
    print(f"{'='*60}{Colors.END}\n")

def check_port_available(port):
    """Check if a port is available"""
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.bind(('localhost', port))
        return True
    except OSError:
        return False

def print_status(status, message):
    """Print colored status message"""
    if status == "error":
        print(f"{Colors.RED}✗ {message}{Colors.END}")
    elif status == "success":
        print(f"{Colors.GREEN}✓ {message}{Colors.END}")
    elif status == "info":
        print(f"{Colors.YELLOW}ℹ {message}{Colors.END}")
    elif status == "running":
        print(f"{Colors.YELLOW}⟳ {message}{Colors.END}")

def start_backend(backend_dir):
    """Start the backend server"""
    print_status("running", "Starting Backend Server...")
    
    # Check if directory exists
    if not os.path.exists(backend_dir):
        print_status("error", f"Backend directory not found: {backend_dir}")
        return None
    
    try:
        # Activate venv and start backend with uvicorn (don't use exec)
        cmd = f"source train_venv/bin/activate && python3 -m uvicorn app.main:app --host 0.0.0.0 --port 8000"
        
        # Write to logfile so we can debug issues
        logfile = open('/tmp/backend.log', 'a')
        
        process = subprocess.Popen(
            cmd,
            shell=True,
            cwd=backend_dir,
            stdout=logfile,
            stderr=logfile,
            text=True,
            preexec_fn=os.setsid if sys.platform != "win32" else None
        )
        
        print_status("success", "Backend starting on http://localhost:8000")
        return process
    except Exception as e:
        print_status("error", f"Failed to start Backend: {e}")
        return None

def start_ml_server(ml_dir):
    """Start the ML server"""
    print_status("running", "Starting ML Server...")
    
    # Check if directory exists
    if not os.path.exists(ml_dir):
        print_status("error", f"ML Server directory not found: {ml_dir}")
        return None
    
    try:
        # Activate venv and start ML server (don't use exec)
        cmd = f"source venv_infer/bin/activate && python3 main.py"
        
        # Write to logfile so we can debug issues
        logfile = open('/tmp/ml_server.log', 'a')
        
        process = subprocess.Popen(
            cmd,
            shell=True,
            cwd=ml_dir,
            stdout=logfile,
            stderr=logfile,
            text=True,
            preexec_fn=os.setsid if sys.platform != "win32" else None
        )
        
        print_status("success", "ML Server starting on http://localhost:8001")
        return process
    except Exception as e:
        print_status("error", f"Failed to start ML Server: {e}")
        return None

def check_server_health(max_retries=15):
    """Check if servers are running"""
    print(f"\n{Colors.BLUE}Checking server health...{Colors.END}")
    
    backend_ok = False
    ml_ok = False
    
    for attempt in range(max_retries):
        if not backend_ok:
            backend_ok = not check_port_available(8000)
            if backend_ok:
                print_status("success", "Backend Server is running on port 8000")
        
        if not ml_ok:
            ml_ok = not check_port_available(8001)
            if ml_ok:
                print_status("success", "ML Server is running on port 8001")
        
        if backend_ok and ml_ok:
            return True
        
        if attempt < max_retries - 1:
            time.sleep(1)
    
    if not backend_ok:
        print_status("error", "Backend Server failed to start")
    if not ml_ok:
        print_status("error", "ML Server failed to start")
    
    return backend_ok and ml_ok

def main():
    print_header()
    
    # Get the directory where this script is located
    script_dir = os.path.dirname(os.path.abspath(__file__))
    
    backend_dir = os.path.join(script_dir, "backend")
    ml_dir = os.path.join(script_dir, "ml_server")
    
    # Verify directories exist
    if not os.path.exists(backend_dir):
        print_status("error", f"Backend directory not found: {backend_dir}")
        sys.exit(1)
    
    if not os.path.exists(ml_dir):
        print_status("error", f"ML Server directory not found: {ml_dir}")
        sys.exit(1)
    
    # Start both servers
    print_status("running", "Starting both servers...\n")
    
    backend_process = start_backend(backend_dir)
    ml_process = start_ml_server(ml_dir)
    
    if not backend_process or not ml_process:
        print_status("error", "Failed to start servers")
        sys.exit(1)
    
    # Wait for servers to be ready
    time.sleep(3)
    servers_ready = check_server_health()
    
    if servers_ready:
        # Print startup complete message
        print(f"\n{Colors.GREEN}{'='*60}")
        print(f"Both servers are running!")
        print(f"{'='*60}{Colors.END}")
        print(f"\n{Colors.BLUE}Backend API:{Colors.END} {Colors.GREEN}http://localhost:8000{Colors.END}")
        print(f"{Colors.BLUE}ML Server:  {Colors.END} {Colors.GREEN}http://localhost:8001{Colors.END}")
        print(f"\n{Colors.YELLOW}Press Ctrl+C to stop both servers{Colors.END}\n")
    else:
        print(f"\n{Colors.RED}Servers may not be fully ready. Check the logs above.{Colors.END}\n")
    
    # Keep processes running
    try:
        # Monitor server ports instead of process objects
        # This is more reliable since we're using shell=True which wraps processes
        while True:
            if check_port_available(8000):
                print_status("error", "Backend Server has stopped")
                break
            
            if check_port_available(8001):
                print_status("error", "ML Server has stopped")
                break
            
            time.sleep(2)
    
    except KeyboardInterrupt:
        print(f"\n\n{Colors.YELLOW}Stopping servers...{Colors.END}")
        
        try:
            if sys.platform != "win32":
                # Send SIGTERM to process groups
                try:
                    os.killpg(os.getpgid(backend_process.pid), signal.SIGTERM)
                except:
                    pass
                try:
                    os.killpg(os.getpgid(ml_process.pid), signal.SIGTERM)
                except:
                    pass
            else:
                backend_process.terminate()
                ml_process.terminate()
            
            time.sleep(2)
            print_status("success", "Both servers stopped")
        except:
            print_status("success", "Servers stopped")
        
        sys.exit(0)

if __name__ == "__main__":
    main()
