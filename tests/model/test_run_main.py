"""Test that runs the main block to get coverage"""

import subprocess
import sys
import os


def test_run_main_for_coverage():
    """Run the main script to get coverage"""
    # Change to the project directory
    os.chdir('.')
    
    # Run the model.py script
    result = subprocess.run(
        [sys.executable, 'challenge/model.py'],
        capture_output=True,
        text=True
    )
    
    # Check it ran successfully
    assert result.returncode == 0
    assert "Starting Flight Delay Prediction Pipeline" in result.stdout
    assert "Pipeline completed successfully" in result.stdout