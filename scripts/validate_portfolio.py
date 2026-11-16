#!/usr/bin/env python3
"""Check the content of this documentation portfolio without private dependencies."""

import json
from pathlib import Path
import re
from urllib.parse import unquote, urlsplit

ROOT = Path(__file__).resolve().parents[1]
PUBLIC_FILES = {
    '.gitignore', 'LICENSE', 'NOTICE.md', 'README.md', 'README.zh-CN.md',
    'docs/release-notes.md',
    'projects/01-vla-reproduction.md', 'projects/02-glove-retargeting.md',
    'projects/03-contact-retargeting.md', 'projects/04-staged-rl.md',
    'results/README.md', 'results/vla-offline-summary.json',
    'results/glove-status.json', 'results/retargeting-summary.json',
    'results/staged-rl-summary.json', 'scripts/validate_portfolio.py',
}


def collect_errors():
    errors = []
    seen = set()
    sensitive_patterns = {
        'credential-shaped value': re.compile(
            r'(?:gh[pousr]_[A-Za-z0-9]{20,}|github_pat_[A-Za-z0-9_]{20,}'
            r'|sk-[A-Za-z0-9_-]{24,}|-----BEGIN [A-Z ]*PRIVATE KEY-----)'
        ),
        'machine-specific home path': re.compile('/' + r'(?:Users|home)/[^\s\]<>]+'),
        'machine-specific data path': re.compile('/' + r'data/[A-Z][^\s\]<>]+'),
        'credential in URL': re.compile(r'https?://[^\s/:]+:[^\s/@]+@'),
    }
    for path in ROOT.rglob('*'):
        relative = path.relative_to(ROOT)
        if '.git' in relative.parts or '__pycache__' in relative.parts:
            continue
        if path.is_symlink():
            errors.append(f'Symlink is not permitted: {relative}')
            continue
        if not path.is_file():
            continue
        name = relative.as_posix()
        seen.add(name)
        if name not in PUBLIC_FILES:
            errors.append(f'Unexpected public file: {relative}')
            continue
        if path.stat().st_size > 100_000:
            errors.append(f'Unexpectedly large file: {relative}')
        try:
            content = path.read_text(encoding='utf-8')
        except UnicodeDecodeError:
            errors.append(f'Non-text content: {relative}')
            continue
        for description, pattern in sensitive_patterns.items():
            if pattern.search(content):
                errors.append(f'Possible {description}: {relative}')
        if path.suffix == '.md':
            for target in re.findall(r'\]\(([^)\s]+)\)', content):
                parsed = urlsplit(target)
                if parsed.scheme:
                    if parsed.scheme != 'https':
                        errors.append(f'Non-HTTPS link: {relative}')
                    continue
                resolved = (path.parent / unquote(parsed.path)).resolve()
                if not resolved.is_relative_to(ROOT) or not resolved.is_file():
                    errors.append(f'Broken or escaping local link: {relative}: {target}')
        if path.suffix == '.json':
            try:
                json.loads(content)
            except json.JSONDecodeError:
                errors.append(f'Invalid JSON: {relative}')
    for name in sorted(PUBLIC_FILES - seen):
        errors.append(f'Missing file: {name}')
    if errors:
        return errors

    def read(name):
        return json.loads((ROOT / 'results' / name).read_text())

    vla = read('vla-offline-summary.json')
    if vla['train_episodes'] + vla['validation_episodes'] != vla['episodes']:
        errors.append('VLA split counts do not sum to the dataset count')
    if vla['physical_closed_loop_evaluated']:
        errors.append('Offline VLA result must not imply physical validation')
    glove = read('glove-status.json')
    if glove['runtime_measurements_available'] or glove['hardware_validated']:
        errors.append('Glove template must not be presented as measured validation')
    rl = read('staged-rl-summary.json')
    if rl['runtime_tactile_feedback'] or rl['learning_benefit_established']:
        errors.append('RL boundary contradicts the recorded experiments')
    if len(rl['offset_probes']) != 4:
        errors.append('Exactly four offset probes are documented')
    for probe in rl['offset_probes']:
        if not probe['approach_success'] and probe['grasp_attempted']:
            errors.append('A failed reaching probe must stop before grasping')
    retarget = read('retargeting-summary.json')
    for trial in retarget['same_start_retries']:
        expected = (trial['sampled_object_penetration_mm'] <= 5
                    and trial['contact_mean_mm'] <= 8)
        if trial['quality_accepted'] and not expected:
            errors.append('Retargeting quality claim contradicts its thresholds')
    return errors


def main():
    errors = collect_errors()
    if errors:
        for error in errors:
            print('FAIL:', error)
        raise SystemExit(1)
    print(f'PASS: {len(PUBLIC_FILES)} text files, local links, selected disclosure patterns and result boundaries checked.')


if __name__ == '__main__':
    main()
