import {
	Entity,
	EntityComponentTypes,
	EntityInitializationCause,
	EquipmentSlot,
	GameMode,
	ItemStack,
	Player,
	system,
	world,
} from "@minecraft/server";
import { BOAT_FAMILY, BOAT_HITS } from "./constants";

// Blocks per tick
const FORWARD_SPEED = 1.34 / 20;
const BACKWARD_SPEED = 0.005;
const TURN_SPEED = 6;
const PLACING_DISTANCE = 8;
const HIT_DAMAGE = 10;
const BREAKING_DAMAGE = 40;
const HITS_WRAP = 16;

const damaged = new Map<string, { boat: Entity; damage: number }>();

function isBoat(entity: Entity | undefined): entity is Entity {
	return !!entity?.isValid && entity.matches({ families: [BOAT_FAMILY] });
}

// The boat and its item share their identifier
function breakBoat(boat: Entity, creative: boolean): void {
	const { dimension, location } = boat;
	if (!creative) dimension.spawnItem(new ItemStack(boat.typeId), location);
	const chest = boat.getComponent(EntityComponentTypes.Inventory)?.container;
	for (let slot = 0; chest && slot < chest.size; slot++) {
		const item = chest.getItem(slot);
		if (item) dimension.spawnItem(item, location);
	}
	damaged.delete(boat.id);
	boat.remove();
}

function hitBoat(boat: Entity, attacker: Entity | undefined): void {
	const player = attacker instanceof Player ? attacker : undefined;
	const creative = player?.getGameMode() === GameMode.Creative;
	const held = player
		?.getComponent(EntityComponentTypes.Equippable)
		?.getEquipment(EquipmentSlot.Mainhand);
	if (creative || held?.hasTag("minecraft:is_axe")) return breakBoat(boat, creative);

	const damage = (damaged.get(boat.id)?.damage ?? 0) + HIT_DAMAGE;
	if (damage > BREAKING_DAMAGE) return breakBoat(boat, false);
	damaged.set(boat.id, { boat, damage });
	const hits = (boat.getProperty(BOAT_HITS) as number | undefined) ?? 0;
	boat.setProperty(BOAT_HITS, (hits + 1) % HITS_WRAP);
}

function steer(player: Player): void {
	const boat = player.getComponent(EntityComponentTypes.Riding)?.entityRidingOn;
	if (!isBoat(boat)) return;
	if (boat.getComponent(EntityComponentTypes.Rideable)?.getRiders()[0]?.id !== player.id) return;

	// x is 1 for A and -1 for D; yaw grows turning right
	const { x, y: move } = player.inputInfo.getMovementVector();
	if (x === 0 && move === 0) return;

	const yaw = boat.getRotation().y - x * TURN_SPEED;
	boat.setRotation({ x: 0, y: yaw });
	if (move === 0) return;

	const speed = move * (move > 0 ? FORWARD_SPEED : BACKWARD_SPEED);
	const radians = (yaw * Math.PI) / 180;
	boat.applyImpulse({ x: -Math.sin(radians) * speed, y: 0, z: Math.cos(radians) * speed });
}

export function registerBoatEvents(): void {
	world.afterEvents.entityHitEntity.subscribe(({ damagingEntity, hitEntity }) => {
		if (isBoat(hitEntity)) hitBoat(hitEntity, damagingEntity);
	});
	world.afterEvents.projectileHitEntity.subscribe((event) => {
		const boat = event.getEntityHit()?.entity;
		if (isBoat(boat)) hitBoat(boat, event.source);
	});

	// Placed boats face away from the player
	world.afterEvents.entitySpawn.subscribe(({ entity, cause }) => {
		if (cause !== EntityInitializationCause.Spawned || !isBoat(entity)) return;
		const [player] = entity.dimension.getPlayers({
			location: entity.location,
			maxDistance: PLACING_DISTANCE,
			closest: 1,
		});
		if (player) entity.setRotation({ x: 0, y: player.getRotation().y });
	});

	system.runInterval(() => {
		for (const player of world.getAllPlayers()) steer(player);
		for (const [id, hit] of damaged) {
			hit.damage--;
			if (hit.damage <= 0 || !hit.boat.isValid) damaged.delete(id);
		}
	});
}
