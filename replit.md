# ARCA - Artista IA Project

## Overview
ARCA is a Portuguese language AI-powered web application featuring multiple AI agents for different tasks. The project consists of:
- FastAPI web backend serving a chat interface
- Multiple AI agents (Archaeologist, Arsenal, Scribe, Janus, etc.)
- Textual-based dashboard for agent control
- Frontend chat interface in Portuguese

## Current State
- **Status**: Successfully imported and configured for Replit
- **Backend**: FastAPI server running on port 5000
- **Frontend**: HTML/CSS/JS chat interface
- **Database**: Uses external services (Pinecone, Google APIs, etc.)
- **Language**: Portuguese (pt-br)

## Recent Changes (September 19, 2025)
- Configured FastAPI backend for Replit environment
- Added CORS middleware for proxy compatibility
- Changed server port from 8000 to 5000 (Replit standard)
- Added proper error handling for missing files
- Set up Web Server workflow
- Configured autoscale deployment

## Project Architecture

### Backend (main.py)
- FastAPI application with CORS enabled
- Serves frontend files and API endpoints
- Main API endpoint: `/comando_artista` for chat functionality
- Runs on port 5000 with host 0.0.0.0

### Frontend Files
- `index.html`: Main chat interface
- `style.css`: UI styling 
- `script.js`: Frontend JavaScript for API communication

### AI Agents
- `agente_arqueologo.py`: Email processing agent
- `agente_arsenal.py`: Repository cloning and vectorization
- `agente_escriba.py`: Git operations
- `agente_janus.py`: Google Docs and GitHub integration
- `agente_vetohere.py`: Pinecone indexing
- `agente_ia.py`: Main AI coordination

### Dashboard
- `exercito.py`: Textual-based TUI for agent control
- `exercito.css`: Styling for the dashboard

## Dependencies
- FastAPI & Uvicorn (web framework)
- Textual (terminal UI)
- Pydantic (data models)
- Cohere (AI embeddings)
- Pinecone (vector database)
- GitPython (Git operations)
- Google API clients (Docs integration)
- PyTZ (timezone handling)

## User Preferences
- Portuguese language interface
- Chat-based interaction model
- Agent-based architecture for different tasks
- Terminal dashboard for advanced control

## Deployment Configuration
- Type: Autoscale (suitable for stateless web app)
- Command: python main.py
- Port: 5000
- CORS enabled for all origins (Replit proxy requirement)