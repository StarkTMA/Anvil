import { StartupEvent, Vector3 } from "@minecraft/server";
import { CARDINAL_DIRECTION, DOOR_COMPONENT_ID, HINGE_RIGHT, NAMESPACE } from "./constants";

const SIDE_OFFSETS: Record<string, { left: Vector3; right: Vector3 }> = {
	north: { left: { x: -1, y: 0, z: 0 }, right: { x: 1, y: 0, z: 0 } },
	south: { left: { x: 1, y: 0, z: 0 }, right: { x: -1, y: 0, z: 0 } },
	east: { left: { x: 0, y: 0, z: -1 }, right: { x: 0, y: 0, z: 1 } },
	west: { left: { x: 0, y: 0, z: 1 }, right: { x: 0, y: 0, z: -1 } },
};

export function registerDoorComponent(init: StartupEvent): void {
	init.blockComponentRegistry.registerCustomComponent(DOOR_COMPONENT_ID, {
		beforeOnPlayerPlace: (event) => {
			const permutation = event.permutationToPlace;
			const facing = permutation.getState(CARDINAL_DIRECTION) as string;
			const sides = SIDE_OFFSETS[facing];
			const neighbours = [sides.right, sides.left].map((offset) => {
				const block = event.block.offset(offset);
				if (!block?.typeId.endsWith("_door")) return false;
				return (
					!block.typeId.startsWith(`${NAMESPACE}:`) ||
					block.permutation.getState(CARDINAL_DIRECTION) === facing
				);
			});
			if (neighbours[0] || !neighbours[1]) return;
			event.permutationToPlace = permutation.withState(HINGE_RIGHT, true);
		},
	});
}
