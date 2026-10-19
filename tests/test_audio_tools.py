"""DSP integration checks use generated signals, never a bundled song."""
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

import numpy as np
import soundfile as sf

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
from audio_dsp import SR, compressor, room, tape_stop  # noqa: E402


class AudioToolsTests(unittest.TestCase):
    def test_stretch_preserves_pitch_and_rejects_overwrite(self):
        with tempfile.TemporaryDirectory() as folder:
            path = Path(folder)
            t = np.arange(3 * SR) / SR
            sf.write(path / "source.wav", np.column_stack([.2 * np.sin(2*np.pi*440*t)]*2), SR)
            command = [sys.executable, str(ROOT / "scripts/audio_tools.py"), "stretch",
                       str(path / "source.wav"), "--speed", "1.25", "--out", str(path / "out.wav")]
            subprocess.run(command, check=True, capture_output=True)
            y, sr = sf.read(path / "out.wav")
            self.assertLess(abs(len(y)/sr - 2.4), .06)
            spectrum = np.abs(np.fft.rfft(y[sr//4:sr, 0]))
            frequency = np.fft.rfftfreq(len(y[sr//4:sr]), 1/sr)[spectrum.argmax()]
            self.assertLess(abs(frequency-440), 3)
            before = (path / "out.wav").read_bytes()
            result = subprocess.run(command, capture_output=True, text=True)
            self.assertNotEqual(result.returncode, 0)
            self.assertIn("already exists", result.stderr)
            self.assertEqual((path / "out.wav").read_bytes(), before)

    def test_room_is_seeded_and_tape_stop_has_explicit_length(self):
        y = np.zeros((SR, 2));y[0] = .5
        np.testing.assert_array_equal(room(y, seed=23), room(y, seed=23))
        self.assertFalse(np.array_equal(room(y, seed=23), room(y, seed=24)))
        stopped, _ = tape_stop(y, seconds=1.5)
        self.assertEqual(stopped.shape, (round(1.5*SR), 2))
        self.assertTrue(np.isfinite(stopped).all())

    def test_linked_compressor_preserves_channel_ratio(self):
        t = np.arange(SR) / SR
        mono = np.sin(2*np.pi*440*t) * .8
        y = np.column_stack([mono, mono*.3])
        out = compressor(y)
        self.assertLess(np.max(np.abs(out)), np.max(np.abs(y)))
        np.testing.assert_allclose(out[:, 1], out[:, 0]*.3, atol=1e-7)


if __name__ == "__main__":
    unittest.main()
