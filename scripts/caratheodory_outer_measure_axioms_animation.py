#!/usr/bin/env python3
"""Generate a Japanese GIF for the abstract outer-measure axioms."""

from __future__ import annotations

from pathlib import Path

import lebesgue_outer_measure_axioms_animation as base


base.OUTDIR = Path("figures/measure/animations/caratheodory_outer_measure_axioms")
base.FRAMES_DIR = base.OUTDIR / "frames"
base.GIF_DIR = base.OUTDIR / "gif"
base.GIF_PATH = base.GIF_DIR / "caratheodory_outer_measure_axioms.gif"

base.MEASURE_SYMBOL = "Γ"
base.EMPTY_SYMBOL = "∅"
base.SPACE_LABEL = "全体集合 X"
base.MAIN_TITLE = "Carathéodory の外測度 Γ の基本性質"
base.NONNEG_FORMULA = "Γ(∅)=0,  0 ≤ Γ(A) ≤ ∞"
base.MONOTONE_FORMULA = "A⊂B なら Γ(A) ≤ Γ(B)"
base.SUBADDITIVE_FORMULA = "Γ(A₁∪A₂∪...) ≤ Γ(A₁)+Γ(A₂)+..."


if __name__ == "__main__":
    base.build_animation()
