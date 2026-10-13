"""Package and clean-build the self-contained ACM case study."""
import hashlib
import json
from pathlib import Path
import re
import shutil
import subprocess
import sys
import tempfile
import zipfile

ROOT = Path(__file__).resolve().parents[1]
NAME = 'auditor_obligation_audit'
def run(cmd, **kw):
    return subprocess.run([str(x) for x in cmd], check=True, capture_output=True, encoding='utf-8', **kw)
def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()

def main():
    deliver = ROOT/'deliverables'
    deliver.mkdir(exist_ok=True)
    cache = ROOT/'.native-cache'
    stage = Path(tempfile.mkdtemp(prefix='release-stage-', dir=cache))
    shutil.copy2(ROOT/'paper/main.tex', stage/'main.tex')
    verify = stage/'verification'
    (verify/'src').mkdir(parents=True)
    (verify/'protocol').mkdir()
    for name in ['verify_clinical_release.py', 'clinical_family_audit.py', 'native_consent_controls.py', 'native_consent_audit.py']:
        shutil.copy2(ROOT/'src'/name, verify/'src'/name)
    shutil.copy2(ROOT/'protocol/clinical-inventory-protocol.json', verify/'protocol/clinical-inventory-protocol.json')
    shutil.copytree(ROOT/'analysis/clinical-family', verify/'analysis/clinical-family')
    shutil.copytree(ROOT/'analysis/native-consent', verify/'analysis/native-consent')
    checked = json.loads(run([sys.executable, verify/'src/verify_clinical_release.py', '--source', stage/'main.tex', '--receipt', verify/'analysis/clinical-family/receipt.json']).stdout)
    (stage/'README.md').write_text('''# Auditor obligation audit

Technical case-study preprint candidate. No journal acceptance, new-method priority,
independent requirement adjudication or model-performance result is claimed.

## Compile
Set main.tex as the Overleaf main document. It is self-contained, with inline
bibliography and TikZ/pgfplots figures. Select XeLaTeX. Local verification used
Tectonic 0.17.0, XeTeX 0.999994, acmart 1.83 (2022), sigconf,nonacm.
The current Overleaf service and a different TeX distribution were not tested.

## Check values without the solver
python verification/src/verify_clinical_release.py --source main.tex --receipt verification/analysis/clinical-family/receipt.json

## Reproduce the native audit on Windows
Install official experimental Cedar CLI 4.13.0 and CVC5 1.4.2. Put their extracted
directories below verification/.local-tools/cedar and verification/.local-tools/cvc5.
Run python verification/src/clinical_family_audit.py. It downloads pinned schemas,
plans and references as data, records hashes, and does not execute upstream Python.
It requires internet access. The receipt retains the original machine's command
paths for provenance; the script computes paths for a new extraction.
The earlier motivating request can be rerun with native_consent_audit.py using
its explicit --cedar and --cvc5 arguments. No model API or HPC is required.

## Rights and interpretation
Derived floor-union policies retain the upstream license and notice under
verification/analysis/clinical-family/. Original work is unlicensed pending the
author's decision. This archive excludes downloaded papers and tool binaries.
The family is a selected, related set. The 34 omitted probes are logical slices,
not 34 independent tasks, actual model mistakes or a population failure rate.
''', encoding='utf-8')
    log = (cache/'compile-final.log').read_text(encoding='utf-8-sig')
    final = log.rsplit('note: Rerunning TeX', 1)[-1]
    issues = re.findall(r'Overfull|undefined (?:references|citations)|Missing character|^error:', final, re.M)
    assert not issues, issues
    validation = {'status': 'built-and-data-checked', 'scientific_status': 'case-study preprint candidate; novelty priority and independent interpretation unverified',
        'checks': checked, 'visual_pages_reviewed': 4, 'tables_reviewed': 1, 'figures_reviewed': 2,
        'final_pass_errors_overfull_undefined_missing_glyphs': 0,
        'compiler': 'Tectonic 0.17.0 / XeTeX 0.999994 / acmart 1.83',
        'built_in_compiler': 'unavailable: Windows sandbox helper setup failure',
        'native_tools': 'Cedar CLI 4.13.0 experimental; CVC5 1.4.2',
        'exact_original_4_10_0_environment': 'not tested',
        'clean_directory_rebuild': 'pending',
        'source_sha256': sha(stage/'main.tex'), 'pdf_sha256': sha(ROOT/'paper/main.pdf')}
    (verify/'compile.log').write_text(log, encoding='utf-8')
    archive = deliver/(NAME+'_overleaf.zip')
    def pack():
        (stage/'validation.json').write_text(json.dumps(validation, indent=2), encoding='utf-8')
        with zipfile.ZipFile(archive, 'w', zipfile.ZIP_DEFLATED) as z:
            for path in sorted(stage.rglob('*')):
                if path.is_file():
                    z.write(path, path.relative_to(stage))
    pack()
    clean = Path(tempfile.mkdtemp(prefix='release-clean-', dir=cache))
    with zipfile.ZipFile(archive) as z:
        z.extractall(clean)
    compiler = ROOT/'.local-tools/tectonic/tectonic.exe'
    compiled = run([compiler, '--print', 'main.tex'], cwd=clean)
    (cache/'clean-build.log').write_text(compiled.stdout + compiled.stderr, encoding='utf-8')
    run(['pdftotext', '-layout', ROOT/'paper/main.pdf', cache/'verified.txt'])
    run(['pdftotext', '-layout', clean/'main.pdf', cache/'rebuilt.txt'])
    assert (cache/'verified.txt').read_bytes() == (cache/'rebuilt.txt').read_bytes()
    run([sys.executable, clean/'verification/src/verify_clinical_release.py', '--source', clean/'main.tex', '--receipt', clean/'verification/analysis/clinical-family/receipt.json'])
    validation['clean_directory_rebuild'] = 'passed; exact pdftotext -layout comparison; no normalization'
    validation['status'] = 'release-verified'
    validation['archive_members_sha256'] = {str(p.relative_to(stage)).replace('\\','/'): sha(p) for p in stage.rglob('*') if p.is_file() and p.name != 'validation.json'}
    pack()
    # Verify the final archive's source is exactly what was clean-built.
    with zipfile.ZipFile(archive) as z:
        assert z.read('main.tex') == (clean/'main.tex').read_bytes()
        for name, digest in validation['archive_members_sha256'].items():
            assert hashlib.sha256(z.read(name)).hexdigest() == digest
    shutil.copy2(ROOT/'paper/main.tex', deliver/(NAME+'_acm.tex'))
    shutil.copy2(ROOT/'paper/main.pdf', deliver/(NAME+'_acm.pdf'))
    (ROOT/'analysis/clinical-family/release-validation.json').write_text(json.dumps(validation, indent=2), encoding='utf-8')
    print(json.dumps({'deliverables': [str(p) for p in deliver.iterdir()], 'clean_directory': str(clean), 'validation': validation['clean_directory_rebuild']}, indent=2))

if __name__ == '__main__':
    main()
