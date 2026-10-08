import {
	Block,
	EntityComponentTypes,
	EquipmentSlot,
	GameMode,
	StartupEvent,
} from "@minecraft/server";
import { SAPLING_COMPONENT_ID, SaplingParams, STAGE } from "./constants";

const BONE_MEAL = "minecraft:bone_meal";
// The chance to advance a stage on a random tick, and on a bone meal as in vanilla
const RANDOM_TICK_CHANCE = 1 / 7;
// The light a sapling needs to grow by itself, as in vanilla
const MIN_LIGHT = 9;
const GROWTH_PARTICLE = "minecraft:crop_growth_emitter";
const BONE_MEAL_CHANCE = 0.45;

// Turns the sapling into the tree, and brings it back if the tree doesn't fit
function grow(block: Block, params: SaplingParams): void {
	const sapling = block.permutation;
	block.setType("minecraft:air");
	const placed = block.dimension.placeFeature(params.tree_feature, block.location);
	if (!placed) block.setPermutation(sapling);
}

// The first call moves the sapling to its second stage, the second one grows the tree
function advance(block: Block, params: SaplingParams): void {
	if (block.permutation.getState(STAGE) === true) grow(block, params);
	else block.setPermutation(block.permutation.withState(STAGE, true));
}

export function registerSaplingComponent(init: StartupEvent): void {
	init.blockComponentRegistry.registerCustomComponent(SAPLING_COMPONENT_ID, {
		onRandomTick: ({ block }, { params }) => {
			if (!block.isValid || (block.above()?.getLightLevel() ?? 0) < MIN_LIGHT) return;
			if (Math.random() < RANDOM_TICK_CHANCE) advance(block, params as SaplingParams);
		},

		// Bone meal grows it at once in creative, and advances a stage by chance in survival
		onPlayerInteract: ({ block, player }, { params }) => {
			if (!player) return;
			const hand = player
				.getComponent(EntityComponentTypes.Equippable)
				?.getEquipmentSlot(EquipmentSlot.Mainhand);
			if (hand?.typeId !== BONE_MEAL) return;

			const creative = player.getGameMode() === GameMode.Creative;
			if (!creative) {
				if (hand.amount > 1) hand.amount -= 1;
				else hand.setItem(undefined);
			}
			block.dimension.spawnParticle(GROWTH_PARTICLE, block.center());
			if (creative) grow(block, params as SaplingParams);
			else if (Math.random() < BONE_MEAL_CHANCE) advance(block, params as SaplingParams);
		},
	});
}
