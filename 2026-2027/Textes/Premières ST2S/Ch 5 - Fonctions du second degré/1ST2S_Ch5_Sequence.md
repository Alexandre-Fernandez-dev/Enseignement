# Déroulement de la séquence — Première ST2S, Ch. 5 : Fonctions du second degré

Période : du vendredi 04/12 au vendredi 18/12/2026 : 7 séances de cours (pas de cours le jeudi 03/12 ; le jeudi 10/12 est pris par le contrôle mixte). Le contrôle formatif du chapitre 5 est à placer en janvier.
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
- **Algorithmique** : valeur approchée d'une solution d'une équation par balayage. Retiré du chapitre (choix de l'enseignant), ainsi que la résolution graphique.

## Reprise du chapitre 2024-2025 (Première spécialité, Ch. 1 Polynômes)

Le cours de spécialité est construit autour du discriminant et de la forme canonique : il est inutilisable tel quel. On garde seulement :

| Document 2024-2025 | Utilisation en ST2S |
|---|---|
| Activité 1 « saut du dauphin » | **Reprise et raccourcie** : elle n'introduit que la partie 1 du cours (forme factorisée, racines, forme développée). Le dauphin sort de l'eau à $t = 1$ et replonge à $t = 7$, d'où $f(t) = a(t - 1)(t - 7)$ : le lien avec la forme factorisée est direct. Avec $f(2) = 2{,}5$, on trouve $a = -0{,}5$ ; toutes les valeurs du tableau se calculent sans calculatrice ($0$ ; $2{,}5$ ; $4$ ; $4{,}5$ ; $4$ ; $2{,}5$ ; $0$). L'axe de symétrie et le sommet sont laissés à la séance 3. |
| Activité 2 « racines » (GeoGebra) | Remplacée par le fichier `1ST2S_Ch5_Parabole.ggb` (curseurs $a$, $x_1$, $x_2$ ; $c$ masqué). La partie 4 (complétion du carré, $\Delta$) est supprimée. |
| Cours, parties « Équations de degré 3 et 4 » | Non reprises : hors du chapitre. |
| Exercices 1 à 13 | Presque tous demandent $\Delta$ : on ne garde que les équations produit nul (« $(x - 5)(x + 7) = 0$ ») et l'étude de signe de $(x - 1)(x - 4)$. |
| Contrôles (flash, formatif, sommatif) | Non repris : ils portent sur $\Delta$ et la forme canonique. |

## Documents à produire

| Document | Fichier |
|---|---|
| Progression du chapitre | `1ST2S_Ch5_Progression.tex` |
| Activité 1 (dauphin) | `Activités/Activité 1/1ST2S_Ch5_Act1.tex` (corrigé à faire) |
| Fichier GeoGebra (parabole, curseurs $a$, $x_1$, $x_2$, $c$) | `Activités/Activité 1/1ST2S_Ch5_Parabole.ggb`, généré par `genere_ggb.py` |
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

### Séance 1 — Découverte : le saut du dauphin, puis cours (vendredi 04/12, 1re heure, après les révisions sur les suites)
- **Activité 1** (environ 25 min) : la trajectoire est modélisée par $f(t) = a(t - t_1)(t - t_2)$.
  - Questions 1 et 2 : le dauphin est au niveau de l'eau à $t = 1$ et $t = 7$, donc $f(1) = f(7) = 0$, d'où $t_1 = 1$, $t_2 = 7$ et $f(t) = a(t - 1)(t - 7)$.
  - Question 3 : $f(2) = 2{,}5$ donne $a \times 1 \times (-5) = 2{,}5$, donc $a = -0{,}5$.
  - Question 4 : tableau de valeurs ($0$ ; $2{,}5$ ; $4$ ; $4{,}5$ ; $4$ ; $2{,}5$ ; $0$ ; on peut répartir les calculs entre les élèves), points placés dans le repère, puis courbe projetée avec `1ST2S_Ch5_Parabole.ggb` (la liste T affiche les points du tableau) : c'est une parabole.
  - Question 5 : $f(t) = -0{,}5(t^2 - 8t + 7) = -0{,}5t^2 + 4t - 3{,}5$.
  - Bilan : forme factorisée, racines (solutions de $f(x) = 0$), forme développée ; $a$ est le même dans les deux formes. Avec GeoGebra, faire varier $x_1$ et $x_2$ (la courbe coupe l'axe des abscisses en $x_1$ et $x_2$) et regarder $g$ dans la vue Algèbre (coefficients de la forme développée).
- **Cours**, dans la foulée : partie 1, exemple du dauphin, définition (forme développée, forme factorisée, racine), proposition sur les racines d'une forme factorisée et exemples.
- **Devoir** : donner les racines de deux ou trois formes factorisées.

### Séance 2 — Forme factorisée : racines et signe (vendredi 04/12, 2e heure)
- **Cours** : fin de la partie 1 : vérifier qu'un nombre est racine ; tableau de signes avec un facteur par ligne (lien avec le signe de $ax + b$, chapitre 3).
- **En classe** : racines et tableau de signes de deux expressions factorisées.
- **Devoir** : une troisième étude de signe ; vérifier qu'une valeur donnée est racine.

### Séance 3 — Forme factorisée : allure, axe, sommet, variations (vendredi 11/12, 1re heure)
- **Démonstration GeoGebra projetée** (`1ST2S_Ch5_Parabole.ggb`, curseur $a$) : effet du signe de $a$ sur l'ouverture de la parabole ; retour au dauphin pour l'axe $t = 4$ et la hauteur maximale $f(4) = 4{,}5$ m.
- **Cours** : allure selon le signe de $a$ ; l'axe de symétrie passe par le milieu des racines, $x = \frac{x_1 + x_2}{2}$ (justifié par la symétrie, sans formule générale) ; coordonnées du sommet ; tableau de variations.
- **En classe** : étude complète de $f(x) = 2(x - 1)(x - 5)$ : racines, signe, axe, sommet, variations, allure.
- **Devoir** : même étude pour une parabole tournée vers le bas.

### Séance 4 — Forme développée $ax^2 + bx + c$ (vendredi 11/12, 2e heure)
- **Cours** : passer de la forme factorisée à la forme développée (développer) ; $f(0) = c$ ; trouver l'axe de symétrie en résolvant $f(x) = c$, c'est-à-dire $x(ax + b) = 0$ ; en déduire le sommet et les variations.
- **En classe** : axe et sommet de deux fonctions sous forme développée.
- **Devoir** : développer une forme factorisée et vérifier le résultat sur un exemple numérique.

### Séance 5 — Paraboles $x \mapsto ax^2$ et $x \mapsto ax^2 + c$ ; associer une parabole à son expression (jeudi 17/12)
- **Démonstration GeoGebra projetée** (`1ST2S_Ch5_Parabole.ggb` : afficher le curseur $c$ et la courbe $h$ dans la vue Algèbre) : effet de $c$ (translation verticale).
- **Cours** : cas particuliers de la forme développée ($b = 0$) : axe de symétrie confondu avec l'axe des ordonnées, sommet $(0~;~c)$, variations selon le signe de $a$.
- Associer une parabole à une expression $ax^2$, $ax^2 + c$ ou $a(x - x_1)(x - x_2)$ : signe de $a$, ordonnée à l'origine, racines.
- **En classe** : un exercice d'association de quatre paraboles et quatre expressions.
- **Devoir** : tableau de valeurs et tracé d'une parabole $ax^2 + c$.

### Séance 6 — Factoriser connaissant une racine (vendredi 18/12, 1re heure)
- **Cours** : factoriser dans des cas simples : facteur commun ($x^2 - 4x = x(x - 4)$), ou racine donnée et identification du deuxième facteur ; vérifier en développant. On peut alors étudier le signe d'une forme développée en la factorisant.
- **En classe** : deux factorisations guidées, puis l'étude de signe de l'une des deux formes obtenues.
- **Devoir** : une factorisation connaissant une racine.

### Séance 7 — Problèmes et synthèse (vendredi 18/12, 2e heure)
- Pas de résolution graphique ni de balayage (retirés du cours).
- **En classe** : un problème de modélisation en contexte sanitaire ou social (par exemple, nombre de patients pendant une épidémie modélisé par une parabole, bénéfice d'une association selon le prix d'un ticket).
- **Devoir** : finir le problème ; exercice de synthèse (forme factorisée et forme développée) avant le contrôle.

### Séance 8 — Contrôle formatif (à placer en janvier)
- Sujets A et B, même structure et même difficulté, calculatrice autorisée.
- Contenu : associer parabole et expression, racines et signe à partir de la forme factorisée, axe et sommet (forme factorisée et forme développée), tableau de variations, factorisation simple.

## Points de vigilance

- Jamais de discriminant ni de formule des racines : on travaille sur la forme factorisée ou sur des racines évidentes. Un solveur est admis si une équation n'a pas de racine évidente.
- L'axe de symétrie d'une forme développée se trouve en résolvant $f(x) = c$, pas avec $-\frac{b}{2a}$.
- Les tableaux de signes reprennent la méthode du chapitre 3 (signe de $ax + b$), une ligne par facteur.
- Les variations se lisent grâce à la symétrie et au signe de $a$ : la dérivation n'arrive qu'au chapitre 8.
- Choisir des contextes sanitaires et sociaux, comme le demande le niveau.
- Le développement de $(a + b)^2$ n'est travaillé en questions flash que depuis le 30/11 : à la séance 4, privilégier encore le développement par double distributivité.
