"""Portable verification: lint, structure, offline mock tests and real GenVM Direct Mode tests.

usage: python scripts/verify.py [--skip-direct] [--allow-missing-tools]

Runs from any checkout (paths are derived from this file). Tiers are reported separately and the
offline mock tier is never presented as consensus verification. Exit code is non-zero if any step
fails or a required tool is missing (unless --allow-missing-tools).
"""
import argparse, os, shutil, subprocess, sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CONTRACTS = ['handoff_graph.py', 'handoff_consumer_example.py', 'handoff_capability_consumer.py']


def run(name, cmd, results, env):
    print('\n== %s\n$ %s' % (name, ' '.join(cmd)), flush=True)
    proc = subprocess.run(cmd, cwd=ROOT, env=env)
    results.append((name, proc.returncode == 0, 'pass' if proc.returncode == 0 else 'FAIL'))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--skip-direct', action='store_true')
    ap.add_argument('--allow-missing-tools', action='store_true')
    args = ap.parse_args()
    env = dict(os.environ, PYTHONUTF8='1', PYTHONIOENCODING='utf-8')
    py = sys.executable
    results = []
    run('compile', [py, '-m', 'compileall', '-q', 'contracts', 'tests', 'scripts', 'direct_tests'], results, env)
    run('structural preflight', [py, 'scripts/preflight.py'], results, env)
    lint = shutil.which('genvm-lint')
    for name in CONTRACTS:
        if lint:
            run('genvm-lint ' + name, [lint, 'check', 'contracts/' + name], results, env)
        else:
            results.append(('genvm-lint ' + name, args.allow_missing_tools, 'SKIPPED (genvm-lint not installed)'))
    run('offline mock tests (NOT consensus evidence)', [py, '-m', 'pytest', 'tests', '-q', '-p', 'no:cacheprovider'], results, env)
    if args.skip_direct:
        results.append(('Direct Mode', args.allow_missing_tools, 'SKIPPED (--skip-direct)'))
    else:
        run('real GenVM Direct Mode', [py, '-m', 'pytest', 'direct_tests', '-q', '-p', 'no:cacheprovider'], results, env)
    print('\n== summary')
    for name, ok, note in results:
        print('%-4s %-55s %s' % ('ok' if ok else 'FAIL', name, note))
    return 0 if all(ok for _, ok, _ in results) else 1


if __name__ == '__main__':
    sys.exit(main())
