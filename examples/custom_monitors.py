"""
Example showing how to use individual monitors and sound engine.

This demonstrates lower-level control over EchoTrace components.
"""

from echotrace import CPUMonitor, NetworkMonitor, SensorMonitor, SoundEngine
import time
import numpy as np


def main():
    # Create individual monitors
    cpu = CPUMonitor()
    network = NetworkMonitor()
    sensor = SensorMonitor()
    sound_engine = SoundEngine()
    
    print("Collecting system metrics for 5 seconds...")
    print("This will generate a soundscape based on your system activity.\n")
    
    metrics_list = []
    
    # Collect metrics for 5 seconds
    for i in range(50):
        # Update monitors
        cpu_data = cpu.update()
        network_data = network.update()
        sensor_data = sensor.update()
        
        # Get anomaly scores
        cpu_anomaly = cpu.get_anomaly_score()
        network_anomaly = network.get_anomaly_score()
        sensor_anomaly = sensor.get_anomaly_score()
        
        # Combine for sound generation
        metrics = {
            "cpu_percent": cpu_data["cpu_percent"],
            "network_rate": network_data["total_bytes_rate"],
            "memory_percent": sensor_data["memory_percent"],
            "anomaly_score": (cpu_anomaly + network_anomaly + sensor_anomaly) / 3.0
        }
        
        metrics_list.append(metrics)
        
        # Display progress
        print(f"Sample {i+1}/50: CPU={metrics['cpu_percent']:.1f}% "
              f"Memory={metrics['memory_percent']:.1f}% "
              f"Anomaly={metrics['anomaly_score']:.2f}")
        
        time.sleep(0.1)
    
    # Generate soundscape
    print("\nGenerating soundscape...")
    soundscape = sound_engine.generate_soundscape(metrics_list, duration_per_sample=0.1)
    
    # Save to file
    output_file = "custom_soundscape.wav"
    sound_engine.save_audio(soundscape, output_file)
    
    print(f"\nSoundscape saved to {output_file}")
    print(f"Duration: {len(soundscape)/sound_engine.sample_rate:.1f} seconds")
    print("\nListen to the audio file to hear your system's behavior pattern!")


if __name__ == "__main__":
    main()
