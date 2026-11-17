import subprocess

repo = "/tmp/R46-T001-test"

tests = [
    ("test-area/project/.dart_tool/config.json", ".dart_tool/", 5),
    ("test-area/project/.packages", ".packages", 6),
    ("test-area/project/build/output.txt", "build/", 7),
]

negative_tests = [
    "test-area/project/.dart_tool-file",
    "test-area/project/.packages-backup",
    "test-area/project/build.txt",
    "test-area/near-miss/.dart_tool",
]

# Positive tests
for path, pattern, line in tests:
    result = subprocess.run(
        ["git", "check-ignore", "-v", "--no-index", path],
        capture_output=True,
        text=True,
        cwd=repo
    )

    output = result.stdout.strip()
    assert result.returncode == 0, f"{path} should be ignored"

    parts = output.split("\t")[0].split(":")
    actual_line = int(parts[1])
    actual_pattern = parts[2]

    assert actual_line == line, f"Wrong line for {path}"
    assert actual_pattern == pattern, f"Wrong pattern for {path}"

    print(f"PASS: {path} -> {actual_pattern} (line {actual_line})")

print("All positive tests passed!")

# Negative tests
for path in negative_tests:
    result = subprocess.run(
        ["git", "check-ignore", "-v", "--no-index", path],
        capture_output=True,
        text=True,
        cwd=repo
    )

    assert result.returncode == 1, f"{path} should NOT be ignored"

    print(f"PASS: {path} is not ignored")

print("All negative tests passed!")

# Git status verification
result = subprocess.run(
    ["git", "status", "--porcelain"],
    capture_output=True,
    text=True,
    cwd=repo
)

assert result.returncode == 0, "Git status command failed"

print("\nGit status --porcelain:")
print(result.stdout)