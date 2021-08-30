import pygame
from pydub import AudioSegment
import matplotlib.pyplot as plt
from flask import Flask
import numpy as np
import os
from flask import render_template, request
import librosa as lr
from glob import glob
app = Flask(__name__)


@app.route('/', methods=["GET", "POST"])
def index():
    if request.method == "POST":
        file = request.files["file"]
        file.save(os.path.join('uploads', file.filename))
        data_dir = './uploads'
        audio_file = glob(data_dir + '/*.wav')
        if len(audio_file) == 0:
            audio_file = glob(data_dir + '/*.mp3')
            sound = AudioSegment.from_mp3(audio_file[0])
            sound.export("./uploads/file.wav", format="wav")
            os.remove(audio_file[0])
        audio_file = glob(data_dir + '/*.wav')
        audio, sfreq = lr.load(audio_file[0])
        x = lr.get_duration(y=audio, sr=sfreq)
        x = int(len(audio)/x)
        time = np.arange(0, len(audio)) / sfreq
        pygame.mixer.init()
        my_sound = pygame.mixer.Sound(audio_file[0])
        my_sound.play()
        fig, ax = plt.subplots()
        plt.show(block=False)
        try:
            for i in range(0, len(audio), x):
                pygame.time.wait(887)
                chunk = audio[i:i + x]
                t = time[i:i + x]
                ax.plot(t, chunk)
                ax.set(xlabel='Time(s)', ylabel='Sound Amplitude')
                fig.canvas.draw()
                fig.canvas.flush_events()
                plt.cla()
        except Exception:
            my_sound.stop()
            return render_template("index.html", message="Done")
        finally:
            os.remove(audio_file[0])
        return render_template("index.html", message="success")
    return render_template("index.html", message="Upload the audio file(mp3,wav)")


if __name__ == '__main__':
    app.run(debug=True)
