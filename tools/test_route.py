#!/usr/bin/env python3
"""Behavior tests for the router. Run: python3 tools/test_route.py"""
import os
import sys
import unittest

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, "plugins", "modelwise", "skills", "modelwise", "scripts"))
import route  # noqa: E402

REG = route.load_registry()
TASKS = [t["id"] for t in REG[0]["tasks"]]
CX = ("simple", "moderate", "complex", "frontier")


def r(task, cx="moderate", priority="balanced", provider="any"):
    return route.route(task, cx, priority, provider, registry=REG)


class RouterTests(unittest.TestCase):
    def test_every_task_has_a_route_or_fallback(self):
        for t in TASKS:
            for cx in CX:
                res = r(t, cx)
                self.assertTrue(res["recommended"] or (res["fallback"] and res["fallback"]["route"]["recommended"]),
                                "%s/%s has no route" % (t, cx))

    def test_never_recommends_deprecated_or_restricted(self):
        for t in TASKS:
            for cx in CX:
                for p in ("quality", "balanced", "cost", "speed"):
                    rec = r(t, cx, p)["recommended"]
                    if rec:
                        self.assertIn(rec["status"], ("current", "previous"), "%s %s %s" % (t, cx, p))

    def test_media_capabilities_respected(self):
        self.assertEqual(r("image.generate")["recommended"]["provider"], "openai")
        self.assertIsNone(r("image.generate", provider="anthropic")["recommended"])
        self.assertIsNone(r("video.generate")["recommended"])
        self.assertIsNotNone(r("video.generate")["fallback"])

    def test_media_without_prices_ranks_by_fit(self):
        res = r("image.generate", "moderate")
        self.assertEqual(res["recommended"]["model"], "gpt-image-2.5-sunburst")
        self.assertIn("no published prices", res["ranking_basis"])

    def test_palette_contrast_and_scale(self):
        sys.path.insert(0, os.path.join(ROOT, "plugins", "modelwise", "skills", "modelwise", "scripts"))
        import palette
        self.assertAlmostEqual(palette.contrast((0, 0, 0), (255, 255, 255)), 21.0, places=1)
        r = palette.analyse(["0a4e9b", "e41f26", "d1e5ad"])
        verdict = {t["text"]: t["normal_text"] for t in r["text_on_primary"]}
        self.assertEqual(verdict["white"], "pass")
        self.assertEqual(verdict["#e41f26"], "fail")   # red text on the blue is unreadable
        self.assertEqual([s["step"] for s in r["colours"][0]["scale"]], ["900", "700", "500", "300", "100"])

    def test_cost_priority_is_never_pricier_than_balanced(self):
        for t in TASKS:
            b, c = r(t, "moderate", "balanced")["recommended"], r(t, "moderate", "cost")["recommended"]
            if b and c and b["est_cost_usd"] is not None and c["est_cost_usd"] is not None:
                self.assertLessEqual(c["est_cost_usd"], b["est_cost_usd"], t)

    def test_quality_priority_has_highest_fit(self):
        for t in TASKS:
            res = r(t, "complex", "quality")
            if res["recommended"]:
                self.assertEqual(res["recommended"]["fit"], max(x["fit"] for x in res["ranked"]), t)

    def test_effort_is_a_supported_level(self):
        cards = {c["id"]: c for c in REG[2]}
        for t in TASKS:
            for cx in CX:
                for o in r(t, cx)["ranked"]:
                    levels = cards[o["model"]]["effort"]["levels"]
                    if levels and o["effort"] is not None:
                        self.assertIn(o["effort"], levels, "%s %s %s" % (t, cx, o["model"]))

    def test_harder_tasks_never_get_lower_effort(self):
        order = ["E0", "E1", "E2", "E3", "E4", "E5", "E6"]
        for t in REG[0]["tasks"]:
            levels = [order.index(t["effort"][cx]) for cx in CX]
            self.assertEqual(levels, sorted(levels), t["id"])

    def test_provider_filter(self):
        for p in ("anthropic", "openai"):
            for o in r("code.build", "complex", provider=p)["ranked"]:
                self.assertEqual(o["provider"], p)

    def test_cost_comparison_covers_both_vendors_and_marks_pick(self):
        for t in ("code.build", "text.write", "data.extract"):
            res = r(t, "moderate")
            rows = res["cost_comparison"]
            self.assertEqual({x["provider"] for x in rows}, {"anthropic", "openai"}, t)
            self.assertEqual([x["model"] for x in rows if x["note"] == "recommended"], [res["recommended"]["model"]], t)
            costs = [x["est_cost_usd"] for x in rows if x["est_cost_usd"] is not None]
            self.assertEqual(costs, sorted(costs), t)
            self.assertTrue(all(x["model"] for x in rows if x["note"] != "recommended"))

    def test_volume_totals_and_inline_tips(self):
        res = route.route("data.extract", "simple", "cost", "any", registry=REG, volume=10000)
        row = res["volume"]["rows"][0]
        per_run = res["cost_comparison"][0]["est_cost_usd"]
        self.assertAlmostEqual(row["total_usd"], round(per_run * 10000, 2), places=2)
        self.assertAlmostEqual(row["total_batch_usd"], round(per_run * 10000 * 0.5, 2), places=2)
        self.assertTrue(res["recommended"]["prompt_tips"])
        self.assertIsNone(r("code.build")["volume"])

    def test_known_sensible_picks(self):
        # Guards against accidental regressions in fit ratings or scoring.
        self.assertIn(r("data.extract", "simple")["recommended"]["tier"], ("fast",))
        self.assertIn(r("code.build", "complex")["recommended"]["tier"], ("flagship", "frontier"))
        self.assertEqual(r("reason.hard", "frontier")["recommended"]["tier"], "frontier")


if __name__ == "__main__":
    unittest.main(verbosity=1)
