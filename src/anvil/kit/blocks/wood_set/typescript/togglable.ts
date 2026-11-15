import { Block, StartupEvent, system } from "@minecraft/server";
import { playSound, POWERED, TOGGLABLE_COMPONENT_ID, TogglableParams } from "./constants";

const RELEASE_TICKS = 20;

// Switches back off once nothing stands on the block. Returns whether it is still on.
function switchOffWhenClear(block: Block, params: TogglableParams): boolean {
	if (!block.isValid || block.permutation.getState(POWERED) !== true) return false;
	if (block.dimension.getEntitiesAtBlockLocation(block.location).length > 0)
		return true;
	block.setPermutation(block.permutation.withState(POWERED, false));
	playSound(block, params.off_sound);
	return false;
}

// The blocks only tick while on, which the engine may not start when a script turns them on:
// this checks on its own as well, so they can't stay on
function releaseSoon(block: Block, params: TogglableParams): void {
	system.runTimeout(() => {
		if (switchOffWhenClear(block, params)) releaseSoon(block, params);
	}, RELEASE_TICKS);
}

function switchOn({ block }: { block: Block }, { params }: { params: unknown }): void {
	if (block.permutation.getState(POWERED) !== true) {
		block.setPermutation(block.permutation.withState(POWERED, true));
		playSound(block, (params as TogglableParams).on_sound);
		releaseSoon(block, params as TogglableParams);
	}
}

// Switches on when stepped on, and when interacted with unless `on_interact` is off (a pressure
// plate), and back off once clear (button, pressure plate). They tick only while on.
export function registerTogglableComponent(init: StartupEvent): void {
	init.blockComponentRegistry.registerCustomComponent(TOGGLABLE_COMPONENT_ID, {
		onPlayerInteract: (event, args) => {
			if ((args.params as TogglableParams).on_interact !== false) switchOn(event, args);
		},
		onStepOn: switchOn,
		onTick: ({ block }, { params }) => {
			switchOffWhenClear(block, params as TogglableParams);
		},
	});
}
