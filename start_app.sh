#!/bin/bash

# Colors for output
GREEN='\033[0;32m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

echo -e "${BLUE}🚀 Starting LLM Finetuner App...${NC}"

# Function to kill processes on exit
cleanup() {
    echo -e "\n${BLUE}🛑 Shutting down servers...${NC}"
    kill $BACKEND_PID
    kill $FRONTEND_PID
    exit
}

# Trap SIGINT (Ctrl+C)
trap cleanup SIGINT

# 1. Start Backend
echo -e "${GREEN}📦 Starting Backend Server (FastAPI)...${NC}"
/Users/f.nuno/IronHack/Lab/Teste_MLX/mlx_finetuning_env/bin/python -m uvicorn backend.main:app --reload --port 8000 &
BACKEND_PID=$!

# Wait a moment for backend to initialize
sleep 2

# 2. Start Frontend
echo -e "${GREEN}⚛️  Starting Frontend (Vite)...${NC}"
cd Coach.ai
npm run dev &
FRONTEND_PID=$!

echo -e "${BLUE}✨ App is running!${NC}"
echo -e "Backend: http://localhost:8000"
echo -e "Frontend: http://localhost:5173"
echo -e "Press Ctrl+C to stop both servers."

# Open Browser
sleep 2
open http://localhost:5173

# Keep script running
wait
