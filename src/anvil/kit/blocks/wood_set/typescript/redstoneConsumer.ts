import { StartupEvent } from "@minecraft/server";
import {
	MultiPartParams,
	OPEN,
	REDSTONE_CONSUMER_COMPONENT_ID,
} from "./constants";

// Opens and closes with redstone power.
export function registerRedstoneConsumerComponent(init: StartupEvent): void {
	init.blockComponentRegistry.registerCustomComponent(
		REDSTONE_CONSUMER_COMPONENT_ID,
		{
			onRedstoneUpdate: ({ block, powerLevel }, { params }) => {
				const parts = (params as MultiPartParams).multi_part
					? (block.getParts() ?? [])
					: [block];
				for (const part of parts) {
					part.setPermutation(part.permutation.withState(OPEN, powerLevel > 0));
				}
			},
		},
	);
}
