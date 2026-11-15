import {
	Direction,
	EntityComponentTypes,
	EquipmentSlot,
	GameMode,
	ItemStack,
	Player,
	StartupEvent,
	system,
	world,
} from "@minecraft/server";
import {
	DOUBLE,
	FACE_OFFSETS,
	FaceName,
	SLAB_COMPONENT_ID,
	VERTICAL_HALF,
} from "./constants";

function consumeHeldItem(player: Player | undefined): void {
	if (!player || player.getGameMode() === GameMode.Creative) return;
	const equippable = player.getComponent(EntityComponentTypes.Equippable);
	const held = equippable?.getEquipment(EquipmentSlot.Mainhand);
	if (!held) return;
	if (held.amount > 1) {
		held.amount--;
		equippable?.setEquipment(EquipmentSlot.Mainhand, held);
	} else {
		equippable?.setEquipment(EquipmentSlot.Mainhand, undefined);
	}
}

// Slab: clicking the flat face of a single slab with the same slab makes it a double slab,
// and a double slab drops two slabs.
export function registerSlabComponent(init: StartupEvent): void {
	init.blockComponentRegistry.registerCustomComponent(SLAB_COMPONENT_ID, {
		beforeOnPlayerPlace: (event) => {
			const { block, face, player } = event;
			const slabId = event.permutationToPlace.type.id;

			// The clicked block sits on the other side of the face the placement came through.
			const offset = FACE_OFFSETS[face.toLowerCase() as FaceName];
			const clicked = block.offset({ x: -offset.x, y: -offset.y, z: -offset.z });
			if (
				clicked?.typeId !== slabId ||
				clicked.permutation.getState(DOUBLE) !== false
			)
				return;

			// Only the exposed flat face merges: the top of a bottom slab, the bottom of a top slab.
			const flatFace =
				clicked.permutation.getState(VERTICAL_HALF) === "bottom"
					? Direction.Up
					: Direction.Down;
			if (face !== flatFace) return;

			event.cancel = true;
			system.run(() => {
				if (
					clicked.typeId !== slabId ||
					clicked.permutation.getState(DOUBLE) !== false
				)
					return;

				clicked.setPermutation(clicked.permutation.withState(DOUBLE, true));
				clicked.dimension.playSound("use.wood", clicked.center());
				consumeHeldItem(player);
			});
		},

		// A double slab is two slabs: the engine drops one, drop the second.
		onPlayerBreak: ({ block, brokenBlockPermutation, dimension, player }) => {
			if (brokenBlockPermutation.getState(DOUBLE) !== true) return;
			if (!player || player.getGameMode() === GameMode.Creative) return;

			dimension.spawnItem(
				new ItemStack(brokenBlockPermutation.type.id),
				block.center(),
			);
		},
	});
}

// World events can't be subscribed during startup: call this on world load.
// Clicking a block whose neighbouring cell holds a single slab places a double slab there.
// The engine fires no placement for an occupied cell, so the slab component never sees it.
export function registerSlabEvents(): void {
	world.beforeEvents.playerInteractWithBlock.subscribe((event) => {
		const { block, blockFace, itemStack, player } = event;
		if (!itemStack) return;

		const slabId = itemStack.typeId;
		if (block.typeId === slabId && block.permutation.getState(DOUBLE) === false)
			return;

		const slab = block.offset(FACE_OFFSETS[blockFace.toLowerCase() as FaceName]);
		if (slab?.typeId !== slabId || slab.permutation.getState(DOUBLE) !== false)
			return;

		event.cancel = true;
		system.run(() => {
			if (slab.typeId !== slabId || slab.permutation.getState(DOUBLE) !== false)
				return;

			slab.setPermutation(slab.permutation.withState(DOUBLE, true));
			slab.dimension.playSound("use.wood", slab.center());
			consumeHeldItem(player);
		});
	});
}
