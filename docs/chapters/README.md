# 章別深掘り原稿

このディレクトリは, `docs/measure_theory_lebesgue_seminar_design_balanced.md` の章立てに従い, 各章をスライド化する前の本文原稿として展開したものである.

記法は原則として `docs/preliminary.md` および `docs/measure.md` に合わせる.特に, 集合族は $\mathfrak{F}, \mathfrak{B}$, 外測度は $\Gamma$ または Lebesgue 外測度の場合 $\mu^*$, 測度は $\mu$ と書く.また, 互いに素な集合の和は

$$
A_1 + A_2 + \cdots
$$

または

$$
\sum_{n=1}^{\infty} A_n
$$

と書くことがある.

## 章構成

1. [第0章 導入：測度論は何を拡張するのか](./00_introduction.md)
2. [第1章 古典的面積概念と Jordan 測度](./01_classical_area_jordan_measure.md)
3. [第2章 可算操作への移行：Lebesgue 外測度](./02_lebesgue_outer_measure.md)
4. [第3章 Carathéodory 可測性と Lebesgue 測度](./03_caratheodory_lebesgue_measure.md)
5. [第4章 抽象的測度空間](./04_measure_space.md)
6. [第5章 Riemann 積分から Lebesgue 積分へ](./05_riemann_to_lebesgue.md)
7. [第6章 可測函数と単函数](./06_measurable_simple_functions.md)
8. [第7章 Lebesgue 積分](./07_lebesgue_integral.md)
9. [第8章 極限と積分の交換](./08_limits_and_integrals.md)
10. [Appendix Radon-Nikodym の定理](./appendix_radon_nikodym.md)

## 方針

各章では, 次の順序を基本とする.

1. その章で扱う問題を明確にする.
2. 定義を数学的に正確に述べる.
3. 定義の意味を説明する.
4. 必要な例を最小限に置く.
5. 次章への接続を明記する.

直観的説明は用いるが, 定義の代用にはしない.
