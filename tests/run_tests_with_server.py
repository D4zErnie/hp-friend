import subprocess
import time
import sys
import os

PORT = 3000

def kill_port(port):
    try:
        # Check if port is in use using lsof
        cmd = f"lsof -t -i:{port}"
        try:
            pid_bytes = subprocess.check_output(cmd, shell=True, stderr=subprocess.DEVNULL)
            pids = pid_bytes.decode().strip().split('\n')
            for pid in pids:
                if pid:
                    print(f"Killing process {pid} using port {port}")
                    subprocess.run(f"kill {pid}", shell=True)
        except subprocess.CalledProcessError:
            pass # No process found
    except Exception as e:
        print(f"Error checking port: {e}")

def run_server():
    print(f"Starting server on port {PORT}...")
    server_process = subprocess.Popen(
        [sys.executable, "-m", "http.server", str(PORT)],
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL
    )
    time.sleep(2)
    return server_process

def run_test(test_script):
    print(f"Running test script: {test_script}")
    try:
        # Pass stdout/stderr to parent process so we can see output immediately
        result = subprocess.run([sys.executable, test_script], check=True)
        return 0
    except subprocess.CalledProcessError as e:
        print(f"Test failed with return code {e.returncode}")
        return e.returncode
    except Exception as e:
        print(f"Error running test: {e}")
        return 1

def main():
    if len(sys.argv) < 2:
        print("Usage: python3 tests/run_tests_with_server.py <test_script>")
        sys.exit(1)

    test_script = sys.argv[1]

    # Allow passing script path relative to current directory
    if not os.path.exists(test_script):
        print(f"Error: Test script '{test_script}' not found.")
        sys.exit(1)

    kill_port(PORT)
    server_process = run_server()

    exit_code = 1
    try:
        exit_code = run_test(test_script)
    finally:
        print("Stopping server...")
        server_process.terminate()
        server_process.wait()

    sys.exit(exit_code)

if __name__ == "__main__":
    main()
