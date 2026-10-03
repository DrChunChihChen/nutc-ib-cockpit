"""Export validated, aggregate-only dossiers for Netlify. No deployment performed."""
import argparse
import json
import os
from pathlib import Path
import sys
import tempfile

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))


def export(output_dir, destination):
    from ir_autopilot.src.ai import dossier
    dossier.OUTPUT_DIR = str(output_dir)
    result = {}
    for slug in dossier.SLUG_TO_NAME:
        source = output_dir / slug / 'dept_data.json'
        if not source.is_file():
            raise ValueError(f'Missing source: {source}')
        d = dossier.build_dossier(slug)
        if not d['kpis'] or not d['module5'] or 'destinations' not in d['module5']:
            raise ValueError(f'Incomplete dossier: {slug}')
        result[slug] = d
    destination.parent.mkdir(parents=True, exist_ok=True)
    with tempfile.NamedTemporaryFile(mode='w', encoding='utf-8', dir=destination.parent, delete=False) as tmp:
        json.dump(result, tmp, ensure_ascii=False, indent=2)
        tmp.write('\n')
    os.replace(tmp.name, destination)
    return result


if __name__ == '__main__':
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('--output-dir', type=Path, default=ROOT / 'output')
    p.add_argument('--destination', type=Path, default=ROOT / 'netlify/functions/dossiers.json')
    args = p.parse_args()
    exported = export(args.output_dir, args.destination)
    print(f'Exported {len(exported)} complete dossiers to {args.destination}')
