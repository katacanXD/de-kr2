# -*- coding: utf-8 -*-
import json, os, sys, io
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from data import LESSONS, VOCAB, PRON_RULES, PRON_WORDS, GRAMMAR

ROOT = r"C:\дз\немецкий"
BUILD = os.path.join(ROOT, "build")
os.makedirs(BUILD, exist_ok=True)

TOTAL = sum(len(sec[3]) for l in LESSONS for sec in l["sections"])


# ---------------------------------------------------------------- reference
CSS = r"""
@page { size: A4; margin: 13mm 12.5mm 14mm 12.5mm; }
* { box-sizing: border-box; }
html { -webkit-print-color-adjust: exact; print-color-adjust: exact; }
body {
  font-family: Georgia, "Times New Roman", serif;
  font-size: 9.4pt; line-height: 1.36; color: #1c222c; margin: 0;
}
h1,h2,h3,.sans { font-family: "Segoe UI", "Trebuchet MS", sans-serif; }

/* ---------- cover ---------- */
.cover { page-break-after: always; }
.cv-hero {
  background: #101a29; color: #fff; padding: 16mm 11mm 12mm; border-radius: 1.5mm;
}
.cv-kicker { font-family:"Segoe UI",sans-serif; font-size:8pt; letter-spacing:.22em;
  text-transform:uppercase; color:#7fa8d9; }
.cv-hero h1 { font-size: 25pt; line-height:1.1; margin: 5mm 0 3mm; font-weight:600; letter-spacing:-.01em; }
.cv-hero .lead { font-size: 10.5pt; color:#c3d1e4; margin:0; }
.cv-meta { display:flex; gap:0; margin-top: 9mm; border-top:.4pt solid #37506f; padding-top:4mm; }
.cv-meta div { flex:1; }
.cv-meta .k { font-family:"Segoe UI",sans-serif; font-size:7.4pt; letter-spacing:.14em;
  text-transform:uppercase; color:#7fa8d9; display:block; margin-bottom:1mm; }
.cv-meta .v { font-size:11pt; color:#fff; }

.cv-body { margin-top: 8mm; }
.cv-grid { display:flex; gap: 6mm; }
.cv-col { flex: 1; }
.box { border:.4pt solid #d8dee7; border-left: 2.4pt solid #1f4e8c; padding: 3.5mm 4mm; margin-bottom: 5mm; border-radius: .8mm; break-inside: avoid; }
.box.flow { break-inside: auto; }
.box.alt { border-left-color:#a8562a; }
.box h3 { font-size: 9.6pt; margin:0 0 2mm; color:#101a29; letter-spacing:.01em; }
.box ul { margin:0; padding-left: 4.2mm; }
.box li { margin-bottom: 1.4mm; font-size: 9pt; }
.box p { margin:0 0 1.5mm; font-size:9pt; }
.tag { display:inline-block; font-family:"Segoe UI",sans-serif; font-size:7.2pt; letter-spacing:.1em;
  text-transform:uppercase; background:#eef2f8; color:#1f4e8c; padding:.6mm 1.8mm; border-radius:.6mm; margin-bottom:2mm; }
b.hl { color:#8f3d12; }
.cv-index { display:flex; flex-wrap:wrap; gap:2mm 0; margin-top:2mm; border-top:.4pt solid #d8dee7; padding-top:3mm; }
.cv-index span { font-family:"Segoe UI",sans-serif; font-size:8.1pt; color:#64748b; width:33.33%; }
.cv-index b { display:inline-block; width:4mm; height:4mm; line-height:4mm; text-align:center; border-radius:50%;
  background:#eef2f8; color:#1f4e8c; font-size:7pt; margin-right:1.4mm; }

/* ---------- lesson header ---------- */
.lesson { page-break-before: always; }
.lesson:first-of-type { page-break-before: auto; }
.lsn-bar { background:#101a29; color:#fff; padding: 5mm 5.5mm; border-radius:1mm; margin-bottom: 4mm; }
.lsn-bar .num { font-family:"Segoe UI",sans-serif; font-size:7.6pt; letter-spacing:.2em;
  text-transform:uppercase; color:#7fa8d9; }
.lsn-bar h2 { margin:1.4mm 0 1mm; font-size:16pt; font-weight:600; letter-spacing:-.01em; }
.lsn-bar .tr { font-size:9.4pt; color:#c3d1e4; font-style:italic; }
.lsn-bar .pg { font-family:"Segoe UI",sans-serif; font-size:8pt; color:#8fa9c8; margin-top:2mm;
  border-top:.4pt solid #27384d; padding-top:2mm; }

/* ---------- section ---------- */
.sec { display:flex; align-items:baseline; gap:2.6mm; background:#eef2f8; border-left:2.4pt solid #1f4e8c;
  padding: 1.8mm 3mm; margin: 4.5mm 0 1.5mm; break-after:avoid; break-inside:avoid; border-radius:0 .8mm .8mm 0; }
.sec .k { font-family:"Segoe UI",sans-serif; font-weight:700; font-size:8.6pt; color:#1f4e8c; letter-spacing:.08em; }
.sec .rt { font-family:"Segoe UI",sans-serif; font-weight:600; font-size:9.2pt; color:#101a29; }
.sec .dt { margin-left:auto; font-size:8.2pt; color:#64748b; font-style:italic; white-space:nowrap; }

/* ---------- item ---------- */
.item { display:flex; gap:2.4mm; padding: 1.5mm 0; break-inside:avoid; }
.item + .item { border-top:.35pt solid #e8ecf2; }
.item .n { flex:0 0 6mm; font-family:"Segoe UI",sans-serif; font-size:7.6pt; color:#98a2b3;
  padding-top:.5mm; font-variant-numeric: tabular-nums; }
.item .b { flex:1; }
.ru { color:#4c5666; }
.de { color:#0b1220; font-weight:700; margin-top:.4mm; }
.note { font-size:7.9pt; color:#7a5d33; margin-top:.7mm; line-height:1.3; }
.note::before { content:"▸ "; color:#b9954f; }

/* ---------- appendix ---------- */
.appx { page-break-before: always; }
.appx-h { border-bottom:1.6pt solid #101a29; padding-bottom:2mm; margin-bottom:4mm; }
.appx-h .num { font-family:"Segoe UI",sans-serif; font-size:7.4pt; letter-spacing:.2em;
  text-transform:uppercase; color:#8a94a3; }
.appx-h h2 { margin:1mm 0 0; font-size:15pt; font-weight:600; letter-spacing:-.01em; }
.vgroup { margin-bottom:4mm; break-inside:avoid; }
.vgroup h3 { font-family:"Segoe UI",sans-serif; font-size:8.4pt; letter-spacing:.13em; text-transform:uppercase;
  color:#1f4e8c; margin:0 0 1.6mm; }
.vlist { display:flex; flex-wrap:wrap; gap:0 5mm; }
.vlist span { font-size:9pt; }
.vlist i { color:#64748b; font-style:normal; }
.cols2 { column-count:2; column-gap:7mm; }

table.rules { width:100%; border-collapse:collapse; font-size:8.7pt; }
table.rules th { text-align:left; font-family:"Segoe UI",sans-serif; font-size:7.4pt; letter-spacing:.12em;
  text-transform:uppercase; color:#64748b; border-bottom:.6pt solid #c7d0dc; padding:0 2mm .9mm 0; }
table.rules td { padding:.95mm 2mm .95mm 0; border-bottom:.35pt solid #e8ecf2; vertical-align:top; }
table.rules td.w { font-weight:700; color:#101a29; white-space:nowrap; }
table.rules td.p { color:#8f3d12; white-space:nowrap; }

.gbox { border:.4pt solid #d8dee7; border-radius:.8mm; padding:3mm 3.5mm; margin-bottom:3.5mm; break-inside:avoid; }
.gbox h3 { font-family:"Segoe UI",sans-serif; font-size:9.4pt; margin:0 0 1mm; color:#101a29; }
.gbox .pat { font-family:"Segoe UI",sans-serif; font-size:8.2pt; color:#1f4e8c; margin-bottom:1.6mm; }
.gbox p { margin:0; font-size:8.9pt; line-height:1.4; }

.run .rt { font-family:"Segoe UI",sans-serif; font-size:8.2pt; font-weight:700; color:#1f4e8c;
  margin:4mm 0 1.4mm; letter-spacing:.04em; break-after:avoid; }
.run p { margin:0 0 1.1mm; padding-left:6mm; text-indent:-6mm; font-size:8.9pt; break-inside:avoid; }
.run p b { font-family:"Segoe UI",sans-serif; font-size:7.4pt; color:#98a2b3; font-weight:600; }
.foot { margin-top:6mm; border-top:.4pt solid #d8dee7; padding-top:2mm; font-size:7.6pt; color:#8a94a3;
  font-family:"Segoe UI",sans-serif; }
"""


def ref_html():
    o = []
    A = o.append
    A('<!doctype html><html lang="ru"><head><meta charset="utf-8">')
    A('<title>Перевод · КМ · немецкий</title><style>%s</style></head><body>' % CSS)

    # ---------------- cover
    A('<section class="cover">')
    A('<div class="cv-hero">')
    A('<div class="cv-kicker">Контрольное мероприятие · немецкий язык</div>')
    A('<h1>Перевод: 10 предложений<br>русский → немецкий</h1>')
    A('<p class="lead">Урок 2, упр. 4 (с. 124–126) · Урок 3, упр. 4 (с. 177–180)</p>')
    A('<div class="cv-meta">')
    A('<div><span class="k">Предложений в базе</span><span class="v">%d</span></div>' % TOTAL)
    A('<div><span class="k">В билете</span><span class="v">10</span></div>')
    A('<div><span class="k">Баллы</span><span class="v">10 + 2</span></div>')
    A('<div><span class="k">На повторение</span><span class="v">5–7 минут</span></div>')
    A('</div></div>')

    A('<div class="cv-body"><div class="cv-grid">')

    A('<div class="cv-col">')
    A('<div class="box"><span class="tag">Как устроен КМ</span><ul>')
    A('<li><b>10 предложений</b> русский → немецкий — до <b>10 баллов</b>.</li>')
    A('<li><b>Произношение</b> при переводе — до <b>2 баллов</b>.</li>')
    A('<li>Вытянув билет, можно <b>вернуться на место на 5–7 минут</b> и посмотреть свои записи.</li>')
    A('<li>Потом — ответ <b>только по русскому тексту</b> в билете, без записей.</li>')
    A('</ul></div>')

    A('<div class="box alt"><span class="tag">Главный вывод</span>')
    A('<p>Все формулировки — <b class="hl">дословно из учебных текстов</b>. '
      'Задача — не сочинять свой перевод, а <b class="hl">узнать предложение и воспроизвести его</b> так, как оно стоит в тексте.</p>')
    A('<p style="margin-bottom:0">Поэтому учить надо <b>парами</b>: русская фраза → немецкая фраза, вслух.</p>')
    A('</div>')
    A('</div>')

    A('<div class="cv-col">')
    A('<div class="box"><span class="tag">Как пользоваться файлом</span><ul>')
    A('<li><b>Шаг 1.</b> Прочитайте пары по урокам (с. 2–7). Не зубрите — просто узнайте.</li>')
    A('<li><b>Шаг 2.</b> Прочитайте <b>все немецкие предложения подряд</b> в конце файла — «Прогон вслух». 3–4 раза.</li>')
    A('<li><b>Шаг 3.</b> Прогон вслух ещё раз, но <b>сначала русскую строку, потом немецкую</b>, не подглядывая.</li>')
    A('<li><b>Шаг 4.</b> Возьмите «тренажёр» (файл .html) — режим <i>Билет</i> даёт случайные 10 предложений и озвучку.</li>')
    A('</ul></div>')

    A('<div class="box"><span class="tag">Что даёт баллы на экзамене</span><ul>')
    A('<li><b>Приставки на месте.</b> Половина ошибок — потерянное <i>aus-, auf-, ein-, wider-, hervor-</i> в конце.</li>')
    A('<li><b>Пассив.</b> «проводится / используется» → <i>wird … gemacht</i>, а не актив.</li>')
    A('<li><b>Предлоги.</b> <i>für / an / mit / auf / dank</i> — за них снимают чаще всего.</li>')
    A('<li><b>Произношение.</b> <i>ch</i>, <i>eu</i>, <i>ü/ö</i>, <i>z</i> и ясное конечное <i>-e</i>.</li>')
    A('</ul></div>')
    A('</div>')

    A('</div></div>')
    A('<div class="cv-index">')
    A('<span><b>1</b> 104 пары RU → DE по урокам</span>')
    A('<span><b>2</b> Ключевая лексика</span>')
    A('<span><b>3</b> Произношение · 2 балла</span>')
    A('<span><b>4</b> Шесть грамматических моделей</span>')
    A('<span><b>5</b> Прогон вслух · только немецкий</span>')
    A('</div>')
    A('</section>')

    # ---------------- lessons
    for li, l in enumerate(LESSONS):
        A('<section class="lesson">')
        A('<div class="lsn-bar"><div class="num">%s</div><h2>%s</h2>'
          '<div class="tr">%s</div><div class="pg">%s</div></div>'
          % (l["tag"], l["title"], l["title_ru"], l["pages"]))
        for (k, rt, dt, items) in l["sections"]:
            A('<div class="sec"><span class="k">%s</span><span class="rt">%s</span>'
              '<span class="dt">%s</span></div>' % (k, rt, dt))
            for i, (ru, de, note) in enumerate(items, 1):
                A('<div class="item"><div class="n">%d</div><div class="b">' % i)
                A('<div class="ru">%s</div><div class="de">%s</div>' % (ru, de))
                if note:
                    A('<div class="note">%s</div>' % note)
                A('</div></div>')
        A('</section>')

    # ---------------- appendix 1: vocab
    A('<section class="appx"><div class="appx-h"><div class="num">Приложение 1</div>'
      '<h2>Ключевая лексика</h2></div>')
    for g, words in VOCAB:
        A('<div class="vgroup"><h3>%s</h3><div class="vlist">' % g)
        for de, ru in words:
            A('<span>%s — <i>%s</i></span>' % (de, ru))
        A('</div></div>')
    A('</section>')

    # ---------------- appendix 2: pronunciation
    A('<section class="appx"><div class="appx-h"><div class="num">Приложение 2</div>'
      '<h2>Произношение · 2 балла</h2></div>')
    A('<div class="box"><span class="tag">Правила чтения — их всего несколько</span>')
    A('<table class="rules"><tr><th>Буквы</th><th>Звук</th><th>Пример</th></tr>')
    for a, b, c in PRON_RULES:
        A('<tr><td class="w">%s</td><td class="p">%s</td><td>%s</td></tr>' % (a, b, c))
    A('</table></div>')
    A('<div class="box alt flow"><span class="tag">Трудные слова из ваших текстов</span>')
    A('<p style="margin-bottom:2mm">Жирным выделен ударный слог. Двоеточие означает долгий гласный.</p>')
    A('<div class="cols2">')
    for w, t in PRON_WORDS:
        p = t.split("*")
        t = p[0] + "<b>" + p[1] + "</b>" + p[2] if len(p) == 3 else t
        A('<div style="font-size:8.9pt; margin-bottom:.9mm; break-inside:avoid"><b>%s</b><br>'
          '<span style="color:#65707f">%s</span></div>' % (w, t))
    A('</div></div>')
    A('</section>')

    # ---------------- appendix 3: grammar
    A('<section class="appx"><div class="appx-h"><div class="num">Приложение 3</div>'
      '<h2>Шесть моделей, которые закрывают почти всё</h2></div>')
    for t, pat, txt in GRAMMAR:
        A('<div class="gbox"><h3>%s</h3><div class="pat">%s</div><p>%s</p></div>' % (t, pat, txt))
    A('<div class="foot">Источник формулировок: учебные тексты «Ein Blick in die Geschichte» и '
      '«Forschen an der RTU MIREA». Все немецкие предложения приведены дословно.</div>')
    A('</section>')

    # ---------------- appendix 4: run-through
    A('<section class="appx"><div class="appx-h"><div class="num">Приложение 4</div>'
      '<h2>Прогон вслух · только немецкий</h2></div>')
    A('<div class="box"><p style="margin:0">Читайте подряд, громко, следя за приставками в конце предложения и за <i>ch / eu / ü / ö</i>. '
      'Три полных прогона дают больше, чем десять прочтений таблицы про себя.</p></div>')
    A('<div class="run">')
    for l in LESSONS:
        for (k, rt, dt, items) in l["sections"]:
            A('<div class="rt">%s · %s — %s</div>' % (l["tag"], k, rt))
            for i, (ru, de, note) in enumerate(items, 1):
                A('<p><b>%d</b> %s</p>' % (i, de))
    A('</div></section>')

    A('</body></html>')
    return "".join(o)


# ---------------------------------------------------------------- trainer
TRAINER_CSS = r"""
*{box-sizing:border-box}
:root{
  --ink:#0f1620; --mut:#6b7a8d; --line:#e3e8ef; --bg:#f4f6f9;
  --acc:#1f4e8c; --acc2:#a8562a; --ok:#17795e; --bad:#a84343;
}
body{margin:0;background:var(--bg);color:var(--ink);
  font-family:"Segoe UI","Trebuchet MS",sans-serif;-webkit-font-smoothing:antialiased}
.wrap{max-width:860px;margin:0 auto;padding:0 16px 90px}

header{position:sticky;top:0;z-index:20;background:rgba(244,246,249,.93);
  backdrop-filter:blur(9px);border-bottom:1px solid var(--line);margin-bottom:20px}
.hd{max-width:860px;margin:0 auto;padding:12px 16px 10px;display:flex;align-items:center;gap:14px;flex-wrap:wrap}
.brand{font-weight:700;font-size:15px;letter-spacing:-.01em}
.brand small{display:block;font-weight:400;font-size:11px;color:var(--mut);letter-spacing:.02em;margin-top:1px}
.pill{font-size:11.5px;color:var(--mut);border:1px solid var(--line);background:#fff;
  padding:4px 9px;border-radius:99px;white-space:nowrap}
.pill b{color:var(--ink)}
.spacer{flex:1}
.bar{height:4px;background:var(--line);border-radius:9px;overflow:hidden;margin-top:2px}
.bar i{display:block;height:100%;width:0;background:linear-gradient(90deg,#1f4e8c,#3f7fd0);transition:width .3s}

.modes{display:flex;gap:8px;flex-wrap:wrap;margin:0 0 18px}
.modes button{font:inherit;font-size:13px;padding:8px 14px;border-radius:9px;cursor:pointer;
  border:1px solid var(--line);background:#fff;color:#3d4a5c;transition:.15s}
.modes button:hover{border-color:#c2cddd}
.modes button.on{background:var(--ink);border-color:var(--ink);color:#fff;font-weight:600}

.card{background:#fff;border:1px solid var(--line);border-radius:16px;overflow:hidden;
  box-shadow:0 1px 2px rgba(16,26,41,.04),0 12px 30px -18px rgba(16,26,41,.28)}
.cap{display:flex;align-items:center;gap:10px;padding:13px 22px;border-bottom:1px solid var(--line);
  font-size:11.5px;color:var(--mut);letter-spacing:.06em;text-transform:uppercase;font-weight:600}
.cap .dot{width:7px;height:7px;border-radius:50%;background:var(--acc)}
.cap .fl{margin-left:auto;letter-spacing:.02em;text-transform:none;font-weight:400}

.ru-side{padding:30px 26px 26px}
.ru-side .lbl{font-size:10.5px;letter-spacing:.16em;text-transform:uppercase;color:#9aa6b5;margin-bottom:10px}
.ru-txt{font-family:Georgia,"Times New Roman",serif;font-size:20px;line-height:1.5;color:#1d2733}
.ru-txt.q{color:#8b97a6;font-size:14px;font-style:italic}

.de-side{border-top:1px dashed #cfd8e4;padding:22px 26px 26px;background:#fbfcfe}
.de-side .lbl{font-size:10.5px;letter-spacing:.16em;text-transform:uppercase;color:#9aa6b5;margin-bottom:10px}
.de-txt{font-family:Georgia,"Times New Roman",serif;font-size:20px;line-height:1.5;font-weight:700;color:#0b1220}
.de-txt.q{color:#b6c0cc;font-weight:400}
.note{margin-top:12px;font-size:12.5px;line-height:1.5;color:#7a5d33;border-left:2px solid #d9bc86;padding-left:10px}

.acts{display:flex;gap:10px;flex-wrap:wrap;padding:0 26px 24px}
.btn{font:inherit;font-size:14px;padding:11px 20px;border-radius:10px;cursor:pointer;border:1px solid var(--line);
  background:#fff;color:#33404f;transition:.15s;display:flex;align-items:center;gap:8px}
.btn:hover{border-color:#b9c6d8}
.btn.prim{background:var(--acc);border-color:var(--acc);color:#fff;font-weight:600}
.btn.prim:hover{background:#1a4379;border-color:#1a4379}
.btn.ok{color:var(--ok);border-color:#c4ded6}
.btn.ok:hover{background:#eef7f4;border-color:#8fc7b7}
.btn.bad{color:var(--bad);border-color:#e3cccc}
.btn.bad:hover{background:#fdf1f1;border-color:#d9a9a9}
.btn:disabled{opacity:.4;cursor:default}

.nav{display:flex;align-items:center;gap:12px;margin-top:18px}
.nav .idx{font-size:13px;color:var(--mut);font-variant-numeric:tabular-nums}
.nav button{font:inherit;font-size:13px;padding:8px 14px;border-radius:9px;border:1px solid var(--line);
  background:#fff;cursor:pointer;color:#33404f}
.nav button:hover{border-color:#b9c6d8}

.hintbar{margin-top:22px;font-size:12px;color:var(--mut);line-height:1.9}
kbd{font-family:ui-monospace,Consolas,monospace;font-size:11px;background:#fff;border:1px solid var(--line);
  border-bottom-width:2px;border-radius:5px;padding:1px 6px;color:#3d4a5c}

.done{background:#fff;border:1px solid var(--line);border-radius:16px;padding:34px 26px;text-align:center}
.done h2{margin:0 0 8px;font-size:22px}
.done p{margin:0 0 20px;color:var(--mut);font-size:14px}
.stat{display:flex;gap:26px;justify-content:center;margin:22px 0}
.stat div{font-size:13px;color:var(--mut)}
.stat b{display:block;font-size:26px;color:var(--ink);font-family:Georgia,serif}

@media (max-width:640px){
  .ru-txt,.de-txt{font-size:17px}
  .ru-side,.de-side{padding:22px 18px}
  .acts{padding:0 18px 20px}
  .cap{padding:11px 18px}
}
@media print{
  header,.modes,.acts,.nav,.hintbar{display:none}
  body{background:#fff}
  .card{box-shadow:none}
}
"""

TRAINER_JS = r"""
const DATA = __DATA__;
const S = { deck: [], i: 0, revealed: false, mode: 'all', filter: 'all', known: new Set(), agn: new Set() };

const el = id => document.getElementById(id);
const KEY = 'de-mirea-km-v1';

function save(){ try{ localStorage.setItem(KEY, JSON.stringify({k:[...S.known],a:[...S.agn]})); }catch(e){} }
function load(){ try{ const r = JSON.parse(localStorage.getItem(KEY)||'{}');
  (r.k||[]).forEach(x=>S.known.add(x)); (r.a||[]).forEach(x=>S.agn.add(x)); }catch(e){} }

function shuffle(a){ a=a.slice(); for(let i=a.length-1;i>0;i--){ const j=Math.floor(Math.random()*(i+1)); [a[i],a[j]]=[a[j],a[i]];} return a; }

function currentPool(){
  let pool = DATA.map((d,idx)=>({...d, id:idx}));
  if(S.filter==='L2') pool = pool.filter(d=>d.lesson==='Урок 2');
  return pool;
}

function buildDeck(mode){
  S.mode = mode; S.known = new Set(); S.agn = new Set(); load();
  const pool = currentPool();
  if(mode==='ticket'){
    let cand = pool.filter(d=>!S.known.has(d.id));
    if(cand.length < 10) cand = pool;
    S.deck = shuffle(cand).slice(0,10);
  } else if(mode==='hard'){
    const hard = pool.filter(d=>S.agn.has(d.id));
    S.deck = hard.length ? shuffle(hard) : shuffle(pool);
  } else {
    S.deck = pool;
  }
  S.i = 0; S.revealed = false; render();
}

function speak(text){
  if(!('speechSynthesis' in window)) return;
  const u = new SpeechSynthesisUtterance(text.replace(/[„“«»]/g,''));
  u.lang = 'de-DE'; u.rate = 0.92;
  const vs = speechSynthesis.getVoices().filter(v=>/^de/i.test(v.lang));
  if(vs.length) u.voice = vs[0];
  speechSynthesis.cancel(); speechSynthesis.speak(u);
}

function progress(){
  if(S.mode==='all'){ return (S.i)/(S.deck.length||1); }
  return (S.known.size + S.agn.size)/(S.deck.length||1);
}

function render(){
  const total = S.deck.length;
  el('cKnown').textContent = S.known.size;
  el('cAgn').textContent = S.agn.size;
  el('cTotal').textContent = total;
  el('bar').style.width = Math.min(100, Math.round(progress()*100)) + '%';

  if(S.i >= total){ finish(); return; }
  el('cardWrap').innerHTML = cardHTML();
  bindCard();
}

function finish(){
  el('cardWrap').innerHTML = `
  <div class="done">
    <h2>Круг закончен</h2>
    <p>${S.mode==='ticket' ? 'Билет пройден' : 'Прошли все предложения'} — сверились с ${total()} карточками.</p>
    <div class="stat">
      <div><b>${S.known.size}</b>знаю</div>
      <div><b>${S.agn.size}</b>надо повторить</div>
      <div><b>${S.deck.length}</b>в наборе</div>
    </div>
    <button class="btn prim" onclick="location.reload()">Начать заново</button>
  </div>`;
  speak('');
  el('bar').style.width='100%';
}
function total(){ return S.deck.length; }

function cardHTML(){
  const d = S.deck[S.i];
  const rv = S.revealed;
  const flags = (S.known.has(d.id)?' ✓':'') + (S.agn.has(d.id)?' ↻':'');
  return `<div class="card">
    <div class="cap"><span class="dot"></span>
      <span>${d.lesson} · ${d.sec}</span>
      <span class="fl">${d.secRu} &nbsp;·&nbsp; №${d.n}${flags}</span>
    </div>
    <div class="ru-side">
      <div class="lbl">Русский — переведите вслух</div>
      <div class="ru-txt">${esc(d.ru)}</div>
    </div>
    <div class="de-side">
      <div class="lbl">Немецкий</div>
      <div class="de-txt ${rv?'':'q'}">${rv ? esc(d.de) : 'нажмите «Показать» или пробел'}</div>
      ${(rv && d.note) ? `<div class="note">${esc(d.note)}</div>` : ''}
    </div>
    <div class="acts">
      <button class="btn prim" id="bShow">${rv?'Скрыть':'Показать перевод'}</button>
      <button class="btn" id="bSay" ${rv?'':'disabled'}>🔊 Прослушать</button>
      <button class="btn bad" id="bBad" ${rv?'':'disabled'}>↻ Повторить</button>
      <button class="btn ok" id="bOk" ${rv?'':'disabled'}>✓ Знаю</button>
    </div>
  </div>
  <div class="nav">
    <button id="bPrev">← Назад</button>
    <span class="idx">${S.i+1} / ${S.deck.length}</span>
    <button id="bNext">Дальше →</button>
    <span class="spacer"></span>
    <button id="bShuffle">Перемешать</button>
  </div>`;
}

function esc(s){ return String(s).replace(/&/g,'&amp;').replace(/</g,'&lt;').replace(/>/g,'&gt;'); }

function bindCard(){
  const g = id => el(id);
  g('bShow') && (g('bShow').onclick = ()=>{ S.revealed=!S.revealed; render(); });
  g('bSay')  && (g('bSay').onclick  = ()=> speak(S.deck[S.i].de));
  g('bOk')   && (g('bOk').onclick   = ()=>{ S.known.add(S.deck[S.i].id); S.agn.delete(S.deck[S.i].id); save(); next(); });
  g('bBad')  && (g('bBad').onclick  = ()=>{ S.agn.add(S.deck[S.i].id); S.known.delete(S.deck[S.i].id); save(); next(); });
  g('bNext') && (g('bNext').onclick = next);
  g('bPrev') && (g('bPrev').onclick = ()=>{ if(S.i>0){ S.i--; S.revealed=false; render(); } });
  g('bShuffle') && (g('bShuffle').onclick = ()=>{ S.deck = shuffle(S.deck); S.i=0; S.revealed=false; render(); });
}

function next(){ if(S.i < S.deck.length-1){ S.i++; S.revealed=false; render(); } else { S.i = S.deck.length; render(); } }

document.addEventListener('keydown', e=>{
  if(e.target.tagName === 'INPUT') return;
  if(e.code==='Space'){ e.preventDefault(); S.revealed=!S.revealed; render(); }
  else if(e.key==='ArrowRight'){ e.preventDefault(); next(); }
  else if(e.key==='ArrowLeft'){ e.preventDefault(); if(S.i>0){S.i--;S.revealed=false;render();} }
  else if(e.key==='1'){ const b=el('bBad'); if(b&&!b.disabled) b.click(); }
  else if(e.key==='2'){ const b=el('bOk'); if(b&&!b.disabled) b.click(); }
  else if(e.key==='s'||e.key==='ы'){ if(S.revealed) speak(S.deck[S.i].de); }
});

document.querySelectorAll('.modes button[data-mode]').forEach(b=>{
  b.onclick = ()=>{ document.querySelectorAll('.modes button[data-mode]').forEach(x=>x.classList.remove('on'));
    b.classList.add('on'); buildDeck(b.dataset.mode); };
});
document.querySelectorAll('.modes button[data-filter]').forEach(b=>{
  b.onclick = ()=>{ document.querySelectorAll('.modes button[data-filter]').forEach(x=>x.classList.remove('on'));
    b.classList.add('on'); S.filter = b.dataset.filter; buildDeck(S.mode); };
});

load(); buildDeck('all');
if('speechSynthesis' in window){ speechSynthesis.getVoices(); speechSynthesis.onvoiceschanged = ()=>{}; }
"""


def trainer_data():
    out = []
    for l in LESSONS:
        for (k, rt, dt, items) in l["sections"]:
            for i, (ru, de, note) in enumerate(items, 1):
                out.append({
                    "lesson": l["tag"], "sec": k, "secRu": rt,
                    "n": i, "ru": ru, "de": de, "note": note or ""
                })
    return out


def trainer_html():
    data = json.dumps(trainer_data(), ensure_ascii=False)
    js = TRAINER_JS.replace("__DATA__", data)
    return """<!doctype html><html lang="ru"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>Тренажёр · перевод RU→DE · КМ</title>
<style>%s</style></head><body>

<header><div class="hd">
  <div class="brand">Тренажёр · перевод RU → DE<small>Урок 2 · упр. 4 &nbsp;|&nbsp; Урок 3 · упр. 4</small></div>
  <div class="spacer"></div>
  <div class="pill">знаю <b id="cKnown">0</b></div>
  <div class="pill">повторить <b id="cAgn">0</b></div>
  <div class="pill">в наборе <b id="cTotal">0</b></div>
</div><div class="bar"><i id="bar"></i></div></header>

<div class="wrap">
  <div class="modes">
    <button data-mode="all" class="on">Все подряд</button>
    <button data-mode="ticket">Билет · 10 случайных</button>
    <button data-mode="hard">Только сложные</button>
    <span class="spacer"></span>
    <button data-filter="all" class="on">оба урока</button>
    <button data-filter="L2">только урок 2</button>
  </div>

  <div id="cardWrap"></div>

  <div class="hintbar">
    <kbd>пробел</kbd> показать/скрыть перевод &nbsp;·&nbsp; <kbd>→</kbd> дальше &nbsp;·&nbsp;
    <kbd>←</kbd> назад &nbsp;·&nbsp; <kbd>2</kbd> знаю &nbsp;·&nbsp; <kbd>1</kbd> повторить &nbsp;·&nbsp;
    <kbd>s</kbd> прослушать
    <br>Озвучка идёт через голос браузера (de-DE). Если голоса нет — установите немецкий язык в системе.
    Прогресс сохраняется в браузере.
  </div>
</div>

<script>%s</script>
</body></html>""" % (TRAINER_CSS, js)


if __name__ == "__main__":
    rp = os.path.join(BUILD, "reference.html")
    with io.open(rp, "w", encoding="utf-8") as f:
        f.write(ref_html())
    tp = os.path.join(ROOT, "Тренажер - перевод и произношение.html")
    with io.open(tp, "w", encoding="utf-8") as f:
        f.write(trainer_html())
    print("total sentences:", TOTAL)
    print("reference:", rp)
    print("trainer:", tp)
