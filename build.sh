#!/bin/bash

# Build script for production deployment
# Uses the GitHub repository name as the basepath

echo "Building site for production..."
python3 src/main.py "/staticSiteGenerator/"
echo "Production build complete!"
