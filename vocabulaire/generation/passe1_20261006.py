#!/usr/bin/env python3
"""Passe 1 de la vérification du vocabulaire (2026-10-06) — application unique.

Relecture intégrale des 498 sens, colonne arabe puis colonne française, selon
`Documentation/regles_vocabulaire.md`. Ce script réécrit les blocs `=== VOCA` des
sources au format à 11 colonnes de `gen.py` :

    mots ar | traductions fr | cats | niveau | fréquence | étiquettes | registre | contexte | référence | trad | pluriel

Il est gardé comme trace des décisions (voir `verification_20261006.md`) ; il refuse
de tourner deux fois (les lignes d'origine n'existent plus).
"""
from __future__ import annotations
import re
import glob

# Réécriture complète d'une entrée : clé = mot vocalisé de l'ancienne ligne.
# Liste vide = entrée supprimée (fusionnée dans une autre).
R = {
    # --- ch. 1-3
    "بَاب": ["بَاب | porte:f | noun, mas | niv-a1 | freq-tres | habitation | | | | | أَبْوَاب"],
    "دَار": ["دَار | demeure:f | noun, fem | niv-a2 | freq-tres | logement | | | | | دُور"],
    "طَبِيب": ["طَبِيب | médecin:m | noun, mas | niv-a1 | freq-tres | metier, sante | | | | | أَطِبَّاء"],
    "ظَهْر": ["ظَهْر | dos:m | noun, mas | niv-a2 | freq-freq | corps | | جِسْم"],
    "ضَيْف": ["ضَيْف | invité:m | noun, mas | niv-a2 | freq-freq | relation | | | | | ضُيُوف"],
    "كِتَاب": ["كِتَاب | livre [ouvrage]:m | noun, mas | niv-a1 | freq-ultra | langue-ecrit | | | | | كُتُب"],
    "بَيْت": ["بَيْت | maison:f | noun, mas | niv-a1 | freq-ultra | logement | | مَسْكَن | | | بُيُوت"],
    "لَا": ["لَا | non | particle | niv-a1 | freq-ultra | communication-orale | | جَوَاب"],
    "وَزِير": ["وَزِير | ministre:m | noun, mas | niv-b1 | freq-freq | institution, metier | | | | | وُزَرَاء"],
    "بَلَد": ["بَلَد | pays:m | noun, mas | niv-a1 | freq-tres | geographie | | | | | بُلْدَان"],
    "قَلَم": ["قَلَم | stylo:m; crayon:m | noun, mas | niv-a1 | freq-tres | ecole, objet | | | | | أَقْلَام"],
    "وَلَد": ["وَلَد | garçon [enfant]:m | noun, mas | niv-a1 | freq-tres | famille | | | | | أَوْلَاد"],
    "سُوق": ["سُوق | marché [lieu de vente]:m | noun, fem | niv-a1 | freq-tres | commerce, ville | | | | | أَسْوَاق"],
    "عَفْوًا": [
        "عَفْوًا | de rien | interj | niv-a1 | freq-tres | communication-orale | | رَدّ الشُّكْر",
        "عَفْوًا | pardon | interj | niv-a1 | freq-tres | communication-orale | | اِعْتِذَار"],
    "دَرَّسَ": ["دَرَّسَ | enseigner | verb, verb-trans, verb-derived | niv-a2 | freq-freq | ecole | | | | fr-FR§une matière, comme professeur"],
    "رَئِيس": ["رَئِيس | président:m; chef [dirigeant]:m | noun, mas | niv-a2 | freq-tres | institution | | | | | رُؤَسَاء"],
    "مَدْرَسَة": ["مَدْرَسَة | école:f | noun, fem | niv-a1 | freq-ultra | ecole, batiment | | | | | مَدَارِس"],
    "مُسْتَشْفَى": ["مُسْتَشْفَى | hôpital:m | noun, mas | niv-a1 | freq-tres | sante, batiment | | | | | مُسْتَشْفَيَات"],
    "مَعْنَى": ["مَعْنَى | sens [signification]:m; signification:f | noun, mas | niv-a2 | freq-tres | langue-ecrit | | | | | مَعَانٍ"],
    "الـ": ["الـ | le [article]; la [article]; les [article] | det | niv-a1 | freq-ultra | | | | al-"],
    "رَجُل": ["رَجُل | homme [adulte]:m | noun, mas | niv-a1 | freq-ultra | personne | | | | | رِجَال"],
    "جَدِيد": ["جَدِيد | nouveau; neuf [récent] | adj | niv-a1 | freq-ultra | qualite"],
    # --- ch. 4 : formules
    "السَّلَامُ عَلَيْكُمْ": [
        "السَّلَامُ عَلَيْكُمْ | bonjour | locution, interj | niv-a1 | freq-ultra | communication-orale | | | | fr-FR§à toute heure, formule universelle",
        "وَعَلَيْكُمُ السَّلَامُ | bonjour | locution, interj | niv-a1 | freq-ultra | communication-orale | | | | fr-FR§réponse à as-salāmu ʿalaykum"],
    "مَرْحَبًا": ["مَرْحَبًا | salut; bonjour | interj | niv-a1 | freq-tres | communication-orale | | | | fr-FR§familier"],
    "مَعَ السَّلَامَةِ": ["مَعَ السَّلَامَةِ ; إِلَى اللِّقَاءِ | au revoir | locution, interj | niv-a1 | freq-tres | communication-orale"],
    "إِلَى اللِّقَاءِ": [],
    "صَبَاحُ الخَيْرِ": [
        "صَبَاحُ الخَيْرِ | bonjour | locution, interj | niv-a1 | freq-tres | communication-orale | | | | fr-FR§le matin",
        "صَبَاحُ النُّورِ | bonjour | locution, interj | niv-a1 | freq-tres | communication-orale | | | | fr-FR§réponse, le matin"],
    "مَسَاءُ الخَيْرِ": [
        "مَسَاءُ الخَيْرِ | bonsoir | locution, interj | niv-a1 | freq-tres | communication-orale",
        "مَسَاءُ النُّورِ | bonsoir | locution, interj | niv-a1 | freq-tres | communication-orale | | | | fr-FR§réponse",
        "تُصْبِحُ عَلَى خَيْرٍ | bonne nuit | locution, interj | niv-a1 | freq-freq | communication-orale | | | | fr-FR§à un homme"],
    "خَيْر": ["خَيْر | bien [bonté]:m | noun, mas | niv-a2 | freq-tres | qualite | | ضِدّ الشَّرّ"],
    "اِسْم": ["اِسْم | nom [d'une personne]:m; prénom:m | noun, mas | niv-a1 | freq-ultra | personne | | لِشَخْص | | | أَسْمَاء"],
    "مِنْ فَضْلِكَ": ["مِنْ فَضْلِكَ | s'il te plaît; s'il vous plaît | locution | niv-a1 | freq-tres | communication-orale | | | | fr-FR§à un homme"],
    "لَوْ سَمَحْتَ": ["لَوْ سَمَحْتَ | si tu permets; excusez-moi | locution | niv-a1 | freq-tres | communication-orale | | | | fr-FR§à un homme"],
    "قَهْوَة": [
        "قَهْوَة | café [boisson]:m | noun, fem | niv-a1 | freq-tres | boisson",
        "شُكْرًا جَزِيلًا | merci beaucoup | locution, interj | niv-a1 | freq-tres | communication-orale"],
    "حَال": [
        "حَال | état [situation]:m | noun, mas | niv-a1 | freq-tres | etat | | | | | أَحْوَال",
        "كَيْفَ حَالُكَ | comment vas-tu | locution, question | niv-a1 | freq-ultra | communication-orale | | | | fr-FR§à un homme"],
    # --- ch. 5 : pronoms (contexte de traduction, pas de contexte principal de secours)
    "أَنْتَ": ["أَنْتَ | tu; toi | pron | niv-a1 | freq-ultra | personne | | | | fr-FR§à un homme"],
    "أَنْتِ": ["أَنْتِ | tu; toi | pron | niv-a1 | freq-ultra | personne | | | | fr-FR§à une femme"],
    "طَالِب": ["طَالِب | étudiant:m; élève:m | noun, mas | niv-a1 | freq-tres | ecole, personne | | دِرَاسَة | | | طُلَّاب"],
    "أَنْتُمْ": ["أَنْتُمْ | vous | pron | niv-a1 | freq-tres | personne | | | | fr-FR§à des hommes, ou à un groupe mixte"],
    "أَنْتُنَّ": ["أَنْتُنَّ | vous | pron | niv-a2 | freq-peu | personne | | | | fr-FR§à des femmes"],
    "مُهَنْدِس": ["مُهَنْدِس | ingénieur:m | noun, mas | niv-a1 | freq-freq | metier | | | | | مُهَنْدِسُون"],
    "غُرْفَة": ["غُرْفَة | pièce [maison]:f; chambre [maison]:f | noun, fem | niv-a1 | freq-tres | piece | | | | | غُرَف"],
    "مُعَلِّم": ["مُعَلِّم | instituteur:m; maître d'école:m | noun, mas | niv-a1 | freq-tres | metier, ecole | | | | | مُعَلِّمُون"],
    "اِمْرَأَة": ["اِمْرَأَة | femme [adulte]:f | noun, fem | niv-a1 | freq-tres | personne | | | | | نِسَاء"],
    "أَرْض": ["أَرْض | terre:f; sol:m | noun, fem | niv-a1 | freq-tres | geographie | | | | | أَرَاضٍ"],
    "نَار": ["نَار | feu [flamme]:m | noun, fem | niv-a2 | freq-freq | nature"],
    "عَيْن": ["عَيْن | œil:m | noun, fem | niv-a1 | freq-tres | corps | | لِلنَّظَر | | | عُيُون:yeux"],
    "رِجْل": ["رِجْل | jambe:f | noun, fem | niv-a1 | freq-freq | corps | | | | | أَرْجُل"],
    "يَد": ["يَد | main:f | noun, fem | niv-a1 | freq-tres | corps | | | | | أَيْدٍ"],
    "مُوَظَّف": ["مُوَظَّف | employé:m; fonctionnaire:m | noun, mas | niv-a1 | freq-tres | travail, metier | | | | | مُوَظَّفُون"],
    "مُسْلِم": ["مُسْلِم | musulman:m | noun, mas | niv-a2 | freq-tres | religion | | | | | مُسْلِمُون"],
    "مَطَار": ["مَطَار | aéroport:m | noun, mas | niv-a1 | freq-tres | transport, voyage | | | | | مَطَارَات"],
    "عِنْدَ": ["عِنْدَ | chez | prep | niv-a1 | freq-ultra | echange"],
    "مَكْتَبَة": ["مَكْتَبَة | bibliothèque:f; librairie:f | noun, fem | niv-a1 | freq-tres | langue-ecrit, batiment | | | | | مَكْتَبَات"],
    "كَثِير": ["كَثِير | nombreux | adj | niv-a1 | freq-ultra | quantite"],
    "مَكْتَب": ["مَكْتَب | bureau [lieu de travail]:m | noun, mas | niv-a1 | freq-tres | travail | | | | | مَكَاتِب"],
    "مَسْجِد": ["مَسْجِد | mosquée:f | noun, mas | niv-a1 | freq-tres | religion, batiment | | | | | مَسَاجِد"],
    "طَوِيل": ["طَوِيل | long | adj | niv-a1 | freq-tres | dimension"],
    "صَفّ": ["صَفّ | classe [salle]:f | noun, mas | niv-a1 | freq-tres | ecole | | مَدْرَسَة | | | صُفُوف"],
    "عَرَبِيّ": ["عَرَبِيّ | arabe | adj, nisba | niv-a1 | freq-ultra | nationalite"],
    "تَارِيخ": ["تَارِيخ | histoire [passé]:f | noun, mas | niv-a2 | freq-tres | temps | | المَاضِي"],
    "هٰذَا": ["هٰذَا | ceci; celui-ci | pron | niv-a1 | freq-ultra | | | | hādhā | fr-FR§masculin"],
    "هٰذِهِ": ["هٰذِهِ | ceci; celle-ci | pron | niv-a1 | freq-ultra | | | | hādhihi | fr-FR§féminin, ou pluriel de choses"],
    "ذٰلِكَ": ["ذٰلِكَ | cela; celui-là | pron | niv-a1 | freq-ultra | | | | dhalika | fr-FR§masculin"],
    "تِلْكَ": ["تِلْكَ | cela; celle-là | pron | niv-a1 | freq-tres | | | | tilka | fr-FR§féminin, ou pluriel de choses"],
    "بَعِيد": ["بَعِيد | lointain; éloigné | adj | niv-a1 | freq-tres | lieu"],
    "قَرِيب": ["قَرِيب | proche | adj | niv-a1 | freq-tres | lieu"],
    "كُرَةُ القَدَمِ": [
        "كُرَةُ القَدَمِ | football:m | locution, noun | niv-a1 | freq-freq | sport",
        "قَدَم | pied:m | noun, fem | niv-a1 | freq-tres | corps | | | | | أَقْدَام"],
    "جَامِعَة": ["جَامِعَة | université:f | noun, fem | niv-a1 | freq-tres | ecole, batiment | | | | | جَامِعَات"],
    "مَطْبَخ": ["مَطْبَخ | cuisine [pièce]:f | noun, mas | niv-a1 | freq-freq | piece, repas | | | | | مَطَابِخ"],
    "مُحَامٍ": ["مُحَامٍ | avocat [juriste]:m | noun, mas | niv-a2 | freq-freq | metier, droit | | | | | مُحَامُون"],
    "عَنْ": ["عَنْ | au sujet de; à propos de | prep | niv-a2 | freq-ultra | communication"],
    "حَقِيبَة": ["حَقِيبَة | sac:m; valise:f | noun, fem | niv-a1 | freq-tres | objet, voyage | | | | | حَقَائِب"],
    "خَلْفَ": ["خَلْفَ ; وَرَاءَ | derrière | prep | niv-a1 | freq-tres | lieu"],
    "قِطَّة": ["قِطَّة | chatte:f; chat:m | noun, fem | niv-a1 | freq-freq | animal | | | | | قِطَط"],
    "بَنْك": ["بَنْك | banque:f | noun, mas, loanword | niv-a1 | freq-freq | argent, batiment | | | | | بُنُوك"],
    "هُنَاكَ": [
        "هُنَاكَ | là-bas | adv | niv-a1 | freq-ultra | lieu | | مَكَان",
        "هُنَاكَ | il y a::locution, verb | adv | niv-a1 | freq-ultra | | | وُجُود"],
    "مَطْعَم": ["مَطْعَم | restaurant:m | noun, mas | niv-a1 | freq-tres | commerce, repas | | | | | مَطَاعِم"],
    "هَلْ": ["هَلْ | est-ce que | particle | niv-a1 | freq-ultra | communication"],
    "بَلَى": ["بَلَى | si [réponse] | particle | niv-b1 | freq-peu | communication-orale | reg-soutenu"],
    "مَنْ": ["مَنْ | qui [interrogatif] | pron | niv-a1 | freq-ultra | communication | | اِسْتِفْهَام"],
    "مَا": ["مَا | que [interrogatif]; quoi | pron | niv-a1 | freq-ultra | communication | | اِسْتِفْهَام | | fr-FR§devant un nom"],
    "مَاذَا": ["مَاذَا | que [interrogatif]; quoi | pron | niv-a1 | freq-ultra | communication | | | | fr-FR§devant un verbe"],
    "مَتَى": ["مَتَى | quand | adv | niv-a1 | freq-tres | moment"],
    "مَحَطَّة": ["مَحَطَّة | gare:f; station:f | noun, fem | niv-a1 | freq-tres | transport | | | | | مَحَطَّات"],
    "سَنَة": ["سَنَة | année:f; an:m | noun, fem | niv-a1 | freq-ultra | calendrier, duree | | | | | سَنَوَات"],
    "مِائَة": ["مِائَة ; مِئَة | cent | num | niv-a1 | freq-tres | nombre"],
    "دُولَار": ["دُولَار | dollar:m | noun, mas, loanword | niv-a1 | freq-freq | argent | | | | | دُولَارَات"],
    "أُسْبُوع": ["أُسْبُوع | semaine:f | noun, mas | niv-a1 | freq-tres | calendrier, duree | | | | | أَسَابِيع"],
    "سَاعَة": [
        "سَاعَة | heure:f | noun, fem | niv-a1 | freq-ultra | duree | | زَمَن | | | سَاعَات",
        "سَاعَة | montre:f | noun, fem | niv-a1 | freq-freq | objet | | يَد"],
    "خَرَجَ": ["خَرَجَ | sortir [d'un lieu] | verb, verb-intrans | niv-a1 | freq-ultra | deplacement"],
    "قَدْ": ["قَدْ | déjà | particle | niv-b1 | freq-ultra | moment | | مَعَ المَاضِي"],
    "وَصَلَ": ["وَصَلَ | arriver [quelque part] | verb, verb-intrans | niv-a1 | freq-tres | deplacement"],
    "قِطَار": ["قِطَار | train:m | noun, mas | niv-a1 | freq-tres | transport, voyage | | | | | قِطَارَات"],
    "سَمِعَ": ["سَمِعَ | entendre | verb, verb-trans | niv-a1 | freq-ultra | perception"],
    "حَدِيقَة": ["حَدِيقَة | jardin:m; parc:m | noun, fem | niv-a1 | freq-tres | vegetal, ville | | | | | حَدَائِق"],
    "لَمْ": ["لَمْ | ne… pas::locution, adv | particle | niv-a2 | freq-ultra | | | | lam | fr-FR§au passé"],
    "قَطُّ": ["قَطُّ | jamais | adv | niv-b1 | freq-freq | frequence | | | | fr-FR§dans le passé, après une négation"],
    "أَبَدًا": ["أَبَدًا | jamais | adv | niv-a2 | freq-tres | frequence | | | | fr-FR§au présent ou au futur"],
    "غَيْر": ["غَيْر | autre que | noun | niv-b1 | freq-ultra | qualite"],
    "صَحِيح": ["صَحِيح | exact; correct | adj | niv-a1 | freq-tres | qualite"],
    "كَانَ": ["كَانَ | être | verb, verb-intrans | niv-a1 | freq-ultra | etat | | | | fr-FR§au passé"],
    "جَوّ": ["طَقْس ; جَوّ [طَقْس] | temps [météo]:m | noun, mas | niv-a1 | freq-tres | meteo"],
    "طَقْس": ["طَقْس ; جَوّ [طَقْس] | temps [météo]:m | noun, mas | niv-a1 | freq-tres | meteo"],
    "عِنْدَمَا": ["عِنْدَمَا | quand; lorsque | conj | niv-a2 | freq-tres | moment"],
    "صَارَ": ["صَارَ ; أَصْبَحَ +verb-derived | devenir | verb, verb-intrans | niv-b1 | freq-tres | etat"],
    "أَصْبَحَ": [],
    "مَا زَالَ": ["مَا زَالَ | être encore | locution, verb | niv-b1 | freq-tres | duree"],
    "عَمِلَ": ["عَمِلَ | travailler | verb, verb-intrans | niv-a1 | freq-ultra | travail"],
    "إِنَّ": ["إِنَّ | certes | particle | niv-b1 | freq-ultra | | | | inna"],
    "مُجْتَهِد": ["مُجْتَهِد | studieux; assidu | adj | niv-a2 | freq-freq | caractere"],
    "أَنَّ": ["أَنَّ | que [conjonction] | conj | niv-b1 | freq-ultra | | | | anna | fr-FR§devant un nom ou un pronom"],
    "لَعَلَّ": ["لَعَلَّ | peut-être::adv | particle | niv-b1 | freq-freq | pensee"],
    "لَيْتَ": ["لَيْتَ | si seulement::locution, adv | particle | niv-b2 | freq-peu | volonte | reg-soutenu"],
    "سَوْفَ": ["سَوْفَ | marque du futur::particle, defi | particle | niv-a2 | freq-tres | moment"],
    "لَنْ": ["لَنْ | ne… pas::locution, adv | particle | niv-b1 | freq-tres | | | | lan | fr-FR§au futur"],
    "أَنْ": ["أَنْ | que [conjonction] | conj | niv-a2 | freq-ultra | | | | an | fr-FR§devant un verbe"],
    "حَتَّى": ["حَتَّى | jusqu'à ce que::locution, conj | conj | niv-a2 | freq-ultra | moment | | غَايَة"],
    "جَاءَ": ["جَاءَ ; أَتَى @reg-soutenu | venir | verb, verb-intrans | niv-a1 | freq-ultra | deplacement"],
    "أَتَى": ["جَاءَ ; أَتَى @reg-soutenu | venir | verb, verb-intrans | niv-a1 | freq-ultra | deplacement"],
    "سَفَر": ["سَفَر | voyage:m | noun, mas, masdar | niv-a1 | freq-tres | voyage | | | | | أَسْفَار"],
    "تَعَالَ": ["تَعَالَ | viens | interj | niv-a1 | freq-tres | deplacement | | | | fr-FR§à un homme"],
    "رَجَا": ["رَجَا | prier [demander] | verb, verb-trans | niv-b1 | freq-freq | volonte | reg-soutenu"],
    "قَلِيل": ["قَلِيل | peu nombreux | adj | niv-a1 | freq-tres | quantite"],
    "مُدَرِّس": ["مُدَرِّس | professeur:m | noun, mas | niv-a1 | freq-tres | metier, ecole | | | | fr-FR§dans l'enseignement scolaire | مُدَرِّسُون"],
    "دِرَاسَة": ["دِرَاسَة | études:fpl | noun, fem, masdar | niv-a2 | freq-tres | ecole"],
    "جِذْر": ["جِذْر | racine [d'un mot]:f | noun, mas | niv-b1 | freq-freq | langue-ecrit | | لُغَة | | | جُذُور"],
    "لَاعِب": ["لَاعِب | joueur:m | noun, mas | niv-a1 | freq-freq | sport, personne | | | | | لَاعِبُون"],
    "خَبَّاز": ["خَبَّاز | boulanger:m | noun, mas | niv-a2 | freq-peu | metier, aliment"],
    "اِسْتِقْبَال": ["اِسْتِقْبَال | accueil:m | noun, mas, masdar | niv-b1 | freq-tres | echange"],
    "هَاتِف": ["هَاتِف | téléphone:m | noun, mas | niv-a1 | freq-tres | communication, objet | | | | | هَوَاتِف"],
    "حَاسُوب": ["حَاسُوب ; كُمْبِيُوتَر +loanword | ordinateur:m | noun, mas | niv-a2 | freq-freq | objet | | | | | حَوَاسِيب"],
    "عَلَّمَ": ["عَلَّمَ | enseigner; apprendre [à quelqu'un] | verb, verb-trans, verb-derived | niv-a2 | freq-tres | ecole | | | | fr-FR§à quelqu'un"],
    "فَكَّرَ": ["فَكَّرَ | réfléchir; penser | verb, verb-intrans, verb-derived | niv-a2 | freq-tres | pensee"],
    "كَأْس": ["كَأْس | verre [à boire]:m | noun, fem | niv-a1 | freq-freq | objet, boisson | | لِلشُّرْب | | | كُؤُوس"],
    "شَاهَدَ": ["شَاهَدَ | regarder | verb, verb-trans, verb-derived | niv-a1 | freq-tres | perception"],
    "تِلْفَاز": ["تِلْفَاز | télévision:f | noun, mas, loanword | niv-a1 | freq-freq | media, objet"],
    "فِيلْم": ["فِيلْم | film:m | noun, mas, loanword | niv-a1 | freq-freq | art, media | | | | | أَفْلَام"],
    "أَخْرَجَ": ["أَخْرَجَ | sortir [quelque chose]; faire sortir | verb, verb-trans, verb-derived | niv-b1 | freq-freq | geste"],
    "عَمَل": ["عَمَل | travail:m | noun, mas, masdar | niv-a1 | freq-ultra | travail | | | | | أَعْمَال:travaux"],
    "تَعَلَّمَ": ["تَعَلَّمَ | apprendre [s'instruire] | verb, verb-trans, verb-derived | niv-a1 | freq-tres | ecole"],
    "اِسْتَمَعَ": ["اِسْتَمَعَ | écouter | verb, verb-intrans, verb-derived | niv-a2 | freq-tres | perception"],
    "اِسْتَعْمَلَ": ["اِسْتَعْمَلَ ; اِسْتَخْدَمَ | utiliser; employer | verb, verb-trans, verb-derived | niv-a2 | freq-tres | action"],
    "اِسْتَخْدَمَ": [],
    "وَقَفَ": ["وَقَفَ | s'arrêter | verb, verb-intrans | niv-a2 | freq-tres | geste"],
    "زَارَ": ["زَارَ | visiter; rendre visite | verb, verb-trans | niv-a1 | freq-tres | voyage"],
    "عَادَ": ["عَادَ ; رَجَعَ | revenir; rentrer | verb, verb-intrans | niv-a2 | freq-tres | deplacement"],
    "رَجَعَ": ["عَادَ ; رَجَعَ | revenir; rentrer | verb, verb-intrans | niv-a2 | freq-tres | deplacement"],
    "دَعَا": ["دَعَا | inviter | verb, verb-trans | niv-a2 | freq-tres | relation | | لِلضِّيَافَة"],
    "مَشَى": ["مَشَى | marcher [à pied] | verb, verb-intrans | niv-a1 | freq-tres | deplacement"],
    "رَدَّ": ["رَدَّ | répondre | verb, verb-trans | niv-a2 | freq-tres | communication"],
    "ظَنَّ": ["ظَنَّ | croire; supposer | verb, verb-trans | niv-b1 | freq-tres | pensee"],
    "سَأَلَ": ["سَأَلَ | demander [une question]; interroger | verb, verb-trans | niv-a1 | freq-tres | communication"],
    "جَرِيدَة": ["جَرِيدَة | journal [presse]:m | noun, fem | niv-a1 | freq-freq | media | | | | | جَرَائِد"],
    "دُخُول": ["دُخُول | entrée [action d'entrer]:f | noun, mas, masdar | niv-a2 | freq-tres | deplacement"],
    "خُرُوج": ["خُرُوج | sortie [action de sortir]:f | noun, mas, masdar | niv-a2 | freq-tres | deplacement"],
    "ذَاهِب": ["ذَاهِب | allant | adj | niv-a2 | freq-freq | deplacement"],
    "مُسَاعِد": ["مُسَاعِد | assistant:m; adjoint:m | noun, mas | niv-b1 | freq-freq | travail | | | | | مُسَاعِدُون"],
    "مِكْنَسَة": ["مِكْنَسَة | balai:m | noun, fem | niv-b1 | freq-peu | objet | | | | | مَكَانِس"],
    "ذُو": ["ذُو | doté de; possesseur de | noun | niv-b2 | freq-freq | qualite | reg-soutenu"],
    "سَلَّمَ": ["سَلَّمَ | saluer | verb, verb-trans, verb-derived | niv-b1 | freq-freq | relation | | عَلَى شَخْص"],
    "مَصْنَع": ["مَصْنَع | usine:f | noun, mas | niv-b1 | freq-freq | travail, batiment | | | | | مَصَانِع"],
    "قَاضٍ": ["قَاضٍ | juge:m | noun, mas | niv-b1 | freq-freq | metier, droit | | | | | قُضَاة"],
    "نَادٍ": ["نَادٍ | club:m | noun, mas | niv-a2 | freq-freq | loisir | | | | | أَنْدِيَة"],
    "الَّذِي": ["الَّذِي | qui [relatif]; que [relatif] | pron | niv-b1 | freq-ultra | | | | alladhi | fr-FR§masculin singulier"],
    "الَّتِي": ["الَّتِي | qui [relatif]; que [relatif] | pron | niv-b1 | freq-ultra | | | | allati | fr-FR§féminin singulier, ou pluriel de choses"],
    "الَّذِينَ": ["الَّذِينَ | qui [relatif]; que [relatif] | pron | niv-b1 | freq-tres | | | | alladhina | fr-FR§masculin pluriel"],
    "أَكْثَر": ["أَكْثَر | plus; davantage::adv | adj | niv-a2 | freq-ultra | quantite"],
    "أَقَلّ": ["أَقَلّ | moins::adv | adj | niv-a2 | freq-tres | quantite"],
    "نَشَاط": ["نَشَاط | activité:f; dynamisme:m | noun, mas, masdar | niv-b1 | freq-tres | action | | | | | أَنْشِطَة"],
    "ثَمَن": ["ثَمَن | prix [coût]:m | noun, mas | niv-a2 | freq-freq | argent, commerce | | | | | أَثْمَان"],
    "طَيِّب": ["طَيِّب | délicieux; bon [au goût] | adj | niv-a2 | freq-tres | qualite"],
    "طَعَام": ["طَعَام | nourriture:f | noun, mas | niv-a1 | freq-tres | aliment | | | | | أَطْعِمَة"],
    "قَرْن": ["قَرْن | siècle:m | noun, mas | niv-b1 | freq-tres | temps | | مِائَة سَنَة | | | قُرُون"],
    "يُوجَدُ": [
        "يُوجَدُ | se trouver; exister | verb | niv-b1 | freq-tres | etat",
        "مَكَان | lieu:m; endroit:m | noun, mas | niv-a1 | freq-ultra | lieu | | | | | أَمَاكِن"],
    "بِنَاء": [
        "بِنَاء | construction:f | noun, mas, masdar | niv-b1 | freq-tres | batiment",
        "اِفْتِتَاح | inauguration:f | noun, mas, masdar | niv-b1 | freq-freq | fete"],
    "إِنْ": ["إِنْ | si [condition] | conj | niv-b1 | freq-tres | | reg-soutenu | | in | fr-FR§condition possible, langue soutenue"],
    "إِذَا": ["إِذَا | si [condition] | conj | niv-a2 | freq-ultra | | | | idha | fr-FR§condition courante"],
    "لَوْ": ["لَوْ | si [condition] | conj | niv-b1 | freq-tres | | | | law | fr-FR§condition irréelle"],
    "لَوْلَا": ["لَوْلَا | n'eût été; sans | conj | niv-b2 | freq-freq | | reg-soutenu | | lawla"],
    "أَسْرَعَ": ["أَسْرَعَ | se dépêcher | verb, verb-intrans, verb-derived | niv-b1 | freq-freq | deplacement"],
    "لَحْم": [
        "لَحْم | viande:f | noun, mas | niv-a1 | freq-tres | aliment | | | | | لُحُوم",
        "كِيلُو | kilo:m | noun, mas, loanword | niv-a1 | freq-freq | quantite",
        "اِمْتَلَأَ | se remplir | verb, verb-intrans, verb-derived | niv-b2 | freq-freq | etat"],
    "شَدِيد": [
        "شَدِيد | intense; violent | adj | niv-a2 | freq-tres | qualite",
        "قَاطِع | catégorique | adj | niv-b2 | freq-freq | qualite"],
    "عِلْم": ["عِلْم | savoir:m; science:f | noun, mas | niv-a2 | freq-tres | ecole | | | | | عُلُوم"],
    "سِوَى": ["سِوَى | sauf; excepté | noun | niv-b2 | freq-freq | | | | siwa | fr-FR§suivi d'un génitif"],
    "إِلَّا": ["إِلَّا | sauf; excepté | particle | niv-b1 | freq-ultra | | | | illa | fr-FR§suivi d'un accusatif"],
    "حَضَرَ": ["حَضَرَ | être présent; assister | verb, verb-intrans | niv-b1 | freq-tres | deplacement"],
    "مُسَافِر": ["مُسَافِر | voyageur:m | noun, mas | niv-a2 | freq-freq | voyage, personne | | | | | مُسَافِرُون"],
    "طَائِرَة": ["طَائِرَة | avion:m | noun, fem | niv-a1 | freq-tres | transport, voyage | | | | | طَائِرَات"],
    "طِفْل": ["طِفْل | enfant:m | noun, mas | niv-a1 | freq-tres | famille, age-etat | | | | | أَطْفَال"],
    "أَمْ": ["أَمْ | ou | conj | niv-b1 | freq-freq | | | | am | fr-FR§dans une question"],
    "أَوْ": ["أَوْ | ou | conj | niv-a1 | freq-ultra | | | | aw"],
    "طَلَبَ": ["طَلَبَ | demander [une chose] | verb, verb-trans | niv-a2 | freq-tres | volonte"],
    "أُسْتَاذ": ["أُسْتَاذ | professeur:m | noun, mas | niv-a1 | freq-tres | metier, ecole | | | | fr-FR§d'université, ou titre de politesse | أَسَاتِذَة"],
    "سَيِّد": ["سَيِّد | monsieur:m | noun, mas | niv-a1 | freq-tres | personne | | | | | سَادَة:messieurs"],
    "سَيِّدَة": ["سَيِّدَة | madame:f; dame:f | noun, fem | niv-a1 | freq-tres | personne | | | | | سَيِّدَات:mesdames; dames"],
    "لَهْجَة": ["لَهْجَة | dialecte:m | noun, fem | niv-b1 | freq-freq | parole | | | | | لَهَجَات"],
    "العَامِّيَّة": ["العَامِّيَّة | arabe dialectal:m | noun, fem | niv-b1 | freq-freq | parole"],
    "خَطّ": ["خَطّ | écriture [calligraphie]:f | noun, mas | niv-b1 | freq-tres | art | | كِتَابَة"],
    "خَلَاص": ["خَلَاص | ça suffit; c'est fini | interj | niv-a2 | freq-freq | communication-orale | reg-familier"],
    "عَقْل": ["عَقْل | esprit [intellect]:m; raison [faculté]:f | noun, mas | niv-b1 | freq-tres | pensee | | | | | عُقُول"],
    "مَا شَاءَ اللّٰهُ": ["مَا شَاءَ اللّٰهُ | formule d'admiration::locution, interj, defi | locution, interj | niv-a2 | freq-tres | religion, communication-orale"],
    "إِنْ شَاءَ اللّٰهُ": ["إِنْ شَاءَ اللّٰهُ | si Dieu le veut | locution, interj | niv-a1 | freq-ultra | religion, communication-orale"],
    "بِسْمِ اللّٰهِ": ["بِسْمِ اللّٰهِ | au nom de Dieu | locution, interj | niv-a1 | freq-tres | religion, communication-orale"],
    "الحَمْدُ لِلَّهِ": ["الحَمْدُ لِلَّهِ | Dieu merci | locution, interj | niv-a1 | freq-ultra | religion, communication-orale"],
    "كَلْب": ["كَلْب | chien:m | noun, mas | niv-a1 | freq-tres | animal | | | | | كِلَاب",
              "فِيل | éléphant:m | noun, mas | niv-a1 | freq-freq | animal | | | | | أَفْيَال"],
}

# Ajouts dans une leçon sans entrée existante à réécrire (ref de leçon → lignes).
AJOUTS = {
    "0005": ["سَلَام | paix:f | noun, mas | niv-a1 | freq-tres | relation"],
    "0159": ["وُلِدَ | naître | verb, verb-intrans | niv-a1 | freq-tres | vie"],
}

# Étiquettes enrichies sans autre changement (thème principal + transverses).
TAGS = {
    "دَرْس": "ecole", "رِسَالَة": "langue-ecrit", "فِنْجَان": "objet, boisson",
    "مِفْتَاح": "objet", "مَتْحَف": "art, batiment", "مَعْرِض": "art",
    "مُدِير": "travail, metier", "وِزَارَة": "institution", "اِجْتِمَاع": "travail",
    "حَرْب": "institution", "أَب": "famille", "صَبَاح": "moment",
}


def convertir(ligne: str) -> list[str]:
    c = [x.strip() for x in ligne.split("|")]
    c += [""] * (9 - len(c))
    mot = c[0]
    if mot in R:
        return R[mot]
    mots, fr, cats, niv, freq, tags, reg, ctx, ref = c[:9]
    pluriel = ""
    if ctx.startswith("ج "):
        pluriel, ctx = ctx[2:].strip(), ""
    if mot in TAGS:
        tags = TAGS[mot]
    out = [mots, fr, cats, niv, freq, tags, reg, ctx, ref, "", pluriel]
    while out and out[-1] == "":
        out.pop()
    return [" | ".join(out)]


vus = set()
for p in sorted(glob.glob("sources/*.txt")):
    texte = open(p, encoding="utf-8").read()
    morceaux = re.split(r"(?m)^(?=@ref )", texte)
    sortie = []
    for m in morceaux:
        ref = re.match(r"@ref (\d+)", m)
        if "=== VOCA\n" not in m:
            if ref and ref.group(1) in AJOUTS:
                m = m.rstrip("\n") + "\n=== VOCA\n" + "\n".join(AJOUTS[ref.group(1)]) + "\n"
            sortie.append(m)
            continue
        tete, _, voca = m.partition("=== VOCA\n")
        lignes = []
        for l in voca.splitlines():
            if not l.strip():
                continue
            if l.count("|") > 8:
                raise SystemExit(f"{p} : déjà converti ({l})")
            vus.add(l.split("|")[0].strip())
            lignes += convertir(l)
        if ref and ref.group(1) in AJOUTS:
            lignes += AJOUTS[ref.group(1)]
        sortie.append(tete + "=== VOCA\n" + "".join(x + "\n" for x in lignes))
    open(p, "w", encoding="utf-8").write("".join(sortie))

inconnus = set(R) - vus
if inconnus:
    print("clés sans entrée :", inconnus)
print("converti")
