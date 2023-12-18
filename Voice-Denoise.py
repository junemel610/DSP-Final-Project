import pyaudio
import wave
import noisereduce as nr
import matplotlib.pyplot as plt
from scipy.io import wavfile

def find_input_devices():
    p = pyaudio.PyAudio()
    info = p.get_host_api_info_by_index(0)
    numdevices = info.get('deviceCount')
    devices = []
    for i in range(0, numdevices):
        if (p.get_device_info_by_host_api_device_index(0, i).get('maxInputChannels')) > 0:
            devices.append((i, p.get_device_info_by_host_api_device_index(0, i).get('name')))
    return devices

def record_audio(file_name, duration=15):
    chunk_size = 1024
    format = pyaudio.paInt16
    channels = 1
    rate = 44100

    p = pyaudio.PyAudio()

    stream = p.open(format=format,
                    channels=channels,
                    rate=rate,
                    input=True,
                    frames_per_buffer=chunk_size)

    frames_raw = []

    try:
        print("Recording...")
        for i in range(0, int(rate / chunk_size * duration)):
            data = stream.read(chunk_size)
            frames_raw.append(data)

    except KeyboardInterrupt:
        print("Recording interrupted.")

    finally:
        print("Recording done.")
        stream.stop_stream()
        stream.close()
        p.terminate()

        with wave.open(file_name, 'wb') as wf_raw:
            wf_raw.setnchannels(channels)
            wf_raw.setsampwidth(p.get_sample_size(format))
            wf_raw.setframerate(rate)
            wf_raw.writeframes(b''.join(frames_raw))
        print(f"Raw audio saved to {file_name}")

def plot_audio(signal, title):
    plt.figure(figsize=(14, 5))
    plt.plot(signal)
    plt.title(title)
    plt.xlabel('Sample Index')
    plt.ylabel('Amplitude')
    plt.show()

# Record raw audio
raw_file = "recorded_audio_raw.wav"
record_audio(raw_file)

# Load the raw audio
rate, data_raw = wavfile.read(raw_file)

# Plot the raw audio
plot_audio(data_raw, 'Raw Audio')

# Perform noise reduction
data_reduced = nr.reduce_noise(data_raw, sr=rate)

# Save the processed audio
processed_file = "recorded_audio_processed.wav"
wavfile.write(processed_file, rate, data_reduced)

# Plot the noise-reduced audio
plot_audio(data_reduced, 'Noise-Reduced Audio')
print(f"Processed audio saved to {processed_file}")


