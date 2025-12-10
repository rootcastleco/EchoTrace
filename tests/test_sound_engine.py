"""Tests for sound engine."""

import numpy as np
import os
import tempfile
from echotrace import SoundEngine


def test_sound_engine_init():
    """Test sound engine initialization."""
    engine = SoundEngine()
    assert engine.sample_rate == 22050
    assert engine.channels == 1
    assert engine.base_frequency == 440.0


def test_generate_tone():
    """Test tone generation."""
    engine = SoundEngine()
    tone = engine.generate_tone(440.0, 0.1, 0.3)
    
    assert isinstance(tone, np.ndarray)
    assert len(tone) == int(engine.sample_rate * 0.1)
    assert np.max(np.abs(tone)) <= 1.0  # Should be normalized


def test_generate_chord():
    """Test chord generation."""
    engine = SoundEngine()
    chord = engine.generate_chord(440.0, 0.1, [1.0, 1.25, 1.5], 0.2)
    
    assert isinstance(chord, np.ndarray)
    assert len(chord) == int(engine.sample_rate * 0.1)
    assert np.max(np.abs(chord)) <= 1.0


def test_generate_pulse():
    """Test pulse generation."""
    engine = SoundEngine()
    pulse = engine.generate_pulse(440.0, 5.0, 0.1, 0.3)
    
    assert isinstance(pulse, np.ndarray)
    assert len(pulse) == int(engine.sample_rate * 0.1)
    assert np.max(np.abs(pulse)) <= 1.0


def test_generate_noise():
    """Test noise generation."""
    engine = SoundEngine()
    noise = engine.generate_noise(0.1, 0.1)
    
    assert isinstance(noise, np.ndarray)
    assert len(noise) == int(engine.sample_rate * 0.1)
    assert np.max(np.abs(noise)) <= 1.0


def test_metrics_to_sound():
    """Test converting metrics to sound."""
    engine = SoundEngine()
    metrics = {
        "cpu_percent": 50.0,
        "network_rate": 1000000,
        "memory_percent": 60.0,
        "anomaly_score": 0.3
    }
    
    sound = engine.metrics_to_sound(metrics, 0.1)
    
    assert isinstance(sound, np.ndarray)
    assert len(sound) == int(engine.sample_rate * 0.1)
    assert np.max(np.abs(sound)) <= 1.0


def test_save_audio():
    """Test saving audio to WAV file."""
    engine = SoundEngine()
    audio = engine.generate_tone(440.0, 0.1, 0.3)
    
    with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as f:
        filename = f.name
    
    try:
        engine.save_audio(audio, filename)
        assert os.path.exists(filename)
        assert os.path.getsize(filename) > 0
    finally:
        if os.path.exists(filename):
            os.remove(filename)


def test_generate_soundscape():
    """Test generating a soundscape from multiple metrics."""
    engine = SoundEngine()
    metrics_list = [
        {"cpu_percent": 30.0, "network_rate": 100000, "memory_percent": 40.0, "anomaly_score": 0.1},
        {"cpu_percent": 35.0, "network_rate": 150000, "memory_percent": 45.0, "anomaly_score": 0.2},
        {"cpu_percent": 40.0, "network_rate": 200000, "memory_percent": 50.0, "anomaly_score": 0.3},
    ]
    
    soundscape = engine.generate_soundscape(metrics_list, duration_per_sample=0.1)
    
    assert isinstance(soundscape, np.ndarray)
    expected_length = len(metrics_list) * int(engine.sample_rate * 0.1)
    assert len(soundscape) == expected_length
    assert np.max(np.abs(soundscape)) <= 1.0


def test_generate_demo_sound():
    """Test generating demo sound."""
    engine = SoundEngine()
    demo = engine.generate_demo_sound()
    
    assert isinstance(demo, np.ndarray)
    assert len(demo) > 0
    assert np.max(np.abs(demo)) <= 1.0


if __name__ == "__main__":
    print("Running sound engine tests...")
    test_sound_engine_init()
    print("✓ Sound engine initialization test passed")
    test_generate_tone()
    print("✓ Generate tone test passed")
    test_generate_chord()
    print("✓ Generate chord test passed")
    test_generate_pulse()
    print("✓ Generate pulse test passed")
    test_generate_noise()
    print("✓ Generate noise test passed")
    test_metrics_to_sound()
    print("✓ Metrics to sound test passed")
    test_save_audio()
    print("✓ Save audio test passed")
    test_generate_soundscape()
    print("✓ Generate soundscape test passed")
    test_generate_demo_sound()
    print("✓ Generate demo sound test passed")
    print("\nAll tests passed!")
