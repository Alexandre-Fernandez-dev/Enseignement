# Déroulement de la séquence — Première ST2S, Ch. 4 : Généralités sur les suites

Période : de la 2e séance de la semaine du 09/11 au 27/11/2026, soit 8 séances (décalage dû à la fin du chapitre 3 après la Toussaint).
La séance de synthèse est supprimée : l'exercice 17 est donné en devoir avant le contrôle.
Emploi du temps : jeudi 1 h, vendredi 2 h. Le mercredi 11/11 férié ne supprime donc aucune séance.

## Documents

| Document | Fichier |
|---|---|
| Progression du chapitre | `1ST2S_Ch4_Progression.tex` |
| Activité 1 (crèche) et corrigé | `Activités/Activité 1/1ST2S_Ch4_Act1.tex`, `1ST2S_Ch4_Act1_Corrige.tex` |
| Cours (prof et élève) | `Cours/1ST2S_Ch4_Cours.tex` |
| Fiche d'exercices | `Exercices/1ST2S_Ch4_Exos.tex` |
| Corrigé des exercices | à faire : `Exercices/Corrigés/1ST2S_Ch4_Exos_Corrige.tex` |
| Contrôle formatif A/B | à faire : `Contrôles/Form 1/` |

## Questions flash de la période

| À partir du | Calcul numérique | Calcul littéral | Autre |
|---|---|---|---|
| 02/11 | Comparaison de nombres | Signe des fonctions affines | Tableaux de signes (graphiquement) |
| 16/11 | Racines carrées | Équations produit nul | Coefficient multiplicateur, évolutions successives |

Ces thèmes préparent surtout le chapitre 5 (second degré). La comparaison de nombres sert directement au sens de variation et à la recherche de seuil.

## Séances

Une séance d'1 h compte environ 10 min de questions flash. En classe, on garde les exercices qui installent la notion. La suite d'un exercice commencé, ou un exercice du même type, est donnée en devoir pour la séance suivante (environ 15 min de travail).

### Séance 1 — Découverte (semaine du 09/11)
- **Activité 1** : la crèche. Partie A : $u(n) = 20 + 6n$, tableau, $u(n+1) = u(n) + 6$, nuage de points. Partie B : budget des repas, $v(n+1) = 1{,}1 \times v(n)$.
- Bilan à trous en fin de séance : suite, terme de rang $n$, formule explicite, relation de récurrence, nuage de points.
- **Devoir** : terminer le bilan de l'activité si besoin.

### Séance 2 — Définition et formule explicite (semaine du 09/11)
- **Cours** : 1.1 Définition et notations ($u(n)$, rang, $\mathbb{N}$, puis $u_n$ ; $u_{n+1} \neq u_n + 1$), 1.2 Formule explicite.
- **En classe** : exercice 1, exercice 2 (questions 1 et 2).
- **Devoir** : exercice 2 (questions 3 et 4), exercice 3 (questions 1 à 3).
- La question 4 de l'exercice 3 (équation $150 + 12n = 270$) est corrigée au début de la séance 3, ou laissée aux élèves les plus rapides.

### Séance 3 — Relation de récurrence (semaine du 16/11)
- **Cours** : 1.3 Relation de récurrence, 1.4 Comparer les deux modes.
- **En classe** : exercice 4 (questions 1 et 2), exercice 5.
- **Devoir** : exercice 4 (questions 3 et 4), exercice 6.
- L'exercice 7 (stock de gel, $s_{n+1} = 0{,}5 \times s_n + 40$) est reporté au devoir de la séance 4 : il prépare la modélisation.

### Séance 4 — Représentation graphique (semaine du 16/11)
- **Cours** : 2. Représentation graphique : nuage de points, lecture d'un terme, points alignés si $u_n = an + b$ (lien avec le chapitre 3).
- **En classe** : exercices 8 et 9.
- **Devoir** : exercice 10, exercice 7.

### Séance 5 — Modéliser (semaine du 16/11)
- **Cours** : 3. Modéliser : tableau « ajout de $b$ / pourcentage de $t\,\%$ », exemples EHPAD, bactéries, médicament.
- **En classe** : exercice 11 (questions 1 à 3), exercice 12 (questions 1 et 2).
- **Devoir** : exercice 11 (question 4), exercice 12 (question 3).

### Séance 6 — Sens de variation (semaine du 23/11)
- **Cours** : 4. Sens de variation : conjecture sur un tableau ou un graphique, puis signe de $u_{n+1} - u_n$ dans des cas simples.
- **En classe** : exercice 13, exercice 14 (questions 1 à 4).
- **Devoir** : exercice 14 (questions 5 et 6).

### Séance 7 — Tableur et Python (semaine du 23/11)
- **Cours** : 5.1 Tableur, projeté par le professeur (20 à 30 min) : formule explicite, formule de récurrence recopiée vers le bas, recherche d'un seuil. Puis 5.2 Python : fonctions avec une boucle `for`.
- Les élèves n'ont pas d'ordinateur : ils travaillent sur des captures d'écran et sur papier.
- **En classe** : exercice 15, exercice 16 (questions 1 et 2).
- **Devoir** : exercice 16 (questions 3 et 4), exercice 17 (synthèse : deux centres de soins) à rendre avant le contrôle.

### Séance 8 — Contrôle formatif (semaine du 23/11)
- Sujets A et B, même structure et même difficulté, calculatrice autorisée.
- Contenu : calcul de termes dans les deux modes, traduction d'une phrase en relation de récurrence, nuage de points, sens de variation.

## Points de vigilance

- Notation : $u(n)$ dans l'activité, puis $u_n$ dès la partie 1.1 du cours.
- Toujours détailler les calculs de proche en proche ($u_1 = 2 \times u_0 - 1 = 2 \times 3 - 1 = 5$).
- Le seuil se cherche au tableur ou dans un tableau de valeurs : la boucle `while` arrive au chapitre 7.
- Les suites arithmétiques et géométriques ne sont pas nommées : on parle d'« ajout constant » et d'« augmentation de $t\,\%$ ». Elles seront formalisées au chapitre 7 (janvier).
