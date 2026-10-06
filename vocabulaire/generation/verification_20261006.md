# Vérification du vocabulaire — fr_gram_ar — 2026-10-06

Périmètre : **tout** le lexique de `vocabulaire/assemblage/dictionnaire.md`, avant tout import.
498 sens au départ (rédaction du 2026-10-05), **654** à l'arrivée : 144 sens « pluriel » créés,
quelques sens scindés, fusionnés ou ajoutés. Règles appliquées : `Documentation/regles_vocabulaire.md`
et `procedure_generation_cours.md` §E2. Les décisions sont exécutées par
`passe1_20261006.py` (application unique, gardée comme trace) ; elles portent sur les sources
`sources/<CC>.txt`, qui font foi.

## Passe 1 — relecture intégrale, colonne arabe puis colonne française

### Défauts de structure corrigés sur tout le dépôt

- **Pluriel brisé rangé dans le contexte** (`ج كُتُب`) sur ~120 noms : interdit, le contexte ne sert
  qu'à lever une polysémie. Chaque pluriel devient un **sens propre** (mot vocalisé + nu, traduction
  française au pluriel, catégories `plur` / `plur-broken`, contexte de traduction `fr-FR§pluriel`
  car le pluriel français est parfois identique au singulier — pays, prix, temps), relié au
  singulier par `INFLECTION` dans `vocabulaire/relations.txt`. Pluriels français irréguliers forcés :
  yeux, travaux, messieurs, mesdames ; formes plates remplacées : activités (pas « dynamismes »),
  esprits, sciences (f), aliments (m), bien-aimés, terres.
- **Contexte principal de secours** (« tu [masculin] », « que [devant un verbe] », « si [irréel] »,
  « ne… pas [futur] », « bonjour [le matin] ») : remplacé par un **contexte de traduction** porté par
  le mot arabe (`fr-FR§à un homme`, `fr-FR§devant un verbe`, `fr-FR§condition irréelle`,
  `fr-FR§au futur`, `fr-FR§le matin`…), le mot français redevient nu.
- **Homographes sans voyelles** (درس : leçon / étudier / enseigner ; ذهب ; أنت ; أن ; ساعة…) : la forme
  nue d'une forme partagée par plusieurs sens reçoit sa forme vocalisée en contexte (automatique, `gen.py`).
- **Polysémie de l'arabe** : contexte arabe ajouté — بَيْت (مَسْكَن : pas le vers), عَيْن (لِلنَّظَر : pas la
  source ni la lettre), ظَهْر (جِسْم : pas midi), تَارِيخ (المَاضِي), جِذْر (لُغَة), خَطّ (كِتَابَة), قَرْن (مِائَة
  سَنَة : pas la corne), لَا (جَوَاب), مَا / مَنْ (اِسْتِفْهَام), قَدْ (مَعَ المَاضِي), حَتَّى (غَايَة), دَعَا
  (لِلضِّيَافَة), سَلَّمَ (عَلَى شَخْص), صَفّ (مَدْرَسَة), طَالِب (دِرَاسَة), خَيْر (ضِدّ الشَّرّ), اِسْم (لِشَخْص).
- **Polysémie du français** : contexte ajouté — livre [ouvrage], café [boisson], marché [lieu de vente],
  homme / femme [adulte], garçon [enfant], bureau [lieu de travail], journal [presse], prix [coût],
  feu [flamme], racine [d'un mot], sens [signification], chef [dirigeant], neuf [récent], sortir
  [d'un lieu] / [quelque chose], arriver [quelque part], marcher [à pied], entrée / sortie [action],
  état [situation], nom [d'une personne], le / la / les [article], qui / que [relatif | interrogatif |
  conjonction], esprit [intellect], raison [faculté], demander [une question] / [une chose].
- **Sens fusionnés scindés** : عَفْوًا → « de rien » (رَدّ الشُّكْر) / « pardon » (اِعْتِذَار) ; سَاعَة →
  « heure » (زَمَن) / « montre » (يَد) ; هُنَاكَ → « là-bas » (مَكَان) / « il y a » (وُجُود).
- **Collisions inverses** (même mot français pour deux sens, même nature, sans rien pour départager)
  — révélées par la correction du contrôle `collision-inverse` (voir plus bas) :
  - synonymes réunis dans un seul sens : طَقْس + جَوّ « temps [météo] » ; صَارَ + أَصْبَحَ « devenir » ;
    عَادَ + رَجَعَ « revenir ; rentrer » ; اِسْتَعْمَلَ + اِسْتَخْدَمَ « utiliser ; employer » ; جَاءَ + أَتَى
    (soutenu) « venir » ; مَعَ السَّلَامَةِ + إِلَى اللِّقَاءِ « au revoir » ; خَلْفَ + وَرَاءَ « derrière » ;
    مِائَة + مِئَة « cent » ; حَاسُوب + كَمْبْيُوتَر « ordinateur » ;
  - traduction retirée : « maison » de دَار (gardé : demeure), « enfant » de وَلَد, « voir » de شَاهَدَ,
    « écouter » de سَمِعَ, « penser » de ظَنَّ, « venir » de حَضَرَ, « pied » de رِجْل (→ قَدَم, ajouté),
    « grand » de طَوِيل, « beaucoup » de كَثِير, « avoir » de عِنْدَ, « Tunis » de تُونِس ;
  - contexte de traduction : دَرَّسَ / عَلَّمَ « enseigner » ; مُدَرِّس / أُسْتَاذ « professeur » ; هٰذَا /
    هٰذِهِ « ceci » ; إِلَّا / سِوَى « sauf » ; أَوْ / أَمْ « ou » ; قَطُّ / أَبَدًا « jamais ».
- **Traductions doubles qui n'en étaient pas** : عَمِلَ (« faire » retiré), حَتَّى (« jusqu'à ce que »
  seul), عَنْ (« de » retiré), صَحِيح (« juste » retiré), غَيْر (« non- » retiré), رَدَّ (« rendre »
  retiré), طَعَام (« plat » retiré), بِنَاء (« bâtiment » retiré), وَقَفَ (« s'arrêter » seul).
- **Rendus descriptifs** marqués `defi` : سَوْفَ « marque du futur », مَا شَاءَ اللّٰهُ « formule d'admiration ».
- **Registre** revu mot par mot : `reg-soutenu` pour بَلَى, لَيْتَ, رَجَا, ذُو, إِنْ (conditionnel), لَوْلَا,
  أَتَى ; `reg-familier` pour خَلَاص (colloquial).
- **Catégories** : `loanword` (بَنْك, دُولَار, تِلْفَاز, فِيلْم, كَمْبْيُوتَر, كِيلُوغْرَام), `question` (كَيْفَ حَالُكَ),
  `masdar`, nature des traductions corrigée là où l'inférence trompait (peut-être, plus, moins → adv ;
  il y a → locution verbale ; ne… pas → locution adverbiale).
- **Étiquettes** : étiquettes transverses ajoutées en plus du thème principal (طَبِيب metier + sante,
  مَدْرَسَة ecole + batiment, مَطْعَم commerce + repas, مَطَار transport + voyage, سُوق commerce + ville…).
  Seuls 30 sens restent sans étiquette : tous des mots-outils (articles, pronoms démonstratifs et
  relatifs, conjonctions, particules) et « il y a » — aucun nœud thématique ne les couvre.
- **Ajouts** (mots attendus en réponse ou formules enseignées, absents du dictionnaire) : وَعَلَيْكُمُ
  السَّلَامُ, صَبَاحُ النُّورِ, مَسَاءُ النُّورِ, تُصْبِحُ عَلَى خَيْرٍ, شُكْرًا جَزِيلًا, كَيْفَ حَالُكَ, فِيل, سَلَام,
  قَدَم, مَكَان, اِفْتِتَاح, كِيلُوغْرَام, اِمْتَلَأَ, قَاطِع, وُلِدَ.

### Doutes notés pour la passe 2

Pluriels : مُدِير, بَلَد, كُرْسِيّ, مِكْنَسَة, حَاسُوب, نَادٍ, مُحَامٍ, هَدِيَّة, صَحْرَاء, يَد, لَيْلَة, جَمَل, أُذُن,
رِيح, فِنْجَان, حَقِيبَة, حَبِيب, سَيِّد, سَيِّدَة. Genre : كَأْس, دَار, سُوق, مَطْبَخ, أُذُن, رِيح. Sens ou registre :
خَلَاص, مَا شَاءَ اللّٰهُ, رَجَا, جَوّ, طَقْس, ذَاهِب, لَوْلَا, ثَابِت, قَاطِع, ذُو, سِوَى, عَالٍ, حِصَّة, وَسَط, رِجْل,
عَشَاء, غَدَاء, صَفّ, خَطّ, لَهْجَة, العَامِّيَّة, الفُصْحَى, عَيْن, بَيْت, صِفْر, رَقْم, تَشَرَّفْنَا, مَبْرُوك, تَعَالَ,
كَمْبْيُوتَر, تِلْفَاز, كِيلُو, اِمْتَلَأَ, اِفْتِتَاح, اِصْطَدَمَ, مُزْدَحِم, تَقَابَلَ, تَنَاوَلَ, سَلَّمَ, ظَنَّ, نَشَاط, قَادِم,
عَالَمِيّ, مُجْتَهِد, مَجَّانِيّ, سُكَّان, مَعْرِض, مَجْلِس, مَلْعَب, لَعَلَّ, لَيْتَ, بَلَى, قَطُّ, عِنْدَمَا, لِذٰلِكَ, أَمَّا,
مُسْتَعْمَل, مُفِيد, مُسَافِر, صَبَاحُ النُّورِ, تُصْبِحُ عَلَى خَيْرٍ.

## Passe 2 — sources externes

Source principale : en.wiktionary.org, wikitexte lu en `action=raw` (section Arabic : tête de lemme
avec genre et pluriels, définitions). Recherche web en complément quand Wiktionary n'a pas l'entrée.

| entrée | source | constat | décision |
|---|---|---|---|
| مُدِير | Wiktionary | pl. مُدِيرُون ; مُدَرَاء marqué *proscribed* | pluriel مُدِيرُون maintenu |
| بَلَد | Wiktionary | pl. بِلَاد, بُلْدَان | بُلْدَان maintenu |
| كُرْسِيّ | Wiktionary | pl. كَرَاسِيّ, كَرَاسٍ ; chair, seat | maintenu |
| مِكْنَسَة | Wiktionary | f., pl. مِكْنَسَات, مَكَانِس ; broom | maintenu |
| حَاسُوب | Wiktionary | m., pl. حَوَاسِيب ; computer | maintenu |
| كَمْبْيُوتَر | Wiktionary | m. ; computer ; vocalisation كَمْبْيُوتَر | vocalisation corrigée (كُمْبِيُوتَر → كَمْبْيُوتَر) |
| نَادٍ | Wiktionary | pl. أَنْدِيَة, نَوَادٍ ; club | maintenu |
| مُحَامٍ | Wiktionary | lawyer, attorney ; pluriel sain | maintenu |
| خَلَاص | Wiktionary | interjection *colloquial* : enough!, done! | maintenu, `reg-familier` |
| مَا شَاءَ اللّٰهُ | Wiktionary | gratitude / admiration, « God willed it » | maintenu, rendu `defi` |
| رَجَا | Wiktionary | to hope ; avec أَنْ : implore, ask someone to do | « prier [demander] » maintenu |
| جَوّ | Wiktionary | air, weather, atmosphere | fusionné à طَقْس, contexte طَقْس |
| طَقْس | Wiktionary | weather (court terme) ; aussi rite | maintenu |
| ذَاهِب | Wiktionary | going | « allant » maintenu |
| لَوْلَا | Wiktionary | if not for | « n'eût été ; sans » maintenu |
| كَأْس | Wiktionary | f. ; glass, cup, trophy | maintenu « verre », contexte لِلشُّرْب |
| ثَابِت | Wiktionary | constant, stable, fixed | maintenu |
| دَار | Wiktionary | f. ; house, building, land | « demeure » maintenu |
| سُوق | Wiktionary | f. et m. ; market | maintenu (fiche §6.3 conforme) |
| سَيِّد / سَيِّدَة | Wiktionary | mister, sir / madam, lady, Mrs. ; pl. سَادَة | maintenus |
| قَاطِع | Wiktionary (secant seulement) + almaany, Reverso (رفض قاطع = categorical/flat refusal) | adjectif « catégorique » attesté par l'usage | maintenu |
| ذُو | Wiktionary | possessor of (état construit) | maintenu, `reg-soutenu` |
| سِوَى | Wiktionary | nom en état construit = except | maintenu (nature `noun`) |
| عَالٍ | Wiktionary | high | maintenu |
| هَدِيَّة / صَحْرَاء / يَد / لَيْلَة | Wiktionary | pl. هَدَايَا / صَحَارٍ (aussi صَحَارَى) / أَيْدٍ / لَيَالٍ | maintenus |
| حِصَّة | Wiktionary | share ; lesson, class | « cours [séance] » maintenu |
| وَسَط | Wiktionary | middle, center | maintenu |
| جَمَل | Wiktionary | camel, pl. جِمَال | maintenu |
| أُذُن / رِيح | Wiktionary | f. ; pl. آذَان / رِيَاح | maintenus |
| رِجْل | Wiktionary | f. ; leg ; le pied est قَدَم | « pied » retiré, قَدَم ajouté |
| فِنْجَان | Wiktionary | cup, pl. فَنَاجِين | maintenu |
| مَطْبَخ | Wiktionary | m. ; kitchen | maintenu |
| حَقِيبَة | Wiktionary | bag (seulement) | **« valise » retiré** |
| حَبِيب | Wiktionary | beloved, darling ; pl. أَحِبَّاء | maintenu |
| عَشَاء / غَدَاء | Wiktionary | supper, dinner / lunch | maintenus |
| صَفّ | Wiktionary | row ; class, grade | maintenu, contexte مَدْرَسَة |
| خَطّ | Wiktionary | line ; handwriting, calligraphy | maintenu, contexte كِتَابَة |
| لَهْجَة | Wiktionary | dialect ; accent | « dialecte » maintenu |
| الفُصْحَى | Wiktionary (اللغة العربية الفصحى) | Fusha, Modern Standard Arabic | maintenu |
| العَامِّيَّة | Wiktionary (Ammiyya) + recherche web | colloquial Arabic, opposé à الفصحى | « arabe dialectal » maintenu |
| عَيْن / بَيْت | Wiktionary | polysémiques (source, lettre / vers) | contextes confirmés |
| صِفْر / رَقْم | Wiktionary | zero / number, figure | maintenus |
| تَشَرَّفْنَا | Wiktionary | nice to meet you | maintenu |
| مَبْرُوك | Wiktionary (sections égyptienne et levantine) | congratulations | maintenu |
| تَعَالَ | Wiktionary | come (here)! | maintenu |
| تِلْفَاز | Wiktionary | television | maintenu |
| كِيلُو | Wiktionary | aucune entrée ; كِيلُوغْرَام attesté (kilogram) | **remplacé par كِيلُوغْرَام** (l'exercice accepte aussi كيلو) |
| اِمْتَلَأَ | almaany, bab.la, Quranic Arabic Corpus | form VIII : be filled, become full | maintenu |
| اِفْتِتَاح | Wiktionary | opening, inauguration | maintenu |
| اِصْطَدَمَ / مُزْدَحِم | Wiktionary | collide / crowded | maintenus |
| تَقَابَلَ / تَنَاوَلَ / سَلَّمَ | Wiktionary | meet / take, eat / greet (عَلَى) | maintenus |
| ظَنَّ | Wiktionary | think, suppose, believe | « croire ; supposer » maintenu |
| نَشَاط | Wiktionary | activity, energy, liveliness | maintenu |
| قَادِم / عَالَمِيّ / مُجْتَهِد / مَجَّانِيّ | Wiktionary | next / worldwide / diligent / free of charge | maintenus |
| سُكَّان | Wiktionary | plural of سَاكِن (inhabitants) | **« population » retiré** |
| مَعْرِض / مَجْلِس / مَلْعَب | Wiktionary | exhibition, fair / council / stadium, playing field | maintenus |
| لَعَلَّ / لَيْتَ / بَلَى / قَطُّ | Wiktionary | perhaps / if only / contradicting a negative / never (passé, négatif) | maintenus |
| عِنْدَمَا / لِذٰلِكَ / أَمَّا | Wiktionary | when / therefore / as for (+ فَـ) | maintenus |
| مُسْتَعْمَل / مُفِيد / مُسَافِر | Wiktionary | used, secondhand / useful / traveller | maintenus |
| صَبَاحُ النُّورِ / تُصْبِحُ عَلَى خَيْرٍ | Wiktionary | good morning (réponse) / good night | maintenus |

## Passe 3 — contre-relectures

- **Tour 1** : relecture complète du dictionnaire régénéré (654 sens) + `parrotdict controler`.
  Corrections : genre des pluriels forcés (« sciences » f, « aliments » m — syntaxe `mot@genre`
  ajoutée à `gen.py`), تُونِس réduit à « Tunisie » (pays / ville fusionnés), `question` sur
  « comment vas-tu », contexte de traduction de مَرْحَبًا (« formule neutre et détendue »).
- **Tour 2** : relecture des cinq sens corrigés, `controler`, moteur Swift. **Aucun changement.**

État final de `controler` : 0 anomalie sérieuse ; 2 « à examiner », assumées — formes nues أنت et
أن partagées par deux sens distincts (أَنْتَ / أَنْتِ, أَنَّ / أَنْ), départagés par la forme vocalisée en
contexte et par un contexte de traduction.

## Outillage corrigé en chemin

- `controles.py`, `collision-inverse` : un discriminant de **nature** (`#noun`) était pris pour un
  contexte, si bien que deux sens de **même** nature n'étaient jamais signalés. Corrigé ; cela fait
  apparaître 5 collisions dans `fr_gram_co` et 2 dans `fr_gram_en`, non traitées ici.
- `assemblage.py` : `vocabulaire/relations.txt` n'était lu que par le volet vocabulaire ; les sens
  de leçon d'un chantier « cours » le reçoivent désormais (144 relations INFLECTION).

## Vocabulaire des leçons (§E2)

Chaque leçon référence ses mots enseignés **et** les mots de contenu attendus en réponse (hors
mots-outils, noms propres, nombres, homographes non vocalisés) : 1 043 références, 9 leçons sans
vocabulaire, toutes structurelles (tableaux de conjugaison et formation des modes).

## Validation moteur

Exécutable Swift lié à ParrotCore (`valid_ar`, copie de `valid_ja`) : 40 chapitres, 654 sens,
202 topics, 1 021 items, 1 368 combinaisons de réponse — 0 refusée, 0 injouable.

## Références

Pages consultées pour la passe 2, dans l'ordre des lots. Wiktionary a été lu en wikitexte brut
(`https://en.wiktionary.org/w/index.php?title=<mot>&action=raw`, section *Arabic*) ; les liens
ci-dessous mènent à la page lisible correspondante.

**Wiktionary (en), lot 1** : [مدير](https://en.wiktionary.org/wiki/%D9%85%D8%AF%D9%8A%D8%B1#Arabic), [بلد](https://en.wiktionary.org/wiki/%D8%A8%D9%84%D8%AF#Arabic), [كرسي](https://en.wiktionary.org/wiki/%D9%83%D8%B1%D8%B3%D9%8A#Arabic), [مكنسة](https://en.wiktionary.org/wiki/%D9%85%D9%83%D9%86%D8%B3%D8%A9#Arabic), [حاسوب](https://en.wiktionary.org/wiki/%D8%AD%D8%A7%D8%B3%D9%88%D8%A8#Arabic), [ناد](https://en.wiktionary.org/wiki/%D9%86%D8%A7%D8%AF#Arabic), [خلاص](https://en.wiktionary.org/wiki/%D8%AE%D9%84%D8%A7%D8%B5#Arabic), [رجا](https://en.wiktionary.org/wiki/%D8%B1%D8%AC%D8%A7#Arabic), [جو](https://en.wiktionary.org/wiki/%D8%AC%D9%88#Arabic), [ما شاء الله](https://en.wiktionary.org/wiki/%D9%85%D8%A7_%D8%B4%D8%A7%D8%A1_%D8%A7%D9%84%D9%84%D9%87#Arabic)

**Wiktionary (en), lot 2** : [ذاهب](https://en.wiktionary.org/wiki/%D8%B0%D8%A7%D9%87%D8%A8#Arabic), [لولا](https://en.wiktionary.org/wiki/%D9%84%D9%88%D9%84%D8%A7#Arabic), [كأس](https://en.wiktionary.org/wiki/%D9%83%D8%A3%D8%B3#Arabic), [ثابت](https://en.wiktionary.org/wiki/%D8%AB%D8%A7%D8%A8%D8%AA#Arabic), [دار](https://en.wiktionary.org/wiki/%D8%AF%D8%A7%D8%B1#Arabic), [سوق](https://en.wiktionary.org/wiki/%D8%B3%D9%88%D9%82#Arabic), [سيدة](https://en.wiktionary.org/wiki/%D8%B3%D9%8A%D8%AF%D8%A9#Arabic), [سيد](https://en.wiktionary.org/wiki/%D8%B3%D9%8A%D8%AF#Arabic), [قاطع](https://en.wiktionary.org/wiki/%D9%82%D8%A7%D8%B7%D8%B9#Arabic), [ذو](https://en.wiktionary.org/wiki/%D8%B0%D9%88#Arabic), [سوى](https://en.wiktionary.org/wiki/%D8%B3%D9%88%D9%89#Arabic), [عال](https://en.wiktionary.org/wiki/%D8%B9%D8%A7%D9%84#Arabic), [محام](https://en.wiktionary.org/wiki/%D9%85%D8%AD%D8%A7%D9%85#Arabic), [هدية](https://en.wiktionary.org/wiki/%D9%87%D8%AF%D9%8A%D8%A9#Arabic), [صحراء](https://en.wiktionary.org/wiki/%D8%B5%D8%AD%D8%B1%D8%A7%D8%A1#Arabic), [يد](https://en.wiktionary.org/wiki/%D9%8A%D8%AF#Arabic), [ليلة](https://en.wiktionary.org/wiki/%D9%84%D9%8A%D9%84%D8%A9#Arabic), [حصة](https://en.wiktionary.org/wiki/%D8%AD%D8%B5%D8%A9#Arabic), [وسط](https://en.wiktionary.org/wiki/%D9%88%D8%B3%D8%B7#Arabic), [جمل](https://en.wiktionary.org/wiki/%D8%AC%D9%85%D9%84#Arabic), [أذن](https://en.wiktionary.org/wiki/%D8%A3%D8%B0%D9%86#Arabic), [ريح](https://en.wiktionary.org/wiki/%D8%B1%D9%8A%D8%AD#Arabic), [رجل](https://en.wiktionary.org/wiki/%D8%B1%D8%AC%D9%84#Arabic), [فنجان](https://en.wiktionary.org/wiki/%D9%81%D9%86%D8%AC%D8%A7%D9%86#Arabic), [مطبخ](https://en.wiktionary.org/wiki/%D9%85%D8%B7%D8%A8%D8%AE#Arabic), [حقيبة](https://en.wiktionary.org/wiki/%D8%AD%D9%82%D9%8A%D8%A8%D8%A9#Arabic), [حبيب](https://en.wiktionary.org/wiki/%D8%AD%D8%A8%D9%8A%D8%A8#Arabic), [عشاء](https://en.wiktionary.org/wiki/%D8%B9%D8%B4%D8%A7%D8%A1#Arabic), [غداء](https://en.wiktionary.org/wiki/%D8%BA%D8%AF%D8%A7%D8%A1#Arabic), [طقس](https://en.wiktionary.org/wiki/%D8%B7%D9%82%D8%B3#Arabic), [صف](https://en.wiktionary.org/wiki/%D8%B5%D9%81#Arabic), [خط](https://en.wiktionary.org/wiki/%D8%AE%D8%B7#Arabic), [لهجة](https://en.wiktionary.org/wiki/%D9%84%D9%87%D8%AC%D8%A9#Arabic), [عامية](https://en.wiktionary.org/wiki/%D8%B9%D8%A7%D9%85%D9%8A%D8%A9#Arabic), [فصحى](https://en.wiktionary.org/wiki/%D9%81%D8%B5%D8%AD%D9%89#Arabic), [عين](https://en.wiktionary.org/wiki/%D8%B9%D9%8A%D9%86#Arabic), [بيت](https://en.wiktionary.org/wiki/%D8%A8%D9%8A%D8%AA#Arabic), [صفر](https://en.wiktionary.org/wiki/%D8%B5%D9%81%D8%B1#Arabic), [رقم](https://en.wiktionary.org/wiki/%D8%B1%D9%82%D9%85#Arabic)

**Wiktionary (en), lot 3** : [تشرفنا](https://en.wiktionary.org/wiki/%D8%AA%D8%B4%D8%B1%D9%81%D9%86%D8%A7#Arabic), [مبروك](https://en.wiktionary.org/wiki/%D9%85%D8%A8%D8%B1%D9%88%D9%83#Arabic), [تعال](https://en.wiktionary.org/wiki/%D8%AA%D8%B9%D8%A7%D9%84#Arabic), [كمبيوتر](https://en.wiktionary.org/wiki/%D9%83%D9%85%D8%A8%D9%8A%D9%88%D8%AA%D8%B1#Arabic), [تلفاز](https://en.wiktionary.org/wiki/%D8%AA%D9%84%D9%81%D8%A7%D8%B2#Arabic), [كيلو](https://en.wiktionary.org/wiki/%D9%83%D9%8A%D9%84%D9%88#Arabic), امتلأ (pas de page — voir recherche web), [افتتاح](https://en.wiktionary.org/wiki/%D8%A7%D9%81%D8%AA%D8%AA%D8%A7%D8%AD#Arabic), [اصطدم](https://en.wiktionary.org/wiki/%D8%A7%D8%B5%D8%B7%D8%AF%D9%85#Arabic), [مزدحم](https://en.wiktionary.org/wiki/%D9%85%D8%B2%D8%AF%D8%AD%D9%85#Arabic), [تقابل](https://en.wiktionary.org/wiki/%D8%AA%D9%82%D8%A7%D8%A8%D9%84#Arabic), [تناول](https://en.wiktionary.org/wiki/%D8%AA%D9%86%D8%A7%D9%88%D9%84#Arabic), [سلم](https://en.wiktionary.org/wiki/%D8%B3%D9%84%D9%85#Arabic), [ظن](https://en.wiktionary.org/wiki/%D8%B8%D9%86#Arabic), [نشاط](https://en.wiktionary.org/wiki/%D9%86%D8%B4%D8%A7%D8%B7#Arabic), [قادم](https://en.wiktionary.org/wiki/%D9%82%D8%A7%D8%AF%D9%85#Arabic), [عالمي](https://en.wiktionary.org/wiki/%D8%B9%D8%A7%D9%84%D9%85%D9%8A#Arabic), [مجتهد](https://en.wiktionary.org/wiki/%D9%85%D8%AC%D8%AA%D9%87%D8%AF#Arabic), [مجاني](https://en.wiktionary.org/wiki/%D9%85%D8%AC%D8%A7%D9%86%D9%8A#Arabic), [سكان](https://en.wiktionary.org/wiki/%D8%B3%D9%83%D8%A7%D9%86#Arabic), [معرض](https://en.wiktionary.org/wiki/%D9%85%D8%B9%D8%B1%D8%B6#Arabic), [مجلس](https://en.wiktionary.org/wiki/%D9%85%D8%AC%D9%84%D8%B3#Arabic), [ملعب](https://en.wiktionary.org/wiki/%D9%85%D9%84%D8%B9%D8%A8#Arabic), [لعل](https://en.wiktionary.org/wiki/%D9%84%D8%B9%D9%84#Arabic), [ليت](https://en.wiktionary.org/wiki/%D9%84%D9%8A%D8%AA#Arabic), [بلى](https://en.wiktionary.org/wiki/%D8%A8%D9%84%D9%89#Arabic), [قط](https://en.wiktionary.org/wiki/%D9%82%D8%B7#Arabic), [عندما](https://en.wiktionary.org/wiki/%D8%B9%D9%86%D8%AF%D9%85%D8%A7#Arabic), [لذلك](https://en.wiktionary.org/wiki/%D9%84%D8%B0%D9%84%D9%83#Arabic), [أما](https://en.wiktionary.org/wiki/%D8%A3%D9%85%D8%A7#Arabic), [مستعمل](https://en.wiktionary.org/wiki/%D9%85%D8%B3%D8%AA%D8%B9%D9%85%D9%84#Arabic), [مفيد](https://en.wiktionary.org/wiki/%D9%85%D9%81%D9%8A%D8%AF#Arabic), [قطع](https://en.wiktionary.org/wiki/%D9%82%D8%B7%D8%B9#Arabic), [مسافر](https://en.wiktionary.org/wiki/%D9%85%D8%B3%D8%A7%D9%81%D8%B1#Arabic), [صباح النور](https://en.wiktionary.org/wiki/%D8%B5%D8%A8%D8%A7%D8%AD_%D8%A7%D9%84%D9%86%D9%88%D8%B1#Arabic), [تصبح على خير](https://en.wiktionary.org/wiki/%D8%AA%D8%B5%D8%A8%D8%AD_%D8%B9%D9%84%D9%89_%D8%AE%D9%8A%D8%B1#Arabic)

**Wiktionary (en), compléments** : [كيلوغرام](https://en.wiktionary.org/wiki/%D9%83%D9%8A%D9%84%D9%88%D8%BA%D8%B1%D8%A7%D9%85#Arabic), [ملأ](https://en.wiktionary.org/wiki/%D9%85%D9%84%D8%A3#Arabic), [اللغة العربية الفصحى](https://en.wiktionary.org/wiki/%D8%A7%D9%84%D9%84%D8%BA%D8%A9_%D8%A7%D9%84%D8%B9%D8%B1%D8%A8%D9%8A%D8%A9_%D8%A7%D9%84%D9%81%D8%B5%D8%AD%D9%89#Arabic), [العامية](https://en.wiktionary.org/wiki/%D8%A7%D9%84%D8%B9%D8%A7%D9%85%D9%8A%D8%A9#Arabic) ; [Ammiyya](https://en.wiktionary.org/wiki/Ammiyya)

**Recherche web** :
- قَاطِع (« رفض قاطع » = refus catégorique) : [almaany — الرفض القاطع](https://www.almaany.com/ar/dict/ar-en/%D8%A7%D9%84%D8%B1%D9%81%D8%B6-%D8%A7%D9%84%D9%82%D8%A7%D8%B7%D8%B9/), [almaany — رفضه رفضا قاطعا](https://www.almaany.com/ar/dict/ar-en/%D8%B1%D9%81%D8%B6%D9%87-%D8%B1%D9%81%D8%B6%D8%A7-%D9%82%D8%A7%D8%B7%D8%B9%D8%A7/), [Reverso — رفضا قاطعا](https://context.reverso.net/translation/arabic-english/%D8%B1%D9%81%D8%B6%D8%A7+%D9%82%D8%A7%D8%B7%D8%B9%D8%A7), [almaany — رفض](https://www.almaany.com/en/dict/ar-en/%D8%B1%D9%81%D8%B6/)
- اِمْتَلَأَ (forme VIII, « être rempli ») : [almaany — امتلأ](https://www.almaany.com/en/dict/ar-en/%D8%A7%D9%85%D8%AA%D9%84%D8%A3/), [bab.la — امْتَلَأَ](https://en.bab.la/dictionary/arabic-english/%D8%A7%D9%85%D8%AA%D9%84%D8%A7), [Quranic Arabic Corpus — racine m-l-ʾ](https://corpus.quran.com/qurandictionary.jsp?q=mlA)
- العَامِّيَّة (arabe dialectal) : [Wiktionary — Ammiyya](https://en.wiktionary.org/wiki/Ammiyya), [Wikipedia — Amiyah](https://en.wikipedia.org/wiki/Amiyah), [العامية](https://en.wiktionary.org/wiki/%D8%A7%D9%84%D8%B9%D8%A7%D9%85%D9%8A%D8%A9)

Reverso et almaany n'ont été lus qu'à travers les extraits renvoyés par la recherche web.

## Sources indisponibles

- WordReference, Reverso, Collins : non lus directement (refus de lecture automatique) ; Reverso et
  almaany cités par les extraits de recherche web seulement (قَاطِع, اِمْتَلَأَ).
- Python 3.8 refuse le certificat de en.wiktionary.org : lecture faite par `curl`.
