"""
EchoTrace - System behavior monitoring through sound signatures.

Converts CPU, network, sensor, and timing patterns into sound signatures,
revealing anomalies through rhythm and tone.
"""

__version__ = "0.1.0"

from .monitors import CPUMonitor, NetworkMonitor, SensorMonitor, TimingMonitor
from .sound_engine import SoundEngine
from .echotrace import EchoTrace

__all__ = [
    "CPUMonitor",
    "NetworkMonitor", 
    "SensorMonitor",
    "TimingMonitor",
    "SoundEngine",
    "EchoTrace",
]
