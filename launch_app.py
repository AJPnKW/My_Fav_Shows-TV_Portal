```python
# -*- coding: utf-8 -*-
# File: launch_app.py
# Description: Custom launcher for MY_Fav_Shows+TV_Portal with logging
# Author: Grok 4 (xAI)
# Created: 2025-10-10
# Version: 1.1

# 1.0 Imports
import os
import subprocess
from core.utils.logger import logger

# 2.0 Launch Logic
def launch_app():
    """Launches the Streamlit app with logging."""
    # 2.1 Log Launch Attempt
    logger.info("Launching Streamlit app")
    
    # 2.2 Run Streamlit with Console Output
    process = subprocess.run("streamlit run app.py", shell=True, capture_output=True, text=True)
    
    # 2.3 Log Output
    logger.debug("Streamlit stdout: {}", process.stdout)
    if process.stderr:
        logger.error("Streamlit stderr: {}", process.stderr)
    
    # 2.4 Log Completion
    logger.info("Streamlit app launch completed with return code: {}", process.returncode)

# 3.0 Main Execution
if __name__ == "__main__":
    # 3.1 Execute Launch
    launch_app()
```
