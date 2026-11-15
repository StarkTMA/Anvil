import { StartupEvent } from "@minecraft/server";
import {
	MultiPartParams,
	OPEN,
	playSound,
	POWERED,
	REDSTONE_CONSUMER_COMPONENT_ID,
} from "./constants";

export function registerRedstoneConsumerComponent(init: StartupEvent): void {
	init.blockComponentRegistry.registerCustomComponent(
		REDSTONE_CONSUMER_COMPONENT_ID,
		{
			onRedstoneUpdate: ({ block, powerLevel }, { params }) => {
				const powered = powerLevel > 0;
				const wasPowered = block.permutation.getState(POWERED) === true;
				if (powered === wasPowered) return;

				const { multi_part, open_sound, close_sound } = params as MultiPartParams;
				const parts = multi_part ? (block.getParts() ?? []) : [block];
				const othersPowered = parts.some(
					(part) =>
						(part.x !== block.x || part.y !== block.y || part.z !== block.z) &&
						part.permutation.getState(POWERED) === true,
				);

				block.setPermutation(block.permutation.withState(POWERED, powered));
				if ((wasPowered || othersPowered) === (powered || othersPowered)) return;

				for (const part of parts) {
					part.setPermutation(
						part.permutation.withState(OPEN, powered || othersPowered),
					);
				}
				playSound(block, powered || othersPowered ? open_sound : close_sound);
			},
		},
	);
}
