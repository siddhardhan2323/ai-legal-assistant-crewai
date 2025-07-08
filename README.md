# AI Legal Assistant with Task Status Tracking

An AI-powered legal assistant that provides real-time task status tracking during the legal analysis workflow.

## Features

- **Real-time Status Tracking**: Monitor the progress of each task in the legal analysis workflow
- **Multi-interface Support**: Both CLI and web interfaces with status updates
- **Task Progress Visualization**: Visual progress bars and status icons
- **Error Handling**: Graceful error handling with task failure tracking

## Task Workflow

The system processes legal queries through 4 sequential tasks:

1. **📋 Case Intake**: Analyzing your legal issue and extracting key information
2. **📚 IPC Section Search**: Finding relevant Indian Penal Code sections  
3. **⚖️ Legal Precedent Search**: Searching for relevant legal precedents
4. **📝 Legal Document Drafting**: Drafting formal legal document

## Usage

### CLI Interface
```bash
python main.py
```

### Web Interface  
```bash
streamlit run app.py
```

Both interfaces now provide:
- Real-time progress updates
- Current task status
- Visual progress indicators
- Individual task completion status

## New Files Added

- `task_status_tracker.py`: Core status tracking functionality
- `crew_with_status.py`: Wrapper for CrewAI with status tracking
- Updated `main.py`: CLI interface with status updates
- Updated `app.py`: Streamlit interface with status visualization