"""
Streamlit Cloud Entry Point
This file is required for Streamlit Cloud deployment.
It simply imports and runs the main app.py file.
"""

# Import the main app
import sys
import os

# Add the current directory to the path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# Import and run the main app
# The app.py file contains all the application logic
import app

# Note: Streamlit automatically runs the imported module
# No need to call any functions explicitly
