import {
	Block,
	BlockPermutation,
	StartupEvent,
	world,
} from "@minecraft/server";
import {
	FACE_OFFSETS,
	LEAVES_COMPONENT_ID,
	LeavesParams,
	NATURAL,
} from "./constants";

const DEFAULT_DISTANCE = 4;
const OFFSETS = Object.values(FACE_OFFSETS);

const LOG_TAG = "log";
const LEAVES_TAG = "minecraft:leaves";

// Whether a log is within `distance` blocks, going through leaves of any kind, like vanilla.
// Any log or wood counts (the set's own trunks too). A block that can't be read (an unloaded chunk) counts as held up, so leaves at the
// edge of the loaded world don't decay by mistake.
function isHeldUp(origin: Block, params: LeavesParams): boolean {
	const distance = params.distance ?? DEFAULT_DISTANCE;
	const trunks = new Set(params.trunks);
	const key = (block: Block) => `${block.x},${block.y},${block.z}`;
	const seen = new Set([key(origin)]);
	let frontier = [origin];

	for (let steps = 1; steps <= distance; steps++) {
		const next: Block[] = [];
		for (const block of frontier) {
			for (const offset of OFFSETS) {
				let neighbour: Block | undefined;
				try {
					neighbour = block.offset(offset);
				} catch (e) {
					return true;
				}
				if (!neighbour) return true;
				if (trunks.has(neighbour.typeId) || neighbour.hasTag(LOG_TAG)) return true;
				if (!neighbour.hasTag(LEAVES_TAG) || seen.has(key(neighbour))) continue;
				seen.add(key(neighbour));
				next.push(neighbour);
			}
		}
		frontier = next;
	}
	return false;
}

function decay(block: Block, params: LeavesParams): void {
	if (!block.isValid || block.permutation.getState(NATURAL) !== true) return;
	if (isHeldUp(block, params)) return;

	// Decaying: set block permutation to air, then spawn loot generated via LootTableManager
	const permutation = block.permutation;
	const location = block.center();
	const dimension = block.dimension;

	block.setPermutation(BlockPermutation.resolve("minecraft:air"));

	try {
		const loot = world
			.getLootTableManager()
			.generateLootFromBlockPermutation(permutation);
		if (loot) {
			for (const item of loot) {
				dimension.spawnItem(item, location);
			}
		}
	} catch (e) {}
}

export function registerLeavesComponent(init: StartupEvent): void {
	init.blockComponentRegistry.registerCustomComponent(LEAVES_COMPONENT_ID, {
		// Random ticks, like vanilla leaves. Only natural leaves decay: placed ones stay
		onRandomTick: ({ block }, { params }) => decay(block, params as LeavesParams),
	});
}
