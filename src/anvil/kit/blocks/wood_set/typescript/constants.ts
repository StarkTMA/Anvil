export const NAMESPACE = "{{NAMESPACE}}";

// Component ids match the `wood_set_<name>` custom components on the blocks in `blocks/`.
export const SUPPORT_COMPONENT_ID = `${NAMESPACE}:wood_set_support`;
export const SLAB_COMPONENT_ID = `${NAMESPACE}:wood_set_slab`;
export const STRIPPABLE_COMPONENT_ID = `${NAMESPACE}:wood_set_strippable`;
export const TOGGLABLE_COMPONENT_ID = `${NAMESPACE}:wood_set_togglable`;
export const INTERACTABLE_COMPONENT_ID = `${NAMESPACE}:wood_set_interactable`;
export const REDSTONE_CONSUMER_COMPONENT_ID = `${NAMESPACE}:wood_set_redstone_consumer`;
export const SIGN_COMPONENT_ID = `${NAMESPACE}:wood_set_sign`;
export const BOAT_FAMILY = "wood_set_boat";
export const BOAT_HITS = `${NAMESPACE}:hits`;

export const POWERED = `${NAMESPACE}:powered` as any;
export const OPEN = `${NAMESPACE}:open` as any;
export const DOUBLE = `${NAMESPACE}:double` as any;
export const VERTICAL_HALF = "minecraft:vertical_half" as any;
export const BLOCK_FACE = "minecraft:block_face" as any;
export const CARDINAL_DIRECTION = "minecraft:cardinal_direction" as any;
export const STANDING = `${NAMESPACE}:standing` as any;
export const SIXTEEN_WAY_ROTATION = "minecraft:sixteen_way_rotation" as any;

// Dynamic properties of a sign: its text, the dye colouring it and whether it glows
export const SIGN_TEXT = "text";
export const SIGN_COLOR = "color";
export const SIGN_GLOWING = "glowing";

// Keyed by lowercase `Direction` name.
export const FACE_OFFSETS = {
	north: { x: 0, y: 0, z: -1 },
	south: { x: 0, y: 0, z: 1 },
	east: { x: 1, y: 0, z: 0 },
	west: { x: -1, y: 0, z: 0 },
	up: { x: 0, y: 1, z: 0 },
	down: { x: 0, y: -1, z: 0 },
};

export type FaceName = keyof typeof FACE_OFFSETS;

// The parameters of the components in components.py
export interface MultiPartParams {
	multi_part: boolean;
}

export interface StrippableParams {
	stripped_block: string;
}

export interface SupportParams {
	supported_by?: "below" | "block_face" | "facing" | "sign";
}

export interface SignParams {
	text_offset?: [number, number, number];
	text_scale?: number;
	line_length?: number;
	double_sided?: boolean;
	wall_text_offset?: [number, number, number];
}
