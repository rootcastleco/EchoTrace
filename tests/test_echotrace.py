"""Tests for main EchoTrace application."""

import os
import tempfile
from echotrace import EchoTrace


def test_echotrace_init():
    """Test EchoTrace initialization."""
    echo = EchoTrace()
    assert echo.sample_interval == 0.1
    assert echo.sound_duration == 0.1
    assert echo.cpu_monitor is not None
    assert echo.network_monitor is not None
    assert echo.sensor_monitor is not None
    assert echo.timing_monitor is not None
    assert echo.sound_engine is not None


def test_collect_metrics():
    """Test collecting metrics from all monitors."""
    echo = EchoTrace()
    metrics = echo.collect_metrics()
    
    assert "cpu_percent" in metrics
    assert "network_rate" in metrics
    assert "memory_percent" in metrics
    assert "anomaly_score" in metrics
    assert "timestamp" in metrics
    assert "details" in metrics
    
    # Check details
    assert "cpu" in metrics["details"]
    assert "network" in metrics["details"]
    assert "sensor" in metrics["details"]
    assert "timing" in metrics["details"]
    assert "anomalies" in metrics["details"]


def test_run_with_duration():
    """Test running EchoTrace with a duration limit."""
    echo = EchoTrace(sample_interval=0.1)
    
    with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as f:
        filename = f.name
    
    try:
        # Run for 0.5 seconds
        echo.run(duration=0.5, output_file=filename)
        
        # Check that file was created
        assert os.path.exists(filename)
        assert os.path.getsize(filename) > 0
        
        # Check that samples were collected
        assert echo.sample_count > 0
    finally:
        if os.path.exists(filename):
            os.remove(filename)


def test_generate_demo():
    """Test generating demo audio."""
    echo = EchoTrace()
    
    with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as f:
        filename = f.name
    
    try:
        echo.generate_demo(filename)
        
        # Check that file was created
        assert os.path.exists(filename)
        assert os.path.getsize(filename) > 0
    finally:
        if os.path.exists(filename):
            os.remove(filename)


if __name__ == "__main__":
    print("Running EchoTrace tests...")
    test_echotrace_init()
    print("✓ EchoTrace initialization test passed")
    test_collect_metrics()
    print("✓ Collect metrics test passed")
    test_run_with_duration()
    print("✓ Run with duration test passed")
    test_generate_demo()
    print("✓ Generate demo test passed")
    print("\nAll tests passed!")
