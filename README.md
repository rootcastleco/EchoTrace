# EchoTrace

EchoTrace is a Python application that listens to system behavior instead of reading logs. It converts CPU, network, sensor, and timing patterns into sound signatures, revealing anomalies through rhythm and tone. Healthy systems sound coherent; failing ones sound wrong—letting humans detect issues faster than dashboards or metrics.

## Features

- **Real-time System Monitoring**: Tracks CPU, network, memory, disk I/O, and timing patterns
- **Audio Synthesis**: Converts system metrics into meaningful sound signatures
- **Anomaly Detection**: Irregular patterns create dissonant sounds, making issues immediately audible
- **Flexible Output**: Generate live audio or save to WAV files for later analysis
- **Lightweight**: Minimal dependencies, runs efficiently in the background

## How It Works

EchoTrace maps system metrics to audio parameters:

- **CPU Usage** → Pitch/Frequency (higher CPU = higher pitch)
- **Network Activity** → Rhythm/Pulse Rate (more traffic = faster rhythm)
- **Memory Usage** → Volume/Amplitude (higher memory = louder)
- **Anomalies** → Dissonance/Noise (problems sound wrong)

Healthy systems produce coherent, steady tones. When something goes wrong, you'll hear it—irregular rhythms, dissonant notes, or added noise signal that your system needs attention.

## Installation

### From Source

```bash
git clone https://github.com/rootcastleco/EchoTrace.git
cd EchoTrace
pip install -r requirements.txt
pip install -e .
```

### Dependencies

- Python 3.8+
- psutil (system monitoring)
- numpy (audio signal processing)

## Quick Start

### Generate a Demo

Hear what EchoTrace sounds like with a transition from healthy to anomalous states:

```bash
python -m echotrace --demo
```

This creates `echotrace_demo.wav` showing how the audio changes as system load increases.

### Live Monitoring

Monitor your system in real-time for 60 seconds and save the audio:

```bash
python -m echotrace -d 60 -o system_sound.wav
```

Run indefinitely (press Ctrl+C to stop):

```bash
python -m echotrace
```

### Command-Line Options

```
usage: python -m echotrace [-h] [-d DURATION] [-i INTERVAL] [-o OUTPUT] [--demo]

Options:
  -h, --help            Show help message
  -d, --duration        Duration to run in seconds (default: run indefinitely)
  -i, --interval        Sampling interval in seconds (default: 0.1)
  -o, --output          Output WAV file to save audio
  --demo                Generate a demo audio file and exit
```

## Programmatic Usage

### Basic Example

```python
from echotrace import EchoTrace

# Create instance
echo = EchoTrace(sample_interval=0.1)

# Generate demo
echo.generate_demo("demo.wav")

# Run live monitoring
echo.run(duration=30, output_file="monitoring.wav")
```

### Using Individual Components

```python
from echotrace import CPUMonitor, NetworkMonitor, SoundEngine
import time

# Create monitors and sound engine
cpu = CPUMonitor()
network = NetworkMonitor()
sound_engine = SoundEngine()

# Collect metrics
metrics_list = []
for _ in range(50):
    cpu_data = cpu.update()
    network_data = network.update()
    
    metrics = {
        "cpu_percent": cpu_data["cpu_percent"],
        "network_rate": network_data["total_bytes_rate"],
        "memory_percent": 50.0,
        "anomaly_score": cpu.get_anomaly_score()
    }
    metrics_list.append(metrics)
    time.sleep(0.1)

# Generate audio
soundscape = sound_engine.generate_soundscape(metrics_list)
sound_engine.save_audio(soundscape, "output.wav")
```

See the `examples/` directory for more usage patterns.

## Use Cases

- **System Monitoring**: Keep EchoTrace running in the background; anomalies become immediately audible
- **Performance Testing**: Monitor application behavior during load tests
- **Development**: Detect performance regressions while coding
- **Operations**: Quick health checks without looking at dashboards
- **Accessibility**: Audio-based monitoring for visually impaired system administrators

## Architecture

```
echotrace/
├── monitors.py       # System monitoring (CPU, Network, Sensors, Timing)
├── sound_engine.py   # Audio synthesis and signal generation
├── echotrace.py      # Main application coordinator
└── __main__.py       # CLI interface
```

### Monitors

- **CPUMonitor**: Tracks CPU usage, load average, per-core metrics
- **NetworkMonitor**: Monitors bytes/packets sent and received
- **SensorMonitor**: Tracks temperature, disk I/O, memory usage
- **TimingMonitor**: Measures timing intervals and jitter

### Sound Engine

The `SoundEngine` uses numpy-based audio synthesis to generate:
- Pure tones for steady states
- Pulsing tones for rhythmic activity
- Chords for complex states
- White noise for anomalies

### Anomaly Detection

Each monitor calculates anomaly scores based on:
- Variance and standard deviation from recent history
- Sudden spikes or changes in patterns
- High resource utilization
- Timing irregularities

## Contributing

Contributions are welcome! Areas for improvement:

- Additional audio synthesis techniques
- More sophisticated anomaly detection algorithms
- Support for custom metrics/plugins
- Real-time audio playback (currently WAV file output only)
- Machine learning-based pattern recognition

## License

MIT License - see LICENSE file for details.

## Acknowledgments

EchoTrace is inspired by the idea that humans are excellent at pattern recognition through audio. By sonifying system metrics, we can detect subtle anomalies that might be missed in visual dashboards.
