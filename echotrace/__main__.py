"""
Command-line interface for EchoTrace.
"""

import argparse
import sys
from .echotrace import EchoTrace


def main():
    """Main CLI entry point."""
    parser = argparse.ArgumentParser(
        description="EchoTrace - System behavior monitoring through sound signatures",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Run for 60 seconds and save to file
  python -m echotrace -d 60 -o system_sound.wav
  
  # Run indefinitely with custom sampling
  python -m echotrace -i 0.2
  
  # Generate demo audio
  python -m echotrace --demo
  
EchoTrace converts system metrics into sound:
- CPU usage controls pitch (higher CPU = higher pitch)
- Network activity controls rhythm/pulsing
- Memory usage controls volume
- Anomalies add dissonance and noise

Healthy systems sound coherent; failing ones sound wrong.
        """
    )
    
    parser.add_argument(
        "-d", "--duration",
        type=float,
        help="Duration to run in seconds (default: run indefinitely)"
    )
    
    parser.add_argument(
        "-i", "--interval",
        type=float,
        default=0.1,
        help="Sampling interval in seconds (default: 0.1)"
    )
    
    parser.add_argument(
        "-o", "--output",
        type=str,
        help="Output WAV file to save audio"
    )
    
    parser.add_argument(
        "--demo",
        action="store_true",
        help="Generate a demo audio file and exit"
    )
    
    args = parser.parse_args()
    
    # Create EchoTrace instance
    echo = EchoTrace(sample_interval=args.interval)
    
    # Run demo or monitoring
    if args.demo:
        output_file = args.output or "echotrace_demo.wav"
        echo.generate_demo(output_file)
    else:
        echo.run(duration=args.duration, output_file=args.output)
        
    return 0


if __name__ == "__main__":
    sys.exit(main())
