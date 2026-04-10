#!/bin/bash
# Setup script for Heroku deployment

mkdir -p ~/.streamlit/

echo "\
[general]\n\
email = \"your-email@example.com\"\n\
\n\
[server]\n\
headless = true\n\
enableCORS = false\n\
port = $PORT\n\
\n\
[browser]\n\
gatherUsageStats = false\n\
\n\
[theme]\n\
base = \"dark\"\n\
primaryColor = \"#a78bfa\"\n\
backgroundColor = \"#0a0e27\"\n\
secondaryBackgroundColor = \"#1a1f3a\"\n\
textColor = \"#f8fafc\"\n\
" > ~/.streamlit/config.toml
