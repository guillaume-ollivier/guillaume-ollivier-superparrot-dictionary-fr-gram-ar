/*
 * repertoire.js — prononciation du répertoire HTML statique produit par
 * `parrotdict repertoire` (voir `repertoire.py`).
 *
 * Même geste que l'app (bouton 🔊 après chaque segment `[lang]` de `.sp-cours`,
 * cf. `InsetAdjustingWebView.injectSpeechButtons()` dans `HTMLContentView.swift`),
 * mais sans pont natif : ce document est ouvert tel quel dans un navigateur, la
 * synthèse vocale passe donc directement par l'API Web Speech
 * (`window.speechSynthesis`), disponible sans rien installer sur un navigateur
 * de bureau ou mobile récent.
 *
 * Deux limites propres à ce mode dégradé, absentes de l'app :
 * - `data-ipa` (posé par `cours.py` pour piloter la prononciation exacte via
 *   `AVSpeechSynthesisIPANotationAttribute` côté app) n'a **aucun équivalent**
 *   dans l'API Web Speech standard (`SpeechSynthesisUtterance` ne prend que du
 *   texte brut, pas de notation phonétique ni de SSML) : impossible à honorer
 *   ici. On l'affiche en infobulle du bouton, à défaut de pouvoir le faire
 *   entendre.
 * - si le navigateur/OS n'a **aucune voix** installée pour la langue demandée
 *   (`lang`), `speechSynthesis` ne prévient pas : il peut parler quand même
 *   avec une voix de repli (souvent celle du système), ce qui sonne comme une
 *   mauvaise langue sans que rien ne soit cassé côté balisage. On choisit ici
 *   explicitement la meilleure voix disponible et on signale (bouton grisé,
 *   infobulle) quand aucune ne correspond, plutôt que de laisser le
 *   navigateur substituer une voix en silence.
 */
(function () {
  var voix = [];

  function chargerVoix() {
    voix = window.speechSynthesis.getVoices();
  }

  function meilleureVoix(lang) {
    if (!lang || !voix.length) { return null; }
    var cible = lang.toLowerCase();
    var base = cible.split("-")[0];
    // 1) correspondance exacte de la locale, 2) même langue de base.
    return (
      voix.find(function (v) { return v.lang.toLowerCase() === cible; }) ||
      voix.find(function (v) { return v.lang.toLowerCase().split("-")[0] === base; }) ||
      null
    );
  }

  function speakableText(el) {
    // Comme côté app : jamais prononcer un `<del>` (mauvaise réponse barrée),
    // ni relire le bouton lui-même une fois posé.
    var clone = el.cloneNode(true);
    clone.querySelectorAll("del, .sp-speak-btn").forEach(function (n) { n.remove(); });
    return clone.textContent.trim();
  }

  function injectSpeechButtons() {
    if (!("speechSynthesis" in window)) { return; }
    document.querySelectorAll(".sp-cours [lang]").forEach(function (el) {
      if (el.dataset.spSpeakBound) { return; }
      el.dataset.spSpeakBound = "1";
      var texte = speakableText(el);
      if (!texte) { return; }
      var lang = el.getAttribute("lang") || "fr";
      var ipa = el.getAttribute("data-ipa");

      var btn = document.createElement("button");
      btn.type = "button";
      btn.className = "sp-speak-btn";
      btn.setAttribute("aria-label", "Écouter");
      btn.textContent = "🔊";
      if (ipa) {
        btn.title = "/" + ipa + "/ — non lu par ce navigateur (API Web Speech sans "
          + "notation phonétique), voix approximative uniquement.";
      }

      btn.addEventListener("click", function (event) {
        event.preventDefault();
        event.stopPropagation();
        var v = meilleureVoix(lang);
        var utterance = new SpeechSynthesisUtterance(texte);
        if (v) {
          utterance.voice = v;
          utterance.lang = v.lang;
        } else {
          // Aucune voix pour cette langue sur cet appareil : on demande quand
          // même la langue voulue (certains moteurs la couvrent sans
          // l'annoncer dans getVoices()), mais le survol du bouton aura
          // prévenu que le résultat n'est pas garanti.
          utterance.lang = lang;
        }
        window.speechSynthesis.cancel();
        window.speechSynthesis.speak(utterance);
      });
      el.insertAdjacentElement("afterend", btn);

      if (voix.length && !meilleureVoix(lang)) {
        btn.classList.add("sp-speak-btn-sans-voix");
        btn.title = (btn.title ? btn.title + " " : "")
          + "Aucune voix " + lang + " détectée sur cet appareil : le son entendu "
          + "peut être dans une autre langue.";
      }
    });
  }

  chargerVoix();
  if ("onvoiceschanged" in window.speechSynthesis) {
    window.speechSynthesis.onvoiceschanged = function () {
      chargerVoix();
      // Les boutons déjà posés avant le chargement des voix n'avaient pas pu
      // être évalués : on ne les recrée pas, mais un futur clic bénéficiera
      // désormais de `meilleureVoix`.
    };
  }

  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", injectSpeechButtons);
  } else {
    injectSpeechButtons();
  }
})();
