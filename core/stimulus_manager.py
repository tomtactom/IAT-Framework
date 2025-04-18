# core/stimulus_manager.py

import yaml
import os

class StimulusManager:
    def __init__(self, config_path):
        # 1) Config laden
        with open(config_path, 'r', encoding='utf8') as f:
            self.cfg = yaml.safe_load(f)
        # 2) Stimuli-Datenstrukturen vorbereiten
        self.stimuli = {
            'targets': {},
            'attributes': {}
        }
        # 3) Alle Stimuli einlesen
        self._load_all_stimuli()

    def _load_all_stimuli(self):
        # Targets
        for tgt in self.cfg['targets']:
            self.stimuli['targets'][tgt['name']] = self._load_list(tgt['stimuli_list'], tgt['type'])
        # Attributes
        for att in self.cfg['attributes']:
            self.stimuli['attributes'][att['name']] = self._load_list(att['stimuli_list'], att['type'])

    def _load_list(self, filepath, stim_type):
        """
        Datei einlesen, je nach stim_type (.txt, .png, .wav)
        Returns: list of filepaths or words
        """
        path = os.path.abspath(filepath)
        assert os.path.exists(path), f"Stimuli-File not found: {path}"

        items = []
        if stim_type == 'word':
            # jede Zeile ein Wort
            with open(path, 'r', encoding='utf8') as f:
                items = [w.strip() for w in f if w.strip()]
        elif stim_type in ('image', 'audio'):
            # Ordner liest alle Dateien ein
            for fname in os.listdir(path):
                if fname.lower().endswith(('.png', '.jpg', '.jpeg') if stim_type=='image' else ('.wav', '.mp3')):
                    items.append(os.path.join(path, fname))
        else:
            raise ValueError(f"Unknown stim type: {stim_type}")

        return items

    def get_stimuli(self):
        """Gibt das komplette Stimuli‑Dictionary zurück."""
        return self.stimuli

    def get_block_config(self):
        """Liefert die Blocks-Konfiguration aus cfg."""
        return self.cfg['blocks']

# Test-Code, lässt sich später entfernen
if __name__ == "__main__":
    sm = StimulusManager("../config/config_schema.yml")
    print("Targets:", sm.get_stimuli()['targets'])
    print("Attributes:", sm.get_stimuli()['attributes'])
    print("Blocks:", sm.get_block_config())
