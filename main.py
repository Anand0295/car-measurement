import subprocess
import sys
import os
import webbrowser
import threading
import time

def install_packages():
    packages = ['flask', 'flask-cors', 'opencv-python', 'numpy']
    for package in packages:
        try:
            __import__(package.replace('-', '_'))
        except ImportError:
            subprocess.check_call([sys.executable, '-m', 'pip', 'install', package])

def main():
    install_packages()
    
    script_dir = os.path.dirname(os.path.abspath(__file__))
    os.chdir(script_dir)
    sys.path.insert(0, os.path.join(script_dir, 'src'))
    
    def open_browser():
        time.sleep(1.5)
        webbrowser.open('file://' + os.path.join(script_dir, 'index.html'))
    
    threading.Thread(target=open_browser, daemon=True).start()
    
    from src.app import app
    app.run(debug=False, port=5001, host='127.0.0.1')

if __name__ == '__main__':
    print("Car Measurement System Starting...")
    main()