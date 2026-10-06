# Chantier fr_gram_ar — plan de génération

Grammaire de l'arabe standard moderne pour francophones. Contenu **original,
rédigé par IA**, sur le moule de `fr_gram_co` (sources compactes par chapitre +
`gen.py`) : pas d'ouvrage source ; la vérification porte sur la justesse
grammaticale et la cohérence interne (règle énoncée / exemples / exercice).

**Ampleur** : 40 chapitres, **182 leçons**, de l'alphabet au niveau B2
(`niv-a1` → `niv-b2`). 202 topics, 1021 items, 654 sens de vocabulaire (dont 144 pluriels).

---

## 0. Cadrage (décisions de l'utilisateur, 2026-10-05)

| question | décision |
|---|---|
| variété | **arabe standard** (_fuṣḥā_) ; les dialectes ne sont présentés qu'au ch. 40 |
| forme des réponses attendues | **arabe sans voyelles** (écriture usuelle, clavier arabe) |
| présentation des exemples | **vocalisés + translittération** : arabe entièrement vocalisé / translittération / français |
| ampleur | complète, 40 chapitres |

Pourquoi sans voyelles : la comparaison de l'app est caractère par caractère
(Damerau-Levenshtein après normalisation) et le normaliseur **ne retire pas**
les diacritiques ; *كَتَبَ* exigé contre *كتب* tapé compterait des fautes, et
saisir les harakat au clavier iOS est pénible. Conséquence assumée : les
exercices ne testent jamais une voyelle brève (cas, voix passive, formes I/II
homographes) ; ces points sont travaillés par traduction, où le squelette
consonantique diffère, ou restent du ressort de la fiche.

## 1. Codes de langue

- `ar` : vocabulaire et fiches (`langues_corpus`).
- `ar-SA` : exercices (`question_context` / `answer_context`). Il n'existe pas
  de code régional pour l'arabe standard admis par `parrotdict` (`ar-001` est
  refusé par l'expression de locale) ; `ar-SA` ne sert qu'à choisir une voix,
  et le choix de voix de l'app retombe de toute façon sur une voix `ar*`.
- Pas de voix de substitution : iOS fournit des voix arabes.

## 2. Plan de chapitres

`cours/chapitres.txt` (slugs translittérés en ASCII, titres en français) ;
découpe en leçons dans `PLAN-leçons-ar-fr.md`. Progression : écriture et
lecture → article, salutations → phrase nominale, genre, nombre, pluriels
brisés → adjectif, démonstratifs, annexion, suffixes, prépositions, questions,
nombres → accompli, inaccompli, négations → *kāna*, *ʾinna*, futur, modes
(subjonctif, apocopé, impératif) → morphologie (racines, formes II–X, verbes
faibles, nom verbal, participes) → cas, relatifs, comparatif, passif,
condition, compléments à l'accusatif → structure de la phrase, discours
rapporté, vocatif → langue arabe et dialectes.

L'inaccompli (ch. 18) précède la négation du passé (ch. 19) : *lam* exige
l'apocopé, qui se forme sur l'inaccompli.

## 3. Format des fiches

```
cours/<CC>-<slug-chapitre>/<LL>-<ref>-<slug-leçon>/
  <ref>-1-note.md        # la fiche de cours (ressource NOTE)
  <ref>-2-voca.md        # références vers vocabulaire/assemblage/
  <ref>-3-exercice.md    # 1ʳᵉ série, <ref>-3-exercice.json régénéré
  <ref>-4-exercice.md    # 2ᵉ série éventuelle
```

### Conventions de balisage

- **Italique `*…*` = arabe prononçable** (`<span lang="ar" dir="rtl">`), lu
  par la voix arabe. Jamais de translittération ni de français en `*…*`.
- **Prononciation** : une lettre citée pour son nom ou son son, une paire minimale, un exemple de
  lettres solaires porte la langue et l'IPA (`*[ar] ب /baːʔ/*`) ; un mot d'une autre langue cité
  pour comparaison, sa langue et son IPA (`*[en] think /θɪŋk/*`). Une lettre seulement mentionnée
  (racine *ك ت ب*, forme positionnelle) est muette : `_…_` ou texte simple.
- **Translittération en `_…_`** : italique de prose, jamais prononcé.
- **Exemple cité = trois lignes** :
  ```
  > *البَيْتُ كَبِيرٌ.*
  > _al-baytu kabīrun._
  > La maison est grande.
  ```
- **Vocalisation complète** des exemples, désinences casuelles comprises
  (lecture « de manuel », pas de forme pausale) ; la translittération suit.
- **Translittération** (type DIN 31635 / Arabica) : ʾ b t ṯ ǧ ḥ ḫ d ḏ r z s
  š ṣ ḍ ṭ ẓ ʿ ġ f q k l m n h w y ; ā ī ū ; article assimilé (_aš-šams_) et
  élidé après voyelle (_fī l-bayti_) ; _tāʾ marbūṭa_ → _-a_ / _-at-_.
- **Rendu RTL** : `cours.py` ajoute `dir="rtl"` aux citations d'une langue
  écrite de droite à gauche, et, pour un corpus RTL seulement, un complément
  de style (arabe non italique, corps 1,2) — les autres chantiers sont
  inchangés octet pour octet.
- **Renvois** `(§C.L)` vers une autre leçon.

## 4. Exercices

Rédigés dans `vocabulaire/generation/sources/<CC>.txt`, rendus par `gen.py`
au format tabulé puis régénérés en JSON par `parrotdict exercices`. Modes :

| mode | question | réponse |
|---|---|---|
| `trad` | phrase française, ou translittération + glose (ch. 1–3) | arabe nu |
| `transfo` | forme arabe + consigne courte (personne, schème…) | arabe nu |
| `trou` | phrase arabe à trou(s) | mot ou terminaison manquants |

`gen.py` dérive automatiquement les variantes acceptées : harakat, _šadda_,
_tanwīn_ et tatweel retirés ; variante où *أ إ آ* deviennent *ا* (saisie
courante). Une hamza sur un alif de liaison (*إمتحان*) reste fausse. La
ponctuation finale (y compris *؟*) est en affixe, hors du texte à taper ;
une virgule arabe interne est proposée en alternative explicite.

## 5. Vocabulaire

`vocabulaire/assemblage/dictionnaire.md` (régénéré par `gen.py`) : un sens par entrée, classé selon
`Documentation/regles_vocabulaire.md` — **vérifié le 2026-10-06**, trace dans
`vocabulaire/generation/verification_20261006.md`.

- Mots arabes : forme vocalisée (affichée, lue par la voix) + forme nue (celle qu'on tape), et les
  synonymes du sens (`طَقْس ; جَوّ [طَقْس]`), chacun avec registre et contexte propres. Une forme nue
  partagée par plusieurs sens (درس, ذهب, أنت…) prend sa forme vocalisée pour contexte.
- Contexte principal seulement pour une vraie polysémie dans la langue du mot (بَيْت مَسْكَن, livre
  [ouvrage]) ; les distinctions qui n'existent qu'en traduisant (tu à un homme / à une femme, que
  devant un verbe / un nom, si possible / irréel) sont des **contextes de traduction** (colonne `trad`).
- **Pluriels** : sens propres (catégories `plur`, `plur-broken`), reliés au singulier par
  `INFLECTION` dans `vocabulaire/relations.txt` (généré) — jamais dans le contexte.
- Chaque leçon référence ses mots enseignés et les mots de contenu attendus en réponse (§E2).
- Catégories propres à l'arabe ajoutées à `categories.json` : `particle`, `verb-derived`, `dual`,
  `plur-broken`, `mode-juss`, `masdar`, `nisba`.

## 6. Limites connues, points à faire relire

- **Contenu rédigé par IA** : faire relire par un arabisant, en priorité la
  vocalisation complète des exemples (désinences, _šadda_, _hamza_), les
  pluriels brisés donnés en contexte, les formules du ch. 40.
- Pluriels multiples : un seul est retenu par nom (vérifié sur Wiktionary — *مُدِيرُون*, *مُدَرَاء*
  y étant proscrit) ; *أَيُّهَا السَّيِّدَاتُ وَالسَّادَةُ* (formule usuelle) reste à faire confirmer.
- Les exercices ne vérifient ni les voyelles brèves ni les désinences
  casuelles (choix de cadrage) ; seuls l'alif du _tanwīn_ _-an_, les formes à
  _n_ et les « cinq noms » rendent le cas visible.
- Le vocabulaire enregistre la forme nue comme synonyme : sans l'option
  « synonymes » de la stratégie, l'app peut attendre la forme vocalisée.
