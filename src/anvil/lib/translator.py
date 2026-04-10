import csv
import os
from pathlib import Path
from typing import Dict, List, Optional

import click
from deep_translator import GoogleTranslator

from anvil.lib.config import CONFIG
from anvil.lib.lib import AnvilIO
from anvil.lib.schemas import JsonSchemes


class AnvilTranslator:
    _instance = None

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super(AnvilTranslator, cls).__new__(cls)
        return cls._instance

    def __init__(self):
        """
        Collect localization entries during compilation, merge them with
        localization.csv, optionally fill missing translations, and export
        Minecraft .lang files.
        """
        if hasattr(self, "_initialized") and self._initialized:
            return

        self._csv_file_path = Path("localization.csv")
        self._source_language = "en_US"
        self._translated = False
        self.translated_languages = [self._source_language]
        self.config = CONFIG
        self._languages = list(JsonSchemes.languages())

        self._runtime_entries: Dict[str, str] = {}
        self._entries: Dict[str, Dict[str, Optional[str]]] = {}
        for language in self._languages:
            self._entries[language] = {}

        self._pending_translation_languages: set[str] = set()
        self._initialized = True

        self.add_localization_entry("pack.name", self.config.DISPLAY_NAME)
        self.add_localization_entry(
            "pack.project_description", self.config.PROJECT_DESCRIPTION
        )
        self.add_localization_entry(
            "pack.resource_description", self.config.RESOURCE_DESCRIPTION
        )
        self.add_localization_entry(
            "pack.behaviour_description", self.config.BEHAVIOUR_DESCRIPTION
        )

    def _normalize_value(self, value) -> Optional[str]:
        if value is None:
            return None

        if isinstance(value, float) and value != value:
            return None

        return str(value)

    def _read_csv_entries(
        self,
    ) -> tuple[Dict[str, Dict[str, Optional[str]]], list[str]]:
        entries: Dict[str, Dict[str, Optional[str]]] = {}

        for language in self._languages:
            entries[language] = {}

        if not self._csv_file_path.exists():
            return entries, []

        with self._csv_file_path.open("r", newline="", encoding="utf-8-sig") as file:
            reader = csv.DictReader(file)
            fieldnames = list(reader.fieldnames or [])

            if not fieldnames or fieldnames[0] != "Key":
                return entries, fieldnames

            for row in reader:
                key = self._normalize_value(row.get("Key"))
                if key is None:
                    continue

                for language in self._languages:
                    entries[language][key] = self._normalize_value(row.get(language))

        return entries, fieldnames

    def _parse_language(self, language: str) -> str:
        language = language.replace("zh_CN", "zh-CN")
        language = language.replace("zh_TW", "zh-TW")
        language = language.replace("nb_NO", "no").split("_")[0]
        language = language.replace("en_US", "en")
        language = language.replace("en_GB", "en")
        return language

    def _translate_pending_languages(self, source_keys: List[str]) -> None:
        if not self._pending_translation_languages:
            return

        source_entries = self._entries[self._source_language]

        for language in sorted(self._pending_translation_languages):
            if language == self._source_language:
                continue

            if language not in self._entries:
                continue

            language_entries = self._entries[language]
            keys_to_translate: List[str] = []
            values_to_translate: List[str] = []

            for key in source_keys:
                source_value = source_entries.get(key)
                current_value = language_entries.get(key)

                if source_value is None:
                    continue

                if current_value not in (None, ""):
                    continue

                keys_to_translate.append(key)
                values_to_translate.append(source_value)

            if not values_to_translate:
                continue

            translator = GoogleTranslator(
                source="en", target=self._parse_language(language)
            )
            batch_size = 50

            for index in range(0, len(values_to_translate), batch_size):
                batch_keys = keys_to_translate[index : index + batch_size]
                batch_values = values_to_translate[index : index + batch_size]

                try:
                    translated_values = translator.translate_batch(batch_values)
                    if not isinstance(translated_values, list):
                        translated_values = list(batch_values)
                    elif len(translated_values) != len(batch_values):
                        translated_values = list(batch_values)
                except Exception as error:
                    click.echo(
                        click.style(
                            f"[INFO]: Translation error for {language}: {error}",
                            fg="red",
                        )
                    )
                    translated_values = list(batch_values)

                for key, source_value, translated_value in zip(
                    batch_keys, batch_values, translated_values
                ):
                    normalized_value = self._normalize_value(translated_value)
                    if normalized_value is None:
                        normalized_value = source_value

                    language_entries[key] = normalized_value

        self._translated = True
        self._pending_translation_languages.clear()

    def _write_csv(self) -> None:
        fieldnames = ["Key", *self._languages]

        with self._csv_file_path.open("w", newline="", encoding="utf-8") as file:
            writer = csv.DictWriter(file, fieldnames=fieldnames)
            writer.writeheader()

            for key in self._entries[self._source_language]:
                row = {"Key": key}

                for language in self._languages:
                    value = self._entries[language].get(key)
                    row[language] = "" if value in (None, "") else value

                writer.writerow(row)

    def _sync_csv(self) -> None:
        """
        Open the CSV once, read its current values, merge runtime entries,
        apply any pending translations, and write the CSV back only when
        the row data changed.
        """
        saved_entries, saved_fieldnames = self._read_csv_entries()
        saved_source_entries = saved_entries[self._source_language]

        source_keys: List[str] = []
        for key in saved_source_entries:
            if key in self._runtime_entries:
                source_keys.append(key)

        for key in self._runtime_entries:
            if key not in saved_source_entries:
                source_keys.append(key)

        changed_source_keys: set[str] = set()
        for key, value in self._runtime_entries.items():
            if saved_source_entries.get(key) != value:
                changed_source_keys.add(key)

        merged_entries: Dict[str, Dict[str, Optional[str]]] = {}
        for language in self._languages:
            merged_entries[language] = {}

        source_entries = merged_entries[self._source_language]
        for key in source_keys:
            source_entries[key] = self._runtime_entries[key]

        for language in self._languages:
            if language == self._source_language:
                continue

            saved_language_entries = saved_entries[language]
            merged_language_entries = merged_entries[language]

            for key in source_keys:
                value = saved_language_entries.get(key)
                if key in changed_source_keys:
                    value = None

                merged_language_entries[key] = value

        self._entries = merged_entries
        self._translate_pending_languages(source_keys)

        needs_save = not self._csv_file_path.exists()
        if saved_fieldnames != ["Key", *self._languages]:
            needs_save = True

        if not needs_save:
            for language in self._languages:
                if self._entries[language] != saved_entries[language]:
                    needs_save = True
                    break

        if needs_save:
            self._write_csv()

    def add_localization_entry(self, key: str, value: str) -> None:
        """
        Add or update a localization entry in the source language.
        """
        self._runtime_entries[key] = value

    def add_entries(self, entries: Dict[str, str]) -> None:
        """
        Add multiple localization entries.
        """
        for key, value in entries.items():
            self.add_localization_entry(key, value)

    def get_localization_value(self, key: str) -> Optional[str]:
        """
        Return the current source-language value for a localization key.
        """
        if key in self._runtime_entries:
            return self._runtime_entries[key]

        source_entries = self._entries.get(self._source_language, {})
        return source_entries.get(key)

    def auto_translate_all(self, languages: Optional[list[str]] = None) -> None:
        """
        Queue languages for translation during the next export sync.
        """
        if languages is None:
            languages = self._languages

        for language in languages:
            if language == self._source_language:
                continue

            if language not in self._languages:
                continue

            self._pending_translation_languages.add(language)

            if language not in self.translated_languages:
                self.translated_languages.append(language)

    def format_key(self, key: str) -> str:
        """
        Format a localization key using only alphanumeric characters and dots, no starting with a digit, suitable for use in Minecraft .lang files.
        """
        formatted = "".join(
            char if char.isalnum() or char == "." else "_" for char in key
        )
        if formatted and formatted[0].isdigit():
            formatted = "_" + formatted
        return formatted

    def _export(self) -> None:
        """
        Export translations to Anvil's .lang file format.
        """
        self._sync_csv()

        languages = []
        skipped = []

        for lang_code in self._languages:
            entries = self._entries.get(lang_code, {})
            if not entries:
                continue

            missing_values = False
            for value in entries.values():
                if not value:
                    missing_values = True
                    break

            if missing_values:
                skipped.append(lang_code)
                continue

            languages.append(lang_code)

            lang_content = []
            ordered_keys = [
                "pack.name",
                "pack.project_description",
                "pack.resource_description",
                "pack.behaviour_description",
            ]

            for key in ordered_keys:
                if key in entries:
                    lang_content.append(f"{key}={entries[key]}")

            remaining_entries = []
            for key, value in entries.items():
                if key in ordered_keys:
                    continue

                remaining_entries.append((key, value))

            for key, value in sorted(remaining_entries):
                lang_content.append(f"{key}={value}")

            bp_content = [
                lang_content[0],
                lang_content[3].replace("behaviour_description", "description"),
            ]
            world_content = [
                lang_content[0],
                lang_content[1].replace("project_description", "description"),
            ]

            rp_content = lang_content.copy()
            rp_content[2] = lang_content[2].replace(
                "resource_description", "description"
            )
            del rp_content[1]
            del rp_content[2]

            AnvilIO.file(
                f"{lang_code}.lang",
                "\n".join(rp_content),
                os.path.join(self.config.RP_PATH, "texts"),
                "w",
            )
            AnvilIO.file(
                f"{lang_code}.lang",
                "\n".join(bp_content),
                os.path.join(self.config.BP_PATH, "texts"),
                "w",
            )

            if self.config._TARGET == "world":
                AnvilIO.file(
                    f"{lang_code}.lang",
                    "\n".join(world_content),
                    os.path.join(self.config._WORLD_PATH, "texts"),
                    "w",
                )

        if skipped:
            click.echo(
                click.style(
                    f"\r[INFO]: Skipping [{', '.join(skipped)}] - contains empty values",
                    fg="yellow",
                )
            )

        AnvilIO.file(
            "languages.json",
            languages,
            os.path.join(self.config.BP_PATH, "texts"),
            "w",
        )
        AnvilIO.file(
            "languages.json",
            languages,
            os.path.join(self.config.RP_PATH, "texts"),
            "w",
        )

        if self.config._TARGET == "world":
            AnvilIO.file(
                "languages.json",
                languages,
                os.path.join(self.config._WORLD_PATH, "texts"),
                "w",
            )
