"""Tests for system monitors."""

import time
from echotrace import CPUMonitor, NetworkMonitor, SensorMonitor, TimingMonitor


def test_cpu_monitor():
    """Test CPU monitor basic functionality."""
    monitor = CPUMonitor()
    metrics = monitor.update()
    
    assert "cpu_percent" in metrics
    assert "cpu_count" in metrics
    assert "load_avg" in metrics
    assert "timestamp" in metrics
    assert 0 <= metrics["cpu_percent"] <= 100
    assert metrics["cpu_count"] > 0


def test_network_monitor():
    """Test network monitor basic functionality."""
    monitor = NetworkMonitor()
    time.sleep(0.1)  # Wait a bit for baseline
    metrics = monitor.update()
    
    assert "bytes_sent_rate" in metrics
    assert "bytes_recv_rate" in metrics
    assert "packets_sent_rate" in metrics
    assert "packets_recv_rate" in metrics
    assert "total_bytes_rate" in metrics
    assert "timestamp" in metrics
    assert metrics["bytes_sent_rate"] >= 0
    assert metrics["bytes_recv_rate"] >= 0


def test_sensor_monitor():
    """Test sensor monitor basic functionality."""
    monitor = SensorMonitor()
    time.sleep(0.1)  # Wait a bit for baseline
    metrics = monitor.update()
    
    assert "temperatures" in metrics
    assert "disk_read_rate" in metrics
    assert "disk_write_rate" in metrics
    assert "memory_percent" in metrics
    assert "memory_available" in metrics
    assert "timestamp" in metrics
    assert 0 <= metrics["memory_percent"] <= 100
    assert metrics["memory_available"] >= 0


def test_timing_monitor():
    """Test timing monitor basic functionality."""
    monitor = TimingMonitor()
    time.sleep(0.1)
    metrics = monitor.update()
    
    assert "interval" in metrics
    assert "avg_interval" in metrics
    assert "jitter" in metrics
    assert "uptime" in metrics
    assert "timestamp" in metrics
    assert metrics["interval"] > 0
    assert metrics["uptime"] > 0


def test_anomaly_scores():
    """Test that anomaly scores are calculated."""
    cpu = CPUMonitor()
    network = NetworkMonitor()
    sensor = SensorMonitor()
    timing = TimingMonitor()
    
    # Collect some samples
    for _ in range(15):
        cpu.update()
        network.update()
        sensor.update()
        timing.update()
        time.sleep(0.01)
    
    # Get anomaly scores
    cpu_anomaly = cpu.get_anomaly_score()
    network_anomaly = network.get_anomaly_score()
    sensor_anomaly = sensor.get_anomaly_score()
    timing_anomaly = timing.get_anomaly_score()
    
    # All should be between 0 and 1
    assert 0 <= cpu_anomaly <= 1
    assert 0 <= network_anomaly <= 1
    assert 0 <= sensor_anomaly <= 1
    assert 0 <= timing_anomaly <= 1


if __name__ == "__main__":
    print("Running monitor tests...")
    test_cpu_monitor()
    print("✓ CPU monitor test passed")
    test_network_monitor()
    print("✓ Network monitor test passed")
    test_sensor_monitor()
    print("✓ Sensor monitor test passed")
    test_timing_monitor()
    print("✓ Timing monitor test passed")
    test_anomaly_scores()
    print("✓ Anomaly scores test passed")
    print("\nAll tests passed!")
