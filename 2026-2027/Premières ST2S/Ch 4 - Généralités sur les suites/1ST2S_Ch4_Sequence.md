# Déroulement de la séquence — Première ST2S, Ch. 4 : Généralités sur les suites

Période : du jeudi 19/11 au vendredi 27/11/2026 (7 séances), révisions en début d'heure le vendredi 04/12, contrôle mixte (fonctions affines et suites) le jeudi 10/12. Le tableur et Python (partie 5 du cours) sont reportés au chapitre 7.
L'activité est coupée en deux (activité 1 : formule explicite ; activité 2 : relation de récurrence), chacune suivie du cours et d'exercices. La séance de synthèse est supprimée : l'exercice 17 est donné en devoir avant le contrôle.
Emploi du temps : jeudi 1 h, vendredi 2 h. Le mercredi 11/11 férié ne supprime donc aucune séance.

## Documents

| Document | Fichier |
|---|---|
| Progression du chapitre | `1ST2S_Ch4_Progression.tex` |
| Activité 1 (crèche : suite, formule explicite) et corrigé | `Activités/Activité 1/1ST2S_Ch4_Act1.tex`, `1ST2S_Ch4_Act1_Corrige.tex` |
| Activité 2 (budget des repas : relation de récurrence) et corrigé | `Activités/Activité 2/1ST2S_Ch4_Act2.tex`, `1ST2S_Ch4_Act2_Corrige.tex` |
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

### Séance 1 — Activité 1, définition et formule explicite (jeudi 19/11) — faite
- **Activité 1** : la crèche, $u(n) = 20 + 6n$ : tableau, $u(4)$, calcul de $u(10)$ et formule, nuage de points. Bilan à trous.
- **Cours** : 1.1 Définition et notations, 1.2 Formule explicite. **En classe** : exercice 1.
- **Devoir** : exercice 2, exercice 3 (questions 1 à 3). Exercices 10 et 11 du chapitre 3 ramassés.

### Séance 2 — Correction, activité 2 (vendredi 20/11, 1re heure) — faite
- Correction des exercices 1, 2 (questions 1 et 2) et 3 (questions 1 à 3).
- **Activité 2** : budget des repas, relation de récurrence. Début de l'exercice 4.

### Séance 3 — Relation de récurrence (vendredi 20/11, 2e heure) — faite
- **Cours** : 1.3 Relation de récurrence, 1.4 Comparer les deux modes.
- **En classe** : exercice 4 (questions 1 et 2), exercice 5.
- **Devoir** : finir les exercices 2, 3 et 4 ; exercice 6 facultatif.

### Séance 4 — Représentation graphique (jeudi 26/11) — faite
- **Cours** : 2. Représentation graphique. **En classe** : exercice 8 (pas le temps de traiter l'exercice 9).
- **Devoir** : exercice 9.

### Séance 5 — Modéliser (vendredi 27/11, 1re heure) — faite
- Correction de l'exercice 9.
- **Cours** : 3. Modéliser (tableau « ajout de $b$ / pourcentage de $t\,\%$ », exemples EHPAD, bactéries, médicament). La séance s'est arrêtée au cours.

### Séance 6 — Modéliser (suite) et sens de variation (vendredi 27/11, 2e heure) — faite
- **En classe** : exercice 11, sauf la question 4 (pourcentage).
- **Cours** : 4. Sens de variation (conjecture sur un tableau ou un graphique, puis signe de $u_{n+1} - u_n$ dans des cas simples). Pas d'exercice en classe.
- **Devoir** : exercice 13 seulement (conjecturer le sens de variation), utile pour le contrôle. Les exercices 12 et 14 ne sont pas donnés.
- Bilan de l'enseignant : beaucoup de difficultés sur la modélisation, et surtout sur le sens de variation par le calcul de $u_{n+1} - u_n$.

### Révisions (vendredi 04/12, début de la 1re heure)
- Pas de cours le jeudi 03/12.
- Correction du devoir : exercice 13. Puis début du chapitre 5.

### Tableur et Python — reportés au chapitre 7
- La partie 5 du cours (tableur projeté, seuil, Python) et les exercices 15 à 17 sont reportés au chapitre 7 (suites arithmétiques et géométriques), où la progression prévoit déjà le tableur et Python.

### Contrôle mixte (jeudi 10/12)
- Contrôle de 55 min, **calculatrice non autorisée** (choix de l'enseignant ; tous les calculs se font à la main) : automatismes, fonctions affines (chapitre 3) et suites, en version légère.
- Suites : calcul de termes (formule explicite, relation de récurrence), relation du type $u_{n+1} = u_n + b$ en contexte, lecture d'un nuage de points et conjecture du sens de variation. **Pas** de calcul de $u_{n+1} - u_n$ ni de modélisation avec un pourcentage.
- Sujets A et B (une page chacun) : `Contrôles/Sommatif/1ST2S_Ch4_Sommatif_SujetA.tex`, `1ST2S_Ch4_Sommatif_SujetB.tex`. Corrigé à faire.

## Points de vigilance

- Notation : $u(n)$ dans l'activité, puis $u_n$ dès la partie 1.1 du cours.
- Toujours détailler les calculs de proche en proche ($u_1 = 2 \times u_0 - 1 = 2 \times 3 - 1 = 5$).
- Le seuil se cherche au tableur ou dans un tableau de valeurs : la boucle `while` arrive au chapitre 7.
- Les suites arithmétiques et géométriques ne sont pas nommées : on parle d'« ajout constant » et d'« augmentation de $t\,\%$ ». Elles seront formalisées au chapitre 7 (janvier).
