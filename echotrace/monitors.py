"""
System monitoring modules for EchoTrace.

Monitors various system behaviors including CPU, network, sensors, and timing.
"""

import psutil
import time
from typing import Dict, Any, Optional
from collections import deque


class BaseMonitor:
    """Base class for all monitors."""
    
    def __init__(self, history_size: int = 100):
        self.history = deque(maxlen=history_size)
        self.last_value = None
        
    def get_metrics(self) -> Dict[str, Any]:
        """Get current metrics from the monitor."""
        raise NotImplementedError
        
    def update(self):
        """Update monitor state and store in history."""
        metrics = self.get_metrics()
        self.history.append(metrics)
        self.last_value = metrics
        return metrics


class CPUMonitor(BaseMonitor):
    """Monitor CPU usage patterns."""
    
    def __init__(self, history_size: int = 100):
        super().__init__(history_size)
        # Initialize to get baseline
        psutil.cpu_percent(interval=None)
        
    def get_metrics(self) -> Dict[str, Any]:
        """Get CPU metrics including usage percentage and load average."""
        cpu_percent = psutil.cpu_percent(interval=None)
        cpu_count = psutil.cpu_count()
        
        # Get per-CPU percentages
        per_cpu = psutil.cpu_percent(interval=None, percpu=True)
        
        # Get load average (Unix-like systems)
        try:
            load_avg = psutil.getloadavg()[0]  # 1-minute load average
        except (AttributeError, OSError):
            load_avg = cpu_percent / 100.0  # Fallback for Windows
            
        return {
            "cpu_percent": cpu_percent,
            "cpu_count": cpu_count,
            "per_cpu": per_cpu,
            "load_avg": load_avg,
            "timestamp": time.time()
        }
        
    def get_anomaly_score(self) -> float:
        """Calculate anomaly score based on CPU patterns."""
        if len(self.history) < 10:
            return 0.0
            
        recent_values = [m["cpu_percent"] for m in list(self.history)[-10:]]
        avg = sum(recent_values) / len(recent_values)
        
        # High variance or sudden spikes indicate anomalies
        variance = sum((x - avg) ** 2 for x in recent_values) / len(recent_values)
        std_dev = variance ** 0.5
        
        # Normalize to 0-1 range
        anomaly = min(std_dev / 50.0, 1.0)
        return anomaly


class NetworkMonitor(BaseMonitor):
    """Monitor network traffic patterns."""
    
    def __init__(self, history_size: int = 100):
        super().__init__(history_size)
        self.last_net_io = psutil.net_io_counters()
        self.last_time = time.time()
        
    def get_metrics(self) -> Dict[str, Any]:
        """Get network metrics including bytes sent/received and packet rates."""
        current_io = psutil.net_io_counters()
        current_time = time.time()
        time_delta = current_time - self.last_time
        
        if time_delta > 0:
            bytes_sent_rate = (current_io.bytes_sent - self.last_net_io.bytes_sent) / time_delta
            bytes_recv_rate = (current_io.bytes_recv - self.last_net_io.bytes_recv) / time_delta
            packets_sent_rate = (current_io.packets_sent - self.last_net_io.packets_sent) / time_delta
            packets_recv_rate = (current_io.packets_recv - self.last_net_io.packets_recv) / time_delta
        else:
            bytes_sent_rate = bytes_recv_rate = packets_sent_rate = packets_recv_rate = 0
            
        self.last_net_io = current_io
        self.last_time = current_time
        
        return {
            "bytes_sent_rate": bytes_sent_rate,
            "bytes_recv_rate": bytes_recv_rate,
            "packets_sent_rate": packets_sent_rate,
            "packets_recv_rate": packets_recv_rate,
            "total_bytes_rate": bytes_sent_rate + bytes_recv_rate,
            "timestamp": current_time
        }
        
    def get_anomaly_score(self) -> float:
        """Calculate anomaly score based on network patterns."""
        if len(self.history) < 10:
            return 0.0
            
        recent_values = [m["total_bytes_rate"] for m in list(self.history)[-10:]]
        avg = sum(recent_values) / len(recent_values)
        
        if avg == 0:
            return 0.0
            
        # Calculate coefficient of variation
        variance = sum((x - avg) ** 2 for x in recent_values) / len(recent_values)
        std_dev = variance ** 0.5
        cv = std_dev / (avg + 1e-6)  # Avoid division by zero
        
        # Normalize to 0-1 range
        anomaly = min(cv, 1.0)
        return anomaly


class SensorMonitor(BaseMonitor):
    """Monitor system sensors like temperature and disk I/O."""
    
    def __init__(self, history_size: int = 100):
        super().__init__(history_size)
        self.last_disk_io = psutil.disk_io_counters()
        self.last_time = time.time()
        
    def get_metrics(self) -> Dict[str, Any]:
        """Get sensor metrics including temperature and disk I/O."""
        current_time = time.time()
        
        # Temperature sensors (if available)
        temps = {}
        try:
            sensors = psutil.sensors_temperatures()
            if sensors:
                for name, entries in sensors.items():
                    temps[name] = [entry.current for entry in entries]
        except (AttributeError, OSError):
            pass
            
        # Disk I/O
        current_disk_io = psutil.disk_io_counters()
        time_delta = current_time - self.last_time
        
        if time_delta > 0 and self.last_disk_io:
            read_rate = (current_disk_io.read_bytes - self.last_disk_io.read_bytes) / time_delta
            write_rate = (current_disk_io.write_bytes - self.last_disk_io.write_bytes) / time_delta
        else:
            read_rate = write_rate = 0
            
        self.last_disk_io = current_disk_io
        self.last_time = current_time
        
        # Memory usage
        memory = psutil.virtual_memory()
        
        return {
            "temperatures": temps,
            "disk_read_rate": read_rate,
            "disk_write_rate": write_rate,
            "memory_percent": memory.percent,
            "memory_available": memory.available,
            "timestamp": current_time
        }
        
    def get_anomaly_score(self) -> float:
        """Calculate anomaly score based on sensor patterns."""
        if len(self.history) < 10:
            return 0.0
            
        recent_memory = [m["memory_percent"] for m in list(self.history)[-10:]]
        avg_memory = sum(recent_memory) / len(recent_memory)
        
        # High memory usage indicates potential issues
        memory_score = avg_memory / 100.0
        
        # Check for rapid changes in disk I/O
        recent_disk = [m["disk_read_rate"] + m["disk_write_rate"] for m in list(self.history)[-10:]]
        avg_disk = sum(recent_disk) / len(recent_disk)
        
        if avg_disk > 0:
            variance = sum((x - avg_disk) ** 2 for x in recent_disk) / len(recent_disk)
            std_dev = variance ** 0.5
            disk_score = min(std_dev / (avg_disk + 1e-6), 1.0)
        else:
            disk_score = 0.0
            
        # Combined anomaly score
        anomaly = (memory_score * 0.5 + disk_score * 0.5)
        return min(anomaly, 1.0)


class TimingMonitor(BaseMonitor):
    """Monitor timing patterns and system response times."""
    
    def __init__(self, history_size: int = 100):
        super().__init__(history_size)
        self.start_time = time.time()
        self.last_update_time = self.start_time
        self.update_intervals = deque(maxlen=50)
        
    def get_metrics(self) -> Dict[str, Any]:
        """Get timing metrics including intervals and jitter."""
        current_time = time.time()
        interval = current_time - self.last_update_time
        self.update_intervals.append(interval)
        
        # Calculate jitter (variation in intervals)
        if len(self.update_intervals) > 1:
            intervals = list(self.update_intervals)
            avg_interval = sum(intervals) / len(intervals)
            jitter = sum(abs(i - avg_interval) for i in intervals) / len(intervals)
        else:
            avg_interval = interval
            jitter = 0.0
            
        self.last_update_time = current_time
        uptime = current_time - self.start_time
        
        return {
            "interval": interval,
            "avg_interval": avg_interval,
            "jitter": jitter,
            "uptime": uptime,
            "timestamp": current_time
        }
        
    def get_anomaly_score(self) -> float:
        """Calculate anomaly score based on timing patterns."""
        if len(self.history) < 10:
            return 0.0
            
        recent_jitter = [m["jitter"] for m in list(self.history)[-10:]]
        avg_jitter = sum(recent_jitter) / len(recent_jitter)
        
        # Higher jitter indicates timing anomalies
        # Normalize to 0-1 range (assuming max jitter of 1 second)
        anomaly = min(avg_jitter / 1.0, 1.0)
        return anomaly
