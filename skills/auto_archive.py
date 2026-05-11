#!/usr/bin/env python3
"""Auto-archive skill: scan, confirm, commit, and push all project changes."""

import subprocess
import sys
import os
import argparse
from pathlib import Path


def run(cmd, cwd=None):
    """Run a shell command and return (stdout, stderr, returncode)."""
    result = subprocess.run(
        cmd, shell=True, capture_output=True, text=True,
        cwd=cwd or os.getcwd()
    )
    return result.stdout.strip(), result.stderr.strip(), result.returncode


def is_git_repo(path):
    """Check if directory is inside a git repository."""
    _out, _err, rc = run("git rev-parse --is-inside-work-tree", cwd=path)
    return rc == 0


def init_git_repo(path):
    """Initialize a git repo, create claude-auto branch, set local config."""
    print(f"Initializing git repo in: {path}")
    run("git init", cwd=path)
    run("git checkout -b claude-auto", cwd=path)
    run('git config user.email "auto-archive@local"', cwd=path)
    run('git config user.name "auto-archive"', cwd=path)
    # Create a placeholder file so there's something to commit initially
    readme = os.path.join(path, "README.md")
    if not os.path.exists(readme):
        with open(readme, "w", encoding="utf-8") as f:
            f.write(f"# {os.path.basename(path)}\n")
        run("git add README.md", cwd=path)
        run("git commit -m init", cwd=path)
        print("  Created README.md and initial commit.")
    print("  Git repo ready on branch 'claude-auto'.\n")


def ensure_git_repo(path):
    """Ensure path is a git repo; if not, initialize one."""
    if not os.path.isdir(path):
        print(f"Error: directory not found: {path}")
        sys.exit(1)
    if not is_git_repo(path):
        print(f"Not a git repo. Auto-initializing...")
        init_git_repo(path)


def scan_changes(root):
    """Scan for staged, modified, and untracked files."""
    staged, _err, _rc = run("git diff --cached --name-only", cwd=root)
    staged_list = [f for f in staged.split("\n") if f] if staged else []

    modified, _err, _rc = run("git diff --name-only", cwd=root)
    modified_list = [f for f in modified.split("\n") if f] if modified else []

    untracked, _err, _rc = run("git ls-files --others --exclude-standard", cwd=root)
    untracked_list = [f for f in untracked.split("\n") if f] if untracked else []

    return {
        "staged": staged_list,
        "modified": modified_list,
        "untracked": untracked_list,
        "all": staged_list + modified_list + untracked_list,
    }


def generate_commit_message(files):
    """Generate a concise commit message (<=50 chars)."""
    if not files:
        return "archive: update project files"

    categories = {}
    for f in files:
        ext = Path(f).suffix.lstrip(".").lower() or "file"
        categories.setdefault(ext, []).append(f)

    parts = []
    for ext, flist in categories.items():
        count = len(flist)
        parts.append(ext if count == 1 else f"{count}{ext}")

    summary = ", ".join(parts)
    msg = f"archive: {summary}"
    if len(msg) > 50:
        msg = msg[:47] + "..."
    return msg


def preview(files, commit_msg, root, dry_run=False):
    """Display file list, commit message, and git commands."""
    label = "[DRY RUN] " if dry_run else ""
    print(f"\n{'=' * 60}")
    print(f"  {label}AUTO-ARCHIVE")
    print(f"{'=' * 60}")

    print(f"\n[Files to archive] ({len(files)} total)")
    print("-" * 40)
    for f in sorted(files):
        print(f"  {f}")

    print(f"\n[Commit message] ({len(commit_msg)} chars)")
    print("-" * 40)
    print(f"  {commit_msg}")

    print(f"\n[Git commands]")
    print("-" * 40)
    files_str = " ".join(f'"{f}"' for f in files) if files else "."
    print(f"  git add {files_str}")
    print(f'  git commit -m "{commit_msg}"')
    print(f"  git push origin claude-auto")

    print(f"\n{'=' * 60}")

    if dry_run:
        print("\nDry run complete. No changes made.")
        return False

    while True:
        try:
            ans = input("\nProceed with archive? [y/n] or type new commit message: ").strip()
        except (EOFError, KeyboardInterrupt):
            print("\nAborted.")
            return False
        if ans.lower() == "y":
            return True, commit_msg
        elif ans.lower() == "n":
            print("Archive cancelled.")
            return False, None
        elif ans:
            # User typed a custom commit message
            if len(ans) > 50:
                print(f"  Warning: message is {len(ans)} chars (limit is 50). Truncating.")
                ans = ans[:47] + "..."
            return True, ans
    return False, None


def execute_archive(files, commit_msg, root):
    """Execute git add, commit, and push."""
    # git add
    files_str = " ".join(f'"{f}"' for f in files) if files else "."
    print(f"\n>>> git add {files_str}")
    out, err, rc = run(f"git add {files_str}", cwd=root)
    if rc != 0 and err:
        print(f"  Warning (add): {err}")

    # git commit
    print(f'\n>>> git commit -m "{commit_msg}"')
    out, err, rc = run(f'git commit -m "{commit_msg}"', cwd=root)
    if rc != 0:
        print(f"  Commit failed:\n{err}")
        sys.exit(1)
    print(f"  {out}")

    # git push
    print(f"\n>>> git push origin claude-auto")
    out, err, rc = run("git push origin claude-auto", cwd=root)
    if rc != 0:
        if "set-upstream" in err.lower() or "no upstream branch" in err.lower():
            out2, err2, rc2 = run("git push -u origin claude-auto", cwd=root)
            if rc2 != 0:
                print(f"  Push failed:\n{err2}")
            else:
                print(f"  {out2}")
        else:
            print(f"  Push failed:\n{err}")
    else:
        print(f"  {out}")

    print(f"\n{'=' * 60}")
    print(f"  Archive complete.")
    print(f"{'=' * 60}")


def resolve_files(root, args):
    """Resolve which files to archive based on CLI arguments."""
    if args.all:
        return ["."]

    if args.files:
        # Files provided via CLI
        valid = []
        for f in args.files:
            full = os.path.join(root, f)
            if os.path.exists(full):
                valid.append(f)
            else:
                print(f"  Warning: file not found, skipping: {f}")
        return valid

    # --auto (default): scan for changes
    changes = scan_changes(root)
    return changes["all"]


def main():
    parser = argparse.ArgumentParser(
        description="Auto-archive skill: scan, commit, and push project files."
    )
    parser.add_argument("--root", required=True, help="Target git repository path")
    parser.add_argument("--files", nargs="*", help="Specific files to archive")
    parser.add_argument("--all", action="store_true", help="Archive all files (git add .)")
    parser.add_argument("--auto", action="store_true", help="Auto-detect changed files (default)")
    parser.add_argument("--message", type=str, help="Custom commit message")
    parser.add_argument("--dry-run", action="store_true", help="Preview only, do not execute")
    args = parser.parse_args()

    root = os.path.abspath(args.root)

    # Ensure git repo exists
    ensure_git_repo(root)

    # Determine files
    files = resolve_files(root, args)

    if not files:
        print("No files to archive. Exiting.")
        return

    # Generate or use custom commit message
    commit_msg = args.message if args.message else generate_commit_message(files)

    # Preview and confirm
    result = preview(files, commit_msg, root, dry_run=args.dry_run)

    if args.dry_run:
        return

    if result and result[0]:
        execute_archive(files, result[1], root)


if __name__ == "__main__":
    main()
