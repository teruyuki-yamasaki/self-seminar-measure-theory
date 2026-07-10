# 予備概念

## 空間とその部分集合

- **抽象空間**: 点の集まりとしてだけ考えた空間
- (**部分**) **集合**: 空間$X$の中の点の集まり
- **空集合**: 点を一つも含まない集合 $\emptyset$
- 点$x$が集合$A$に属することを$x\in A$と書く
- 点$x$が集合$A$に属さないことを$x\notin A$と書く
- 集合$A$と$B$の関係
    - $A\subset B$ : $A$は$B$の**部分集合**である
    - $A\subsetneq B$ : $A$は$B$の**真部分集合**である
    - $A=B$ : $A$と$B$は同じ集合である
    - $A\cap B=\emptyset$ : $A$と$B$は**互いに素**である
- **集合族**: 集合の集まり (family)
    - $\mathfrak{F}=\{A \mid A\subset X\}$

---

### 演算
$A, B, C, \cdots \subset X$ 
- **和集合**
    - $A\cup B=\{x\mid x\in A \text{ または } x\in B\}$
- **積集合**
    - $A\cap B=\{x\mid x\in A \text{ かつ } x\in B\}$
- **直和**
    - $A\sqcup B=\{x\mid x\in A \text{ または } x\in B, A\cap B=\emptyset\}$
    - $A + B = A \sqcup B$
- **差集合**
    - $A\setminus B=\{x\mid x\in A \text{ かつ } x\notin B\}$
    - $A - B = A - A \cap B = A \setminus B$
- **補集合/余集合**
    - $A^c=X\setminus A=\{x\mid x\notin A\}$

---

### 法則
- **交換律**: 
    - $A\cup B=B\cup A$
    - $A\cap B=B\cap A$
- **結合律**:
    - $(A\cup B)\cup C=A\cup(B\cup C)$
    - $(A\cap B)\cap C=A\cap(B\cap C)$
- **分配律**:
    - $A\cap(B\cup C)=(A\cap B)\cup(A\cap C)$
    - $A\cup(B\cap C)=(A\cup B)\cap(A\cup C)$
- **de Morganの法則**:
    - $(A\cup B)^c=A^c\cap B^c$

---

### 集合列
集合列 $A_1, A_2, A_3, \ldots$ (有限または無限) に対して
- 和集合:
    $$
    \bigcup_{n=1}^{N}A_n
    = A_1\cup A_2\cup A_3\cup\cdots A_N
    $$
    $$
    \bigcup_{n=1}^{\infty}A_n
    = A_1\cup A_2\cup A_3\cup\cdots
    $$

- 直和:
    $$
    \bigsqcup_{n=1}^{N}A_n
    = A_1\sqcup A_2\sqcup A_3\sqcup\cdots A_N
    $$
    $$
    \bigsqcup_{n=1}^{\infty}A_n
    = A_1\sqcup A_2\sqcup A_3\sqcup\cdots
    $$
    $$
    \sum_{n=1}^{N}A_n
    = A_1 + A_2 + A_3 + \cdots + A
    $$
    $$
    \sum_{n=1}^{\infty}A_n
    = A_1 + A_2 + A_3 + \cdots
    $$

- 積集合:
    $$
    \bigcap_{n=1}^{N}A_n
    = A_1\cap A_2\cap A_3\cap\cdots A_N
    $$
    $$
    \bigcap_{n=1}^{\infty}A_n
    = A_1\cap A_2\cap A_3\cap\cdots
    $$

- de Morganの法則:
    $$
    \left(\bigcup_{n=1}^{N}A_n\right)^c
    = \bigcap_{n=1}^{N}A_n^c
    $$
    $$
    \left(\bigcup_{n=1}^{\infty}A_n\right)^c
    = \bigcap_{n=1}^{\infty}A_n^c
    $$

- **上極限集合**
    $$
    \overline{\lim}A_n
    = \overline{\lim}_{n\to\infty}A_n
    = \limsup_{n\to\infty}A_n
    = \bigcap_{n=1}^{\infty}\bigcup_{k=n}^{\infty}A_k
    $$

- **下極限集合**
    $$
    \underline{\lim}A_n
    = \underline{\lim}_{n\to\infty}A_n
    = \liminf_{n\to\infty}A_n
    = \bigcup_{n=1}^{\infty}\bigcap_{k=n}^{\infty}A_k
    $$

- 明らかに
　　$$\underline{\lim}A_n \subset \overline{\lim}A_n$$

- **極限集合**
    - $\underline{\lim}A_n = \overline{\lim}A_n$のとき, その共通集合を極限集合と呼び, 以下のように書く
    $$
    \lim A_n \text{または} \lim_{n\to\infty}A_n
    $$
    - 極限集合が存在するとき, 集合列は**収束する**という

- 実数列の上極限・下極限との対応:
    実数列 $\{a_n\}$ に対して, 以下の$\inf, \sup$をそれぞれ
    $$
    \overline{\lim}a_n = \inf_{n \in \mathbb{N}} \sup_{k \ge n} a_k
    $$
    $$
    \underline{\lim}a_n = \sup_{n \in \mathbb{N}} \inf_{k \ge n} a_k
    $$

---

### 直積

- **直積空間**
    - 2つの空間$X, Y$が与えられたとき, $X$の点$x$と$Y$の点$y$の対$z = (x, y)$からなる空間$Z$を１つの空間と考えてこれを$X$と$Y$の直積空間と呼び, 
    $$
    Z = X \times Y = \{(x, y)\mid x\in X, y\in Y\}
    $$
    と書く. 直積空間の点$z=(x, y)$に対して, $x$を$z$の$X$成分, $y$を$z$の$Y$成分と呼ぶ.
    
- **直積集合**
    - 2つの集合$A\subset X, B\subset Y$が与えられたとき, $A$の点$x$と$B$の点$y$の対$(x, y)$からなる集合を１つの集合と考えてこれを$A$と$B$の直積集合と呼び, 
    $$
    A \times B = \{(x, y)\mid x\in A, y\in B\}
    $$
    と書く. 直積集合は直積空間の部分集合である.

---

### 有限集合・無限集合・可算集合

- **有限集合**: 点の個数が有限である集合（空集合も0個の点からなると考えてこれに含める）
- **無限集合**: 点の個数が有限でない集合
- **可算無限集合**: 無限集合のうち, 自然数を割り当てることで全ての点を並べ尽くすことができる集合
- **可算集合**: 有限集合または可算無限集合のこと

---

### 集合の定義函数

$A$を空間$X$の部分集合とする. このとき, $X$上で函数 $$\mathbf{1}_A(x) = \begin{cases} 1 & (x\in A) \\ 0 & (x\notin A) \end{cases}$$ を定義する. この函数を$A$の**定義函数**と呼ぶ. 

このとき
$$
\mathbf{1}_{A^c}(x) = 1 - \mathbf{1}_A(x)
$$
$$
\mathbf{1}_{A\cap B}(x) = \mathbf{1}_A(x)\mathbf{1}_B(x)
$$
$$
\mathbf{1}_{A\cup B}(x) = \mathbf{1}_A(x) + \mathbf{1}_B(x) - \mathbf{1}_{A\cap B}(x)
$$
$$
\mathbf{1}_{\overline{\lim}A_n}(x) = \overline{\lim}\mathbf{1}_{A_n}(x)
$$
$$
\mathbf{1}_{\underline{\lim}A_n}(x) = \underline{\lim}\mathbf{1}_{A_n}(x)
$$

---

## 点函数と集合函数

空間$X$と集合族$\mathfrak{F}$と集合$F$が与えられたとき, 次の二種類の函数を考える:

1) **点函数**: 集合$F$の各点$x\in F$に対して実数を割り当てる函数 
$$
f:F\to\mathbb{R}; x \mapsto f(x)
$$
を$F$で定義された点函数と呼ぶ.

2) **集合函数**: 集合$F$の部分集合であって集合族$\mathfrak{F}$に属する各集合$E\in\mathfrak{F} \; s.t. \; E \subset F$に対して実数を割り当てる函数
$$
\Phi:\mathfrak{F}\to\mathbb{R}; E \mapsto \Phi(E)
$$
を ($\mathfrak{F}$-) 集合函数と呼ぶ.

---

## Euclid空間の場合

- **(1次元) 区間**
    $-\infty \leq a < b \leq \infty$とし, 空集合$\emptyset$も区間の１つと考える.
    - **閉区間**: $[a, b] = \{x\in\mathbb{R}\mid a\le x\le b\}$
    - **開区間**: $(a, b) = \{x\in\mathbb{R}\mid a< x< b\}$
    - **半開区間**: $(a, b] = \{x\in\mathbb{R}\mid a< x\le b\}, [a, b) = \{x\in\mathbb{R}\mid a\le x< b\}$

- **N次元区間**: 
    - $\mathbb{R}^N$において, $-\infty \leq a_k < b_k \leq \infty$なる$a_k, b_k \; (k=1, 2, \ldots, N)$に対して
    $$
    [a_1, b_1)\times[a_2, b_2)\times\cdots\times[a_N, b_N) = \{(x_1, x_2, \ldots, x_N)\in\mathbb{R}^N\mid a_k\le x_k< b_k, k=1, 2, \ldots, N\}
    $$

- **区間塊**
    - N次元区間の有限個の直和として表される集合をN次元**区間塊**と呼ぶ. 
    - $\mathfrak{I}_N$ : $\mathbb{R}^N$における区間の全体
    - $\mathfrak{F}_N$ : $\mathbb{R}^N$における区間塊の全体

- 例
    - $f(x) := (x_1, \cdots, x_N)$を$\mathbb{R}^N$上の連続な点函数で
    $$
    \int_{\mathbb{R}^N} |f(x)| dx < \infty
    $$
    であるとする. 
    - このとき
    $$
    \Phi(E) := \int_E f(x) dx \quad (E \in \mathfrak{F}_N)
    $$
    は $\mathfrak{F}_N$-集合函数である. 
    - ただし $\Phi(\emptyset) := 0$.

- 例
    - $f_1, f_2, \ldots, f_N$を$\mathbb{R}^N$上の単調増加な点函数とする.
    - このとき, 
        - 有界な区間 $I = [a_1, b_1)\times[a_2, b_2)\times\cdots\times[a_N, b_N) \in \mathfrak{I}_N$ に対して
        $$
        \Psi(I) := \prod_{k=1}^N (f_k(b_k) - f_k(a_k))
        $$
        - 有界でない区間$I$に対しては
        $$
        \Psi(I) := \sup\{\Psi(J) \mid J \subset I, J \in \mathfrak{I}_N, J \text{は有界}\}
        $$
        - 空集合に対しては
        $$
        \Psi(\emptyset) := 0
        $$
        と定めると, $\Psi$は$\mathfrak{I}_N$-集合函数である. 
    - 特に, $f_k(x) = x$のとき, $\Psi(I)$は区間$I$の普通の意味での体積を与える.