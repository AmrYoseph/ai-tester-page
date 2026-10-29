# Generates the Egyptian Arabic voiceover lines (edge-tts, ar-EG-ShakirNeural) into assets/vo/.
import os, subprocess
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
LINES = {
 "hook": "فريق تستنج كامل بالذكاء الاصطناعي.. يشتغل في متصفح حقيقي.",
 "excel": "ابعتلي ستوري أو جزء من الريكوايرمنت.. واستلم ملف إكسل بتستات إيجابية وسلبية وإيدج كيسز.",
 "replay": "كل سيناريو بيتنفّذ فعلاً، والناجح بيتسجّل وممكن يتعاد كل مرة بعد كده من غير ذكاء اصطناعي، عشان توفر توكنز في الريجريشن.",
 "verify": "كل تست بيتراجع مرتين ويحتاج دليل.. فنقلّل النجاح والفشل الفلاكي.",
 "report": "أرقام واضحة، وصور وفيديو وتتبّع لكل اختبار، وتقدر تشاركه برابط للقراءة فقط مع أي حد.",
 "integrate": "تكامل مع أدوات التتبّع، وتصدير مشروع جاهز، مع إصلاح ذاتي للاختبارات بالذكاء الاصطناعي.",
 "cta": "أول فحص مجاني.. ابعتلي ستوري أو رابط موقع تجريبي.",
}
for k, t in LINES.items():
    subprocess.run(["edge-tts", "--proxy", os.environ["HTTPS_PROXY"], "--voice", "ar-EG-ShakirNeural", "--rate=+15%",
                    "--text", t, "--write-media", f"{ROOT}/assets/vo/{k}.mp3"], check=True)
    f = f"{ROOT}/assets/vo/{k}.mp3"; subprocess.run(["ffmpeg","-y","-loglevel","error","-i",f,"-af","silenceremove=start_periods=1:start_threshold=-45dB,areverse,silenceremove=start_periods=1:start_threshold=-45dB,areverse","-ar","44100",f[:-4]+".wav"], check=True); os.remove(f)
    d = subprocess.run(["ffprobe","-v","error","-show_entries","format=duration","-of","csv=p=0",f[:-4]+".wav"],capture_output=True,text=True).stdout.strip()
    print(k, d)
