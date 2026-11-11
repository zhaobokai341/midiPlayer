import sys
import os
import numpy as np
import pretty_midi
import sounddevice as sd
from PIL import Image, ImageDraw

Image.MAX_IMAGE_PIXELS = None

# ==============================
# Configuration
# ==============================

TIME_STEP = 0.02       # 20 ms per pixel
SAMPLE_RATE = 44100
ATTACK = 0.005
RELEASE = 0.025

# ==============================
# MIDI -> PNG
# ==============================

def encode(midi_path, image_path):

    midi = pretty_midi.PrettyMIDI(midi_path)

    notes = []

    for instrument in midi.instruments:
        for note in instrument.notes:
            notes.append(note)

    notes.sort(key=lambda n: n.start)

    if not notes:
        raise ValueError("MIDI contains no notes!")

    width = int(np.ceil(midi.get_end_time() / TIME_STEP)) + 2
    height = len(notes) + 1

    # Black background
    image = Image.new("RGB", (width, height), (0, 0, 0))
    draw = ImageDraw.Draw(image)

    for row, note in enumerate(notes):

        start = int(note.start / TIME_STEP)
        end = int(np.ceil(note.end / TIME_STEP))

        end = max(start + 1, end)
        end = min(end, width - 1)

        # Red = pitch
        # Green = velocity
        # Blue = 0
        color = (note.pitch, note.velocity, 0)

        draw.line(
            (start, row, end - 1, row),
            fill=color
        )

    # White end-of-song marker
    draw.point(
        (width - 1, height - 1),
        fill=(255, 255, 255)
    )

    image.save(image_path, optimize=True)

    print("Encoding completed!")
    print("Notes:", len(notes))
    print("Image dimensions:", image.size)
    print("Saved:", image_path)


# ==============================
# PNG -> Notes
# ==============================

def decode(image_path):

    image = Image.open(image_path).convert("RGB")
    pixels = np.asarray(image)

    notes = []

    height, width, _ = pixels.shape

    for row in range(height):

        # Ignore the end marker
        active = (
            (pixels[row, :, 1] > 0) &
            (pixels[row, :, 2] == 0)
        )

        positions = np.flatnonzero(active)

        if len(positions) == 0:
            continue

        start = positions[0]
        end = positions[-1] + 1

        pitch = int(pixels[row, start, 0])
        velocity = int(pixels[row, start, 1])

        notes.append({
            "pitch": pitch,
            "velocity": velocity,
            "start": start * TIME_STEP,
            "end": end * TIME_STEP
        })

    return notes


# ==============================
# Play reconstructed music
# ==============================

def play(image_path):

    notes = decode(image_path)

    if not notes:
        raise ValueError("No notes found in image!")

    duration = max(n["end"] for n in notes)

    total_samples = int(duration * SAMPLE_RATE) + 1

    audio = np.zeros(total_samples, dtype=np.float32)

    for note in notes:

        frequency = pretty_midi.note_number_to_hz(
            note["pitch"]
        )

        start = int(note["start"] * SAMPLE_RATE)
        end = int(note["end"] * SAMPLE_RATE)

        length = end - start

        if length <= 0:
            continue

        t = np.arange(length) / SAMPLE_RATE

        # Simple sine-wave synthesizer
        wave = np.sin(2 * np.pi * frequency * t)

        # Attack and release envelope
        envelope = np.ones(length)

        attack_samples = min(
            int(ATTACK * SAMPLE_RATE), length
        )

        release_samples = min(
            int(RELEASE * SAMPLE_RATE), length
        )

        if attack_samples > 0:
            envelope[:attack_samples] = np.linspace(
                0, 1, attack_samples
            )

        if release_samples > 0:
            envelope[-release_samples:] = np.linspace(
                1, 0, release_samples
            )

        volume = note["velocity"] / 127 * 0.12

        audio[start:end] += (
            wave * envelope * volume
        )

    # Prevent clipping
    peak = np.max(np.abs(audio))

    if peak > 0:
        audio *= 0.95 / peak

    print("Playing reconstructed song...")
    print("Notes:", len(notes))
    print("Duration:", round(duration, 2), "seconds")

    sd.play(audio, SAMPLE_RATE)
    sd.wait()

    print("Playback finished!")


# ==============================
# Command line
# ==============================

if __name__ == "__main__":

    if len(sys.argv) < 3:
        print("""
Usage:

Generate image:
    python convertToImageAndPlay.py encode input.mid output.png

Play image:
    python convertToImageAndPlay.py play output.png
""")
        sys.exit(1)

    command = sys.argv[1]

    if command == "encode":
        encode(sys.argv[2], sys.argv[3])

    elif command == "play":
        play(sys.argv[2])

    else:
        print("Unknown command:", command)
	

