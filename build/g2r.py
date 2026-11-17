# -*- coding: utf-8 -*-
"""IPA (de) -> практическая русская транскрипция."""
import io, os, re

HERE = os.path.dirname(os.path.abspath(__file__))

MAP = [
    ("t͡s", "ц"), ("t͡ʃ", "ч"), ("d͡ʒ", "дж"),
    ("ɔʏ̯", "ой"), ("aɪ̯", "ай"), ("aʊ̯", "ау"),
    ("i̯oː", "ьо:"), ("i̯ɔ", "ьо"), ("i̯o", "ьо"), ("i̯øː", "ьё:"),
    ("i̯ø", "ьё"), ("i̯œ", "ьё"),
    ("i̯aː", "иа:"), ("i̯a", "иа"), ("i̯eː", "ие:"), ("i̯e", "ие"),
    ("i̯ɛ", "иэ"), ("i̯iː", "ии:"), ("i̯i", "ии"), ("i̯ə", "иэ"),
    ("i̯uː", "иу:"), ("i̯ʊ", "иу"), ("i̯u", "иу"),
    ("i̯", "и"), ("u̯", "у"),
    ("aː", "а:"), ("ɛː", "э:"), ("eː", "е:"), ("iː", "и:"),
    ("oː", "о:"), ("uː", "у:"), ("yː", "ю:"), ("øː", "ё:"),
    ("ɐ̯", "р"), ("ɐ", "эр"),
    ("lja", "лья"), ("lje", "лье"), ("ljo", "льо"), ("lju", "лью"),
    ("ŋk", "нк"), ("lj", "ль"), ("nj", "нь"),
    ("a", "а"), ("ɛ", "э"), ("e", "э"), ("i", "и"), ("ɪ", "и"),
    ("o", "о"), ("ɔ", "о"), ("u", "у"), ("ʊ", "у"), ("y", "ю"),
    ("ʏ", "ю"), ("ø", "ё"), ("œ", "ё"), ("ə", "э"),
    ("p", "п"), ("b", "б"), ("t", "т"), ("d", "д"), ("k", "к"),
    ("ɡ", "г"), ("g", "г"), ("f", "ф"), ("v", "в"), ("s", "с"),
    ("z", "з"), ("ʃ", "ш"), ("ʒ", "ж"), ("ç", "хь"), ("x", "х"),
    ("h", "х"), ("m", "м"), ("n", "н"), ("ŋ", "нг"), ("l", "л"),
    ("ʁ", "р"), ("ʀ", "р"), ("j", "й"), ("ʔ", ""), ("ˈ", "ˈ"), ("ˌ", ""),
]
VOWELS = set("аэиоуёюяе")
ACUTE = "\u0301"


def norm(ipa):
    return (ipa.replace("n̩", "ən").replace("l̩", "əl").replace("m̩", "əm")
               .replace("r̩", "ɐ"))


def ru(ipa, drop_len_before_r=True):
    ipa = norm(ipa)
    out = []
    stress = False
    i = 0
    while i < len(ipa):
        for k, v in MAP:
            if ipa.startswith(k, i):
                if k == "ˈ":
                    stress = True
                    i += len(k)
                    break
                if k == "ɐ̯":
                    if drop_len_before_r and out and out[-1].endswith(":"):
                        out[-1] = out[-1][:-1]
                        if not out[-1]:
                            out.pop()
                    out.append("р")
                    i += len(k)
                    break
                if stress and any(c in VOWELS for c in v):
                    idx = next(j for j, c in enumerate(v) if c in VOWELS)
                    if v[idx] == "ё":
                        out.append(v)
                    else:
                        out.append(v[:idx + 1] + ACUTE + v[idx + 1:])
                    stress = False
                else:
                    out.append(v)
                i += len(k)
                break
        else:
            out.append(ipa[i])
            i += 1
    return "".join(out)


def status_vowel(s):
    return bool(s) and s[0] in VOWELS


def load():
    d = {}
    for f in ("lex1.txt", "lex2.txt", "lex3.txt"):
        p = os.path.join(HERE, f)
        if not os.path.exists(p):
            continue
        for line in io.open(p, encoding="utf-8"):
            line = line.strip()
            if not line or line.startswith("#"):
                continue
            w, ipa = line.split("|", 1)
            d[w.strip().lower()] = ipa.strip()
    return d


UNITS = {
    "RTU MIREA", "MIREA", "RTU", "BI.ZONE", "DCS APROL", "APROL", "DCS", "WZEI",
    "LED", "CNC", "VR", "AR", "KI", "HTC", "3D", "DevSecOps", "TACTOT", "Cyberzone",
}

TOK = re.compile(r"[A-Za-zÄÖÜäöüß0-9]+(?:[.\-][A-Za-zÄÖÜäöüß0-9]+)*")


def tokenize(s):
    return TOK.findall(s)


if __name__ == "__main__":
    import sys
    sys.path.insert(0, HERE)
    from data import LESSONS
    lex = load()
    missing = {}
    total = 0
    for l in LESSONS:
        for k, rt, dt, items in l["sections"]:
            for ru_s, de, note in items:
                for w in tokenize(de):
                    total += 1
                    if w.lower() not in lex:
                        missing[w] = missing.get(w, 0) + 1
    print("tokens", total, "| lex", len(lex), "| missing uniq", len(missing))
    for w, c in sorted(missing.items()):
        print("  MISSING:", w, c)
