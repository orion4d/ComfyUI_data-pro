import { app } from "../../../scripts/app.js";

app.registerExtension({
	name: "DataPro.SimpleFileWriter.Widgets",
	async beforeRegisterNodeDef(nodeType, nodeData, app) {
		// Vérifie si c'est le bon node que nous voulons modifier
		if (nodeData.name === "SimpleFileWriter") {
			
			// Garde une référence à la fonction 'onNodeCreated' originale
			const onNodeCreated = nodeType.prototype.onNodeCreated;

			// Surcharge la fonction pour ajouter notre logique
			nodeType.prototype.onNodeCreated = function () {
				// Appelle la fonction originale
				if(onNodeCreated) {
					onNodeCreated.apply(this, arguments);
				}

				// Trouve les widgets que nous voulons contrôler
				const extensionChoiceWidget = this.widgets.find((w) => w.name === "extension_choice");
				const customExtensionWidget = this.widgets.find((w) => w.name === "custom_extension");

				// Fonction pour mettre à jour la visibilité du widget personnalisé
				const updateVisibility = () => {
					if (customExtensionWidget) {
						// Affiche le widget si "custom" est sélectionné, sinon le cache
						customExtensionWidget.hidden = extensionChoiceWidget.value !== "custom";
						this.computeSize(); // Demande au node de recalculer sa taille
					}
				};

				// Sauvegarde la fonction 'callback' originale du widget de choix
				const originalCallback = extensionChoiceWidget.callback;
				
				// Ajoute notre propre logique au callback
				extensionChoiceWidget.callback = () => {
					// Appelle le callback original s'il existe
					if (originalCallback) {
						originalCallback.apply(this, arguments);
					}
					// Met à jour la visibilité
					updateVisibility();
				};

				// Appelle la fonction une première fois pour définir l'état initial correct
				updateVisibility();
			};
		}
	},
});