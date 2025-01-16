import os
import subprocess
import sys
import argparse


def initialize_migrations():
    if not os.path.exists('migrations/env.py'):
        print("Initializing migrations...")
        subprocess.check_call(['flask', 'db', 'init'])

def check_env_file():
    if not os.path.exists('migrations/env.py'):
        print("Error: migrations/env.py not found. Initialization may have failed.")
        sys.exit(1)

def generate_migration():
    print("Generating migration...")
    subprocess.check_call(['flask', 'db', 'migrate', '-m', 'Auto migration.'])

def apply_migrations():
    print("Applying migrations...")
    subprocess.check_call(['flask', 'db', 'upgrade'])

def start_flask_app():
    print("Starting Flask app...")
    subprocess.check_call(['flask', 'run', "--host=0.0.0.0", "--port=5000"])

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Setup Flask application.")
    parser.add_argument('--start-app', action='store_true', help="Start the Flask app after setup")
    
    args = parser.parse_args()
    initialize_migrations()
    check_env_file()
    generate_migration()
    apply_migrations()
    if args.start_app:
        start_flask_app()
    else:
        print("Setup completed. Flask app was not started because --start-app was not provided.")