# Localization in Anvil

This page explains how Anvil handles localization keys and Excel sheets, and how to translate/export languages correctly.

---

## How keys are created

Whenever you pass a **plain string** to an Anvil component, Anvil automatically:

1. **Creates a localization key** for that string, and
2. **Writes the key–value pair** into the Excel workbook at your project root (e.g., `localization.xlsx`).

```py title="examples that create keys"
ItemDisplayName("Arcane User Guide")
BlockDisplayName("Enchanting Plus Table")
# Any other component argument that is a plain string will be tracked too
```

!!! info "Where it goes"
    The English source string is saved under the **`en_us` sheet** as the value for the generated key. The **same key** is also created (with an empty value) in the **other Minecraft‑supported locale sheets** inside the same workbook.

---

## Translating other languages

You have two options for non‑English locales:

* **Manual translation**: open `localization.xlsx` and fill in the empty values in the non‑`en_us` sheets.
* **Automatic translation**: call `anvil.translate()` to auto‑fill missing values using Google Translate.

```py title="auto translate missing locales"
# Populates only empty cells in non-en_us sheets via Google Translate
import anvil
anvil.translate()
```

!!! note
    `anvil.translate()` **does not overwrite** values that are already translated — whether they were filled **manually** or by a previous run. It only fills **empty** cells.

---

## What happens when strings change

* If you **change** the source text in code, the corresponding **key’s value is updated** in `en_us` and the old value is removed from the other language sheets.
* If you **delete** a plain string from your Anvil code, its entry is **removed** from the workbook (or its values are **emptied** across all languages).

!!! warning
    Keep your source of truth in code: adding text directly in Excel that doesn’t exist in code will **not** be referenced at build time.

---

## Build vs package behavior

* `anvil compile()` → compiles **only `en_us`**.
* `anvil.package()`, `anvil.mcaddon()`, `anvil.mcworld()` → compile **all languages** present in `localization.xlsx`.

!!! tip
    Any **language sheet** that has a key with an **empty value** will **not be exported** to the final `.lang` file. Make sure you fill required translations or leave the sheet out entirely.

---

## Quick checklist

* Use **plain strings** in components; Anvil will create keys automatically.
* Verify keys and values in `localization.xlsx` → `en_us` is the source of truth.
* Translate others **manually** or with `anvil.translate()`.
* Remember build rules: `compile` = English only, packaging commands = all languages.
* Empty values in a locale sheet → that locale **won’t export** to `.lang`.
