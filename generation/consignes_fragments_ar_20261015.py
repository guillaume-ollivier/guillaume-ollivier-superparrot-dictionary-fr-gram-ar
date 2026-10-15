"""Balise l'arabe des consignes françaises (2026-10-15).

Même démarche que `fr_gram_pt/generation/consignes_fragments_pt_20261015.py`,
mécanique ici : toute suite de caractères arabes (mots séparés par des blancs
compris) d'une consigne `fr-FR` devient un fragment `{lang=ar-SA§…}`, affiché en
romain et lu avec la voix arabe (« Écrivez « نعم » ou « لا » », « avec لم »).
Les translittérations de suffixe (-āni, -ūna) restent en français, comme les
lettres et digrammes des autres chantiers.

Les consignes arabes n'ont rien à baliser.

Usage : python3 consignes_fragments_ar_20261015.py [--ecrire] <dossier exercises>
"""
from __future__ import annotations
import re
import sys
from pathlib import Path

PT = "lang=ar-SA§"
ARABE = re.compile(r"[\u0600-\u06FF\u0750-\u077F\uFB50-\uFDFF\uFE70-\uFEFF]+"
                   r"(?:\s+[\u0600-\u06FF\u0750-\u077F\uFB50-\uFDFF\uFE70-\uFEFF]+)*")


def baliser(texte: str) -> str:
    return ARABE.sub(lambda m: "{" + PT + m.group(0) + "}", texte)


def traiter(chemin: Path, ecrire: bool, changements: list):
    lignes = chemin.read_bytes().decode("utf-8").split("\n")
    attribut, modifie = "", False
    for i, ligne in enumerate(lignes):
        cr = "\r" if ligne.endswith("\r") else ""
        f = ligne[:len(ligne) - len(cr)].split(";", 6)
        if len(f) < 7:
            continue
        if f[2]:
            attribut = f[2]
        if attribut != "wording" or f[5] != "fr-FR" or PT in f[6]:
            continue
        nouveau = baliser(f[6])
        if nouveau != f[6]:
            changements.append((chemin.name, f[6], nouveau))
            f[6] = nouveau
            lignes[i] = ";".join(f) + cr
            modifie = True
    if ecrire and modifie:
        chemin.write_bytes("\n".join(lignes).encode("utf-8"))


def main():
    ecrire = "--ecrire" in sys.argv
    dossier = Path([a for a in sys.argv[1:] if not a.startswith("-")][0])
    changements = []
    for chemin in sorted(dossier.rglob("*.csv")):
        traiter(chemin, ecrire, changements)
    vus = set()
    for fichier, avant, apres in changements:
        if (avant, apres) in vus:
            continue
        vus.add((avant, apres))
        print(f"- {avant}\n  {apres.replace('{' + PT, '⟦').replace('}', '⟧')}")
    print(f"\n{len(changements)} lignes, {len(vus)} consignes distinctes")


if __name__ == "__main__":
    main()
