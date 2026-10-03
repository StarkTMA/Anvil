import {
	Block,
	BlockDynamicPropertiesComponent,
	BlockPermutation,
	EntityComponentTypes,
	EquipmentSlot,
	GameMode,
	Player,
	type RGBA,
	StartupEvent,
	system,
	TextPrimitive,
	type Vector3,
	world,
} from "@minecraft/server";
import {
	CustomForm,
	DataDrivenScreenClosedReason,
	ObservableBoolean,
	ObservableString,
} from "@minecraft/server-ui";
import {
	BLOCK_FACE,
	CARDINAL_DIRECTION,
	SIGN_COLOR,
	SIGN_COMPONENT_ID,
	SIGN_GLOWING,
	SIGN_TEXT,
	SignParams,
	SIXTEEN_WAY_ROTATION,
} from "./constants";

const MAX_LINES = 4;
const FORMATTING_CODES = /§[0-9a-v]/gi;
const COLOR_CODES = /§[0-9a-jmnpqs-v]/gi;
const LINE_BREAKS = /\r\n|\r|\n/g;

const DYE_COLORS = {
	white: [249, 255, 254],
	orange: [249, 128, 29],
	magenta: [199, 78, 189],
	light_blue: [58, 179, 218],
	yellow: [254, 216, 61],
	lime: [128, 199, 31],
	pink: [243, 139, 170],
	gray: [71, 79, 82],
	light_gray: [157, 157, 151],
	cyan: [22, 156, 156],
	purple: [137, 50, 184],
	blue: [60, 68, 170],
	brown: [131, 84, 50],
	green: [94, 124, 22],
	red: [176, 46, 38],
	black: [29, 29, 33],
} as const;
type DyeColor = keyof typeof DYE_COLORS;
const DYED_BRIGHTNESS = 0.2;
const OUTLINE_BRIGHTNESS = 0.25;
const BLACK: RGBA = { red: 0, green: 0, blue: 0, alpha: 1 };
const CREAM: RGBA = { red: 240 / 255, green: 235 / 255, blue: 204 / 255, alpha: 1 };

const DEFAULT_TEXT_SCALE = 0.46;
const OUTLINE_WIDTH = 0.0125;
const OUTLINE_DEPTH = 0.002;
const OUTLINE_OFFSETS = [
	[1, 0],
	[-1, 0],
	[0, 1],
	[0, -1],
	[1, 1],
	[1, -1],
	[-1, 1],
	[-1, -1],
] as const;

const ANGLES: Record<string, number> = { north: 0, west: 90, south: 180, east: 270 };
const OPPOSITE: Record<string, string> = {
	north: "south",
	south: "north",
	east: "west",
	west: "east",
};

const signShapes = new Map<string, TextPrimitive[][]>();

function signAngle(permutation: BlockPermutation): number {
	const face = permutation.getState(BLOCK_FACE) as string | undefined;
	if (face && face in ANGLES) return (ANGLES[face] + 90) % 360;
	const cardinal = permutation.getState(CARDINAL_DIRECTION) as string | undefined;
	if (cardinal) return ANGLES[cardinal];
	return (
		((permutation.getState(SIXTEEN_WAY_ROTATION) as number | undefined) ?? 0) *
		-22.5
	);
}

function sideAngles(permutation: BlockPermutation, params?: SignParams): number[] {
	const angle = signAngle(permutation);
	return params?.double_sided ? [angle, angle + 180] : [angle];
}

function turned(angle: number, x: number, z: number): [number, number] {
	const radians = (angle * Math.PI) / 180;
	const [cos, sin] = [Math.cos(radians), Math.sin(radians)];
	return [x * cos + z * sin, -x * sin + z * cos];
}

function textLocation(block: Block, angle: number, params?: SignParams): Vector3 {
	const [x = 0, y = 0, z = 0] = params?.text_offset ?? [];
	const [dx, dz] = turned(angle, x - 8, z - 8);
	return {
		x: block.location.x + (8 + dx) / 16,
		y: block.location.y + y / 16,
		z: block.location.z + (8 + dz) / 16,
	};
}

function outlineLocations(location: Vector3, angle: number, scale: number): Vector3[] {
	const width = (OUTLINE_WIDTH * scale) / DEFAULT_TEXT_SCALE;
	const depth = (OUTLINE_DEPTH * scale) / DEFAULT_TEXT_SCALE;
	const [alongX, alongZ] = turned(angle, 1, 0);
	const [outX, outZ] = turned(angle, 0, 1);
	return OUTLINE_OFFSETS.map(([along, up]) => ({
		x: location.x + alongX * along * width - outX * depth,
		y: location.y + up * width,
		z: location.z + alongZ * along * width - outZ * depth,
	}));
}

function visibleLength(line: string): number {
	return Array.from(line.replace(FORMATTING_CODES, "")).length;
}

function signTextProblem(lines: string[], maxLength: number): string | undefined {
	const tooLong = lines.findIndex((line) => visibleLength(line) > maxLength);
	if (tooLong >= 0)
		return `Line ${tooLong + 1} is longer than ${maxLength} characters.`;
	if (lines.join("\n").length > 256) return "The text uses too much formatting.";
	return undefined;
}

function readLines(fields: ObservableString[]): string[] {
	return fields.map((field) => field.getData().replace(LINE_BREAKS, " "));
}

function carryFormatting(lines: string[]): string[] {
	let active = "";
	return lines.map((line) => {
		const shown = active + line;
		const codes = (shown.match(FORMATTING_CODES) ?? []).join("");
		const reset = codes.toLowerCase().lastIndexOf("§r");
		active = reset >= 0 ? codes.slice(reset + 2) : codes;
		return shown;
	});
}

function displayText(saved: unknown, dye?: DyeColor): string {
	const lines = typeof saved === "string" ? saved.split(LINE_BREAKS) : [];
	const shown = carryFormatting(
		dye ? lines.map((line) => line.replace(COLOR_CODES, "")) : lines,
	).filter((line) => visibleLength(line) > 0);
	while (shown.length < MAX_LINES) shown.push(" ");
	return shown.join("\n");
}

function dyeColor(dye: DyeColor, brightness: number): RGBA {
	const [red, green, blue] = DYE_COLORS[dye].map(
		(value) => (value / 255) * brightness,
	);
	return { red, green, blue, alpha: 1 };
}

function applyHeldItem(player: Player, block: Block, params?: SignParams): boolean {
	const equippable = player.getComponent(EntityComponentTypes.Equippable);
	const held = equippable?.getEquipment(EquipmentSlot.Mainhand);
	const properties = block.getComponent(BlockDynamicPropertiesComponent.componentId);
	if (!equippable || !held || !properties) return false;

	const dye = /^minecraft:(\w+)_dye$/.exec(held.typeId)?.[1];
	let key: string;
	let value: string | boolean;
	if (dye && dye in DYE_COLORS) [key, value] = [SIGN_COLOR, dye];
	else if (held.typeId === "minecraft:glow_ink_sac")
		[key, value] = [SIGN_GLOWING, true];
	else if (held.typeId === "minecraft:ink_sac") [key, value] = [SIGN_GLOWING, false];
	else return false;

	if ((properties.get(key) ?? false) === value) return true;
	properties.set(key, value);
	if (player.getGameMode() !== GameMode.Creative) {
		const last = held.amount === 1;
		if (!last) held.amount--;
		equippable.setEquipment(EquipmentSlot.Mainhand, last ? undefined : held);
	}
	updateBlockPrimitiveText(block, params);
	return true;
}

async function editSignText(
	player: Player,
	block: Block,
	params?: SignParams,
): Promise<void> {
	const typeId = block.typeId;
	const maxLength = params?.line_length ?? 15;
	const saved = block
		.getComponent(BlockDynamicPropertiesComponent.componentId)
		?.get(SIGN_TEXT);
	const savedLines = typeof saved === "string" ? saved.split(LINE_BREAKS) : [];
	const fields = Array.from(
		{ length: MAX_LINES },
		(_, index) =>
			new ObservableString(savedLines[index] ?? "", { clientWritable: true }),
	);

	const error = new ObservableString("");
	const hasError = new ObservableBoolean(false);
	const showProblem = () => {
		const problem = signTextProblem(readLines(fields), maxLength);
		error.setData(problem ? `§c${problem}` : "");
		hasError.setData(problem !== undefined);
	};
	fields.forEach((field) => field.subscribe(showProblem));
	showProblem();

	let save = false;
	const form = new CustomForm(player, "Sign");
	fields.forEach((field, index) => form.textField(`Line ${index + 1}`, field));
	form.label(error, { visible: hasError });
	form.button(
		"Save",
		() => {
			save = true;
			form.close();
		},
		{ disabled: hasError },
	);

	for (
		let retry = 0;
		retry < 20 && (await form.show()) === DataDrivenScreenClosedReason.UserBusy;
		retry++
	)
		await system.waitTicks(1);

	const lines = readLines(fields);
	if (
		!save ||
		!block.isValid ||
		block.typeId !== typeId ||
		signTextProblem(lines, maxLength)
	)
		return;
	while (lines.at(-1) === "") lines.pop();
	block
		.getComponent(BlockDynamicPropertiesComponent.componentId)
		?.set(SIGN_TEXT, lines.join("\n"));
}

function signKey(block: Block): string {
	const { x, y, z } = block.location;
	return `${block.dimension.id}|${x},${y},${z}`;
}

function removeLeftovers(block: Block, location: Vector3): void {
	for (const shape of world.primitiveShapesManager.getShapes({
		location,
		maxDistance: 0.1,
	})) {
		const { x, y, z } = shape.location ?? { x: Infinity, y: 0, z: 0 };
		const near = Math.hypot(x - location.x, y - location.y, z - location.z) <= 0.1;
		const dimension = shape.dimension?.id ?? block.dimension.id;
		if (near && dimension === block.dimension.id && "setText" in shape)
			shape.remove();
	}
}

function trackedShapes(block: Block, locations: Vector3[]): TextPrimitive[][] {
	let sides = signShapes.get(signKey(block));
	if (!sides) {
		for (const location of locations) removeLeftovers(block, location);
		sides = locations.map(() => []);
		signShapes.set(signKey(block), sides);
	}
	return sides;
}

function showText(
	shapes: TextPrimitive[],
	index: number,
	block: Block,
	location: Vector3,
	text: string,
	color: RGBA,
	angle: number,
	scale: number,
): void {
	const shape = shapes[index] ?? new TextPrimitive(location, text);
	shape.setText(text);
	shape.rotation = { x: 0, y: (((180 + angle) % 360) + 360) % 360, z: 0 };
	shape.useRotation = true;
	shape.scale = scale;
	shape.color = color;
	shape.backfaceVisible = false;
	shape.backgroundColorOverride = { red: 0, green: 0, blue: 0, alpha: 0 };
	shape.depthTest = true;
	if (!shapes[index]) {
		world.primitiveShapesManager.addText(shape, block.dimension);
		shapes[index] = shape;
	}
}

function updateBlockPrimitiveText(block: Block, params?: SignParams): void {
	const properties = block.getComponent(BlockDynamicPropertiesComponent.componentId);
	if (!properties) return;

	const stored = properties.get(SIGN_COLOR);
	const dye =
		typeof stored === "string" && stored in DYE_COLORS
			? (stored as DyeColor)
			: undefined;
	const glowing = properties.get(SIGN_GLOWING) === true;
	const text = displayText(properties.get(SIGN_TEXT), dye);
	const color = dye ? dyeColor(dye, glowing ? 1 : DYED_BRIGHTNESS) : BLACK;
	const outline = !dye || dye === "black" ? CREAM : dyeColor(dye, OUTLINE_BRIGHTNESS);
	const scale = params?.text_scale ?? DEFAULT_TEXT_SCALE;
	const angles = sideAngles(block.permutation, params);
	const locations = angles.map((angle) => textLocation(block, angle, params));
	const sides = trackedShapes(block, locations);

	try {
		angles.forEach((angle, side) => {
			const shapes = (sides[side] ??= []);
			showText(shapes, 0, block, locations[side], text, color, angle, scale);
			if (!glowing) {
				for (const copy of shapes.splice(1)) copy.remove();
				return;
			}
			const outlineText = text.replace(COLOR_CODES, "");
			outlineLocations(locations[side], angle, scale).forEach((location, index) =>
				showText(
					shapes,
					index + 1,
					block,
					location,
					outlineText,
					outline,
					angle,
					scale,
				),
			);
		});
	} catch (error) {
		signShapes.delete(signKey(block));
		throw error;
	}
}

export function registerSignComponent(init: StartupEvent): void {
	init.blockComponentRegistry.registerCustomComponent(SIGN_COMPONENT_ID, {
		beforeOnPlayerPlace: (event, { params }) => {
			const sign = params as SignParams | undefined;
			const wall = OPPOSITE[event.face.toLowerCase()];
			if (sign?.wall_sign && wall) {
				event.permutationToPlace = BlockPermutation.resolve(sign.wall_sign, {
					[CARDINAL_DIRECTION]: wall,
				} as Record<string, string>);
			}

			const { block, player } = event;
			if (!player) return;
			const typeId = event.permutationToPlace.type.id;
			system.run(() => {
				if (block.isValid && block.typeId === typeId)
					void editSignText(player, block, sign);
			});
		},

		onPlayerInteract: ({ block, player }, { params }) => {
			const sign = params as SignParams | undefined;
			if (player && !applyHeldItem(player, block, sign))
				void editSignText(player, block, sign);
		},

		onBreak: ({ block, brokenBlockPermutation }, { params }) => {
			const sign = params as SignParams | undefined;
			for (const shape of signShapes.get(signKey(block))?.flat() ?? [])
				shape.remove();
			signShapes.delete(signKey(block));
			for (const angle of sideAngles(brokenBlockPermutation, sign))
				removeLeftovers(block, textLocation(block, angle, sign));
		},

		onTick: ({ block }, { params }) => {
			if (block.isValid)
				updateBlockPrimitiveText(block, params as SignParams | undefined);
		},
	});
}
