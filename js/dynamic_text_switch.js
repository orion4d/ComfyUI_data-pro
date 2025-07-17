// --- START OF FILE js/dynamic_text_switch.js (Version Finale Corrigée et Testée) ---
import { app } from "../../../scripts/app.js";

const MAX_INPUTS = 20;

function syncWidgets(node) {
	// Affiche/masque les widgets index/seed en fonction du mode
	const mode = node.widgets.find(w => w.name === "select_mode").value;
	const indexWidget = node.widgets.find(w => w.name === "index");
	const seedWidget = node.widgets.find(w => w.name === "seed");
	if (indexWidget) indexWidget.hidden = mode !== "Numbered";
	if (seedWidget) seedWidget.hidden = mode !== "Random";

	// Met à jour les boutons
	const currentInputs = node.inputs?.filter(i => i.name.startsWith("text_")).length || 0;
	node.widgets.find(w => w.name === "+ Add Input").disabled = currentInputs >= MAX_INPUTS;
	node.widgets.find(w => w.name === "- Remove Last").disabled = currentInputs <= 1;
	
	node.setDirtyCanvas(true, true);
}

app.registerExtension({
	name: "DataPro.DynamicInputTextSwitch.Final",

	async beforeRegisterNodeDef(nodeType, nodeData) {
		if (nodeData.name === "DynamicInputTextSwitch") {
			const onNodeCreated = nodeType.prototype.onNodeCreated;
			nodeType.prototype.onNodeCreated = function () {
				onNodeCreated?.apply(this, arguments);
				const node = this;

				// Ajoute les entrées initiales (2 par défaut)
				node.addInput("text_1", "STRING");
				node.addInput("text_2", "STRING");

				// Ajoute les boutons
				node.addWidget("button", "+ Add Input", "add", () => {
					const currentCount = node.inputs.filter(i => i.name.startsWith("text_")).length;
					if (currentCount < MAX_INPUTS) {
						node.addInput(`text_${currentCount + 1}`, "STRING");
						syncWidgets(node);
					}
				});
				node.addWidget("button", "- Remove Last", "remove", () => {
					const currentCount = node.inputs.filter(i => i.name.startsWith("text_")).length;
					if (currentCount > 1) {
						node.removeInput(node.findInputSlot(`text_${currentCount}`));
						syncWidgets(node);
					}
				});

				// Configure le callback pour le sélecteur de mode
				node.widgets.find(w => w.name === "select_mode").callback = () => syncWidgets(node);

				syncWidgets(node);
			};
		}
	},
});