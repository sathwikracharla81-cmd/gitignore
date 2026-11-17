
import subprocess
import tempfile
from pathlib import Path


def run_git(repo, *args):
    return subprocess.run(
        ["git", *args],
        cwd=repo,
        text=True,
        capture_output=True
    )


def check(condition, message):
    assert condition, message
    print("PASS:", message)


with tempfile.TemporaryDirectory() as temp:
    repo = Path(temp)

    result = run_git(repo, "init")
    check(result.returncode == 0, "Temporary Git repository created")

    (repo / ".gitignore").write_text(
        ".ninja_deps\n"
        ".ninja_log\n"
        "\n"
        "!keep.ninja_log\n"
    )

    files = [
        ".ninja_deps",
        "build/.ninja_deps",
        ".ninja_log",
        "build/.ninja_log",
        ".ninja_deps-backup",
        ".ninja_log-backup",
        "keep.ninja_log",
    ]

    for name in files:
        path = repo / name
        path.parent.mkdir(parents=True, exist_ok=True)
        path.touch()

    expected = {
        ".ninja_deps": (True, ".ninja_deps"),
        "build/.ninja_deps": (True, ".ninja_deps"),
        ".ninja_log": (True, ".ninja_log"),
        "build/.ninja_log": (True, ".ninja_log"),
        ".ninja_deps-backup": (False, None),
        ".ninja_log-backup": (False, None),
        "keep.ninja_log": (False, "!keep.ninja_log"),
    }

    for name, (should_ignore, rule) in expected.items():
        result = run_git(
            repo, "check-ignore", "-v", "--no-index", name
        )
        output = result.stdout.strip()

        status = run_git(
            repo, "status", "--porcelain",
            "--untracked-files=all", "--", name
        )

        is_ignored = status.stdout.strip() == ""

        check(
            is_ignored == should_ignore,
            f"{name}: ignored status"
        )

        if rule:
            check(
                rule in output,
                f"{name}: matching rule is {rule}"
            )

    run_git(repo, "add", "-f", ".ninja_deps")

    tracked = run_git(
        repo, "check-ignore", "-v", ".ninja_deps"
    )
    check(
        tracked.returncode == 1,
        "Tracked file is not reported as ignored"
    )

    no_index = run_git(
        repo, "check-ignore", "-v", "--no-index", ".ninja_deps"
    )
    check(
        no_index.returncode == 0
        and ".ninja_deps" in no_index.stdout,
        "No-index check identifies the matching rule"
    )

    status = run_git(repo, "status", "--porcelain")
    check(
        "A  .ninja_deps" in status.stdout,
        "Tracked file appears in Git status"
    )

print("\nAll R46-T003 checks passed.")
