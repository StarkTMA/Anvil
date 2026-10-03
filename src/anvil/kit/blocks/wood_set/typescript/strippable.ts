import {
	BlockPermutation,
	EntityComponentTypes,
	EquipmentSlot,
	StartupEvent,
} from "@minecraft/server";
import { STRIPPABLE_COMPONENT_ID, StrippableParams } from "./constants";

// An axe turns the block into the block named in `stripped_block`, keeping its states (rotation included).
export function registerStrippableComponent(init: StartupEvent): void {
	init.blockComponentRegistry.registerCustomComponent(STRIPPABLE_COMPONENT_ID, {
		onPlayerInteract: ({ block, player }, { params }) => {
			const held = player
				?.getComponent(EntityComponentTypes.Equippable)
				?.getEquipment(EquipmentSlot.Mainhand);
			if (!held?.hasTag("minecraft:is_axe")) return;

			block.setPermutation(
				BlockPermutation.resolve(
					(params as StrippableParams).stripped_block,
					block.permutation.getAllStates(),
				),
			);
		},
	});
}
