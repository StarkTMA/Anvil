import {
	BlockCustomComponentInstance,
	BlockPermutation,
	StartupEvent,
	world,
} from "@minecraft/server";
import {
	BLOCK_FACE,
	CARDINAL_DIRECTION,
	FACE_OFFSETS,
	STANDING,
	SUPPORT_COMPONENT_ID,
	SupportParams,
} from "./constants";

const OPPOSITE: Record<string, string> = {
	north: "south",
	south: "north",
	east: "west",
	west: "east",
};

// Which way the block sits from the block holding it up
function directionFromSupport(permutation: BlockPermutation, params?: SupportParams): string {
	switch (params?.supported_by) {
		case "block_face":
			return permutation.getState(BLOCK_FACE) as string;
		case "facing":
			return OPPOSITE[permutation.getState(CARDINAL_DIRECTION) as string];
		case "sign":
			return permutation.getState(STANDING) === false
				? OPPOSITE[permutation.getState(CARDINAL_DIRECTION) as string]
				: "up";
		default:
			return "up";
	}
}

// Marks a block that breaks when the block it is attached to is broken.
export function registerSupportComponent(init: StartupEvent): void {
	init.blockComponentRegistry.registerCustomComponent(SUPPORT_COMPONENT_ID, {});
}

// World events can't be subscribed during startup: call this on world load.
export function registerSupportEvents(): void {
	world.afterEvents.playerBreakBlock.subscribe(({ block }) => {
		for (const [face, offset] of Object.entries(FACE_OFFSETS)) {
			const neighbour = block.offset(offset);
			const support = neighbour?.getComponent(SUPPORT_COMPONENT_ID) as
				| BlockCustomComponentInstance
				| undefined;
			if (!neighbour || !support) continue;
			const params = support.customComponentParameters.params as SupportParams | undefined;
			if (directionFromSupport(neighbour.permutation, params) === face) {
				neighbour.dimension.runCommand(
					`setblock ${neighbour.x} ${neighbour.y} ${neighbour.z} air destroy`,
				);
			}
		}
	});
}
