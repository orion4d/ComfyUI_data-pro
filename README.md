# Data Pro Nodes for ComfyUI

![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)
![Made for ComfyUI](https://img.shields.io/badge/Made%20for-ComfyUI-blueviolet)

Une suite complète de nœuds pour la manipulation de données, le traitement de texte avancé et l'automatisation de workflows dans ComfyUI.

Ce pack est conçu pour les utilisateurs qui souhaitent dépasser les limites des nœuds standards, en offrant des outils pour lire des métadonnées, construire des chaînes de texte complexes, interagir avec le système de fichiers et même exécuter des scripts Python personnalisés directement dans ComfyUI.

<img width="321" height="809" alt="image" src="https://github.com/user-attachments/assets/3b8c21d7-05c2-4af4-bcbd-5830b5b3d65f" />

---

## 🚀 Installation

1.  Ouvrez un terminal ou une invite de commande.
2.  Naviguez jusqu'au répertoire `ComfyUI/custom_nodes/`.
3.  Clonez ce dépôt avec la commande suivante :
    ```bash
    git clone https://github.com/votre-nom-utilisateur/votre-repo-nom.git
    ```
4.  Redémarrez ComfyUI.
5.  Vous trouverez tous les nœuds de ce pack dans la catégorie **"Data pro"**.

---

## ✨ Fonctionnalités et Nœuds

Ce pack est organisé en plusieurs catégories pour une utilisation intuitive.

### 🐍 Scripting Avancé

<img width="1664" height="1045" alt="image" src="https://github.com/user-attachments/assets/69962a94-c49f-432b-a3df-dae90359ce3e" />

Ces nœuds permettent une personnalisation extrême de vos workflows. **Utilisez-les avec une extrême prudence.**

*   **PyCode Pro** & **PyCode Pro (Custom)**: Exécutez du code Python directement dans votre workflow. Parfait pour des opérations complexes, des intégrations d'API ou des manipulations de données uniques. **La version `Custom` offre beaucoup plus d'entrées/sorties pour les workflows très complexes.**
    > **⚠️ AVERTISSEMENT DE SÉCURITÉ CRITIQUE :** Ce nœud exécute du code sans isolation. N'exécutez **JAMAIS** de code provenant d'une source inconnue ou non fiable. **[Lisez impérativement le guide de sécurité complet avant toute utilisation.](./GUIDE_PYCODEPRO.md)**

### 🖼️ Métadonnées & Gestion de Workflow

Prenez le contrôle total des informations intégrées dans vos images.

*   **Read EXIF Data**: Extrayez des données EXIF et XMP détaillées d'une image (modèle de caméra, objectif, ISO, etc.).
*   **Load Image & Get Workflow**: Chargez une image et extrayez simultanément le workflow JSON complet qui a servi à la créer.
*   **Save Image with Rich Metadata**: Sauvegardez vos images en y intégrant des métadonnées riches (prompts, modèles, LoRAs, données personnalisées) pour une reproductibilité parfaite.
*   **Parse Metadata** & **Parse json**: Décodez des métadonnées brutes ou un workflow JSON pour en extraire des informations clés comme les prompts, les modèles, les LoRAs et les paramètres d'échantillonnage. Parse Metadata est plutôt dédié pour la récupération de données d'automatic1111 ou de Civitai (les fichiers jpeg par exemple). J'ai dû faire des compromis pour la récupération de données comfyUI, compte tenu de la diversité des nodes et versions.
*   **Convert API to Workflow**: Transformez un JSON au format API en un fichier de workflow `.json` complet et chargeable dans ComfyUI.

### ✍️ Traitement de Texte

Construisez, modifiez et manipulez des chaînes de caractères avec facilité.

*   **Simple Text Concat**: Concaténez deux textes avec un préfixe, un délimiteur et un suffixe.
*   **Text Concat (x5, x10, x20)**: Fusionnez jusqu'à 20 chaînes de texte avec un délimiteur commun.
*   **Dynamic Text (TxtPlus)**: Un outil puissant avec des entrées de texte dynamiques qui apparaissent au besoin.
*   **Text Switch (Boolean)** & **Dynamic Text Switch**: Dirigez le flux de texte en fonction d'une condition booléenne ou d'un index numérique/aléatoire.
*   **Find & Replace Text**: Effectuez une recherche et un remplacement simples dans une chaîne de texte.
*   **Format Text (f-string style)**: Construisez des chaînes complexes en utilisant une syntaxe similaire aux f-strings de Python, avec des entrées `{0}`, `{1}`, etc.
*   **Text Wrapper**: Encadrez facilement votre texte avec des parenthèses, des crochets, ou des préfixes/suffixes personnalisés.

### 🗂️ Fichiers & Variables

Interagissez avec le système de fichiers et gérez des variables au sein de votre workflow.

*   **Simple File Reader**: Lisez le contenu d'un fichier texte et sortez-le sous forme de chaîne.
*   **Simple File Writer**: Écrivez du texte dans un fichier `.txt`, `.json`, `.md`, et plus encore, avec un mode d'écrasement ou d'ajout.
*   **Variable Bus (Start)**, **Set Variable**, **Get Variable**: Un système de bus pour définir et récupérer des variables textuelles n'importe où dans votre workflow, garantissant l'ordre d'exécution.

---

## ⚠️ AVERTISSEMENT DE SÉCURITÉ : Nœud `PyCodePro`

Le nœud `PyCodePro` est un outil extrêmement puissant qui comporte des risques de sécurité importants. Il n'y a **AUCUNE** sandbox. Un script malveillant peut accéder à vos fichiers, supprimer des données ou installer des logiciels malveillants.

**Règles d'Or :**
1.  **NE JAMAIS** exécuter de scripts de sources inconnues.
2.  **LISEZ** et comprenez chaque ligne de code avant de l'exécuter.
3.  **PRIVILÉGIEZ** vos propres scripts.

➡️ **[Cliquez ici pour lire le GUIDE DE SÉCURITÉ COMPLET de PyCodePro](./GUIDE_PYCODEPRO.md)**

---

## 📜 Licence

Ce projet est sous licence MIT. Voir le fichier `LICENSE` pour plus de détails.
