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

        # Runtime storage for user-registered entries
        self._runtime_entries: Dict[str, str] = {}
        
        # Original state from file
        self._original_entries: Dict[str, str] = {}
        
        if self._excel_file_path.exists():
            try:
                # Load original en_US entries to track deletions/modifications
                df = pd.read_excel(self._excel_file_path, sheet_name=self._source_language)
                self._original_entries = dict(zip(df["Key"], df["Value"]))
            except ValueError:
                pass
        else:
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

    def _sync_excel(self) -> None:
        """
        Synchronizes the runtime entries with the Excel file.
        """
        if not self._runtime_entries:
            return

        # Load all existing sheets
        all_dfs = {}
        for language in self._get_languages():
            try:
                df = pd.read_excel(self._excel_file_path, sheet_name=language)
                all_dfs[language] = df
            except ValueError:
                all_dfs[language] = pd.DataFrame(columns=["Key", "Value"])

        original_set = set(self._original_entries.keys())
        runtime_set = set(self._runtime_entries.keys())
        
        # Identify changes
        new_keys = runtime_set - original_set
        deleted_keys = original_set - runtime_set
        shared_keys = runtime_set.intersection(original_set)

        # 1. Handle New Keys
        if new_keys:
            new_rows_en = pd.DataFrame({"Key": list(new_keys), "Value": [self._runtime_entries[k] for k in new_keys]})
            all_dfs[self._source_language] = pd.concat([all_dfs[self._source_language], new_rows_en], ignore_index=True)
            
            for lang, df in all_dfs.items():
                if lang == self._source_language: 
                    continue
                new_rows_other = pd.DataFrame({"Key": list(new_keys), "Value": [""] * len(new_keys)})
                all_dfs[lang] = pd.concat([df, new_rows_other], ignore_index=True)

        # 2. Handle Deleted Keys
        if deleted_keys:
            for lang in all_dfs:
                all_dfs[lang] = all_dfs[lang][~all_dfs[lang]["Key"].isin(deleted_keys)]

        # 3. Handle Modified Values
        for key in shared_keys:
            original_val = self._original_entries[key]
            runtime_val = self._runtime_entries[key]
            
            if original_val != runtime_val:
                # Update en_US
                df_en = all_dfs[self._source_language]
                df_en.loc[df_en["Key"] == key, "Value"] = runtime_val
                
                # Clear other languages
                for lang in all_dfs:
                    if lang == self._source_language:
                        continue
                    df_lang = all_dfs[lang]
                    if key in df_lang["Key"].values:
                         df_lang.loc[df_lang["Key"] == key, "Value"] = pd.NA

        # Write back to Excel
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
                    key_lengths = [len(str(k)) for k in df["Key"] if pd.notna(k)]
                    max_key_length = max(key_lengths) if key_lengths else 10
                    worksheet.column_dimensions["A"].width = max(
                        max_key_length + 5, 20
                    )
                worksheet.column_dimensions["B"].width = 20
        
        # Update original entries after sync
        self._original_entries = self._runtime_entries.copy()

    def add_localization_entry(self, key: str, value: str) -> None:
        """
        Add a new localization entry to the runtime memory.

        Parameters:
            key (str): The localization key
            value (str): The English value
        """
        self._runtime_entries[key] = value

    def add_entries(self, entries: Dict[str, str]) -> None:
        """
        Add multiple localization entries to the en_US sheet.

        Parameters:
            entries (Dict[str, str]): A dictionary of localization entries
        """
        for key, value in entries.items():
            self.add_localization_entry(key, value)

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
        self._sync_excel()

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
        self._sync_excel()

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
