import { StartupEvent } from "@minecraft/server";
import { INTERACTABLE_COMPONENT_ID, MultiPartParams, OPEN, playSound } from "./constants";

// Opens and closes when a player interacts with it (door, trapdoor, fence gate).
export function registerInteractableComponent(init: StartupEvent): void {
	init.blockComponentRegistry.registerCustomComponent(INTERACTABLE_COMPONENT_ID, {
		onPlayerInteract: ({ block }, { params }) => {
			const open = !block.permutation.getState(OPEN);
			const { multi_part, open_sound, close_sound } = params as MultiPartParams;
			const parts = multi_part ? (block.getParts() ?? []) : [block];
			for (const part of parts) {
				part.setPermutation(part.permutation.withState(OPEN, open));
			}
			playSound(block, open ? open_sound : close_sound);
		},
	});
}
