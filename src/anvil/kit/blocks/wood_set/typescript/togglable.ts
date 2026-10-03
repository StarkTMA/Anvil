import { Block, StartupEvent } from "@minecraft/server";
import { POWERED, TOGGLABLE_COMPONENT_ID } from "./constants";

function switchOn({ block }: { block: Block }): void {
	if (block.permutation.getState(POWERED) !== true) {
		block.setPermutation(block.permutation.withState(POWERED, true));
	}
}

// Switches on when interacted with or stepped on, and back off on tick (button, pressure plate).
export function registerTogglableComponent(init: StartupEvent): void {
	init.blockComponentRegistry.registerCustomComponent(TOGGLABLE_COMPONENT_ID, {
		onPlayerInteract: switchOn,
		onStepOn: switchOn,
		onTick: ({ block }) => {
			if (block.dimension.getEntitiesAtBlockLocation(block.location).length > 0)
				return;
			if (block.permutation.getState(POWERED) !== false) {
				block.setPermutation(block.permutation.withState(POWERED, false));
			}
		},
	});
}
