# Cleans Amr's recorded voice (assets/vo-src/amr-voice.mp4) and splits it into one WAV per scene.
import os, subprocess
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRC = f"{ROOT}/assets/vo-src/amr-voice.mp4"
# Speech spans (s) found with silencedetect at -35 dB, one per scene.
CUTS = {"hook": (1.19, 5.59), "excel": (7.29, 13.11), "replay": (15.11, 23.36), "verify": (25.29, 29.83),
        "report": (31.10, 38.52), "integrate": (40.19, 47.15), "cta": (48.76, 53.72)}
PAD = 0.12
CLEAN = "highpass=f=80,lowpass=f=12000,afftdn=nf=-25,acompressor=threshold=-20dB:ratio=3:attack=5:release=120,loudnorm=I=-16:TP=-1.5:LRA=7"
full = f"{ROOT}/assets/vo-src/clean.wav"
subprocess.run(["ffmpeg","-y","-loglevel","error","-i",SRC,"-vn","-ac","1","-ar","48000","-af",CLEAN,full], check=True)
for k, (a, b) in CUTS.items():
    a, b = max(0, a - PAD), b + PAD
    subprocess.run(["ffmpeg","-y","-loglevel","error","-i",full,"-ss",str(a),"-to",str(b),
                    "-af","afade=t=in:d=0.04,areverse,afade=t=in:d=0.08,areverse",f"{ROOT}/assets/vo/{k}.wav"], check=True)
    print(k, round(b - a, 2))
