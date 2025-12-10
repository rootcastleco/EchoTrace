"""
Basic usage example for EchoTrace.

This script demonstrates how to use EchoTrace programmatically.
"""

from echotrace import EchoTrace

def main():
    # Create EchoTrace instance
    echo = EchoTrace(
        sample_interval=0.1,  # Sample every 100ms
        sound_duration=0.1     # Each sound lasts 100ms
    )
    
    # Option 1: Generate a demo
    print("Generating demo audio...")
    echo.generate_demo("demo_output.wav")
    
    # Option 2: Run live monitoring for 10 seconds
    print("\nRunning live monitoring for 10 seconds...")
    echo.run(duration=10, output_file="live_monitoring.wav")
    
    print("\nDone! Check the generated WAV files.")
    print("- demo_output.wav: Shows healthy -> anomalous transition")
    print("- live_monitoring.wav: Captures your system's actual behavior")

if __name__ == "__main__":
    main()
