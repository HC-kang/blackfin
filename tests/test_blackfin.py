import copy
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
CHECKPOINT = ROOT / "scripts" / "blackfin_checkpoint.py"


def run(*args, cwd, check=True):
    return subprocess.run(
        args, cwd=cwd, check=check, text=True, capture_output=True
    )


class BlackfinTest(unittest.TestCase):
    def test_checkpoint_tracks_worktree_without_touching_index(self):
        with tempfile.TemporaryDirectory() as directory:
            repo = Path(directory)
            run("git", "init", "-q", cwd=repo)
            run("git", "config", "user.email", "blackfin@example.invalid", cwd=repo)
            run("git", "config", "user.name", "Blackfin Test", cwd=repo)
            (repo / "tracked.txt").write_text("base\n")
            run("git", "add", ".", cwd=repo)
            run("git", "commit", "-qm", "base", cwd=repo)

            clean = self.checkpoint(repo)
            self.assertEqual([], clean["changedFiles"])
            (repo / "tracked.txt").write_text("changed\n")
            (repo / "untracked.txt").write_text("new\n")
            (repo / ".blackfin").mkdir()
            (repo / ".blackfin" / "handoff.json").write_text("first")

            dirty = self.checkpoint(repo)
            self.assertEqual(["tracked.txt", "untracked.txt"], dirty["changedFiles"])
            self.assertNotEqual(clean["checkpoint"], dirty["checkpoint"])
            self.assertEqual(" M tracked.txt\n?? .blackfin/\n?? untracked.txt\n", run("git", "status", "--short", cwd=repo).stdout)
            self.assertEqual(0, run(sys.executable, CHECKPOINT, "--repo", repo, "--verify", dirty["checkpoint"], cwd=repo).returncode)

            (repo / ".blackfin" / "handoff.json").write_text("second")
            self.assertEqual(dirty["checkpoint"], self.checkpoint(repo)["checkpoint"])
            (repo / "untracked.txt").write_text("different\n")
            failed = run(sys.executable, CHECKPOINT, "--repo", repo, "--verify", dirty["checkpoint"], cwd=repo, check=False)
            self.assertEqual(1, failed.returncode)

    def checkpoint(self, repo):
        output = run(sys.executable, CHECKPOINT, "--repo", repo, "--json", cwd=repo).stdout
        return json.loads(output)

    def test_checkpoint_rejects_dirty_submodule(self):
        with tempfile.TemporaryDirectory() as directory:
            base = Path(directory)
            source, repo = base / "source", base / "repo"
            source.mkdir()
            repo.mkdir()
            for path in (source, repo):
                run("git", "init", "-q", cwd=path)
                run("git", "config", "user.email", "blackfin@example.invalid", cwd=path)
                run("git", "config", "user.name", "Blackfin Test", cwd=path)
            (source / "file.txt").write_text("base\n")
            run("git", "add", ".", cwd=source)
            run("git", "commit", "-qm", "base", cwd=source)
            (repo / "tracked.txt").write_text("base\n")
            run("git", "add", ".", cwd=repo)
            run("git", "commit", "-qm", "base", cwd=repo)
            run("git", "-c", "protocol.file.allow=always", "submodule", "add", "-q", source, "sub", cwd=repo)
            run("git", "commit", "-qam", "add submodule", cwd=repo)
            (repo / "sub" / "file.txt").write_text("dirty\n")

            result = run(sys.executable, CHECKPOINT, "--repo", repo, cwd=repo, check=False)
            self.assertEqual(2, result.returncode)
            self.assertIn("dirty submodule is unsupported", result.stderr)

    def test_schemas_enforce_hard_gates_and_packaged_copies_match(self):
        for name in ("acceptance-contract", "generator-handoff", "evaluation"):
            path = ROOT / "schemas" / f"{name}.schema.json"
            json.loads(path.read_text())

        contract = {
            "schemaVersion": "0.1.0",
            "objective": "Keep one result",
            "taskClass": "NORMAL",
            "requiredBehaviors": [{"id": "AC-1", "description": "One result", "mandatory": True}],
            "constraints": [],
            "assumptions": [],
            "unknowns": [],
            "verification": [{"criterion": "AC-1", "method": "test", "requirement": "Observe one result"}],
            "humanApprovalRequired": False,
        }
        self.assertSchema("acceptance-contract", contract)

        revision = {
            "head": "b" * 40,
            "worktreeState": "DIRTY",
            "checkpoint": "blackfin-checkpoint-v1:sha256:" + "c" * 64,
        }
        handoff = {
            "schemaVersion": "0.1.0",
            "role": "FORGE",
            "status": "READY_FOR_EVALUATION",
            "acceptanceContract": {"location": "contract.json", "sha256": "a" * 64},
            "revision": revision,
            "changedFiles": ["src/example.py"],
            "checks": [{"command": "test", "result": "PASS"}],
            "criteriaClaimed": ["AC-1"],
            "knownRisks": [],
            "uncertainties": [],
            "blockers": [],
        }
        self.assertSchema("generator-handoff", handoff)
        bad = copy.deepcopy(handoff)
        bad["checks"][0]["result"] = "FAIL"
        self.assertSchema("generator-handoff", bad, valid=False)
        bad = copy.deepcopy(handoff)
        bad["revision"] = {"head": "b" * 40, "worktreeState": "CLEAN", "checkpoint": revision["checkpoint"]}
        self.assertSchema("generator-handoff", bad, valid=False)

        evaluation = {
            "schemaVersion": "0.1.0",
            "role": "VIGIL",
            "decision": "FAIL",
            "acceptanceContract": handoff["acceptanceContract"],
            "revision": revision,
            "criteria": [{"id": "AC-1", "mandatory": True, "status": "FAIL", "evidence": ["Observed two"], "reproduction": ["Run race"]}],
            "checks": [{"command": "test", "result": "FAIL"}],
            "blockers": [],
            "summary": "Duplicate observed",
        }
        self.assertSchema("evaluation", evaluation)
        clean = copy.deepcopy(evaluation)
        clean["decision"] = "PASS"
        clean["revision"] = {"head": "b" * 40, "worktreeState": "CLEAN"}
        clean["criteria"][0]["status"] = "PASS"
        clean["criteria"][0].pop("reproduction")
        clean["checks"][0]["result"] = "PASS"
        self.assertSchema("evaluation", clean)
        del evaluation["criteria"][0]["reproduction"]
        self.assertSchema("evaluation", evaluation, valid=False)

        bad = copy.deepcopy(evaluation)
        bad["decision"] = "BLOCKED"
        bad["criteria"][0]["status"] = "BLOCKED"
        self.assertSchema("evaluation", bad, valid=False)

        bad = copy.deepcopy(handoff)
        bad["revision"]["checkpoint"] = "sha256:" + "c" * 64
        self.assertSchema("generator-handoff", bad, valid=False)

        copies = {
            "acceptance-contract": ROOT / "skills/blackfin-atlas/references/acceptance-contract.schema.json",
            "generator-handoff": ROOT / "skills/blackfin-forge/references/generator-handoff.schema.json",
            "evaluation": ROOT / "skills/blackfin-vigil/references/evaluation.schema.json",
        }
        for name, copy_path in copies.items():
            self.assertEqual((ROOT / "schemas" / f"{name}.schema.json").read_bytes(), copy_path.read_bytes())
        for role in ("blackfin-forge", "blackfin-vigil"):
            self.assertEqual(CHECKPOINT.read_bytes(), (ROOT / "skills" / role / "scripts" / CHECKPOINT.name).read_bytes())
            self.assertEqual((ROOT / "references/checkpoint.md").read_bytes(), (ROOT / "skills" / role / "references/checkpoint.md").read_bytes())

    def assertSchema(self, name, data, valid=True):
        with tempfile.NamedTemporaryFile("w", suffix=".json") as artifact:
            json.dump(data, artifact)
            artifact.flush()
            result = run(
                "npx",
                "--yes",
                "ajv-cli@5",
                "validate",
                "--spec=draft2020",
                "--strict=true",
                "-s",
                ROOT / "schemas" / f"{name}.schema.json",
                "-d",
                artifact.name,
                cwd=ROOT,
                check=False,
            )
        self.assertEqual(valid, result.returncode == 0, result.stdout + result.stderr)


if __name__ == "__main__":
    unittest.main()
