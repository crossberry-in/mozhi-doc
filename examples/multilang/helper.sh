#!/bin/bash
# helper.sh — Example shell script for run_sh() demo

echo "Hello from Shell!"
echo "Date: $(date)"
echo "User: $(whoami)"
echo "Host: $(hostname)"
echo ""

echo "Current directory: $(pwd)"
echo ""

echo "System info:"
uname -a
echo ""

echo "Disk usage:"
df -h / | tail -1
echo ""

echo "Memory:"
free -h 2>/dev/null | grep Mem || echo "(free not available)"
echo ""

echo "Files in current directory:"
ls -la | head -10
