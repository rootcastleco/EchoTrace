"""
Main EchoTrace application class.

Coordinates monitors and sound engine to create real-time audio feedback
from system behavior.
"""

import time
import signal
import sys
import numpy as np
from typing import Dict, Any, Optional
from .monitors import CPUMonitor, NetworkMonitor, SensorMonitor, TimingMonitor
from .sound_engine import SoundEngine


class EchoTrace:
    """
    Main EchoTrace application.
    
    Coordinates system monitoring and sound generation to create
    audio signatures that reveal system health and anomalies.
    """
    
    def __init__(self, sample_interval: float = 0.1, sound_duration: float = 0.1):
        """
        Initialize EchoTrace.
        
        Args:
            sample_interval: Time between system samples in seconds
            sound_duration: Duration of each sound sample in seconds
        """
        self.sample_interval = sample_interval
        self.sound_duration = sound_duration
        
        # Initialize monitors
        self.cpu_monitor = CPUMonitor()
        self.network_monitor = NetworkMonitor()
        self.sensor_monitor = SensorMonitor()
        self.timing_monitor = TimingMonitor()
        
        # Initialize sound engine
        self.sound_engine = SoundEngine()
        
        # State
        self.running = False
        self.sample_count = 0
        self.sound_history = []
        
    def collect_metrics(self) -> Dict[str, Any]:
        """Collect metrics from all monitors."""
        cpu_metrics = self.cpu_monitor.update()
        network_metrics = self.network_monitor.update()
        sensor_metrics = self.sensor_monitor.update()
        timing_metrics = self.timing_monitor.update()
        
        # Calculate anomaly scores
        cpu_anomaly = self.cpu_monitor.get_anomaly_score()
        network_anomaly = self.network_monitor.get_anomaly_score()
        sensor_anomaly = self.sensor_monitor.get_anomaly_score()
        timing_anomaly = self.timing_monitor.get_anomaly_score()
        
        # Combined anomaly score (weighted average)
        overall_anomaly = (
            cpu_anomaly * 0.3 +
            network_anomaly * 0.2 +
            sensor_anomaly * 0.3 +
            timing_anomaly * 0.2
        )
        
        # Combine metrics for sound generation
        combined_metrics = {
            "cpu_percent": cpu_metrics["cpu_percent"],
            "network_rate": network_metrics["total_bytes_rate"],
            "memory_percent": sensor_metrics["memory_percent"],
            "anomaly_score": overall_anomaly,
            "timestamp": time.time(),
            # Additional details for logging
            "details": {
                "cpu": cpu_metrics,
                "network": network_metrics,
                "sensor": sensor_metrics,
                "timing": timing_metrics,
                "anomalies": {
                    "cpu": cpu_anomaly,
                    "network": network_anomaly,
                    "sensor": sensor_anomaly,
                    "timing": timing_anomaly,
                    "overall": overall_anomaly
                }
            }
        }
        
        return combined_metrics
        
    def run(self, duration: Optional[float] = None, output_file: Optional[str] = None):
        """
        Run EchoTrace monitoring and sound generation.
        
        Args:
            duration: How long to run in seconds (None = run indefinitely)
            output_file: Optional WAV file to save audio output
        """
        self.running = True
        start_time = time.time()
        
        print("EchoTrace starting...")
        print(f"Sampling interval: {self.sample_interval}s")
        print(f"Sound duration: {self.sound_duration}s")
        if output_file:
            print(f"Output file: {output_file}")
        print("\nListening to system behavior...")
        print("Press Ctrl+C to stop\n")
        
        # Setup signal handler for graceful shutdown
        def signal_handler(sig, frame):
            print("\n\nStopping EchoTrace...")
            self.running = False
            
        signal.signal(signal.SIGINT, signal_handler)
        
        try:
            while self.running:
                # Check duration limit
                if duration and (time.time() - start_time) >= duration:
                    break
                    
                # Collect metrics
                metrics = self.collect_metrics()
                self.sample_count += 1
                
                # Generate sound
                sound = self.sound_engine.metrics_to_sound(metrics, self.sound_duration)
                
                # Store for output file
                if output_file:
                    self.sound_history.append(sound)
                    
                # Display status
                if self.sample_count % 10 == 0:
                    self._display_status(metrics)
                    
                # Wait for next sample
                time.sleep(self.sample_interval)
                
        except Exception as e:
            print(f"\nError: {e}")
            self.running = False
            
        finally:
            # Save audio if requested
            if output_file and self.sound_history:
                print(f"\nSaving audio to {output_file}...")
                full_audio = np.concatenate(self.sound_history)
                self.sound_engine.save_audio(full_audio, output_file)
                print(f"Saved {len(self.sound_history)} samples ({len(full_audio)/self.sound_engine.sample_rate:.1f}s)")
                
            print(f"\nTotal samples collected: {self.sample_count}")
            print("EchoTrace stopped.")
            
    def _display_status(self, metrics: Dict[str, Any]):
        """Display current system status."""
        cpu = metrics["cpu_percent"]
        memory = metrics["memory_percent"]
        network_mb = metrics["network_rate"] / 1_000_000  # Convert to MB/s
        anomaly = metrics["anomaly_score"]
        
        # Create visual indicators
        cpu_bar = self._create_bar(cpu, 100)
        memory_bar = self._create_bar(memory, 100)
        anomaly_bar = self._create_bar(anomaly * 100, 100)
        
        print(f"\rSamples: {self.sample_count:4d} | "
              f"CPU: {cpu:5.1f}% {cpu_bar} | "
              f"MEM: {memory:5.1f}% {memory_bar} | "
              f"NET: {network_mb:6.2f}MB/s | "
              f"ANOMALY: {anomaly:.2f} {anomaly_bar}", end="", flush=True)
              
    def _create_bar(self, value: float, max_value: float, width: int = 10) -> str:
        """Create a simple ASCII bar chart."""
        filled = int((value / max_value) * width)
        return "█" * filled + "░" * (width - filled)
        
    def generate_demo(self, output_file: str = "echotrace_demo.wav"):
        """Generate a demo audio file showing healthy vs anomalous states."""
        print("Generating demo audio...")
        demo_audio = self.sound_engine.generate_demo_sound()
        self.sound_engine.save_audio(demo_audio, output_file)
        print(f"Demo audio saved to {output_file}")
        print("The demo shows a transition from healthy system to anomalous state.")
        print("Listen for changes in pitch, rhythm, and dissonance.")
