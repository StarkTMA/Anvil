import os
from pathlib import Path
from typing import Dict, List, Optional

import click
import pandas as pd
from deep_translator import GoogleTranslator

from anvil.lib.config import CONFIG
from anvil.lib.lib import File
from anvil.lib.schemas import JsonSchemes


class AnvilTranslator:
    _instance = None

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super(AnvilTranslator, cls).__new__(cls)
        return cls._instance

    def __init__(self):
        """
        Initialize the translator with an Excel file path.
        """
        if hasattr(self, "_initialized") and self._initialized:
            return
        self._excel_file_path = Path("localization.xlsx")
        self._source_language = "en_US"
        self._translated = False
        self.translated_languages = [self._source_language]
        self._initialized = True
        self.config = CONFIG

        if not self._excel_file_path.exists():
            with pd.ExcelWriter(self._excel_file_path, engine="openpyxl") as writer:
                for lang_code in JsonSchemes.languages():
                    df = pd.DataFrame(columns=["Key", "Value"])
                    df.to_excel(writer, sheet_name=lang_code, index=False)

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

    def _get_languages(self) -> List[str]:
        """Returns a list of all languages."""
        languages = [lang for lang in JsonSchemes.languages()]
        return languages

    def _get_localization_entries(self, language: str) -> Dict[str, str]:
        """
        Returns a dictionary of localization entries for a specific language.
        """
        try:
            df = pd.read_excel(self._excel_file_path, sheet_name=language)
            return dict(zip(df["Key"], df["Value"]))
        except ValueError:
            return {}

    def _cleanup_orphaned_keys(self) -> None:
        """
        Remove keys from other languages that don't exist in the source language (en_US).
        """
        try:
            source_df = pd.read_excel(
                self._excel_file_path, sheet_name=self._source_language
            )
            source_keys = set(source_df["Key"].tolist())
        except ValueError:
            return

        all_dfs = {}
        languages_to_update = []

        for language in self._get_languages():
            try:
                df_lang = pd.read_excel(self._excel_file_path, sheet_name=language)
                lang_keys = set(df_lang["Key"].tolist())

                orphaned_keys = lang_keys - source_keys

                if orphaned_keys:
                    df_lang = df_lang[~df_lang["Key"].isin(orphaned_keys)]
                    all_dfs[language] = df_lang
                    languages_to_update.append(language)

            except ValueError:
                continue

        if languages_to_update:
            with pd.ExcelWriter(
                self._excel_file_path,
                engine="openpyxl",
                mode="a",
                if_sheet_exists="replace",
            ) as writer:
                for language in languages_to_update:
                    df = all_dfs[language]
                    df.to_excel(writer, sheet_name=language, index=False)
                    worksheet = writer.sheets[language]
                    if not df.empty:
                        max_key_length = (
                            max(len(str(key)) for key in df["Key"])
                            if len(df["Key"]) > 0
                            else 10
                        )
                        worksheet.column_dimensions["A"].width = max(
                            max_key_length + 5, 20
                        )
                    worksheet.column_dimensions["B"].width = 20

    def add_localization_entry(self, key: str, value: str) -> None:
        """
        Add a new localization entry to the en_US sheet.

        Parameters:
            key (str): The localization key
            value (str): The English value
        """
        try:
            df_en_us = pd.read_excel(
                self._excel_file_path, sheet_name=self._source_language
            )
        except ValueError:
            df_en_us = pd.DataFrame(columns=["Key", "Value"])

        existing_mask = df_en_us["Key"] == key
        if existing_mask.any():
            current_value = df_en_us.loc[existing_mask, "Value"].iloc[0]
            if current_value == value:
                return
            df_en_us.loc[existing_mask, "Value"] = value
        else:
            new_row = pd.DataFrame({"Key": [key], "Value": [value]})
            df_en_us = pd.concat([df_en_us, new_row], ignore_index=True)

        all_dfs = {self._source_language: df_en_us}

        for language in self._get_languages():
            if language == self._source_language:
                continue

            try:
                df_lang = pd.read_excel(self._excel_file_path, sheet_name=language)
                if existing_mask.any():
                    if key in df_lang["Key"].values:
                        df_lang.loc[df_lang["Key"] == key, "Value"] = pd.NA
                else:
                    if key not in df_lang["Key"].values:
                        new_row = pd.DataFrame({"Key": [key], "Value": [""]})
                        df_lang = pd.concat([df_lang, new_row], ignore_index=True)
            except ValueError:
                df_lang = pd.DataFrame({"Key": [key], "Value": [""]})

            all_dfs[language] = df_lang

        with pd.ExcelWriter(
            self._excel_file_path,
            engine="openpyxl",
            mode="a",
            if_sheet_exists="replace",
        ) as writer:
            for lang, df in all_dfs.items():
                df.to_excel(writer, sheet_name=lang, index=False)
                worksheet = writer.sheets[lang]
                if not df.empty:
                    max_key_length = (
                        max(len(str(key)) for key in df["Key"])
                        if len(df["Key"]) > 0
                        else 10
                    )
                    worksheet.column_dimensions["A"].width = max(max_key_length + 5, 20)
                worksheet.column_dimensions["B"].width = 20

    def get_localization_value(self, key: str) -> Optional[str]:
        """
        Get the localization value for a specific key from the source language (en_US).
        """
        try:
            df = pd.read_excel(self._excel_file_path, sheet_name=self._source_language)
            return df.loc[df["Key"] == key, "Value"].iloc[0]
        except (ValueError, IndexError):
            return None

    def auto_translate_all(self, languages: Optional[list[str]] = None) -> None:
        """
        Automatically translate all entries from source language to target languages.
        """

        def parse(lang: str):
            lang = lang.replace("zh_CN", "zh-CN")
            lang = lang.replace("zh_TW", "zh-TW")
            lang = lang.replace("nb_NO", "no").split("_")[0]
            lang = lang.replace("en_US", "en")
            lang = lang.replace("en_GB", "en")
            return lang

        if languages is None:
            languages = self._get_languages()

        source_entries = self._get_localization_entries(self._source_language)

        with pd.ExcelWriter(
            self._excel_file_path,
            engine="openpyxl",
            mode="a",
            if_sheet_exists="replace",
        ) as writer:
            for target_lang in languages:

                if target_lang == self._source_language:
                    continue

                existing_entries = self._get_localization_entries(target_lang)
                keys_to_translate = []
                values_to_translate = []

                for key, value in source_entries.items():
                    if (
                        key not in existing_entries
                        or existing_entries[key] == ""
                        or pd.isna(existing_entries[key])
                    ):
                        keys_to_translate.append(key)
                        values_to_translate.append(value)

                if not values_to_translate:
                    continue

                translator = GoogleTranslator(source="en", target=parse(target_lang))
                translated_values = []
                batch_size = 50
                for i in range(0, len(values_to_translate), batch_size):
                    batch = values_to_translate[i : i + batch_size]
                    try:
                        translated_values.extend(translator.translate_batch(batch))
                    except Exception as e:
                        click.echo(
                            click.style(
                                f"[INFO]: Translation error for {target_lang}: {e}",
                                fg="red",
                            )
                        )
                        translated_values.extend(batch)

                translation_map = dict(zip(keys_to_translate, translated_values))

                all_keys = list(source_entries.keys())
                all_values = []

                for key in all_keys:
                    if key in existing_entries and not pd.isna(existing_entries[key]):
                        all_values.append(existing_entries[key])
                    else:
                        all_values.append(translation_map[key])

                df = pd.DataFrame({"Key": all_keys, "Value": all_values})
                df.to_excel(writer, sheet_name=target_lang, index=False)

        self._cleanup_orphaned_keys()

        self._translated = True
        self.translated_languages.extend(languages)

    def _export(self) -> None:
        """
        Export translations to Anvil's .lang file format.
        """

        languages = []
        skipped = []

        for lang_code in self._get_languages():
            entries = self._get_localization_entries(lang_code)
            if not entries:
                continue

            if any(not value or pd.isna(value) for value in entries.values()):
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

            remaining_entries = {
                k: v for k, v in entries.items() if k not in ordered_keys
            }
            for key, value in sorted(remaining_entries.items()):
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

            File(
                f"{lang_code}.lang",
                "\n".join(rp_content),
                os.path.join(self.config.RP_PATH, "texts"),
                "w",
            )
            File(
                f"{lang_code}.lang",
                "\n".join(bp_content),
                os.path.join(self.config.BP_PATH, "texts"),
                "w",
            )

            if self.config._TARGET == "world":
                File(
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
        File(
            "languages.json", languages, os.path.join(self.config.BP_PATH, "texts"), "w"
        )
        File(
            "languages.json", languages, os.path.join(self.config.RP_PATH, "texts"), "w"
        )
        if self.config._TARGET == "world":
            File(
                "languages.json",
                languages,
                os.path.join(self.config._WORLD_PATH, "texts"),
                "w",
            )
