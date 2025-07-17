// --- START OF FILE js/txtplus.js ---

import { app } from "../../../scripts/app.js";
import { ComfyWidgets } from "../../../scripts/widgets.js";

app.registerExtension({
	// Nom mis à jour pour éviter le cache
	name: "DataPro.TxtPlus.InitFix",

	async beforeRegisterNodeDef(nodeType, nodeData, app) {
		if (nodeData.name === "TextPlus") {

			const onNodeCreated = nodeType.prototype.onNodeCreated;
			nodeType.prototype.onNodeCreated = function () {
				onNodeCreated?.apply(this, arguments);
				const node = this;

				// S'assure que la propriété existe pour un nouveau noeud
				node.properties = node.properties || {};
				if (node.properties.visibleInputs === undefined) {
					node.properties.visibleInputs = 1;
				}

				// Fonction centrale pour synchroniser l'état des widgets
				node.syncWidgets = (visibleCount) => {
					// Met à jour les boutons d'abord
					const addBtn = node.widgets.find(w => w.name === "+ Add Input");
					const remBtn = node.widgets.find(w => w.name === "- Remove Last");
					if (addBtn) addBtn.disabled = visibleCount >= 20;
					if (remBtn) remBtn.disabled = visibleCount <= 1;

					// Crée les widgets à la demande et gère leur visibilité
					for (let i = 1; i <= 20; i++) {
						let widget = node.widgets.find(w => w.name === `text_${i}`);
						if (i <= visibleCount) {
							if (!widget) {
								widget = ComfyWidgets.STRING(node, `text_${i}`, ["STRING", { multiline: true }], app).widget;
							}
							widget.hidden = false;
						} else {
							if (widget) widget.hidden = true;
						}
					}
					
					// Force le recalcul de la taille du noeud. C'est plus sûr.
					node.computeSize();
					node.setDirtyCanvas(true, true);
				};

				// Ajoute les boutons de contrôle s'ils n'existent pas
				if (!node.widgets.find(w => w.name === "+ Add Input")) {
					node.addWidget("button", "+ Add Input", "add", () => {
						if (node.properties.visibleInputs < 20) {
							node.properties.visibleInputs++;
							node.syncWidgets(node.properties.visibleInputs);
						}
					});
					node.addWidget("button", "- Remove Last", "remove", () => {
						if (node.properties.visibleInputs > 1) {
							const widget = node.widgets.find(w => w.name === `text_${node.properties.visibleInputs}`);
							if (widget) widget.value = "";
							node.properties.visibleInputs--;
							node.syncWidgets(node.properties.visibleInputs);
						}
					});
				}

				// Gère la sauvegarde des données
				const onSerialize = node.onSerialize;
				node.onSerialize = function (o) {
					onSerialize?.apply(node, arguments);
					o.properties = o.properties || {};
					o.properties.visibleInputs = node.properties.visibleInputs;
				};

                // Gère le chargement d'un workflow
                const onConfigure = node.onConfigure;
                node.onConfigure = function(info) {
                    onConfigure?.apply(this, arguments);
                    // S'assure que la propriété est chargée ou initialisée
                    this.properties.visibleInputs = (this.properties && this.properties.visibleInputs) || 1;
                    // On appelle la fonction de synchro au chargement
                    node.syncWidgets(this.properties.visibleInputs);
                };

                // **LA CORRECTION :**
                // On appelle la fonction une fois à la création pour afficher le premier widget.
                // Le setTimeout garantit que le noeud est entièrement prêt.
                setTimeout(() => {
                    node.syncWidgets(node.properties.visibleInputs);
                }, 0);
			};
		}
	},
});