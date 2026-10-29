# Generates index.html and compositions/*.html for the Testopia intro.
import json, os
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
os.makedirs(f"{ROOT}/compositions", exist_ok=True)

FONT = """@font-face{font-family:'IBM Plex Sans Arabic';font-weight:400;src:url('assets/fonts/ibm-plex-sans-arabic-arabic-400-normal.woff2') format('woff2');}
@font-face{font-family:'IBM Plex Sans Arabic';font-weight:700;src:url('assets/fonts/ibm-plex-sans-arabic-arabic-700-normal.woff2') format('woff2');}"""
BASE = """#root{position:absolute;inset:0;background:#101216;color:#eceef2;font-family:'IBM Plex Sans Arabic','Inter',sans-serif;direction:rtl;overflow:hidden}
#root .glow{position:absolute;width:1400px;height:1400px;border-radius:50%;background:radial-gradient(circle,rgba(126,162,255,.16),rgba(181,78,224,.06) 45%,transparent 70%);left:260px;top:-300px}
#root .wrap{position:absolute;inset:0;padding:120px 160px;display:flex;flex-direction:column;gap:56px}
#root h1{font-size:76px;line-height:1.35;font-weight:700;max-width:1600px}
#root h1 em{font-style:normal;color:#7ea2ff}
#root .card{background:#171a20;border:2px solid #2a2f38;border-radius:24px}
#root .chip{display:inline-flex;align-items:center;gap:14px;padding:16px 30px;border-radius:999px;background:#1b2440;color:#eceef2;font-size:36px;font-weight:700}
#root .pass{color:#5fd49a}#root .fail{color:#ff8a80}#root .block{color:#f2b65e}
#root .mono{font-family:'JetBrains Mono',monospace;direction:ltr}
#root .row{display:flex;gap:28px;align-items:center}
#root .logo{width:120px;height:120px;border-radius:30px;background:linear-gradient(135deg,#8b7bef,#b54ee0 55%,#e901b7);display:flex;align-items:center;justify-content:center;font:900 72px Inter,sans-serif;color:#fff}"""

def scene(sid, dur, body, js):
    html = f"""<template>
  <style>
{FONT}
{BASE}
  </style>
  <div id="root" data-composition-id="{sid}" data-width="1920" data-height="1080">
    <div class="glow"></div>
    <div id="{sid}-c" class="clip wrap" data-start="0" data-duration="{dur}">
{body}
    </div>
  </div>
  <script>
    (function(){{
    const tl = gsap.timeline({{ paused: true }});
    const q = s => "#root [data-a='" + s + "']";
{js}
    tl.to("#{sid}-c > *", {{ opacity: 0, y: -24, duration: 0.35, ease: "power2.in", stagger: 0.03 }}, {dur} - 0.5);
    window.__timelines["{sid}"] = tl;
    }})();
  </script>
</template>
"""
    open(f"{ROOT}/compositions/{sid}.html", "w").write(html)

IN = 'tl.from({sel}, {{ opacity: 0, y: 40, duration: 0.6, ease: "power3.out", stagger: {st} }}, {t});'
def into(sel, t, st=0.12): return IN.format(sel=json.dumps(sel), t=t, st=st)

S = []  # (id, duration)

# 1 — hook
S.append(("hook", 4.6))
scene("hook", 4.6, """      <div class="row" data-a="brand" style="margin-top:60px"><div class="logo">T</div><div style="font:700 64px Inter,sans-serif;direction:ltr">Testopia</div></div>
      <h1 data-a="t">فريق تستنج كامل <em>بالذكاء الاصطناعي</em>..<br>يشتغل في متصفح حقيقي</h1>
      <div class="card row mono" data-a="bar" style="padding:22px 34px;font-size:30px;color:#a3a9b5;width:900px;justify-content:flex-end">
        <span>https://your-app.com/login</span><span style="width:22px;height:22px;border-radius:50%;background:#5fd49a;display:inline-block"></span></div>""",
  into("#root [data-a='t']", 0.1) + into("#root [data-a='bar']", 1.0))

# 2 — story to Excel
S.append(("excel", 6.6))
rows = [("TC-001","إيجابي","pass","تسجيل دخول ببيانات صحيحة"),("TC-002","سلبي","fail","باسورد غلط بيطلّع رسالة خطأ"),("TC-003","Edge","block","إيميل بمسافات زيادة"),("TC-004","سلبي","fail","حقل فاضي")]
rh = "".join(f'<div class="row er" style="padding:18px 32px;border-top:2px solid #2a2f38;font-size:32px"><span class="mono" style="color:#a3a9b5;width:170px">{a}</span><span class="{c}" style="width:150px;font-weight:700">{b}</span><span>{d}</span></div>' for a,b,c,d in rows)
scene("excel", 6.6, f"""      <h1 data-a="t">ابعتلي <em>ستوري</em> أو جزء من الريكوايرمنت..<br>واستلم ملف <em>إكسل</em> بتستات إيجابية وسلبية وإيدج كيسز</h1>
      <div class="row" style="gap:48px;align-items:stretch">
        <div class="card" data-a="story" style="padding:34px;width:520px;font-size:30px;line-height:1.6"><div style="color:#7ea2ff;font-weight:700">User Story</div>كمستخدم، عايز أسجّل دخول بالإيميل والباسورد</div>
        <div data-a="arrow" style="font-size:80px;color:#7ea2ff;align-self:center">←</div>
        <div class="card" data-a="sheet" style="flex:1;overflow:hidden"><div class="row" style="padding:18px 32px;background:#1f7a51;font-size:30px;font-weight:700">test-cases.xlsx</div>{rh}</div>
      </div>""",
  into("#root [data-a='t']", 0.1) + into("#root [data-a='story']", 0.8) + into("#root [data-a='arrow']", 1.3) + into("#root [data-a='sheet']", 1.6) + into("#root .er", 2.0, 0.25))

# 3 — executed, recorded, replayed without AI
S.append(("replay", 8.6))
steps = ["افتح /login","اكتب الإيميل","اكتب باسورد غلط","اضغط دخول","تأكد من رسالة الخطأ"]
sh = "".join(f'<div class="row st" style="font-size:32px;padding:12px 0"><span class="pass">✓</span><span>{s}</span></div>' for s in steps)
scene("replay", 8.6, f"""      <h1 data-a="t" style="font-size:66px">كل سيناريو <em>بيتنفّذ فعلاً</em>، والناجح بيتسجّل ويتعاد<br>في الريجريشن <em>من غير ذكاء اصطناعي</em> عشان توفر توكنز</h1>
      <div class="row" style="gap:48px;align-items:stretch">
        <div class="card" data-a="run" style="padding:30px 40px;width:760px">{sh}</div>
        <div style="display:flex;flex-direction:column;gap:30px;flex:1">
          <div class="chip" data-a="rec" style="background:#3a1620"><span class="fail">●</span> اتسجّل كسكريبت Playwright</div>
          <div class="chip" data-a="rep"><span>↻</span> Replay — ريجريشن كل مرة</div>
          <div class="card" data-a="tok" style="padding:30px 40px"><div style="font-size:30px;color:#a3a9b5">توكنز الذكاء الاصطناعي في الإعادة</div><div class="mono pass" style="font-size:110px;font-weight:700;text-align:right"><span id="tokn">12,480</span></div></div>
        </div>
      </div>""",
  into("#root [data-a='t']", 0.1) + into("#root [data-a='run']", 0.9) + into("#root .st", 1.2, 0.45) + into("#root [data-a='rec']", 3.6) + into("#root [data-a='rep']", 4.4) + into("#root [data-a='tok']", 5.0)
  + """
    const tk = { v: 12480 };
    tl.to(tk, { v: 0, duration: 1.6, ease: "power2.inOut", onUpdate: () => { const e = document.querySelector("#tokn"); if (e) e.textContent = Math.round(tk.v).toLocaleString("en-US"); } }, 5.8);""")

# 4 — double-checked with evidence
S.append(("verify", 5.2))
scene("verify", 5.2, """      <h1 data-a="t">كل تست <em>بيتراجع مرتين</em> ويحتاج <em>دليل</em>..<br>فنقلّل النجاح والفشل الفلاكي</h1>
      <div class="row" style="gap:40px">
        <div class="card ck" style="padding:40px 50px;font-size:38px;font-weight:700"><span class="pass">✓</span> مراجعة 1 — المتصفح</div>
        <div class="card ck" style="padding:40px 50px;font-size:38px;font-weight:700"><span class="pass">✓</span> مراجعة 2 — الدليل</div>
        <div class="chip ck" style="font-size:40px;padding:26px 44px;background:#123826"><span class="pass">Passed</span> مؤكد</div>
      </div>""",
  into("#root [data-a='t']", 0.1) + into("#root .ck", 1.0, 0.6))

# 5 — numbers, evidence, read-only link
S.append(("report", 6.6))
scene("report", 6.6, """      <h1 data-a="t" style="font-size:66px"><em>أرقام واضحة</em>، وصور وفيديو وتتبّع لكل اختبار،<br>وتقدر تشاركه <em>برابط للقراءة فقط</em> مع أي حد</h1>
      <div class="row" style="gap:36px">
        <div class="card nm" style="padding:30px 48px;text-align:center"><div class="mono pass" style="font-size:100px;font-weight:700">42</div><div style="font-size:30px">ناجح</div></div>
        <div class="card nm" style="padding:30px 48px;text-align:center"><div class="mono fail" style="font-size:100px;font-weight:700">3</div><div style="font-size:30px">فاشل</div></div>
        <div class="card nm" style="padding:30px 48px;text-align:center"><div class="mono block" style="font-size:100px;font-weight:700">1</div><div style="font-size:30px">محجوب</div></div>
        <div style="display:flex;flex-direction:column;gap:20px">
          <div class="row"><span class="chip ev">📸 صور</span><span class="chip ev">🎬 فيديو</span><span class="chip ev mono">Trace</span></div>
          <div class="card row mono ev" style="padding:20px 30px;font-size:28px;color:#7ea2ff">🔗 testopia.app/r/8f2c · read-only</div>
        </div>
      </div>""",
  into("#root [data-a='t']", 0.1) + into("#root .nm", 1.0, 0.2) + into("#root .ev", 2.2, 0.3))

# 6 — integrations, export, self-heal
S.append(("integrate", 5.6))
scene("integrate", 5.6, """      <h1 data-a="t">تكامل مع <em>أدوات التتبّع</em>، وتصدير مشروع جاهز،<br>مع <em>إصلاح ذاتي</em> للاختبارات بالذكاء الاصطناعي</h1>
      <div class="row" style="gap:30px">
        <span class="chip ig">Jira</span><span class="chip ig">Azure DevOps</span><span class="chip ig">📦 Playwright project</span>
      </div>
      <div class="card mono ig" style="padding:28px 40px;font-size:30px;line-height:1.7">
        <div class="fail">- page.locator('#btn-login')</div><div class="pass">+ page.getByRole('button', { name: 'Sign in' })</div></div>""",
  into("#root [data-a='t']", 0.1) + into("#root .ig", 1.0, 0.3))

# 7 — CTA
S.append(("cta", 5.8))
scene("cta", 5.8, """      <div class="row" data-a="brand" style="margin-top:80px"><div class="logo">T</div><div style="font:700 64px Inter,sans-serif;direction:ltr">Testopia</div></div>
      <h1 data-a="t" style="font-size:96px"><em>أول فحص مجاني</em></h1>
      <div data-a="s" style="font-size:52px;color:#a3a9b5">ابعتلي ستوري أو رابط موقع تجريبي</div>
      <div class="chip mono" data-a="u" style="font-size:36px;align-self:flex-start">amryoseph.github.io/ai-tester-page</div>""",
  into("#root [data-a='brand']", 0.1) + into("#root [data-a='t']", 0.4) + into("#root [data-a='s']", 0.9) + into("#root [data-a='u']", 1.4)
  .replace('tl.to("#cta-c', 'tl.to("#cta-x'))

t = 0; hosts = []
for i, (sid, d) in enumerate(S):
    hosts.append(f'      <div id="{sid}" data-composition-id="{sid}" data-composition-src="compositions/{sid}.html" data-start="{round(t,2)}" data-duration="{d}" data-track-index="1" data-track-kind="graphics" data-width="1920" data-height="1080" style="z-index:{i+1}"></div>')
    t += d
total = round(t, 2)
open(f"{ROOT}/index.html", "w").write(f"""<!doctype html>
<html lang="ar">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=1920, height=1080" />
    <script src="assets/js/gsap.min.js"></script>
    <style>
      * {{ margin: 0; padding: 0; box-sizing: border-box; }}
      html, body {{ width: 1920px; height: 1080px; overflow: hidden; background: #101216; }}
      #root {{ position: relative; width: 100%; height: 100%; }}
      #root > div {{ position: absolute; inset: 0; }}
    </style>
  </head>
  <body>
    <div id="root" data-composition-id="main" data-start="0" data-duration="{total}" data-width="1920" data-height="1080">
{chr(10).join(hosts)}
    </div>
    <script>
      window.__timelines["main"] = gsap.timeline({{ paused: true }});
    </script>
  </body>
</html>
""")
print("total", total)
