#!/bin/bash
# Build script for Render deployment

# Install Python dependencies
pip install --upgrade pip
pip install -r requirements.txt

# Create Streamlit config directory
mkdir -p ~/.streamlit/

# Create Streamlit config file
echo "\
[general]
email = \"\"

[server]
headless = true
enableCORS = false
port = \$PORT

[browser]
gatherUsageStats = false
" > ~/.streamlit/config.toml

echo "Build completed successfully!"
