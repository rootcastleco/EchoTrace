"""
Sound generation engine for EchoTrace.

Converts system metrics into sound signatures using audio synthesis.
"""

import numpy as np
import wave
import time
from typing import Dict, Any


class SoundEngine:
    """
    Generates audio signals based on system metrics.
    
    Maps different metrics to audio parameters:
    - CPU usage -> Base frequency (higher CPU = higher pitch)
    - Network activity -> Rhythm/pulse rate
    - Memory/Sensors -> Amplitude/volume
    - Anomalies -> Dissonance/irregular patterns
    """
    
    def __init__(self, sample_rate: int = 22050, channels: int = 1):
        self.sample_rate = sample_rate
        self.channels = channels
        self.base_frequency = 440.0  # A4 note
        
    def generate_tone(self, frequency: float, duration: float, amplitude: float = 0.3) -> np.ndarray:
        """Generate a pure tone at given frequency."""
        num_samples = int(self.sample_rate * duration)
        t = np.linspace(0, duration, num_samples, False)
        
        # Generate sine wave
        tone = amplitude * np.sin(2 * np.pi * frequency * t)
        
        # Apply envelope to avoid clicks
        envelope = np.ones(num_samples)
        fade_samples = int(self.sample_rate * 0.01)  # 10ms fade
        if num_samples > 2 * fade_samples:
            envelope[:fade_samples] = np.linspace(0, 1, fade_samples)
            envelope[-fade_samples:] = np.linspace(1, 0, fade_samples)
        
        return tone * envelope
        
    def generate_chord(self, base_freq: float, duration: float, 
                      intervals: list = [1.0, 1.25, 1.5], amplitude: float = 0.2) -> np.ndarray:
        """Generate a chord with multiple frequencies."""
        chord = np.zeros(int(self.sample_rate * duration))
        
        for interval in intervals:
            freq = base_freq * interval
            tone = self.generate_tone(freq, duration, amplitude / len(intervals))
            chord += tone
            
        return chord
        
    def generate_pulse(self, frequency: float, pulse_rate: float, duration: float, 
                      amplitude: float = 0.3) -> np.ndarray:
        """Generate a pulsing tone with rhythm."""
        num_samples = int(self.sample_rate * duration)
        t = np.linspace(0, duration, num_samples, False)
        
        # Carrier wave
        carrier = np.sin(2 * np.pi * frequency * t)
        
        # Modulation for pulse effect
        pulse = (1 + np.sin(2 * np.pi * pulse_rate * t)) / 2
        
        return amplitude * carrier * pulse
        
    def generate_noise(self, duration: float, amplitude: float = 0.1) -> np.ndarray:
        """Generate white noise for anomaly indication."""
        num_samples = int(self.sample_rate * duration)
        return amplitude * np.random.uniform(-1, 1, num_samples)
        
    def metrics_to_sound(self, metrics: Dict[str, Any], duration: float = 0.1) -> np.ndarray:
        """
        Convert system metrics to audio signal.
        
        Mapping strategy:
        - CPU usage: Controls base frequency (20-80% CPU -> 200-800 Hz)
        - Network rate: Controls pulse/rhythm rate (0-10 Hz)
        - Memory usage: Controls amplitude (0.1-0.5)
        - Anomaly score: Adds dissonance/noise
        """
        cpu_percent = metrics.get("cpu_percent", 50.0)
        network_rate = metrics.get("network_rate", 0.0)
        memory_percent = metrics.get("memory_percent", 50.0)
        anomaly_score = metrics.get("anomaly_score", 0.0)
        
        # Map CPU to frequency (200-800 Hz range)
        base_freq = 200 + (cpu_percent / 100.0) * 600
        
        # Map network activity to pulse rate (1-10 Hz)
        # Normalize network rate (assume max of 100 MB/s = 100000000 bytes/s)
        network_normalized = min(network_rate / 10_000_000, 1.0)
        pulse_rate = 1.0 + network_normalized * 9.0
        
        # Map memory to amplitude (0.1-0.5)
        amplitude = 0.1 + (memory_percent / 100.0) * 0.4
        
        # Generate base sound
        if network_rate > 100:  # If there's network activity
            sound = self.generate_pulse(base_freq, pulse_rate, duration, amplitude)
        else:
            sound = self.generate_tone(base_freq, duration, amplitude)
            
        # Add dissonance for anomalies
        if anomaly_score > 0.3:
            # Add a dissonant frequency (tritone interval)
            dissonant_freq = base_freq * 1.414  # sqrt(2) - tritone
            dissonance = self.generate_tone(dissonant_freq, duration, amplitude * anomaly_score * 0.5)
            sound = sound + dissonance
            
        # Add noise for high anomalies
        if anomaly_score > 0.6:
            noise = self.generate_noise(duration, amplitude * anomaly_score * 0.3)
            sound = sound + noise
            
        # Normalize to prevent clipping
        max_val = np.max(np.abs(sound))
        if max_val > 1.0:
            sound = sound / max_val
            
        return sound
        
    def save_audio(self, audio_data: np.ndarray, filename: str):
        """Save audio data to WAV file."""
        # Convert to 16-bit PCM
        audio_int = np.int16(audio_data * 32767)
        
        with wave.open(filename, 'w') as wav_file:
            wav_file.setnchannels(self.channels)
            wav_file.setsampwidth(2)  # 16-bit
            wav_file.setframerate(self.sample_rate)
            wav_file.writeframes(audio_int.tobytes())
            
    def generate_soundscape(self, metrics_list: list, duration_per_sample: float = 0.1) -> np.ndarray:
        """Generate a continuous soundscape from a list of metric samples."""
        if not metrics_list:
            return np.array([])
            
        sounds = []
        for metrics in metrics_list:
            sound = self.metrics_to_sound(metrics, duration_per_sample)
            sounds.append(sound)
            
        # Concatenate all sounds
        soundscape = np.concatenate(sounds)
        return soundscape
        
    def generate_demo_sound(self) -> np.ndarray:
        """Generate a demo sound showing healthy vs anomalous system states."""
        demo_metrics = []
        
        # Healthy system (10 samples)
        for i in range(10):
            demo_metrics.append({
                "cpu_percent": 30.0 + np.random.uniform(-5, 5),
                "network_rate": 1000000,  # 1 MB/s
                "memory_percent": 40.0 + np.random.uniform(-3, 3),
                "anomaly_score": 0.1
            })
            
        # Transition to anomalous state (10 samples)
        for i in range(10):
            progress = i / 10.0
            demo_metrics.append({
                "cpu_percent": 30.0 + progress * 60.0 + np.random.uniform(-10, 10),
                "network_rate": 1000000 * (1 + progress * 5),
                "memory_percent": 40.0 + progress * 50.0,
                "anomaly_score": progress * 0.8
            })
            
        return self.generate_soundscape(demo_metrics, duration_per_sample=0.2)
