---
theme: default
title: 測度論から確率論へ
info: |
  理学部出身者向けの確率論勉強会資料。
  PDF出力を前提に、定義・直感・応用の流れを重視する。
class: text-left
drawings:
  persist: false
transition: none
routerMode: hash
mdc: true
comark: true
fonts:
  sans: Noto Sans JP
  serif: Noto Serif JP
  mono: Fira Code
layout: cover
---

# 測度論から確率論へ

確率変数・収束・確率過程・応用までの見取り図

[40-60分想定 / 測度論・Lebesgue積分の概論後]{class="mt-10 text-sm opacity-70"}

---
layout: two-cols-header
---

# 今日のゴール

測度論の言葉で確率論を読み替え、確率論でよく出てくる対象の位置づけをつかむ。

::left::

## 前半

- 確率空間と確率変数
- 分布と期待値
- 独立性
- 4種類の収束
- 大数の法則と中心極限定理

::right::

## 後半

- 確率過程
- Poisson過程
- Brown運動とMarkov性
- 条件付き期待値とMartingale
- 伊藤の公式の入口
- Black-Scholesと最適戦略

---

# 時間配分

PDFとして読んでも流れが追えるように、定義はやや明示的に残す。

| パート | 内容 | 目安 |
|---|---|---:|
| 1 | 確率空間・確率変数・分布 | 8分 |
| 2 | 独立性・期待値・収束概念 | 12分 |
| 3 | 大数の法則・中心極限定理 | 8分 |
| 4 | 確率過程・条件付き期待値・Martingale | 15分 |
| 5 | 伊藤の公式・Black-Scholes・最適戦略 | 12分 |
| 6 | まとめ・議論 | 5分 |

---
layout: section
---

# 1. 測度論から確率論へ

---

# 確率空間

測度空間 $(\Omega,\mathcal{F},P)$ が以下を満たすとき、**確率空間** と呼ぶ。

$$
P(\Omega)=1
$$

| 記号 | 確率論での読み方 |
|---|---|
| $\Omega$ | 標本空間 |
| $\omega\in\Omega$ | 標本、実現値 |
| $A\in\mathcal{F}$ | 事象 |
| $P(A)$ | 事象 $A$ の確率 |

::note
測度論の a.e. は、確率論では a.s. と呼ぶ。$\mathcal{F}$ は「観測・判定できる事象の集まり」と見ると、後の filtration とつながりやすい。
::

---
layout: two-cols-header
---

# 確率測度の具体例

同じ「測度と積分」の形で、離散分布と連続分布を見ておく。

::left::

## 離散: 二項分布

$X\sim\mathrm{Bin}(n,p)$ とする。

$$
\Omega=\{0,1,\dots,n\},\quad \mathcal{F}=2^\Omega
$$

$$
P(\{k\})=\binom{n}{k}p^k(1-p)^{n-k}
$$

関数 $f:\Omega\to\mathbb{R}$ の積分は

$$
\int_\Omega f\,dP=\sum_{k=0}^n f(k)P(\{k\})
$$

::right::

## 連続: 正規分布

$X\sim N(\mu,\sigma^2)$ とする。

$$
\Omega=\mathbb{R},\quad \mathcal{F}=\mathcal{B}(\mathbb{R})
$$

$$
P(A)=\int_A
\frac{1}{\sqrt{2\pi\sigma^2}}
\exp\left(-\frac{(x-\mu)^2}{2\sigma^2}\right)\,dx
$$

関数 $f:\mathbb{R}\to\mathbb{R}$ の積分は

$$
\int_\mathbb{R} f\,dP
=\int_\mathbb{R} f(x)\varphi_{\mu,\sigma}(x)\,dx
$$

---
layout: two-cols-header
---

# 確率変数

実数値確率変数とは、可測写像

$$
X:(\Omega,\mathcal{F})\to(\mathbb{R},\mathcal{B}(\mathbb{R}))
$$

のこと。

::left::

## 定義の読み方

| 要素 | 意味 |
|---|---|
| $\Omega$ | 起こりうる全ての標本 |
| $X(\omega)$ | 標本から取り出した数値 |
| 可測性 | $X\in B$ の確率を定義できる条件 |

確率変数は「ランダムな値」ではなく、標本から観測量を取り出す写像。

::right::

::example-box{title="例: サイコロ2個の合計を見る"}
サイコロ2個を振る。

$$
\Omega=\{1,\dots,6\}^2
$$

合計を見るなら

$$
X(\omega_1,\omega_2)=\omega_1+\omega_2
$$

同じ合計になる出方は、$X$ だけを見ると区別しない。
::

---

# 分布

確率変数 $X$ により、値域側に新しい確率測度を定義できる。

$$
P_X(A)
=P(X^{-1}(A))
=P(\{\omega\in\Omega:X(\omega)\in A\})
$$

これを $X$ の **分布** という。

::diagram
$(\Omega,\mathcal{F},P)$
$\xrightarrow{\quad X\quad}$
$(S,\mathcal{S},P_X)$
::

::note
測度論では pushforward measure と呼ぶ考え方。確率論では「$X$ の分布」と呼ぶことが多い。
::

---

# 期待値

可積分な確率変数 $X$ に対して、

$$
E[X]=\int_{\Omega}X(\omega)\,P(d\omega)
$$

と定義する。

分布 $P_X$ を使えば、Borel可測な $f$ に対して

$$
E[f(X)]=\int_S f(x)\,P_X(dx)
$$

と書ける。

::note
測度論での積分が、そのまま期待値になる。確率論固有の記法に見えて、中身は Lebesgue 積分。
::

---

# 生成する$\sigma$加法族

確率変数 $X$ が生成する $\sigma$ 加法族は

$$
\sigma(X)=\{X^{-1}(B):B\in\mathcal{B}(\mathbb{R})\}
$$

を含む最小の $\sigma$ 加法族。

$X$ を観測して判別できる事象の全体。

::example-box{title="例: 2回のコイントスを「1回でも表が出たか」だけで見る"}
標本空間を $\Omega=\{0,1\}^2$、$X(\omega)=\max(\omega_1,\omega_2)$ とする。

$$
A_0=X^{-1}(\{0\})=\{(0,0)\},\quad
A_1=X^{-1}(\{1\})=\{(0,1),(1,0),(1,1)\}
$$

$$
\sigma(X)=\{\emptyset,A_0,A_1,\Omega\}
$$

$(0,1),(1,0),(1,1)$ は $X=1$ としか見えないので区別できない。
::

::note
生成する $\sigma$ 加法族は、後で filtration を「時刻 $t$ までに分かる情報」と読むための土台になる。
::

---

# 独立性

事象 $A,B$ が独立とは

$$
P(A\cap B)=P(A)P(B)
$$

であること。

部分 $\sigma$ 加法族 $\mathcal{G},\mathcal{H}\subset\mathcal{F}$ が独立とは、

$$
P(G\cap H)=P(G)P(H)
\quad(G\in\mathcal{G},\ H\in\mathcal{H})
$$

が成り立つこと。

確率変数 $X,Y$ が独立とは、

$$
\sigma(X)\text{ と }\sigma(Y)
$$

が独立であること。

::note
「値が無関係」という直感を、可測集合全体の積構造として定式化している。
::

---
layout: section
---

# 2. 収束概念

---

# 確率変数列の4つの収束

同じ確率空間上の確率変数列 $X_n$ と $X$ を考える。

| 収束 | 定義 | 見方 |
|---|---|---|
| 概収束 | $X_n\to X$ a.s. | 標本ごとに見る |
| 確率収束 | $P(\lvert X_n-X\rvert>\varepsilon)\to0$ | 外れる確率を見る |
| $L^p$ 収束 | $E[\lvert X_n-X\rvert^p]\to0$ | 距離の平均を見る |
| 法則収束 | $P_{X_n}\Rightarrow P_X$ | 分布だけを見る |

::note
法則収束は分布だけを見る。$X_n$ と $X$ が同一の確率空間上にある必要はない。
::

---
layout: two-cols-header
---

# 法則収束と弱収束

法則収束とは、確率変数の分布が弱収束すること。

$$
X_n\Rightarrow X
\quad\Longleftrightarrow\quad
P_{X_n}\Rightarrow P_X
$$

::left::

## 関数で見る

任意の有界連続関数 $f$ に対して

$$
\int f\,dP_{X_n}\to \int f\,dP_X
$$

すなわち

$$
E[f(X_n)]\to E[f(X)]
$$

::right::

## 分布関数で見る

実数値の場合、$F_X$ の連続点 $x$ で

$$
F_{X_n}(x)\to F_X(x)
$$

と同値。

中心極限定理は、この意味で正規分布へ近づくことを述べる。

---

# 収束概念の関係

基本的な含意関係は次の通り。

$$
\left.
\begin{array}{c}
L^p\text{収束}\\
\text{概収束}
\end{array}
\right\}
\Rightarrow
\text{確率収束}
\Rightarrow
\text{法則収束}
$$

::note
上にあるほど、同じ標本空間上で強い比較をしている。右へ行くほど分布だけを見る話になる。
::

---
layout: section
---

# 3. 大数の法則と中心極限定理

---
layout: two-cols-header
---

# 大数の法則

$X_1,X_2,\dots$ を独立同分布、$E[|X_1|]<\infty$ とする。

標本平均

$$
\overline{X}_n=\frac{1}{n}\sum_{k=1}^n X_k
$$

は、期待値 $m=E[X_1]$ に近づく。

::left::

## 弱法則

$$
\overline{X}_n\to m
$$

in probability

各 $n$ で外れる確率が小さくなる。

$$
P(|\overline{X}_n-m|>\varepsilon)\to0
$$

::right::

## 強法則

$$
\overline{X}_n\to m
$$

almost surely

ほとんどすべての標本列で、最終的に平均が近づく。

$$
P\left(\lim_{n\to\infty}\overline{X}_n=m\right)=1
$$

---
layout: two-cols-header
---

# 大数の法則の直感

個々の試行は揺らぐが、平均を取ると揺らぎがならされる。

::left::

## サイコロの平均

サイコロを何度も振ると、出目の平均は $3.5$ に近づく。

$$
\overline{X}_n=\frac{1}{n}\sum_{k=1}^nX_k
$$

ただし、有限回では当然ぶれる。

::right::

## 分散有限なら

$$
\mathrm{Var}(\overline{X}_n)
=\frac{\mathrm{Var}(X_1)}{n}
$$

これは定理そのものではなく、平均のばらつきが小さくなる直感を与える式。

---

# 中心極限定理

$X_1,X_2,\dots$ を独立同分布、$E[X_1]=m$、$\mathrm{Var}(X_1)=\sigma^2<\infty$ とする。

標本平均の揺らぎを $\sqrt{n}$ 倍して見ると、

$$
\sqrt{n}\frac{\overline{X}_n-m}{\sigma}
\Rightarrow N(0,1)
$$

すなわち、標準化した標本平均が標準正規分布へ **法則収束** する。

::note
平均そのものは $m$ に近づく。一方、$\sqrt{n}$ 倍して揺らぎを拡大すると、極限分布として正規分布が現れる。
::

---

# 大数の法則と中心極限定理の違い

| 定理 | 見ているもの | 結論 |
|---|---|---|
| 大数の法則 | 平均の極限 | 定数 $m$ へ収束 |
| 中心極限定理 | 平均の揺らぎ | 正規分布へ法則収束 |

$$
\overline{X}_n\to m
$$

$$
\sqrt{n}\frac{\overline{X}_n-m}{\sigma}\Rightarrow N(0,1)
$$

::note
「平均が収束する」と「収束の周りの揺らぎがどう見えるか」は別の問い。
::

---
layout: section
---

# 4. 確率過程

---

# 確率過程

確率過程とは、時間 $t$ をパラメータにもつ確率変数の族。

$$
X=(X_t)_{t\ge0}
$$

各 $t$ に対して

$$
X_t:\Omega\to\mathbb{R}^d
$$

が確率変数である。

::note
$\omega$ を固定すると $t\mapsto X_t(\omega)$ という関数が得られる。これを標本路という。
::

---

# 経路値確率変数として見る

連続な標本路を持つ過程なら、

$$
X:\Omega\to C([0,\infty),\mathbb{R}^d)
$$

という関数空間値確率変数として見られる。

::diagram
$\omega$
$\longmapsto$
$(X_t(\omega))_{t\ge0}$
::

::note
確率過程は「時間ごとの確率変数の族」でもあり、「ランダムな関数」でもある。
::

---

# 可測性と適合性

まず、時刻とともに情報が増える状況を

$$
(\mathcal{F}_t)_{t\ge0},\quad
\mathcal{F}_s\subseteq\mathcal{F}_t\ (s\le t)
$$

で表す。これを **filtration**、または情報増大系という。

| 概念 | 意味 |
|---|---|
| 適合性 | $X_t$ が $\mathcal{F}_t$ 可測 |
| 可測性 | $(t,\omega)\mapsto X_t(\omega)$ が直積空間上で可測 |

::note
例: 株価 $S_t$ を時刻 $t$ まで観測しているなら、$\mathcal{F}_t$ は「時刻 $t$ までの株価から分かる事象」の集まり。
::

---
layout: two-cols-header
---

# 情報増大系の例

サイコロを2回振る。標本空間は $\Omega=\{1,\dots,6\}^2$ とする。

::left::

## 時刻1

1回目だけ見える。

$$
\mathcal{F}_1=\sigma(\omega_1)
$$

この時点では、2回目の出目はまだ区別できない。

::right::

## 時刻2

2回目まで見える。

$$
\mathcal{F}_2=\sigma(\omega_1,\omega_2)
$$

$$
\mathcal{F}_1\subseteq\mathcal{F}_2
$$

情報は時間とともに増える。

---

# 条件付き期待値

部分 $\sigma$ 加法族 $\mathcal{G}\subset\mathcal{F}$ に対する条件付き期待値

$$
E[X\mid\mathcal{G}]
$$

は、$\mathcal{G}$ の情報だけで作る $X$ の予測値。

厳密には、$\mathcal{G}$ 可測な確率変数 $Y$ で、任意の $G\in\mathcal{G}$ に対して

$$
\int_G Y\,dP=\int_G X\,dP
$$

を満たすものを $E[X\mid\mathcal{G}]$ と書く。

::note
条件付き期待値は「条件付き確率の平均版」というだけでなく、情報を粗くしたときの最良予測として働く。
::

---
layout: two-cols-header
---

# 条件付き期待値の見方

::left::

## 情報で粗く見る

$E[X\mid\mathcal{G}]$ は $\mathcal{G}$ 可測なので、$\mathcal{G}$ で区別できない標本には同じ値を返す。

細かい未来の情報は使わず、今見える情報だけで平均を取る。

::right::

## 時間付きで見る

情報増大系 $(\mathcal{F}_t)$ に対して、

$$
E[X\mid\mathcal{F}_t]
$$

は「時刻 $t$ までの情報から見た $X$ の予測」。

金融では、将来ペイオフの現在時点での価値を表すときに現れる。

---
layout: two-cols-header
---

# Poisson過程

Poisson過程 $(N_t)_{t\ge0}$ は、ランダムな到着回数を数える過程。

強度 $\lambda>0$ のPoisson過程では、

$$
N_t-N_s\sim \mathrm{Poisson}(\lambda(t-s))
$$

かつ、互いに重ならない時間区間の増分は独立。

::left::

## 具体例

- コールセンターへの着信数
- 工場ラインの不良品発生数
- Webサイトへのアクセス数
- 放射性崩壊の観測数

::right::

## 時刻 $t$ までの回数

$$
P(N_t=k)=e^{-\lambda t}\frac{(\lambda t)^k}{k!}
$$

$\lambda$ は単位時間あたりの平均発生回数。

---
layout: two-cols-header
---

# Poisson過程と待ち時間

イベントの到着時刻を

$$
0<T_1<T_2<\cdots
$$

とする。

::left::

## 最初の待ち時間

$$
P(T_1>t)=P(N_t=0)=e^{-\lambda t}
$$

したがって

$$
T_1\sim \mathrm{Exp}(\lambda)
$$

::right::

## 記憶なし性

指数分布は

$$
P(T>s+t\mid T>s)=P(T>t)
$$

を満たす。

「しばらく来ていないから、そろそろ来るはず」とはならない。

---

# Brown運動

1次元Brown運動、またはWiener過程 $(W_t)_{t\ge0}$ は、次を満たす連続確率過程。

1. $W_0=0$ a.s.
2. 標本路 $t\mapsto W_t(\omega)$ は連続
3. $0\le s<t$ に対して $W_t-W_s\sim N(0,t-s)$
4. 重ならない時間区間の増分は独立

::note
連続な標本路を持つが、典型的には非常に荒く、有限変動でも微分可能でもない。
::

---

# Wiener測度

Brown運動は、経路空間

$$
C_0([0,\infty),\mathbb{R})
$$

上の確率測度としても理解できる。

この経路空間上で、座標過程

$$
W_t(w)=w(t)
$$

がBrown運動になるような確率測度をWiener測度という。

::note
確率過程を「経路空間上の確率測度」と見る視点は、測度論的確率論の中心的な発想。
::

---

# Markov性

Markov性は、未来の分布が現在だけで決まり、過去の詳細には依存しないという性質。

Brown運動では、

$$
W_{t+s}-W_s
$$

が $\mathcal{F}_s$ と独立で、分布は $W_t$ と同じ。

条件付き期待値で書けば、

$$
E[f(W_{t+s})\mid\mathcal{F}_s]
=E_{W_s}[f(W_t)]
$$

---
layout: two-cols-header
---

# Martingale

情報増大系 $(\mathcal{F}_t)$ に適合した過程 $(M_t)$ が **Martingale** とは、

$$
E[|M_t|]<\infty
$$

かつ $s\le t$ に対して

$$
E[M_t\mid\mathcal{F}_s]=M_s
$$

を満たすこと。

::left::

## Markov性との違い

Markov性は「未来の分布が現在で決まる」という性質。

Martingaleは「未来の条件付き期待値が現在値と一致する」という性質。

::right::

::example-box{title="例"}
独立な平均0の増分を足した

$$
M_n=\sum_{k=1}^n \xi_k
$$

は離散時間Martingale。

Wiener過程 $(W_t)$ もMartingale。
::

---

# 伊藤積分は紹介に留める

Brown運動に沿った積分

$$
\int_0^t H_s\,dW_s
$$

は、普通のリーマン-Stieltjes積分としては扱いにくい。

Brown運動の標本路は連続だが、典型的には有界変動ではないため。

この勉強会では、伊藤積分の構成は深入りせず、次の2点だけ押さえる。

- 未来を見ない適合過程に対して定義される積分
- 伊藤の公式で、通常の微分公式とは違う2階微分項が現れる

---
layout: two-cols-header
---

# 伊藤の公式

過程 $X_t$ が

$$
dX_t=b(t,X_t)\,dt+\sigma(t,X_t)\,dW_t
$$

で動くとき、滑らかな関数 $f(t,x)$ に対して

$$
df(t,X_t)
=\partial_t f\,dt+\partial_x f\,dX_t
+\frac{1}{2}\partial_{xx}f\,(dX_t)^2
$$

と書ける。

::left::

## 通常の微分との違い

古典的な連鎖律なら1階微分だけでよい。

Brown運動では揺らぎの2乗が $dt$ と同じ次数で残る。

::right::

## 記号計算の要点

$$
(dW_t)^2=dt,\quad dW_t\,dt=0,\quad (dt)^2=0
$$

というルールで2階微分項が残る。

---

# 2階微分項が残る意味

普通の滑らかな経路なら、微小変化の2乗は高次の小さい量として消える。

しかしBrown運動では、

$$
W_{t+\Delta t}-W_t
$$

の大きさが典型的に $\sqrt{\Delta t}$ 程度なので、2乗すると $\Delta t$ 程度になる。

つまり、

$$
(\Delta W)^2\sim \Delta t
$$

が極限で無視できず、伊藤の公式に

$$
\frac12\sigma^2\partial_{xx}f\,dt
$$

が現れる。

::note
金融工学では、この2階微分項がBlack-Scholes方程式のガンマ項につながる。
::

---
layout: two-cols-header
---

# 確率微分方程式の例

::left::

## Brown運動に駆動される

$$
dX_t=b(t,X_t)\,dt+\sigma(t,X_t)\,dW_t
$$

ドリフト項とランダムな揺らぎを持つ過程。

::right::

## 幾何Brown運動

$$
dS_t=\mu S_t\,dt+\sigma S_t\,dW_t
$$

金融で株価モデルとして使われる。相対変化率にノイズが入る形。

---
layout: section
---

# 5. 応用

---

# Black-Scholesモデル

株価 $S_t$ を幾何Brown運動でモデル化する。

$$
dS_t=\mu S_t\,dt+\sigma S_t\,dW_t
$$

ここで、

| 記号 | 意味 |
|---|---|
| $\mu$ | 平均成長率 |
| $\sigma$ | ボラティリティ |
| $W_t$ | Wiener過程 |

::note
価格そのものではなく、相対変化率にランダムな揺らぎが入るモデル。
::

---
layout: two-cols-header
---

# オプションとは何か

オプションは、将来の時点で資産を売買する **権利**。

義務ではない。

::left::

## コールオプション

満期 $T$ に、株を価格 $K$ で買う権利。

満期の価値は

$$
(S_T-K)^+
$$

::right::

## 直感

$S_T>K$ なら、安く買えるので得をする。

$S_T\le K$ なら、権利を行使しない。

損失は最初に払うプレミアムに限られる。

---

# オプション価格

ヨーロピアン・コールオプションの満期 $T$ でのペイオフは

$$
(S_T-K)^+
$$

ここで $K$ は権利行使価格。

Black-Scholes理論では、無裁定の考え方から価格関数 $V(t,S)$ が満たす方程式を導く。

$$
\partial_t V+\frac{1}{2}\sigma^2S^2\partial_{SS}V
+rS\partial_SV-rV=0
$$

終端条件:

$$
V(T,S)=(S-K)^+
$$

---
layout: two-cols-header
---

# Black-Scholesの見方

Black-Scholes方程式は、オプション価格を決めるPDE。

::left::

## 確率論側

リスク中立測度の下で

$$
V(t,S)=e^{-r(T-t)}E[(S_T-K)^+\mid S_t=S]
$$

という条件付き期待値で価格を表す。

::right::

## 解析側

同じ価格関数 $V(t,S)$ は

$$
\partial_t V+\frac12\sigma^2S^2\partial_{SS}V
+rS\partial_SV-rV=0
$$

を満たす。

確率過程とPDEが接続する。

---

# 何が確率論とつながるか

Black-Scholesは、次の概念が一気につながる例。

- Brown運動
- 確率微分方程式
- 伊藤の公式
- Markov性
- 偏微分方程式
- 条件付き期待値
- Martingale
- リスク中立測度

::note
この勉強会では厳密な金融数学の完成より、「確率過程が解析と応用へ接続する」ことを見せる位置づけにする。
::

---
layout: two-cols-header
---

# 金融工学とMartingale

リスク中立測度 $Q$ の下では、割引後の価格過程がMartingaleになる。

$$
E^Q[e^{-rt}S_t\mid\mathcal{F}_s]=e^{-rs}S_s
\quad(s\le t)
$$

::left::

## 価格づけの見方

将来ペイオフを割り引いた期待値が現在価格になる。

$$
V_t=E^Q[e^{-r(T-t)}H\mid\mathcal{F}_t]
$$

::right::

## ここで効く概念

- 条件付き期待値
- filtration
- Martingale
- 伊藤の公式
- 無裁定

---

# 最適戦略

確率論では、ランダムな状況のもとで最適な意思決定を考える。

典型例:

- サイコロを振り直すか止めるか
- 秘書問題
- 停止時刻
- 動的計画法

::note
「事前に全部見られない」「途中で止める必要がある」という状況では、情報の増え方が本質になる。
::

---

# 最適停止とMartingale

ある時刻で止めるルールを停止時刻という。

$$
\tau
$$

は「時刻 $\tau$ までの情報だけで、止めたかどうかを判定できる」時刻。

Martingale $(M_t)$ に対しては、条件を満たす停止時刻 $\tau$ で

$$
E[M_\tau]=E[M_0]
$$

となる。これを任意停止定理という。

公平なゲームでは、止め方だけを工夫しても期待値は増やせない、という主張。

---
layout: two-cols-header
---

# 戦略の例

::left::

## サイコロの停止問題

最大 $n$ 回まで振れる。各回で止めるか続けるかを決める。

$$
V_k=E[\max(D,V_{k-1})]
$$

動的計画法で「今止める価値」と「続ける価値」を比べる。

::right::

## 秘書問題

$n$ 人を順番に見て、その場で採用するか見送る。

古典的には

$$
\text{最初の約 }n/e\text{ 人を見送り、その後の暫定1位を採用}
$$

::note
最適戦略は細かく解くより、情報が増える中で止める時刻を選ぶ問題として紹介する。
::

---
layout: section
---

# 6. まとめ

---

# 全体像

::flow
- 測度論
- 確率空間
- 確率変数
- 分布
- 収束
- 確率過程
- 条件付き期待値
- Martingale
- 応用
::

今日の主眼は、個々の定理を証明し切ることではなく、測度論の言葉が確率論のどこで効くかを見えるようにすること。

---

# 次に深掘りするなら

候補は3方向。

1. 収束定理を丁寧にやる  
   Borel-Cantelli、強法則、特性関数、中心極限定理

2. 確率過程へ進む  
   filtrations、条件付き期待値、Martingale、停止時刻、Brown運動

3. 応用へ進む  
   伊藤の公式、Black-Scholes、最適停止、秘書問題

::note
参加者の関心が物理・生物寄りなら、拡散過程やBrown運動を厚めにするのも自然。
::

---

# 参考文献

- 熊谷隆『確率論』
- 舟木直久『確率微分方程式』
- 既存メモ: `work/kakuritsubibun01.tex`

::note
本資料は勉強会用の導入資料として構成した。厳密な証明は必要に応じて補助ノートに分ける。
::

---
layout: end
---

# おしまい

議論したいところ:

- 一回完結にするか、複数回シリーズにするか
- Black-Scholesをどこまで厚くするか
- Martingaleと最適停止をどこまで掘るか
