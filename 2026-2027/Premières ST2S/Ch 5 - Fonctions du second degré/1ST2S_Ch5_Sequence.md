# Déroulement de la séquence — Première ST2S, Ch. 5 : Fonctions du second degré

Période : du 30/11 au 18/12/2026, soit 3 semaines à 3 h par semaine (9 séances). Décalé d'une semaine après la Toussaint (fin du chapitre 3).
Le chapitre ne traite que du second degré : les fonctions de degré 3 ont été retirées du programme lors de l'aménagement de 2025. Les polynômes de degré 3 ne reviennent qu'avec la dérivation (chapitres 8 et 10).

## Cadre du programme (BO, première technologique)

- **Contenus** : allure de la parabole, axe de symétrie, coordonnées du sommet (en lien avec la symétrie) et tableau de variations ; racines et signe d'un polynôme de degré 2 **donné sous forme factorisée**.
- **Capacités** :
  - associer une parabole aux expressions $ax^2$, $ax^2 + c$ et $a(x - x_1)(x - x_2)$ ;
  - déterminer les éléments caractéristiques de $ax^2 + bx + c$, **sans formule** : l'axe de symétrie se trouve en résolvant $f(x) = c$ ;
  - vérifier qu'une valeur conjecturée est racine ;
  - factoriser, dans des cas simples, en connaissant au moins une racine ;
  - utiliser la forme factorisée pour trouver les racines et étudier le signe.
- **Hors programme** : discriminant, formules des racines, forme canonique, formule $-\frac{b}{2a}$. En cas de besoin, un solveur est admis.
- **Algorithmique** : valeur approchée d'une solution d'une équation par balayage.

## Reprise du chapitre 2024-2025 (Première spécialité, Ch. 1 Polynômes)

Le cours de spécialité est construit autour du discriminant et de la forme canonique : il est inutilisable tel quel. On garde seulement :

| Document 2024-2025 | Utilisation en ST2S |
|---|---|
| Activité 1 « saut du dauphin » | **Reprise et simplifiée** comme activité d'introduction. On garde la forme générale $f(t) = a(t - t_1)(t - t_2)$ : les élèves trouvent $t_1 = 0$ et $t_2 = 6$ grâce au contexte (instants où $f(t) = 0$), puis $a = -0{,}3$ avec $f(2) = 2{,}4$ (le poisson est attrapé à $t = 2$ s). On ajoute un tableau de valeurs, la courbe, l'axe $t = 3$ et la hauteur maximale $f(3) = 2{,}7$ m. Les élèves n'ont plus à démontrer la règle du produit nul, vue en questions flash. |
| Activité 2 « racines » (GeoGebra) | **Parties 1 à 3 seulement**, projetées par le professeur : effet de $a$ et de $c$ sur la parabole. La partie 4 (complétion du carré, $\Delta$) est supprimée. |
| Cours, parties « Équations de degré 3 et 4 » | Non reprises : hors du chapitre. |
| Exercices 1 à 13 | Presque tous demandent $\Delta$ : on ne garde que les équations produit nul (« $(x - 5)(x + 7) = 0$ ») et l'étude de signe de $(x - 1)(x - 4)$. |
| Contrôles (flash, formatif, sommatif) | Non repris : ils portent sur $\Delta$ et la forme canonique. |

## Documents à produire

| Document | Fichier |
|---|---|
| Progression du chapitre | `1ST2S_Ch5_Progression.tex` |
| Activité 1 (dauphin) et corrigé | `Activités/Activité 1/1ST2S_Ch5_Act1.tex`, `1ST2S_Ch5_Act1_Corrige.tex` |
| Cours (prof et élève) | `Cours/1ST2S_Ch5_Cours.tex` |
| Fiche d'exercices et corrigé | `Exercices/1ST2S_Ch5_Exos.tex`, `Exercices/Corrigés/1ST2S_Ch5_Exos_Corrige.tex` |
| Contrôle formatif A/B | `Contrôles/Form 1/` |

## Questions flash de la période

| À partir du | Calcul numérique | Calcul littéral | Autre |
|---|---|---|---|
| 30/11 | Ordres de grandeur | Développer $(a+b)^2$, $(a-b)^2$ | Probabilités |
| 14/12 | Conversions | Suites | Pourcentages, coefficient multiplicateur |

Les questions flash du 02/11 (signe des fonctions affines, tableaux de signes graphiquement) et du 16/11 (équations produit nul) ont préparé ce chapitre : on s'appuie dessus dès la séance 2. Le développement de $(a+b)^2$ commence en questions flash avec le chapitre (30/11) et accompagne la forme développée (séance 4).

## Séances

Une séance d'1 h compte environ 10 min de questions flash. En classe, on garde les exercices qui installent la notion. La suite d'un exercice commencé, ou un exercice du même type, est donnée en devoir (environ 15 min de travail).

### Séance 1 — Découverte : le saut du dauphin (semaine du 30/11)
- **Activité 1** : la trajectoire est modélisée par $f(t) = a(t - t_1)(t - t_2)$.
  - À quels instants le dauphin est-il au niveau de l'eau, c'est-à-dire $f(t) = 0$ ? Le contexte donne $t_1 = 0$ et $t_2 = 6$, d'où $f(t) = a(t - 0)(t - 6) = a\,t(t - 6)$.
  - Calcul de $a$ avec $f(2) = 2{,}4$ (le poisson est attrapé à $t = 2$ s) : $a \times 2 \times (-4) = 2{,}4$, donc $a = -0{,}3$.
  - Tableau de valeurs, tracé de la courbe, symétrie par rapport à $t = 3$ (milieu de $0$ et $6$), hauteur maximale $f(3) = 2{,}7$ m.
  - Développement : $f(t) = -0{,}3t^2 + 1{,}8t$.
- Bilan : parabole, **forme factorisée** $a(t - t_1)(t - t_2)$, les **racines** $t_1$ et $t_2$ sont les solutions de $f(t) = 0$, axe de symétrie au milieu des racines, sommet.
- **Devoir** : terminer le développement de $f(t)$ si besoin.

### Séance 2 — Forme factorisée : racines et signe (semaine du 30/11)
- **Cours** : forme factorisée $a(x - x_1)(x - x_2)$, dans le prolongement de l'activité ; racines par la règle du produit nul ; vérifier qu'un nombre est racine ; tableau de signes avec un facteur par ligne (lien avec le signe de $ax + b$, chapitre 3).
- **En classe** : racines et tableau de signes de deux expressions factorisées.
- **Devoir** : une troisième étude de signe ; vérifier qu'une valeur donnée est racine.

### Séance 3 — Forme factorisée : allure, axe, sommet, variations (semaine du 30/11)
- **Démonstration GeoGebra projetée** (reprise de l'activité 2024-2025) : effet du signe de $a$ sur l'ouverture de la parabole.
- **Cours** : allure selon le signe de $a$ ; l'axe de symétrie passe par le milieu des racines, $x = \frac{x_1 + x_2}{2}$ (justifié par la symétrie, sans formule générale) ; coordonnées du sommet ; tableau de variations.
- **En classe** : étude complète de $f(x) = 2(x - 1)(x - 5)$ : racines, signe, axe, sommet, variations, allure.
- **Devoir** : même étude pour une parabole tournée vers le bas.

### Séance 4 — Forme développée $ax^2 + bx + c$ (semaine du 07/12)
- **Cours** : passer de la forme factorisée à la forme développée (développer) ; $f(0) = c$ ; trouver l'axe de symétrie en résolvant $f(x) = c$, c'est-à-dire $x(ax + b) = 0$ ; en déduire le sommet et les variations.
- **En classe** : axe et sommet de deux fonctions sous forme développée.
- **Devoir** : développer une forme factorisée et vérifier le résultat sur un exemple numérique.

### Séance 5 — Paraboles $x \mapsto ax^2$ et $x \mapsto ax^2 + c$ ; associer une parabole à son expression (semaine du 07/12)
- **Démonstration GeoGebra projetée** : effet de $c$ (translation verticale).
- **Cours** : cas particuliers de la forme développée ($b = 0$) : axe de symétrie confondu avec l'axe des ordonnées, sommet $(0~;~c)$, variations selon le signe de $a$.
- Associer une parabole à une expression $ax^2$, $ax^2 + c$ ou $a(x - x_1)(x - x_2)$ : signe de $a$, ordonnée à l'origine, racines.
- **En classe** : un exercice d'association de quatre paraboles et quatre expressions.
- **Devoir** : tableau de valeurs et tracé d'une parabole $ax^2 + c$.

### Séance 6 — Factoriser connaissant une racine (semaine du 07/12)
- **Cours** : factoriser dans des cas simples : facteur commun ($x^2 - 4x = x(x - 4)$), ou racine donnée et identification du deuxième facteur ; vérifier en développant. On peut alors étudier le signe d'une forme développée en la factorisant.
- **En classe** : deux factorisations guidées, puis l'étude de signe de l'une des deux formes obtenues.
- **Devoir** : une factorisation connaissant une racine.

### Séance 7 — Résolution graphique et problèmes (semaine du 14/12)
- **Cours** : résoudre graphiquement $f(x) = k$ et $f(x) < k$ (rappel du chapitre 1) ; valeur approchée d'une solution par balayage (table de la calculatrice ou tableur projeté) ; solveur en cas de besoin.
- **En classe** : un problème de modélisation en contexte sanitaire ou social (par exemple, nombre de patients pendant une épidémie modélisé par une parabole, bénéfice d'une association selon le prix d'un ticket).
- **Devoir** : finir le problème.

### Séance 8 — Synthèse (semaine du 14/12)
- **En classe** : un exercice de synthèse mêlant forme factorisée et forme développée : racines, signe, axe, sommet, variations, interprétation en contexte.
- Révision des points fragiles avant le contrôle.
- **Devoir** : réviser le savoir-faire du chapitre.

### Séance 9 — Contrôle formatif (semaine du 14/12)
- Sujets A et B, même structure et même difficulté, calculatrice autorisée.
- Contenu : associer parabole et expression, racines et signe à partir de la forme factorisée, axe et sommet (forme factorisée et forme développée), tableau de variations, factorisation simple.

## Points de vigilance

- Jamais de discriminant ni de formule des racines : on travaille sur la forme factorisée ou sur des racines évidentes. Un solveur est admis si une équation n'a pas de racine évidente.
- L'axe de symétrie d'une forme développée se trouve en résolvant $f(x) = c$, pas avec $-\frac{b}{2a}$.
- Les tableaux de signes reprennent la méthode du chapitre 3 (signe de $ax + b$), une ligne par facteur.
- Les variations se lisent grâce à la symétrie et au signe de $a$ : la dérivation n'arrive qu'au chapitre 8.
- Choisir des contextes sanitaires et sociaux, comme le demande le niveau.
- Le développement de $(a + b)^2$ n'est travaillé en questions flash que depuis le 30/11 : à la séance 4, privilégier encore le développement par double distributivité.
