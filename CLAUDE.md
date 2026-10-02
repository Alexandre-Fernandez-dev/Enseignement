# Documents de mathématiques — Lycée

Supports de cours de mathématiques (lycée, Lycée Louise Michel), rédigés en LaTeX et en français.
Auteur : Alexandre Fernandez (pied de page : « A. Fernandez »).

## Arborescence

```
<année>/<niveau>/Ch N - Titre/
    def.tex          ← \Chapitre, \ChapitreCourt
    <Niveau>_ChN_Progression.tex ← progression du chapitre : pré-requis / contenus / objectifs
                       (à ne pas confondre avec <niveau>/progression.md, la progression annuelle)
    Cours/  Exercices/  Activités/  Contrôles/  Images/
```

- `2026-2027/` : année en cours, au Lycée Louise Michel.
- `2024-2025/` : archive d'un autre établissement (Lycée Lucie Aubrac), **à ne jamais modifier**. On peut y reprendre des contenus, mais en adaptant l'en-tête et les conventions à l'année en cours (le `\Structure` n'est pas le même).
- Les images d'un chapitre sont dans `Images/` (via `\graphicspath{ {../Images/} }` ou `{../../Images/}`, selon la profondeur).

## Nommage des fichiers (partage Pronote)

Le nom du `.tex` détermine celui du PDF ; il doit être unique et explicite :
`<Niveau>_Ch<N>_<Type>[_<Variante>].tex`, sans espace ni accent.
- Niveau : `1ST2S`, `2nde`. N : numéro du dossier `Ch N`.
- Type : `Cours`, `Progression`, `Act1`, `Exos1` (ou `Exos` s'il n'y en a qu'une), `Manuel` (scan du manuel), `Flash1`, `Form2`, `TestAP`…
- Variante : `_SujetA` / `_SujetB`, `_Corrige`. Version élève générée : suffixe `_ELEVE`.
- Hors chapitre : `2nde_AP_Fractions1`, `2nde_FicheCalcul2`…

Exemples : `1ST2S_Ch2_Cours.pdf`, `2nde_Ch1_Form2_SujetA.pdf`, `2nde_Ch1_Form2_Corrige.pdf`.

## Chaîne `def.tex` (en-têtes automatiques)

Chaque dossier contient un `def.tex` qui charge celui du dossier parent, puis ajoute une macro :
- `2026-2027/def.tex` → `\Structure`
- `<niveau>/def.tex` → `\Niveau`
- `Ch N/def.tex` → `\Chapitre`, `\ChapitreCourt`
- dossier du document → `\Document` (ex. `Activité 2`, `Contrôle 2`)

Forme type : `\input{\currfiledir ../def.tex}` puis `\def \Document {...}`.
Pour un nouveau dossier de document, il faut créer ce `def.tex`. Le document lui-même fait `\input{def.tex}` (le paquet `currfile` est requis).

## Compilation

- **XeLaTeX** (le préambule charge `fontspec`) : `latexmk -xelatex fichier.tex`, lancé **dans le dossier du fichier** (les chemins `def.tex` et `graphicspath` sont relatifs).
- Les fichiers auxiliaires sont ignorés par git. Les PDF sont versionnés.
- Après une modification, recompiler pour vérifier qu'il n'y a pas d'erreur.

## Conventions LaTeX

- Première ligne : `%LTeX: language=fr-FR`.
- Pour un nouveau document, **copier le préambule d'un document existant du même type** (cours, exercices, contrôle) au lieu d'en inventer un.
- Environnements de cours (tcolorbox) : `definition`, `proposition`, `method`, `savoir`, avec deux arguments `{titre}{label}`, souvent vides : `\begin{definition}{}{}`. Environnements sans cadre : `example`, `examples`, `remark`, `remarks`, `demo`.
- **Version prof / version élève** : les trous à compléter utilisent `\hide{}`, `\hideM{}` (maths), `\multihide` (bloc) et `\hidetk{}` (TikZ).
  La version prof affiche le contenu sur fond gris. La version élève s'obtient en échangeant les définitions commentées (celles avec `\phantom`), ce qui produit `<nom>.pdf` (prof) et `<nom>_ELEVE.pdf` (élève).
  Toute notion à faire compléter en classe doit être placée dans ces macros.
- Typographie française : `\geqslant` / `\leqslant`, intervalles `[a\,;\,b]`, coordonnées `(x~;~y)`, virgule décimale `2{,}5`, ponctuation haute précédée de `~` (`~:`, `~?`).
- Vecteurs : `\overrightarrow{AB}` (ou `\wvec` / `\vv` selon le préambule du fichier).

## Contrôles

- Dossiers `Contrôles/Flash N`, `Form N` (formatif), `Sommatif`, etc.
- Souvent deux sujets **A et B** : même structure et même difficulté, valeurs différentes.
- En-tête : `\Niveau` | `\Chapitre` | `\Document (A) -- durée`, puis une ligne « Nom et prénom ».
- Barème indiqué par exercice. Correction dans `<Niveau>_Ch<N>_<Contrôle>_Corrige.tex` à côté du sujet.

## Programmes officiels (BO)

Dans `BO/` : les PDF, plus une version texte à consulter avec `grep` et `Read`.
- `programme-secondes.txt` : Seconde générale et technologique
- `programme-1ere-techno.txt` : Première voie technologique, tronc commun (valable pour la ST2S ; ignorer les parties « STD2A »)

À consulter **avant** de rédiger un cours, un contrôle ou un nouveau chapitre, pour vérifier les capacités attendues, les limites du programme, les notations et les automatismes officiels. Ne pas les charger en entier sans raison.

## Consignes générales

- Rédaction adaptée au niveau : phrases courtes, vocabulaire du programme officiel, pas de notion hors programme.
- Ne pas committer sans demande explicite.
- Les consignes propres à chaque niveau sont dans `CLAUDE.md` de chaque dossier de niveau.
