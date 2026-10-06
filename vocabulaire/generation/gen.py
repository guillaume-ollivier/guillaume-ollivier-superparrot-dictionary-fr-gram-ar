#!/usr/bin/env python3
"""Générateur du chantier fr_gram_ar à partir de sources compactes par chapitre.

Source : sources/<CC>.txt — un fichier par chapitre, plusieurs leçons :
    @ref 0021
    @chap 05
    @slug prisente-in-a
    @niv niv-a1
    === NOTE
    # Titre
    ... markdown ...
    === EXO
    title: titre fr | titre ar
    wording: consigne fr | consigne ar
    mode: trad | trou | transfo
    question => réponse | alternative ## indice français
    === VOCA
    mots ar | fr1:m; fr2 [contexte] | cats ar | niveau | fréquence | étiquettes | registre | contexte ar | référence | trad | pluriel
    @ref 0022
    ...

Modes : `trad` question française → réponse arabe ; `trou` phrase arabe à
trous `___`, une réponse par trou séparée par ` ;; ` (`∅` = rien) ; `transfo`
consigne courte en arabe (forme à produire) → réponse arabe.

Arabe (cadrage 2026-10-05) : l'élève tape **sans voyelles**. Les réponses
peuvent être écrites vocalisées dans les sources : les harakat et le tatweel en
sont retirés ; une variante où أ إ آ deviennent ا est ajoutée (saisie
courante). Les questions gardent leur vocalisation. Vocabulaire : chaque sens
porte deux mots `ar`, la forme vocalisée (affichée, lue par la voix) et la
forme nue (celle qu'on tape) — synonymes.

Produit, dans le chantier : cours/chapitres.txt, les dossiers de leçon
(<ref>-1-note.md, <ref>-2-voca.md, <ref>-3-exercice.md…) et
vocabulaire/assemblage/dictionnaire.md (références gelées des mots conservées).
Relancer **écrase** les dossiers de leçon.
"""
from __future__ import annotations
import re
import shutil
import sys
import unicodedata
from pathlib import Path

ICI = Path(__file__).resolve().parent
CHANTIER = ICI.parent.parent
sys.path.insert(0, str(CHANTIER.parent.parent / "tools" / "dictionnaire"))
from parrotdict import exercices_md, dictionnaire_md  # noqa: E402

SOURCE_CODE = "AR"
LANG_FR, LANG_CO, LANG_CO_MOT = "fr-FR", "ar-SA", "ar"

# Harakat, tanwin, shadda, sukun, alif suscrit, hamza suscrite/souscrite
# combinantes, tatweel.
HARAKAT = re.compile("[\u064B-\u065F\u0670\u0640]")
LETTRE_LATINE = re.compile("[A-Za-zÀ-ž]")


def nu(t: str) -> str:
    """Forme tapée : sans voyelles ni tatweel."""
    return HARAKAT.sub("", t)


def sans_hamza(t: str) -> str:
    return t.replace("أ", "ا").replace("إ", "ا").replace("آ", "ا")



class Erreur(Exception):
    pass


def nfc(t: str) -> str:
    return unicodedata.normalize("NFC", t)


# ------------------------------------------------------------- lecture
def lire_chapitre(chemin: Path) -> list[dict]:
    texte = nfc(chemin.read_text(encoding="utf-8"))
    morceaux = re.split(r"^(?=@ref )", texte, flags=re.M)
    lecons = []
    for m in morceaux:
        if not m.strip().startswith("@ref"):
            if m.strip():
                raise Erreur(f"{chemin.name} : texte hors leçon : {m[:60]!r}")
            continue
        lecons.append(lire_lecon(m, chemin.name))
    return lecons


def lire_lecon(texte: str, fichier: str) -> dict:
    entete, sep, reste = texte.partition("=== NOTE\n")
    if not sep:
        raise Erreur(f"{fichier} : leçon sans NOTE : {texte[:40]!r}")
    meta = {}
    for ligne in entete.splitlines():
        if ligne.startswith("@"):
            k, _, v = ligne[1:].partition(" ")
            meta[k] = v.strip()
    for k in ("ref", "chap", "slug", "niv"):
        if k not in meta:
            raise Erreur(f"{fichier} : @{k} manquant ({meta})")
    if not re.fullmatch(r"[a-z0-9-]+", meta["slug"]):
        raise Erreur(f"{fichier} : slug non ASCII {meta['slug']!r}")
    blocs = re.split(r"^=== (EXO|VOCA)\s*$", reste, flags=re.M)
    note = blocs[0].strip() + "\n"
    exos, voca = [], []
    for i in range(1, len(blocs), 2):
        (exos if blocs[i] == "EXO" else voca).append(blocs[i + 1])
    return {"meta": meta, "note": note, "exos": exos, "voca": "\n".join(voca),
            "origine": f"{fichier}#{meta['ref']}"}


FIN_PONCT = re.compile(r"^(.*?)(\s*[.?!…؟]+)$", re.S)


def separer_ponct(texte: str) -> tuple[str, str]:
    m = FIN_PONCT.match(texte.strip())
    if not m or not m.group(1).strip():
        return texte.strip(), ""
    return m.group(1).strip(), m.group(2).strip()


def affixe(p: str) -> str:
    return "{type=affix§" + p + "}" if p else ""


def groupe(alts: list[str], index: int) -> str:
    coeur = alts[0] if len(alts) == 1 else "{" + "|".join(alts) + "}"
    return "{?" + str(index) + "§" + coeur + "}"


def composer_reponse(spec: str, origine: str) -> str:
    """`a | b` (un trou) — ponctuation finale commune sortie en affixe."""
    alts_brutes = [a.strip() for a in spec.split(" | ") if a.strip()]
    if not alts_brutes:
        raise Erreur(f"{origine} : réponse vide")
    coeurs, poncts = [], set()
    for a in alts_brutes:
        c, p = separer_ponct(a)
        coeurs.append(c)
        poncts.add(p)
    if len(poncts) > 1:
        raise Erreur(f"{origine} : ponctuation finale divergente entre alternatives {alts_brutes}")
    alts = variantes(coeurs, origine)
    return groupe(alts, 1) + affixe(poncts.pop())


def variantes(coeurs: list[str], origine: str) -> list[str]:
    """Réponses tapées : forme nue, puis sa variante sans hamza sur alif."""
    out = []
    for c in coeurs:
        if LETTRE_LATINE.search(c):
            raise Erreur(f"{origine} : lettre latine dans une réponse arabe {c!r}")
        out += [nu(c), sans_hamza(nu(c))]
    return list(dict.fromkeys(out))


def composer_trous(spec: str) -> str:
    out = []
    for i, trou in enumerate(spec.split(" ;; "), start=1):
        brutes = [a.strip() for a in trou.split(" | ")]
        alts = variantes([a for a in brutes if a != "∅"], spec)
        if "∅" in brutes:
            alts.append("")
        out.append(groupe(alts, i))
    return "".join(out)


def verifier_accolades(texte: str, origine: str):
    if any(c in texte for c in "{}§|"):
        raise Erreur(f"{origine} : caractère réservé dans {texte!r}")


def lire_exo(bloc: str, ref: str, n: int, niv: str, origine: str) -> dict:
    meta, items = {}, []
    for ligne in bloc.splitlines():
        if not ligne.strip() or ligne.startswith("#"):
            continue
        m = re.match(r"^(title|wording|mode|niv):\s*(.*)$", ligne)
        if m and "=>" not in ligne:
            meta[m.group(1)] = m.group(2).strip()
            continue
        if "=>" not in ligne:
            raise Erreur(f"{origine} : ligne d'exercice illisible : {ligne!r}")
        items.append(ligne)
    mode = meta.get("mode", "trad")
    if mode not in ("trad", "trou", "transfo"):
        raise Erreur(f"{origine} : mode inconnu {mode}")
    if " | " not in meta.get("title", "") or " | " not in meta.get("wording", ""):
        raise Erreur(f"{origine} : title/wording doivent être « fr | ar »")
    tfr, _, tco = meta["title"].partition(" | ")
    wfr, _, wco = meta["wording"].partition(" | ")
    qlang = LANG_FR if mode == "trad" else LANG_CO
    frag = {
        "topic_ref": f"{ref}-{n - 2}",
        "source": f"source={SOURCE_CODE}§reference={ref}-{n - 2}",
        "title": f"lang={LANG_FR}§{{{tfr.strip()}}}lang={LANG_CO}§{{{tco.strip()}}}",
        "wording": f"lang={LANG_FR}§{{{wfr.strip()}}}lang={LANG_CO}§{{{wco.strip()}}}",
        "question_context": f"#1§lang={qlang}§",
        "answer_context": f"#1§lang={LANG_CO}§",
        "language": LANG_CO,
        "categories": [meta.get("niv", niv)],
        "tags": [],
        "items": [],
    }
    for k, ligne in enumerate(items, start=1):
        o = f"{origine} exo {n} item {k}"
        q, _, r = ligne.partition("=>")
        r, _, indice = r.partition(" ## ")
        q, r = q.strip(), r.strip()
        verifier_accolades(q + indice + r.replace(" | ", " "), o)
        if mode == "trou":
            nb = q.count("___")
            if not nb:
                raise Erreur(f"{o} : trou ___ absent")
            if nb != len(r.split(" ;; ")):
                raise Erreur(f"{o} : {nb} trou(s) mais {len(r.split(' ;; '))} réponse(s)")
            corps, p = separer_ponct(q)
            for i in range(1, nb + 1):
                corps = corps.replace("___", "{?" + str(i) + "§}", 1)
            question = corps + affixe(p)
            reponse = composer_trous(r)
        else:
            corps, p = separer_ponct(q)
            question = "{?1§" + corps + "}" + affixe(p)
            reponse = composer_reponse(r, o)
        if indice.strip():
            question += "{type=clue§lang=" + LANG_FR + "§" + indice.strip() + "}"
        frag["items"].append({"item_ref": str(k), "question": question, "answer": reponse,
                              "categories": [], "tags": []})
    if not frag["items"]:
        raise Erreur(f"{origine} : exercice sans item")
    return frag


# ------------------------------------------------------------- vocabulaire
NATURE_FR = [("verb", "verb, tense-inf"), ("adj", "adj"), ("adv", "adv"), ("interj", "interj"),
             ("pron", "pron"), ("num", "num"), ("conj", "conj"), ("prep", "prep"),
             ("noun", "noun"), ("det", "det"), ("particle", "particle")]
GENRES = {"m": "mas", "f": "fem", "mpl": "mas, plur", "fpl": "fem, plur", "pl": "plur"}


def cats_fr(cats_co: list[str], marque: str) -> str:
    out = []
    if "locution" in cats_co:
        out.append("locution")
    for cle, val in NATURE_FR:
        if any(c == cle or c.startswith(cle + "-") for c in cats_co):
            out.append(val)
            break
    if marque:
        if marque not in GENRES:
            raise Erreur(f"marque de genre inconnue :{marque}")
        if not any(o.startswith("noun") for o in out):
            out = [o for o in out if o not in ("adj", "verb, tense-inf")] + ["noun"]
        out.append(GENRES[marque])
    return ", ".join(dict.fromkeys(", ".join(out).split(", "))) if out else ""


def pluriel_fr(mot: str) -> str:
    """Pluriel français régulier d'un nom (les exceptions s'écrivent `:livres`)."""
    def un(m: str) -> str:
        if re.search(r"[sxz]$", m):
            return m
        if re.search(r"(eau|eu)$", m):
            return m + "x"
        if m.endswith("al") and m not in ("bal", "festival", "carnaval", "récital"):
            return m[:-2] + "aux"
        return m + "s"
    tete, sep, reste = mot.partition(" ")
    return un(tete) + sep + reste


def lire_synonyme(spec: str, origine: str) -> dict:
    """`mot [contexte] @reg-xxx` : un mot arabe du sens, contexte et registre propres."""
    plus = re.findall(r"\s\+([a-z-]+)", spec)
    spec = re.sub(r"\s\+[a-z-]+", "", spec).strip()
    reg = ""
    m = re.match(r"^(.*?)\s*@(reg-[a-z]+)$", spec)
    if m:
        spec, reg = m.group(1).strip(), m.group(2)
    ctx = ""
    m = re.match(r"^(.*?)\s*\[(.+)\]$", spec)
    if m:
        spec, ctx = m.group(1).strip(), m.group(2).strip()
    if not spec or LETTRE_LATINE.search(spec):
        raise Erreur(f"{origine} : mot arabe mal formé {spec!r}")
    return {"mot": spec, "context": ctx, "registre": reg, "plus": plus}


def lire_trads(fr: str, cats_ar: list[str], origine: str) -> list[dict]:
    trads = []
    for t in fr.split(";"):
        t = t.strip()
        marque, override = "", None
        if "::" in t:
            t, override = [x.strip() for x in t.split("::", 1)]
        m = re.match(r"^(.*):(m|f|mpl|fpl|pl)$", t)
        if m:
            t, marque = m.group(1).strip(), m.group(2)
        ctx_fr = ""
        m = re.match(r"^(.*?)\s*\[(.+)\]$", t)
        if m:
            t, ctx_fr = m.group(1).strip(), m.group(2).strip()
        if ":" in t or "[" in t or "]" in t or not t:
            raise Erreur(f"{origine} : traduction mal formée {t!r} (écrire « mot [contexte]:m »)")
        trads.append({"mot": t, "context": ctx_fr, "marque": marque,
                      "cats": override if override is not None else cats_fr(cats_ar, marque)})
    return trads


def lire_voca(bloc: str, origine: str) -> list[dict]:
    """Une ligne = un sens :
    mots ar | traductions fr | cats | niveau | fréquence | étiquettes | registre | contexte | référence | trad | pluriel

    - mots ar : `mot [contexte] @reg-xxx ; synonyme …` — le premier est la vedette ;
      la colonne contexte (8) vaut pour la vedette.
    - trad : contexte de traduction porté par les mots arabes (`fr-FR§à un homme`).
    - pluriel : pluriel du nom (`كُتُب`, ou `كُتُب:livres` pour forcer le pluriel
      français) → sens propre, relié au singulier par INFLECTION.
    """
    entrees = []
    for ligne in bloc.splitlines():
        if not ligne.strip() or ligne.lstrip().startswith("#"):
            continue
        c = [x.strip() for x in ligne.split("|")]
        c += [""] * (11 - len(c))
        mots, fr, cats, niv, freq, tags, reg, ctx, ref, trad, pluriel = c[:11]
        if not (mots and fr and cats and niv):
            raise Erreur(f"{origine} : entrée de vocabulaire incomplète : {ligne!r}")
        if " ج " in f" {ctx} " or ctx.startswith("ج "):
            raise Erreur(f"{origine} : pluriel dans le contexte de {mots!r} (colonne pluriel)")
        cats_ar = [x.strip() for x in cats.split(",") if x.strip()]
        syn = [lire_synonyme(x.strip(), origine) for x in mots.split(" ; ")]
        if syn[0]["context"]:
            raise Erreur(f"{origine} : contexte de la vedette dans la colonne contexte : {mots!r}")
        syn[0]["context"] = ctx
        if trad and "§" not in trad:
            raise Erreur(f"{origine} : trad sans langue {trad!r}")
        vedette = syn[0]["mot"]
        entrees.append({
            "reference": ref or (vedette if not ctx else f"{vedette} ({ctx})"),
            "mot": vedette, "synonymes": syn, "trads": lire_trads(fr, cats_ar, origine),
            "cats": ", ".join(cats_ar), "niveau": niv, "frequence": freq, "tags": tags,
            "registre": reg or "reg-courant", "context": ctx, "origine": origine,
            "trad": trad, "pluriel": pluriel,
        })
        if pluriel:
            entrees[-1]["sens_pluriel"] = sens_du_pluriel(entrees[-1], origine)
    return entrees


def trad_pluriel(trad: str) -> str:
    """Contexte de traduction du sens pluriel : « pluriel » côté français — le pluriel
    français est souvent identique au singulier (pays, prix, temps)."""
    segments = [x for x in trad.split(" ; ") if x]
    if any(x.startswith("fr-FR§") for x in segments):
        return " ; ".join("fr-FR§pluriel, " + x[6:] if x.startswith("fr-FR§") else x for x in segments)
    return " ; ".join(segments + ["fr-FR§pluriel"])


def sens_du_pluriel(e: dict, origine: str) -> dict:
    pl, _, fr_force = e["pluriel"].partition(":")
    pl = pl.strip()
    cats = [x.strip() for x in e["cats"].split(",")]
    if "noun" not in cats:
        raise Erreur(f"{origine} : pluriel sur un non-nom {e['mot']!r}")
    sain = re.search("(ون|ين|ات)$", nu(pl)) is not None
    cats_pl = [x for x in cats if x not in ("sing", "masdar")] + ["plur"] + ([] if sain else ["plur-broken"])
    trads = []
    for t in e["trads"]:
        if not t["marque"] or t["marque"] not in ("m", "f"):
            continue
        mot = pluriel_fr(t["mot"])
        trads.append({"mot": mot, "context": t["context"], "marque": t["marque"] + "pl",
                      "cats": cats_fr(cats, t["marque"] + "pl")})
    if fr_force:
        forces = []
        for x in fr_force.split(";"):
            mot, _, genre = x.strip().partition("@")
            if genre and genre not in ("m", "f"):
                raise Erreur(f"{origine} : genre forcé inconnu {x!r}")
            marque = (genre + "pl") if genre else trads[0]["marque"]
            forces.append(dict(trads[0], mot=mot, marque=marque, cats=cats_fr(cats, marque)))
        trads = forces
    if not trads:
        raise Erreur(f"{origine} : pluriel de {e['mot']!r} sans traduction française au genre marqué")
    return {"reference": pl, "mot": pl, "synonymes": [{"mot": pl, "context": "", "registre": "", "plus": []}],
            "trads": trads, "cats": ", ".join(dict.fromkeys(cats_pl)), "niveau": e["niveau"],
            "frequence": "", "tags": e["tags"], "registre": "reg-courant", "context": "",
            "origine": origine, "trad": trad_pluriel(e["trad"]),
            "pluriel": "", "singulier": e["reference"]}


# ------------------------------------------------------------- écriture
def main():
    plan = {}
    for ligne in (ICI / "chapitres.txt").read_text(encoding="utf-8").splitlines()[1:]:
        if ligne.strip():
            slug, _, titre = ligne.partition(" | ")
            plan[slug[:2]] = (slug.strip(), titre.strip())
    lecons = []
    erreurs = []
    for p in sorted((ICI / "sources").glob("*.txt")):
        try:
            lecons.extend(lire_chapitre(p))
        except Erreur as ex:
            erreurs.append(str(ex))
    refs = [l["meta"]["ref"] for l in lecons]
    if len(set(refs)) != len(refs):
        erreurs.append("références de leçon en double")
    attendu = [f"{i:04d}" for i in range(1, len(refs) + 1)]
    if sorted(refs) != attendu:
        erreurs.append(f"références non séquentielles : {sorted(set(attendu) ^ set(refs))}")
    dico_md = CHANTIER / "vocabulaire" / "assemblage" / "dictionnaire.md"
    anciennes = {}
    if dico_md.exists():
        for ref, entree in dictionnaire_md.lire_dictionnaire(dico_md.parent).items():
            for w in entree["words"]:
                if w.get("ref") and ":" in w["ref"]:
                    anciennes[(ref, w["lang"], w["mot"])] = w["ref"]
    (CHANTIER / "cours").mkdir(exist_ok=True)
    (CHANTIER / "cours" / "chapitres.txt").write_text(
        "slug | titre\n" + "".join(f"{s} | {t}\n" for s, t in sorted(plan.values())), encoding="utf-8")
    for d in (CHANTIER / "cours").iterdir():
        if d.is_dir() and re.match(r"^\d\d-", d.name):
            shutil.rmtree(d)
    par_chap = {}
    for l in lecons:
        par_chap.setdefault(l["meta"]["chap"], []).append(l)
    dico = {}
    a_ecrire = []
    for chap, ls in sorted(par_chap.items()):
        if chap not in plan:
            erreurs.append(f"chapitre {chap} absent de chapitres.txt")
            continue
        ls.sort(key=lambda l: l["meta"]["ref"])
        for rang, l in enumerate(ls, start=1):
            ref = l["meta"]["ref"]
            dossier = CHANTIER / "cours" / plan[chap][0] / f"{rang:02d}-{ref}-{l['meta']['slug']}"
            dossier.mkdir(parents=True)
            (dossier / f"{ref}-1-note.md").write_text(l["note"], encoding="utf-8")
            try:
                if not l["exos"]:
                    raise Erreur(f"{l['origine']} : leçon sans exercice")
                reponses = set()
                for n, bloc in enumerate(l["exos"], start=3):
                    frag = lire_exo(bloc, ref, n, l["meta"]["niv"], l["origine"])
                    for it in frag["items"]:
                        reponses |= set(re.findall("[\u0621-\u064A]+", it["answer"]))
                    (dossier / f"{ref}-{n}-exercice.md").write_text(
                        exercices_md.rendre(frag, SOURCE_CODE), encoding="utf-8")
                refs_voca = []
                lus = []
                for e in lire_voca(l["voca"], l["origine"]):
                    lus.append(e)
                    if "sens_pluriel" in e:
                        lus.append(e["sens_pluriel"])
                for e in lus:
                    if e["reference"] in dico:
                        anc = dico[e["reference"]]
                        if [t["mot"] for t in anc["trads"]] != [t["mot"] for t in e["trads"]]:
                            erreurs.append(f"{l['origine']} : {e['reference']} redéfini différemment ({anc['origine']})")
                    else:
                        dico[e["reference"]] = e
                    if e["reference"] not in refs_voca:
                        refs_voca.append(e["reference"])
                a_ecrire.append((dossier, ref, refs_voca, reponses))
            except Erreur as ex:
                erreurs.append(str(ex))
    # §E2 : la leçon référence aussi les mots de contenu attendus en réponse —
    # sens étiquetés, hors mots-outils, noms propres et nombres (§E2), forme nue reconnue seule ou précédée
    # d'une proclitique (و ف ب ل ال…), et seulement si cette forme nue
    # n'appartient qu'à un sens (un homographe ne se devine pas).
    par_forme = {}
    for reference, e in dico.items():
        natures = {x.strip() for x in e["cats"].split(",")}
        if not e["tags"].strip() or natures & {"pron", "prep", "particle", "conj", "det", "num", "noun-pro"}:
            continue
        for sy in e["synonymes"]:
            par_forme.setdefault(nu(sy["mot"]), set()).add(reference)
    def formes(mot):
        out = {mot}
        for pre in ("وال", "فال", "بال", "لل", "ال", "و", "ف", "ب", "ل"):
            if mot.startswith(pre) and len(mot) - len(pre) >= 2:
                out.add(mot[len(pre):])
        return out
    for dossier, ref, refs_voca, reponses in a_ecrire:
        for mot in sorted(reponses):
            for f in formes(mot):
                cands = par_forme.get(f, set()) | par_forme.get(sans_hamza(f), set())
                if len(cands) == 1:
                    (cand,) = cands
                    if cand not in refs_voca:
                        refs_voca.append(cand)
        if refs_voca:
            dictionnaire_md.ecrire_voca_lecon(dossier / f"{ref}-2-voca.md", refs_voca)
    # Homographes sans voyelles : une forme nue portée par plusieurs sens reçoit
    # pour contexte sa forme vocalisée (ou le contexte explicite du synonyme).
    porteurs = {}
    for reference, e in dico.items():
        for sy in e["synonymes"]:
            porteurs.setdefault(nu(sy["mot"]), set()).add(reference)
    sortie = {}
    relations = []
    for reference, e in dico.items():
        trad = dict(x.split("§", 1) for x in e["trad"].split(" ; ")) if e["trad"] else {}
        mots = []
        for sy in e["synonymes"]:
            commun = {"lang": LANG_CO_MOT, "trad": trad, "registre": sy["registre"] or e["registre"],
                      "frequence": e["frequence"], "niveau": e["niveau"],
                      "cats": [", ".join([e["cats"]] + sy["plus"])]}
            mots.append(dict(commun, mot=sy["mot"], context=sy["context"]))
            bare = nu(sy["mot"])
            if bare != sy["mot"]:
                ctx_nu = sy["context"] or (sy["mot"] if len(porteurs[bare]) > 1 else "")
                mots.append(dict(commun, mot=bare, context=ctx_nu))
        for t in e["trads"]:
            mots.append({"lang": LANG_FR, "mot": t["mot"], "context": t["context"], "registre": "reg-courant",
                         "cats": [t["cats"]] if t["cats"] else []})
        if e.get("singulier"):
            relations.append(f"{e['singulier']} | INFLECTION | {reference}")
        for w in mots:
            w["ref"] = anciennes.get((reference, w["lang"], w["mot"]), "")
        sortie[reference] = {"tags": [x.strip() for x in e["tags"].split(",") if x.strip()], "words": mots}
    dico_md.parent.mkdir(parents=True, exist_ok=True)
    dictionnaire_md.ecrire_dictionnaire(dico_md, dict(sorted(sortie.items(), key=lambda kv: kv[0])))
    (CHANTIER / "vocabulaire" / "relations.txt").write_text(
        "# Généré par vocabulaire/generation/gen.py — ne pas éditer.\ntete | type | cible\n"
        + "".join(r + "\n" for r in sorted(relations)), encoding="utf-8")
    nb_items = sum(len(re.findall(r"=>", "\n".join(l["exos"]))) for l in lecons)
    print(f"{len(lecons)} leçons, {nb_items} items, {len(dico)} sens")
    if erreurs:
        print("ERREURS :")
        for e in erreurs:
            print("  -", e)
        sys.exit(1)


if __name__ == "__main__":
    main()
