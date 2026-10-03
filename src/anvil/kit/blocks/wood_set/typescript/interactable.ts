import { StartupEvent } from "@minecraft/server";
import { INTERACTABLE_COMPONENT_ID, MultiPartParams, OPEN } from "./constants";

// Opens and closes when a player interacts with it (door, trapdoor, fence gate).
export function registerInteractableComponent(init: StartupEvent): void {
	init.blockComponentRegistry.registerCustomComponent(INTERACTABLE_COMPONENT_ID, {
		onPlayerInteract: ({ block }, { params }) => {
			const open = !block.permutation.getState(OPEN);
			const parts = (params as MultiPartParams).multi_part
				? (block.getParts() ?? [])
				: [block];
			for (const part of parts) {
				part.setPermutation(part.permutation.withState(OPEN, open));
			}
		},
	});
}
