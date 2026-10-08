import { Block, StartupEvent, system } from "@minecraft/server";
import { POWERED, TOGGLABLE_COMPONENT_ID } from "./constants";

const RELEASE_TICKS = 20;

// Switches back off once nothing stands on the block. Returns whether it is still on.
function switchOffWhenClear(block: Block): boolean {
	if (!block.isValid || block.permutation.getState(POWERED) !== true) return false;
	if (block.dimension.getEntitiesAtBlockLocation(block.location).length > 0)
		return true;
	block.setPermutation(block.permutation.withState(POWERED, false));
	return false;
}

// The blocks only tick while on, which the engine may not start when a script turns them on:
// this checks on its own as well, so they can't stay on
function releaseSoon(block: Block): void {
	system.runTimeout(() => {
		if (switchOffWhenClear(block)) releaseSoon(block);
	}, RELEASE_TICKS);
}

function switchOn({ block }: { block: Block }): void {
	if (block.permutation.getState(POWERED) !== true) {
		block.setPermutation(block.permutation.withState(POWERED, true));
		releaseSoon(block);
	}
}

// Switches on when interacted with or stepped on, and back off once clear (button, pressure
// plate). They tick only while on.
export function registerTogglableComponent(init: StartupEvent): void {
	init.blockComponentRegistry.registerCustomComponent(TOGGLABLE_COMPONENT_ID, {
		onPlayerInteract: switchOn,
		onStepOn: switchOn,
		onTick: ({ block }) => {
			switchOffWhenClear(block);
		},
	});
}
