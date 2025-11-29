import sys
import os

# 1. Get the directory containing this file (the 'src' folder)
current_dir = os.path.dirname(os.path.abspath(__file__))

# 2. Get the project root directory (parent of 'src')
project_root = os.path.dirname(current_dir)

# 3. Add the PROJECT ROOT to sys.path
# This allows imports like 'from src.backend...' to work correctly
if project_root not in sys.path:
    sys.path.insert(0, project_root)

from src.frontend.gradio_app import create_app

if __name__ == "__main__":
    print(f"Starting Financial Analyst Agent...")
    print(f"Project Root detected at: {project_root}")
    
    app = create_app()
    app.launch(server_name="0.0.0.0", server_port=7860)