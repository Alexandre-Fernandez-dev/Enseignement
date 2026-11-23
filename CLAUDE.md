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

## Progression annuelle (par niveau)

Dans chaque dossier de niveau :
- `progression_initiale.xlsx` : la progression de départ, fournie en début d'année. **Figée, ne jamais la modifier** ; elle sert de référence.
- `progression.xlsx` : la progression adaptée au fil de l'année, avec le cahier de textes. **C'est elle qui fait foi.** Séances faites en bleu, séances prévues en violet italique (légende en N1).
- `progression.md` : résumé lisible de `progression.xlsx`, à tenir à jour en même temps que le classeur.
- `<Niveau>_ChN_Sequence.md` dans chaque chapitre : déroulement séance par séance.

### Classeurs du Drive (lecture seule)

L'enseignant remplit au fil des séances un classeur sur le Drive (cahier de textes, liens des questions flash) :
`Enseignement/2026-2027/2GT/progression seconde 2026-2027 AF.xlsx` et `Enseignement/2026-2027/1ST2S/progression 1 ST2S 2026-2027.xlsx`. Il a les mêmes colonnes que `progression.xlsx`. La colonne B « Chapitre » doit y rester : si elle manque, la lecture s'adapte, mais il faut le signaler.
- **Lecture seule, toujours.** Ne jamais écrire, déplacer ni partager quoi que ce soit sur le Drive : ni avec `rclone` (le remote `Drive:` ne sert qu'au hook `post-commit` pour les PDF), ni dans le montage `~/Drive`. Pour un changement de progression, modifier le dépôt et dire à l'enseignant quoi reporter sur le Drive.
- Lecture : `scripts/progressions.py`, avec un compte de service Google qui n'a que le droit de lecture sur ces deux classeurs. Mise en place décrite en tête du script ; `python3 scripts/progressions.py verifier` teste l'accès.
- Quand l'enseignant dit avoir mis à jour sa progression (plus besoin de snapshot) : `python3 scripts/progressions.py comparer [date]` liste ce que le Drive dit de différent du dépôt. Reporter ces changements dans `progression.xlsx`, `progression.md` et les `*_Sequence.md`. Si le Drive contredit une décision prise avec Claude, demander à l'enseignant laquelle garder. Pour travailler sur les fichiers eux-mêmes (mise en forme, liens), `telecharger DOSSIER` en fait une copie locale.
- Les dossiers du Drive contiennent aussi des documents personnels d'élèves : ne jamais les partager avec le compte de service ni les lire.

## Nommage des fichiers (partage Pronote)

Le nom du `.tex` détermine celui du PDF ; il doit être unique et explicite :
`<Niveau>_Ch<N>_<Type>[_<Variante>].tex`, sans espace ni accent.
- Niveau : `1ST2S`, `2nde`. N : numéro du dossier `Ch N`.
- Type : `Cours`, `Progression`, `Act1`, `Exos1` (ou `Exos` s'il n'y en a qu'une), `Manuel` (scan du manuel), `Flash1`, `Form2`, `TestAP`…
- Variante : `_SujetA` / `_SujetB`, `_Corrige`. Version élève générée : suffixe `_ELEVE`. PDF annoté au tableau : suffixe `_Annote` en dernier (ex. `2nde_Ch1_Cours_ELEVE_Annote.pdf`).
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
- `compile.sh fichier.tex` (recette LaTeX Workshop par défaut) produit les versions prof et élève. Les fichiers auxiliaires vont dans le sous-dossier `.build/` (option `-auxdir=.build`). Seul le `.synctex.gz` reste à côté du PDF.
- Les fichiers auxiliaires sont ignorés par git. Les PDF sont versionnés.
- Après une modification, recompiler pour vérifier qu'il n'y a pas d'erreur.

## Diffusion des PDF (Drive, clé USB, tableau)

- **Drive** : le hook `scripts/hooks/post-commit` (versionné, installé par `git config core.hooksPath scripts/hooks`) met à chaque commit `Drive:Enseignement/2026-2027/PDF Lycée` en **miroir** des PDF de `2026-2027/` (`rclone sync`, en arrière-plan, une synchronisation à la fois) : un PDF supprimé ou renommé dans le dépôt disparaît aussi du Drive. Journal : `.git/rclone-sync.log`. Un fichier en double sur le Drive (« Duplicate object found » dans le journal) n'est plus mis à jour : le signaler à l'enseignant.
- **Clé USB** (pour l'écran Vivitek NovoTouch de la classe) : lancer à la main `scripts/sync-cle.sh` quand la clé `AFERNANDEZ` est branchée, ou la tâche VS Code « Synchroniser la clé ». L'option `--dry-run` (tâche « simulation ») montre ce qui serait fait.
  - La clé reçoit un miroir exact des PDF de `2026-2027/` dans `PDF Lycée/` à la racine de la clé (mêmes sous-dossiers que le Drive). Puis chaque PDF reçoit un `.iwb` à côté de lui, généré s'il manque ou s'il est plus ancien que le PDF.
  - Fichiers jamais supprimés par le miroir : `*.iwb` (sauf ceux dont le PDF a disparu), `*.enb` (annotations créées par le tableau), `*_Annote.pdf`. Tout le reste (ex. `.ubz`) est supprimé.
  - Le premier passage convertit tout (environ 4 s par page) ; les suivants ne convertissent que ce qui a changé (un `.iwb` porte la date de son PDF ; dates différentes = à reconvertir).
- `scripts/pdf2iwb.sh fichier.pdf` : convertit un PDF en `fichier.iwb` (pages en PNG de 4320 px de haut). L'import PDF direct du tableau est en basse résolution.
- `scripts/enb2pdf.sh fichier.enb [fichier.pdf]` : produit `fichier_Annote.pdf`, le PDF d'origine avec les traits du tableau redessinés en vectoriel (calés sur la page même si elle a été zoomée ou déplacée). Une diapositive ajoutée au tableau devient une page blanche en paysage, après la page qui la précède.
  Format `.enb` : ZIP avec `Slides/Slide_N.xml` (une diapositive par page : une `Picture` `p-N.png` placée par une `Transform`, et des traits `Ink`), plus des vignettes `Slide_N.png`.
- Dépendances : `rsync`, `poppler` (`pdftoppm`, `pdfinfo`), `imagemagick` (`identify`), `zip`, `qpdf`, `python-cairo`.
- Sur la clé, le script n'écrit que dans `PDF Lycée/` et s'arrête si ce dossier manque. Les documents personnels (plans de classe, listes d'élèves) sont dans `Documents/`, à côté, avec les mêmes sous-dossiers par niveau : hors du miroir, sans `.iwb`, jamais modifiés par le script.
- Changement d'année : mettre à jour `ANNEE` dans `scripts/sync-cle.sh` et dans `scripts/hooks/post-commit`.

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

## Trame du jour (aussi depuis le téléphone ou une session cloud)

Quand on demande « la trame du jour », « les cours d'aujourd'hui » ou ceux d'une autre date :
1. Lancer `python3 scripts/trame_du_jour.py [date]` depuis la racine (sans argument : aujourd'hui, heure de Paris ; sinon `demain`, `26/11` ou `2026-11-26`). Il lit les progressions du Drive (lecture seule) et du dépôt. Il affiche pour ce jour : les séances, la fiche calcul (lundi) et l'AP (jeudi), les thèmes de questions flash, et les passages des `*_Sequence.md` qui mentionnent la date. Quand le Drive et le dépôt diffèrent, il donne les deux : le Drive est la saisie la plus récente, le dépôt contient les décisions prises avec Claude. Dans la trame, signaler l'écart en une ligne.
2. Compléter si besoin avec le reste du `*_Sequence.md` (points de vigilance) et retrouver les fichiers des documents cités (cours, exercices, contrôles) pour donner leurs chemins.
3. Rédiger une trame courte et lisible sur téléphone, classe par classe et heure par heure : objectif de la séance ; déroulé avec durées (questions flash, correction, cours, exercices) ; documents à ouvrir au tableau ; devoirs à donner ; points de vigilance et rappels (élèves absents, contrôle à venir, choses à ramasser) ; ce qui reste à préparer.
4. Une session cloud ne voit du dépôt que ce qui a été poussé sur GitHub. Elle lit le Drive si l'environnement cloud a la variable `GOOGLE_COMPTE_SERVICE`. Si le script affiche « dépôt seulement », le dire en tête de la trame : la progression peut être en retard.

## Projet Claude « Cours » (claude.ai)

Le Projet Claude lit le dépôt GitHub (branche `main`) : le dossier `2026-2027/Textes/`, versions texte allégées des documents produites par `scripts/textes_projet.py`, et les `CLAUDE.md` s'ils sont sélectionnés. Il ne modifie rien ; il se met à jour seulement quand on clique « Sync now » dans le projet.
- Après toute modification d'un `.tex`, d'un `*_Sequence.md` ou d'un `progression.md` de `2026-2027/`, relancer `python3 scripts/textes_projet.py` et committer `2026-2027/Textes/` **avec** les fichiers sources concernés (jamais les textes d'un travail qu'on ne committe pas).
- Après le push, rappeler à l'enseignant de cliquer « Sync now » dans le projet.

## Nouvel ordinateur

Le dépôt GitHub contient tout le contexte (documents, PDF, scripts, CLAUDE.md, progressions). À refaire sur la machine :
1. `git clone git@github.com:Alexandre-Fernandez-dev/Enseignement.git`, puis, à la racine : `git config core.hooksPath scripts/hooks` (sans cela, les PDF n'arrivent plus sur le Drive, sans message d'erreur).
2. Logiciels : TeX Live (XeLaTeX, `latexmk`), `rclone`, `python3`, et les dépendances de la clé USB listées plus haut.
3. `rclone config` : recréer le remote `Drive:` (type drive, compte Google du Drive), utilisé par le hook.
4. Clé du compte de service : console.cloud.google.com, projet du compte de service > Clés > Ajouter une clé > JSON, ranger le fichier dans `~/.config/lycee/compte-service.json` (`chmod 600`), puis `python3 scripts/progressions.py verifier`. Les partages du Drive restent valables ; la variable de l'environnement cloud aussi.
Ne restent que sur l'ancienne machine : le travail non committé ou non poussé, la mémoire locale de Claude Code et l'historique des conversations locales (les sessions cloud restent sur claude.ai).

## Consignes générales

- Rédaction adaptée au niveau : phrases courtes, vocabulaire du programme officiel, pas de notion hors programme.
- Dans un document élève (tous niveaux), ne jamais renvoyer à un autre document (« la situation de la fiche calcul », « comme dans l'activité ») : chaque énoncé redonne lui-même tout son contexte et ses données. Exception : un cours peut citer l'activité qui l'introduit (« Dans l'activité 1… »), à condition de redonner les données utiles, comme c'est déjà fait. Les renvois restent possibles dans les fichiers prof (`*_Sequence.md`, progression).
- Un script qui génère un document (sujets A/B, courbes, tableaux…) se range dans le dossier de ce document et se versionne avec lui, jamais seulement dans un dossier temporaire. En tête du script : ce qu'il produit et comment le relancer.
- Ne pas committer sans demande explicite.
- Les consignes propres à chaque niveau sont dans `CLAUDE.md` de chaque dossier de niveau.
