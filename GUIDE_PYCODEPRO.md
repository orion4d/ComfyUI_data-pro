# Guide PyCodePro pour ComfyUI

Ce document présente les spécificités et un exemple de script Python à utiliser avec le custom node **PyCodePro** dans ComfyUI.

---

## 🟢 Spécificités des entrées (`IN`)

Les données entrantes sont accessibles via le dictionnaire `IN` avec des clés préformatées :

* **Texte (STRING)**
  Clés : `txt_in_1`, `txt_in_2`, etc.

  ```python
  mon_texte = IN.get("txt_in_1", "")
  ```

* **Entiers (INT)**
  Clés : `int_in_1`, `int_in_2`, etc.

  ```python
  mon_entier = IN.get("int_in_1", 0)
  ```

* **Flottants (FLOAT)**
  Clés : `float_in_1`, `float_in_2`, etc.

  ```python
  mon_float = IN.get("float_in_1", 0.0)
  ```

* **Images (IMAGE)**
  Converties automatiquement en objet PIL Image.
  Clés : `img_in_1`, `img_in_2`

  ```python
  mon_image_pil = IN.get("img_in_1")  # PIL Image
  ```

* **Mask (MASK)**
  Clé : `mask_in`

  ```python
  masque = IN.get("mask_in")
  ```

* **Latents, Conditioning, MODEL, CLIP, VAE**
  Clés : `latent_in`, `positive`, `negative`, `model`, `clip`, `vae`

  ```python
  latent = IN.get("latent_in")
  model = IN.get("model")
  ```

---

## 🔵 Spécificités des sorties (`OUT`)

Place les résultats dans `OUT` en respectant ces noms :

* **Texte (STRING)** : `txt_out_1`, `txt_out_2`, etc.

  ```python
  OUT["txt_out_1"] = "mon résultat"
  ```

* **Entiers (INT)** : `int_out_1`, `int_out_2`

  ```python
  OUT["int_out_1"] = 42
  ```

* **Flottants (FLOAT)** : `float_out_1`, `float_out_2`

  ```python
  OUT["float_out_1"] = 3.14
  ```

* **Images (IMAGE)** : fournir un objet PIL Image

  ```python
  OUT["img_out_1"] = mon_image_pil
  ```

* **Mask, LATENT, VAE, etc.**

  ```python
  OUT["mask_out"] = masque_sortie
  OUT["latent_out"] = latent_sortie
  OUT["model"] = modele_modifie
  ```

---

## 🟡 Affichage console

Pour des messages de debug ou d’information :

```python
print("Script exécuté avec succès.")
```

---

## 📌 Exemple complet de script

```python
# Exemple minimal PyCodePro

# Lire les entrées
texte_entre = IN.get("txt_in_1", "Entrée vide")
nombre = IN.get("int_in_1", 10)

# Traitement simple
texte_resultat = f"Le texte reçu est : '{texte_entre}' et le nombre reçu est : {nombre}"

# Sorties
OUT["txt_out_1"] = texte_resultat
OUT["int_out_1"] = nombre * 2  # exemple traitement numérique

# Image (si entrée présente)
image_entree = IN.get("img_in_1")
if image_entree:
    image_sortie = image_entree.convert("L")  # niveaux de gris
    OUT["img_out_1"] = image_sortie

# Afficher dans console
print("Script exécuté avec succès.")
```

---

> ## ⚠️ **AVERTISSEMENT DE SÉCURITÉ CRITIQUE** ⚠️
>
> Le node `PyCodePro` exécute du code Python **sans aucune isolation** (sandbox). Un script malveillant a les mêmes droits d'accès que votre propre session utilisateur et peut être **aussi dangereux qu'un virus**.
>
> ### Un script malveillant peut :
> -   **Voler vos fichiers personnels** (documents, mots de passe, clés d'API).
> -   **Supprimer définitivement vos données**.
> -   **Installer des logiciels malveillants** (virus, ransomware).
> -   **Envoyer vos informations** à un pirate sur Internet.
> -   **Utiliser votre ordinateur à votre insu** (minage de cryptomonnaies, attaques DDoS).

---

## 🚩 Drapeaux Rouges : Les Mots-Clés à Surveiller

Méfiez-vous **systématiquement** si un script contient les termes suivants. Un script simple de manipulation d'image ou de texte n'en a quasiment jamais besoin.

#### **Accès aux fichiers :**
-   `import os`
-   `import shutil`
-   `open(...)` avec des chemins de fichiers inhabituels.
> _Permet de lire, modifier, et supprimer n'importe quel fichier sur votre ordinateur._

#### **Connexion Internet :**
-   `import requests`
-   `import socket`
-   `import urllib`
> _Permet de télécharger des fichiers (virus) ou d'envoyer vos données personnelles._

#### **Exécution de commandes système :**
-   `import subprocess`
-   `os.system(...)`
> _Permet de lancer n'importe quel programme ou commande, comme formater un disque dur._

#### **Code caché ou obfusqué :**
-   `exec(...)`
-   `eval(...)`
-   `import base64` (suivi de longues chaînes de texte qui sont ensuite décodées et exécutées)
> _Souvent utilisé pour masquer des actions malveillantes dans du code qui paraît inoffensif._

---

## ✅ Règles d'Or pour Rester en Sécurité

1.  **NE JAMAIS exécuter un script de source inconnue.** Ne faites confiance qu'à des créateurs et des sites que vous connaissez et en qui vous avez une confiance absolue.

2.  **LISEZ LE SCRIPT AVANT DE L'EXÉCUTER.** Parcourez le code à la recherche des "drapeaux rouges" listés ci-dessus. Si vous ne comprenez pas ce que fait une ligne, **ne l'exécutez pas**.

3.  **PRIVILÉGIEZ VOS PROPRES SCRIPTS.** La méthode la plus sûre est de n'utiliser que du code que vous avez écrit vous-même.

> **En résumé : traitez chaque script pour ce node comme un programme exécutable (`.exe` ou `.sh`).**
>
> ### **En cas de doute, la réponse est simple : ne l'exécutez pas.**

---

*Fin du guide.*
