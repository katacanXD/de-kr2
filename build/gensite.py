# -*- coding: utf-8 -*-
"""Генерирует assets/data.js для сайта."""
import io, os, sys, json, re

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from data import LESSONS, VOCAB, PRON_RULES, GRAMMAR
from g2r import load as load_lex, ru as ipa2ru, tokenize

ROOT = os.path.dirname(HERE)
lex = load_lex()

WORD = re.compile(r"[A-Za-zÄÖÜäöüß0-9]+(?:[.\-][A-Za-zÄÖÜäöüß0-9]+)*")
TOKEN = re.compile(r"[A-Za-zÄÖÜäöüß0-9]+(?:[.\-][A-Za-zÄÖÜäöüß0-9]+)*|\S")

NO_SPACE_BEFORE = set(",.!?;:—–%)»“\"'")
OPEN_AFTER = set("„«(\"'")
MISSING = set()


SKIP = set("„“«»\"'()")

def join_tokens(tokens, fn):
    s = ""
    for kind, val in tokens:
        if kind == "w":
            if s and not s.endswith(" "):
                s += " "
            s += fn(val)
        else:
            if val in SKIP:
                continue
            if val in ("—", "–"):
                s = s.rstrip() + " " + val + " "
            elif val in (",", ".", "!", "?", ";", ":"):
                s = s.rstrip() + val + " "
            else:
                s = s.rstrip() + val
    return re.sub(r"\s+", " ", s).strip()


def tokens_of(text):
    out = []
    for t in TOKEN.findall(text):
        out.append(("w" if WORD.fullmatch(t) else "p", t))
    return out


def word_ipa(w):
    k = w.lower()
    if k not in lex:
        MISSING.add(k)
        return w
    return lex[k]


def sentence_ipa(s):
    return join_tokens(tokens_of(s), word_ipa)


def sentence_ru(s):
    return join_tokens(tokens_of(s), lambda w: ipa2ru(word_ipa(w)))


HARD = [
    "Außergewöhnliches", "Errungenschaften", "Dreiviertelstunde", "Verteidigungsindustrie",
    "Automatisierungstechnik", "wiederverwendbare", "Durchbruch", "Landeabweichung",
    "Orbitalfluggeräts", "beeindruckte", "Dankurkunde", "würdigte", "Heraldische", "Register",
    "Bewegungserfassung", "Präzision", "Spektrumanalysatoren", "Hochfrequenzgeneratoren",
    "Schwachstelle", "Sicherheitsvorfälle", "Grafikbeschleunigern", "angriffsresistente",
    "Fernerkundung", "erdnahen", "Penetrationstests", "Oberflächenmontage",
    "Zuverlässigkeit", "Lötverbindungen", "Multiagentensysteme", "Robotergruppen",
    "Steuerungsalgorithmen", "Kommunikationssystemen", "Bildungseinrichtung",
    "interdisziplinären", "wiedergegeben", "ausgestattet", "Kaganow", "Baikonur", "Kosmodrom",
]


def build():
    data = {"lessons": [], "vocab": [], "rules": [], "grammar": [], "hard": []}
    n = 0
    for l in LESSONS:
        ls = {"tag": l["tag"], "title": l["title"], "titleRu": l["title_ru"], "pages": l["pages"], "sections": []}
        for (k, rt, dt, items) in l["sections"]:
            sec = {"k": k, "ru": rt, "de": dt, "items": []}
            for (ru, de, note) in items:
                n += 1
                sec["items"].append({
                    "n": len(sec["items"]) + 1,
                    "ru": ru, "de": de,
                    "ipa": sentence_ipa(de),
                    "tr": sentence_ru(de),
                    "note": note or "",
                })
            ls["sections"].append(sec)
        data["lessons"].append(ls)
    data["total"] = n

    for g, words in VOCAB:
        data["vocab"].append({"group": g, "words": [[a, b] for a, b in words]})

    for a, b, c in PRON_RULES:
        data["rules"].append([a, b, c])

    for t, pat, txt in GRAMMAR:
        data["grammar"].append([t, pat, txt])

    for w in HARD:
        k = w.lower()
        if k in lex:
            data["hard"].append({"w": w, "ipa": lex[k], "tr": ipa2ru(lex[k])})
        else:
            MISSING.add(k)

    js = "window.KM = " + json.dumps(data, ensure_ascii=False, indent=0) + ";\n"
    out = os.path.join(ROOT, "assets")
    os.makedirs(out, exist_ok=True)
    io.open(os.path.join(out, "data.js"), "w", encoding="utf-8").write(js)
    print("sentences:", n, "| data.js", len(js), "bytes")
    print("MISSING:", sorted(MISSING) if MISSING else "none")

    # проверка
    for ls in data["lessons"]:
        for sec in ls["sections"]:
            for it in sec["items"]:
                for bad in ("ː", "̯", "ˈ", "ˌ", "ʔ", "["):
                    if bad in it["tr"]:
                        print("LEAK:", it["n"], bad, it["tr"][:80])


if __name__ == "__main__":
    build()
