import copy
import importlib.util
import json
import re
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

            # A normal ignored artifact directory must not prevent checkpoint creation.
            (repo / ".gitignore").write_text(".blackfin/\nignored.tmp\n")
            (repo / "ignored.tmp").write_text("not source")
            (repo / "[literal].txt").write_text("literal pathspec")
            (repo / "tracked.txt").unlink()
            ignored = self.checkpoint(repo)
            self.assertEqual([".gitignore", "[literal].txt", "tracked.txt", "untracked.txt"], ignored["changedFiles"])
            (repo / ".blackfin" / "handoff.json").write_text("ignored evidence")
            (repo / "ignored.tmp").write_text("new cache")
            self.assertEqual(ignored, self.checkpoint(repo))
            self.assertEqual("", run("git", "diff", "--cached", cwd=repo).stdout)

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
            "schemaVersion": "0.2.0",
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
        minimal = copy.deepcopy(contract)
        for field in ("constraints", "assumptions", "unknowns"):
            minimal.pop(field)
        self.assertSchema("acceptance-contract", minimal)
        high_risk = dict(minimal, taskClass="HIGH_RISK")
        self.assertSchema("acceptance-contract", high_risk, valid=False)
        high_risk["humanApprovalRequired"] = True
        self.assertSchema("acceptance-contract", high_risk)
        self.assertSchema("acceptance-contract", dict(minimal, taskClass="TRIVIAL"), valid=False)
        self.assertSchema("acceptance-contract", dict(minimal, schemaVersion="0.1.0"), valid=False)

        revision = {
            "head": "b" * 40,
            "worktreeState": "DIRTY",
            "checkpoint": "blackfin-checkpoint-v1:sha256:" + "c" * 64,
        }
        handoff = {
            "schemaVersion": "0.2.0",
            "role": "FORGE",
            "status": "READY_FOR_EVALUATION",
            "acceptanceContract": {"location": "contract.json", "sha256": "a" * 64},
            "revision": revision,
            "changedFiles": ["src/example.py"],
            "checks": [{"command": "test", "result": "PASS", "mandatory": True}],
            "criteriaClaimed": ["AC-1"],
            "knownRisks": [],
            "uncertainties": [],
            "blockers": [],
        }
        self.assertSchema("generator-handoff", handoff)
        optional = copy.deepcopy(handoff)
        for field in ("criteriaClaimed", "knownRisks", "uncertainties"):
            optional.pop(field)
        optional["checks"].extend([
            {"command": "optional probe", "result": "FAIL", "mandatory": False, "evidence": "Unrelated optional diagnostic failed"},
            {"command": "optional environment", "result": "NOT_RUN", "mandatory": False, "evidence": "Optional environment unavailable"},
        ])
        self.assertSchema("generator-handoff", optional)
        bad_optional = copy.deepcopy(optional)
        del bad_optional["checks"][1]["evidence"]
        self.assertSchema("generator-handoff", bad_optional, valid=False)
        only_optional = copy.deepcopy(optional)
        only_optional["checks"] = only_optional["checks"][1:]
        self.assertSchema("generator-handoff", only_optional, valid=False)
        for result in ("FAIL", "NOT_RUN"):
            bad_gate = copy.deepcopy(optional)
            bad_gate["checks"][0]["result"] = result
            self.assertSchema("generator-handoff", bad_gate, valid=False)
        blocked_ready = dict(optional, blockers=["Missing required environment"])
        self.assertSchema("generator-handoff", blocked_ready, valid=False)
        missing_flag = copy.deepcopy(handoff)
        del missing_flag["checks"][0]["mandatory"]
        self.assertSchema("generator-handoff", missing_flag, valid=False)
        bad = copy.deepcopy(handoff)
        bad["checks"][0]["result"] = "FAIL"
        self.assertSchema("generator-handoff", bad, valid=False)
        bad = copy.deepcopy(handoff)
        bad["revision"] = {"head": "b" * 40, "worktreeState": "CLEAN", "checkpoint": revision["checkpoint"]}
        self.assertSchema("generator-handoff", bad, valid=False)

        evaluation = {
            "schemaVersion": "0.2.0",
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
        self.assertSchema("evaluation", dict(clean, blockers=["Reviewed state drifted"]), valid=False)
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

    def test_skill_entrypoints_stay_small_and_portable(self):
        link = re.compile(r"\]\(([^)#]+)\)")
        for skill_dir in sorted((ROOT / "skills").iterdir()):
            text = (skill_dir / "SKILL.md").read_text()
            head, body = text.split("\n---\n", 1)
            fields = dict(line.split(": ", 1) for line in head.splitlines()[1:])
            self.assertEqual({"name", "description"}, set(fields), skill_dir.name)
            self.assertEqual(skill_dir.name, fields["name"])
            self.assertLessEqual(len(fields["description"]), 300, skill_dir.name)
            self.assertLessEqual(len(body.splitlines()), 60, skill_dir.name)
            for target in link.findall(body):
                self.assertTrue((skill_dir / target).is_file(), f"{skill_dir.name}: {target}")
        orchestrator = (ROOT / "skills/blackfin-orchestrator/SKILL.md").read_text()
        for phrase in ("worktree note", "before completion", "trivial tasks included", "Verify the write"):
            self.assertIn(phrase, orchestrator)

    def test_report_check_blocks_text_dumps_and_passes_template(self):
        spec = importlib.util.spec_from_file_location("report_check", ROOT / "skills/blackfin-report/scripts/report_check.py")
        report_check = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(report_check)
        template = (ROOT / "skills/blackfin-report/assets/report-template.html").read_text()
        self.assertEqual(([], []), report_check.check(template)[:2])
        # Printing must not drop rows a filter hid, because print hides the filter chips.
        print_css = re.search(r"@media print \{(.*?)\n\}", template, re.S).group(1)
        self.assertIn("tr[hidden] { display: table-row; }", print_css)
        # Korean feedback the script writes into buttons is interface text, so it uses 합니다체.
        script = re.search(r"<script>(.*?)</script>", template, re.S).group(1)
        feedback = re.findall(r'textContent = "([^"]*[가-힣][^"]*)"', script)
        self.assertTrue(feedback)
        for text in feedback:
            self.assertRegex(text, r"(니다|십시오)\.$")

        title, viewport = "<title>t</title>", "<meta name=viewport content=width=device-width>"
        head = f"<!doctype html><html><head>{title}{viewport}</head><body><h1>Report</h1>"
        table = "<table><tr><td>1</td></tr></table>"
        prose = "<p>" + "The migration moved most endpoints and some are blocked. " * 12 + "</p>"
        lead = "<p>We changed <code>queue.py</code>. " + "The worker now retries failed jobs with backoff and logs each attempt. " * 20 + "</p>"
        page = lambda body, h=head: h + body + "</body></html>"
        cases = {
            "no <title>": page(table, head.replace(title, "")),
            "no <meta name=viewport>": page(table, head.replace(viewport, "")),
            "not self-contained": [page(d + table) for d in (
                '<link rel=stylesheet href="https://fonts.example/x.css">', '<link rel=stylesheet href="theme.css">',
                '<img srcset="https://example.com/a.png 1x" alt="plot">', '<script src="app.js"></script>',
                '<style>@import url(theme.css);</style>', '<script type="module">import * as d3 from "https://cdn.example/d3.js";</script>',
                '<svg role="img" aria-label="x"><image href="https://example.com/p.png"/></svg>', '<svg role="img" aria-label="x"><use href="sprite.svg#i"/></svg>',
                '<img srcset="data:image/png;base64,AAAA 1x, https://example.com/plot.png 2x" alt="plot">',
            )],
            "no visual encoding": [page(b) for b in (
                '<div style="width:100%">Finished.</div>', '<template><svg aria-label="chart"></svg></template><p>Finished.</p>',
                '<svg aria-hidden="true"><path d="M0 0"/></svg><p>Finished.</p>', '<svg style="display:none" aria-label="x"></svg><p>Finished.</p>',
                '<div hidden><table><tr><td>1</td></tr></table></div><p>Finished.</p>', '<div style="height:100%"></div><p>Finished.</p>',
                '<div style="--gap:16px"></div><p>Finished.</p>', '<div style="width:0%"></div><p>Finished.</p>',
                '<svg aria-label="chart"></svg><p>Finished.</p>',
            )],
            "text dump": [page("<div class=card>" + prose * 3 + "</div>"), page("<figure>" + prose * 3 + "</figure>" + table)],
            "a text block has": [page("<figure><p>" + "All endpoints migrated successfully. " * 90 + "</p></figure>" + table),
                                 head + table + "<p>" + "word " * 101,
                                 page("<p>" + "one two<br>" * 60 + "</p>" + table)],
            "characters of prose before": page(lead + table),
        }
        for prefix, htmls in cases.items():
            for html in htmls if isinstance(htmls, list) else [htmls]:
                fails = report_check.check(html)[0]
                self.assertTrue(any(prefix in f for f in fails), (prefix, html[:120], fails))

        self.assertEqual([], report_check.check(page('<div role="img" aria-label="1 of 1 done">■</div>'))[0])
        for clean in ('<style>/* url(x.png) */</style>', '<style>@import url("data:text/css,body{color:red}");</style>',
                      '<script>// import x from "https://cdn.example/x.js";\nconst example = \'import x from "old.js";\';</script>',
                      "<p>" + "w<b>or</b>d " * 35 + "</p>", "<p hidden>" + "word " * 110 + "</p>"):
            self.assertEqual([], report_check.check(page(clean + table))[0], clean)
        hidden_padding = "<div class=card>" + ("<p>" + "migration " * 30 + "</p>") * 5 + "</div><pre hidden>" + "word " * 400 + "</pre>"
        self.assertTrue(any(f.startswith("text dump") for f in report_check.check(page(hidden_padding + table))[0]))
        words = lambda body: report_check.check(page(body + table))[2]["longestBlockWords"]
        self.assertEqual(20, words("<p>" + "one two<br>" * 10 + "</p>"))
        self.assertEqual(4, words("<div>alpha omega<p>x</p>tail beta</div>"))
        self.assertEqual(1, words("<div>" + "one<br hidden>" * 101 + "</div>"))
        self.assertEqual(1, words("<div>one<span hidden><br></span>two</div>"))
        self.assertEqual(1, words("<div>one<div hidden>x</div>two</div>"))
        long_sentence = "<p>" + "word " * 30 + "end. Short one.</p>"
        self.assertTrue(any("ASD-STE100" in w for w in report_check.check(page(long_sentence + table))[1]))
        self.assertFalse(any("ASD-STE100" in w for w in report_check.check(page("<p>" + "word " * 20 + "end. " * 3 + "</p>" + table))[1]))
        warns = report_check.check(page(table + '<svg></svg><svg aria-label="x"><title>x</title></svg>'))[1]
        self.assertTrue(any("without aria-label" in w for w in warns), warns)
        warns = report_check.check(page(table + '<style>@media only print { a { color: #000 } }</style>'))[1]
        self.assertFalse(any("print" in w for w in warns), warns)

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
