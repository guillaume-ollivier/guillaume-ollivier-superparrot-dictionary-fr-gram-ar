# Génération de fr_gram_ar

Comme pour `fr_gram_co`, **les sources font foi** : `sources/<CC>.txt` (un fichier
par chapitre, plusieurs leçons) + `chapitres.txt`. `gen.py` régénère tous les
dossiers de leçon de `cours/` et `../assemblage/dictionnaire.md` (en conservant
les références gelées des mots). Toute correction se fait dans les sources, puis :

```sh
python3 gen.py
cd ../../../../tools/dictionnaire
R=../../repositories/fr_gram_ar
python3 -m parrotdict exercices $R && python3 -m parrotdict refs $R \
  && python3 -m parrotdict assembler $R && python3 -m parrotdict controler $R
```

Format d'une leçon dans une source :

```
@ref 0021
@chap 05
@slug al-jumla                 # ASCII seulement
@niv niv-a1
=== NOTE
# Titre (H1 = titre de la leçon)
...markdown : arabe vocalisé en *…*, translittération en _…_...
=== EXO                        # une série d'exercices (plusieurs possibles)
title: titre fr | titre ar
wording: consigne fr | consigne ar
mode: trad | trou | transfo
question => réponse | alternative ## indice français
phrase à ___ trous ___ => rép1 | alt1 ;; rép2   (∅ = trou vide)
=== VOCA
mots ar | trad1 [contexte fr]:m; trad2 | cats ar | niveau | fréquence | étiquettes | registre | contexte ar | référence | trad | pluriel
```

- `mots ar` : `vedette ; synonyme [contexte] @reg-soutenu +verb-derived` — le contexte de la vedette
  va dans la colonne contexte ; un synonyme peut avoir contexte, registre et catégories en plus.
- `trad` : contexte de traduction porté par les mots arabes (`fr-FR§à un homme`).
- `pluriel` : `كُتُب` (pluriel français régulier généré) ou `أَعْمَال:travaux` / `عُلُوم:sciences@f`
  (forcé) → sens propre relié par INFLECTION (`../relations.txt`, généré).
- traduction française : `mot [contexte]:m` ; `::cats` remplace la nature inférée (`il y a::locution, verb`).

Réponses : on peut les écrire vocalisées, `gen.py` retire harakat et tatweel et
ajoute la variante sans hamza sur alif (*أ إ آ* → *ا*). Une traduction française
s'écrit `mot [contexte]:genre` (contexte **avant** le genre).

`gen.py` refuse : références de leçon non séquentielles, slug non ASCII,
caractère réservé QualifiedText (`{ } § |`) dans un texte, lettre latine dans une
réponse, nombre de trous ≠ nombre de réponses, ponctuation finale divergente
entre alternatives, traduction mal formée, sens redéfini avec d'autres
traductions, pluriel dans la colonne contexte, pluriel sur un non-nom.

Validation au moteur Swift : paquet scratch `valid_ar` (copie de `valid_ja`,
checkouts SPM et `Package.resolved` copiés depuis `SuperParrotCoreSwift`,
`swift build --skip-update` hors sandbox) — le 2026-10-06 : 1368 combinaisons,
0 refusée, 0 injouable.

Vérification des traductions : `verification_20261006.md` ; `passe1_20261006.py` est la trace
exécutable de la passe 1 (ne pas relancer).
