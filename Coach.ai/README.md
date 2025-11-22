# LLM Finetuner Studio

## Overview
The **LLM Finetuner Studio** is a React-based web application designed to simulate the workflow of fine-tuning Large Language Models. It features a premium "Deep Navy" aesthetic and a step-by-step wizard interface.

## Features
1.  **System Check**: Simulates hardware validation (RAM, Disk, GPU).
2.  **Configuration**: Select models (Mistral, Llama 3) and upload datasets.
3.  **Summary**: Review settings and run a simulated integrity check.
4.  **Training**: Real-time visualization of loss curves and terminal logs.
5.  **Results**: Dashboard with F1 scores, radar charts, and deployment options.

## How to Run

### Prerequisites
- Node.js installed.

### Steps
1.  Navigate to the project directory:
    ```bash
    cd test
    ```
2.  Install dependencies (if not already done):
    ```bash
    npm install
    ```
3.  Start the development server:
    ```bash
    npm run dev
    ```
4.  Open your browser at the URL shown (usually `http://localhost:5173`).

## Tech Stack
- **Framework**: React (Vite)
- **Styling**: Vanilla CSS (CSS Variables)
- **Icons**: Lucide React
- **Charts**: Recharts
