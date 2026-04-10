# Localization in Anvil

This page explains how Anvil handles localization keys and the localization CSV, and how to translate/export languages correctly.

---

## How keys are created

Whenever you pass a **plain string** to an Anvil component, Anvil automatically:

1. **Creates a localization key** for that string, and
2. **Writes the key–value pair** into the CSV file at your project root (e.g., `localization.csv`).

```py title="examples that create keys"
ItemDisplayName("Arcane User Guide")
BlockDisplayName("Enchanting Plus Table")
# Any other component argument that is a plain string will be tracked too
```

!!! info "Where it goes"
    The English source string is saved under the **`en_US` column** as the value for the generated key. The **same key** is also created in the **other Minecraft-supported locale columns** inside the same CSV, with empty values until you translate them.

---

## Translating other languages

You have two options for non‑English locales:

* **Manual translation**: open `localization.csv` and fill in the empty values in the non-`en_US` language columns.
* **Automatic translation**: call `anvil.translate()` to auto-fill missing values using Google Translate.

```py title="auto translate missing locales"
# Populates only empty cells in non-en_US language columns via Google Translate
import anvil
anvil.translate()
```

!!! note
    `anvil.translate()` **does not overwrite** values that are already translated — whether they were filled **manually** or by a previous run. It only fills **empty** cells.

---

## What happens when strings change

* If you **change** the source text in code, the corresponding **key's value is updated** in `en_US` and the old value is removed from the other language columns.
* If you **delete** a plain string from your Anvil code, its entry is **removed** from the CSV.

!!! warning
    Keep your source of truth in code: adding text directly in `localization.csv` that does not exist in code will **not** be referenced at build time.

---

## Build vs package behavior

* `anvil compile()` → compiles **only `en_us`**.
* `anvil.package()`, `anvil.mcaddon()`, `anvil.mcworld()` → compile **all languages** present in `localization.csv`.

!!! tip
    Any **language column** that has a key with an **empty value** will **not be exported** to the final `.lang` file. Make sure you fill required translations before packaging.

---

## Quick checklist

* Use **plain strings** in components; Anvil will create keys automatically.
* Verify keys and values in `localization.csv` -> `en_US` is the source of truth.
* Translate others **manually** or with `anvil.translate()`.
* Remember build rules: `compile` = English only, packaging commands = all languages.
* Empty values in a locale column -> that locale **won't export** to `.lang`.
