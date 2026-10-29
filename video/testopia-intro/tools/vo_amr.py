# Cleans Amr's recorded voice (assets/vo-src/amr-voice-2.m4a) and splits it into one WAV per scene.
import os, subprocess
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRC = f"{ROOT}/assets/vo-src/amr-voice-2.m4a"
# Speech spans (s) found with silencedetect at -35 dB, one per scene.
CUTS = {"hook": (1.12, 5.13), "excel": (9.22, 13.96), "replay": (17.02, 22.65), "verify": (26.27, 32.38),
        "report": (33.31, 39.12), "integrate": (40.36, 47.81), "cta": (48.45, 52.05)}
PAD = 0.12
CLEAN = "highpass=f=80,lowpass=f=12000,afftdn=nf=-25,acompressor=threshold=-20dB:ratio=3:attack=5:release=120,loudnorm=I=-16:TP=-1.5:LRA=7"
full = f"{ROOT}/assets/vo-src/clean.wav"
subprocess.run(["ffmpeg","-y","-loglevel","error","-i",SRC,"-vn","-ac","1","-ar","48000","-af",CLEAN,full], check=True)
for k, (a, b) in CUTS.items():
    a, b = max(0, a - PAD), b + PAD
    subprocess.run(["ffmpeg","-y","-loglevel","error","-i",full,"-ss",str(a),"-to",str(b),
                    "-af","afade=t=in:d=0.04,areverse,afade=t=in:d=0.08,areverse",f"{ROOT}/assets/vo/{k}.wav"], check=True)
    print(k, round(b - a, 2))
