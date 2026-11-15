import {
	BlockCustomComponentInstance,
	BlockPermutation,
	EntityComponentTypes,
	EquipmentSlot,
	StartupEvent,
	system,
	world,
} from "@minecraft/server";
import { STRIPPABLE_COMPONENT_ID, StrippableParams } from "./constants";

export function registerStrippableComponent(init: StartupEvent): void {
	init.blockComponentRegistry.registerCustomComponent(STRIPPABLE_COMPONENT_ID, {});
}

export function registerStrippableEvents(): void {
	world.beforeEvents.playerInteractWithBlock.subscribe((event) => {
		const { block, player, itemStack, isFirstEvent } = event;
		if (!isFirstEvent || !itemStack?.hasTag("minecraft:is_axe")) return;
		const strippable = block.getComponent(STRIPPABLE_COMPONENT_ID) as
			| BlockCustomComponentInstance
			| undefined;
		if (!strippable) return;
		const params = strippable.customComponentParameters.params as StrippableParams;

		const held = player
			.getComponent(EntityComponentTypes.Equippable)
			?.getEquipment(EquipmentSlot.Mainhand);
		if (!held?.hasTag("minecraft:is_axe")) return;

		system.run(() => {
			if (!block.isValid) return;
			block.setPermutation(
				BlockPermutation.resolve(
					params.stripped_block,
					block.permutation.getAllStates(),
				),
			);
		});
	});
}
