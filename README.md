# Produit-Digital-Spam

Ce projet consiste à développer une architecture neuronale  utilisant BERT pour effectuer une détection de mails spam se basant sur le contexte du textuel du mail pour effectuer la prédiction. Le contexte est construit uniquement à partir de la base texte et non pas sur les adresses d'envoi du mail.
# Plan 
-Recolte des données
-Prétraitement du texte
-Modèle
-Résultats
## Recolte des données 
### Structure base de données d'entrée
Notre base de données se compose de ... Mails labellisés comme étant des spam ou non. Elle comporte 2 colonnes : 
- `body` <- le corpus de texte du mail 
- `Spam` <- la variable cible à deux modalités "True" si le mail est un spam "False" s'il ne l'est pas

## Prétraitement du texte 
Avant d'appliquer un modèle, il faut d'abord vectoriser les mots contenus dans les mails pour en avoir une représentation matricielle. 
Deux techniques de NLP sont ici utilisées. 
### TF-IDF
D'abord, le TF-IDF (de l'anglais term frequency-inverse document frequency) permet d'évaluer l'importance d'un terme contenu dans un document, relativement à une collection ou un corpus. Le poids augmente proportionnellement au nombre d'occurrences du mot dans le document. Il varie également en fonction de la fréquence du mot dans le corpus.
La fréquence « brute » d'un terme est simplement le nombre d'occurrences de ce terme dans le document considéré (on parle de « fréquence » par abus de langage). On peut choisir cette fréquence brute pour exprimer la fréquence d'un terme.
Les mots sont donc traités indépendamment les uns des autres. 
![image](https://user-images.githubusercontent.com/114995738/205308416-2b42c111-b4b5-46e5-b1df-ee20fbf2dabc.png)
![image](https://user-images.githubusercontent.com/114995738/205308464-6c9f02ac-79f6-44df-aa5d-92bc8deb6834.png)


### BERT et les transformers
Ensuite, le modèle de BERT développé par Google permet de mieux comprendre le sens d'une phrase et le contexte dans lequel le mot apparait. Pour cela, il utilise l'architecture de Transformers qui inclue un mécanisme d'auto-attention. 

## Résultats des modèles 
### Classifier Bayésien Naif

