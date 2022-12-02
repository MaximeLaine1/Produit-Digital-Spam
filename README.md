# Produit-Digital-Spam

Ce projet consiste à la mise en en place de différentes technique de machine Learning afin de prédire la nature d'un mail. Notre analyse s'appuie sur une base de données construite via la récupération de mail spam d'une boîte de récéption. Les modèles NLP qui ont été choisis dans ce travail sont les suivants :
- Le classifier Bayesien Naïf 
- Le modèle de Bert 
- Modèle TF-IDF + SVM (Support Vector Machine)

# Plan 
- Recolte des données
- Prétraitement du texte
- Modèle
- Résultats
## Recolte des données 
La base de données de ce projet a deux sources. 

D'abord, une adresse gmail a été créée et abonnée à des dizaines de sites qui envoient des spams (vente en ligne, pornographie, site de rencontre, site d'argent facile, etc) et des newsletters. Un script python permet de télécharger les contenus des mails et les mettre en individus dans un fichier parquet. 
<!-- Ensuite, une autre base de données a été utilisée pour compléter la première (disponible à l'adresse suivante :

Ainsi, notre base contient 2000 mails, 1000 spams et 1000 non-spams. 

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

#### Comptage de mots avec CountVectorizer
Le CountVectorizer fournit un moyen simple à la fois de tokeniser une collection de documents texte et de construire un vocabulaire de mots connus, mais aussi d'encoder de nouveaux documents en utilisant ce vocabulaire.
On peut l'utiliser comme suit :
1.	Créez une instance de la classe CountVectorizer.
2.	Appelez la fonction fit() afin d'apprendre un vocabulaire à partir d'un ou plusieurs documents.
3.	Appelez la fonction transform() sur un ou plusieurs documents selon les besoins pour encoder chacun en tant que vecteur.
Un vecteur codé est renvoyé avec une longueur du vocabulaire entier et un nombre entier pour le nombre de fois où chaque mot est apparu dans le document.


Les mots sont donc traités indépendamment les uns des autres. 
![image](https://user-images.githubusercontent.com/114995738/205308416-2b42c111-b4b5-46e5-b1df-ee20fbf2dabc.png)
![image](https://user-images.githubusercontent.com/114995738/205308464-6c9f02ac-79f6-44df-aa5d-92bc8deb6834.png)


### BERT et les transformers
Ensuite, le modèle de BERT développé par Google permet de mieux comprendre le sens d'une phrase et le contexte dans lequel le mot apparait. Pour cela, il utilise l'architecture de Transformers qui inclue un mécanisme d'auto-attention. 

## Résultats des modèles 
### Classifier Bayésien Naif
![image](https://user-images.githubusercontent.com/114995738/205309627-7c4167ba-882b-42e4-a342-334e77832030.png)
Matrice de confusion pour le classifier bayésien naïf

Accuracy : 89 %
### Modèle de BERT
![image](https://user-images.githubusercontent.com/114995738/205309952-f49f73ce-a2c4-4266-b91d-5d215673d44f.png)
Matrice de confusion pour le modèle de BERT
Accuracy : 84 %
### Modèle SVM Linear Kernel
![image](https://user-images.githubusercontent.com/114995738/205310278-46dbaf60-da32-4765-8305-2f400c693105.png)
Matrice de confusion pour le modèle SVM
Accuracy : 98 %






