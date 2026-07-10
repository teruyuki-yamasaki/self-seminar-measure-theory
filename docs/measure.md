# 測度

## 有限加法的測度

### 有限加法族

与えられた空間$X$の部分集合の族$\mathfrak{F}$が次の条件を満たすとき, $\mathfrak{F}$を**有限加法族**と呼ぶ:
1. **空集合**：$\emptyset \in \mathfrak{F}$
2. **補集合**：$A \in \mathfrak{F}$ならば, $A^c \in \mathfrak{F}$
3. **和集合**：$A, B \in \mathfrak{F}$ならば, $A \cup B \in \mathfrak{F}$

この３つの性質より
- **全体集合**：$X \in \mathfrak{F}$
- **有限回演算**：$\mathfrak{F}$に属する集合の有限回の和・差・積の演算により得られる集合もまた$\mathfrak{F}$に属する

#### 例
- Euclid空間 $\mathbb{R}^N$において$\mathfrak{F}_N$は有限加法族である

---

### 有限加法的測度

空間$X$とその部分集合の有限加法族$\mathfrak{F}$があって, $\mathfrak{F}$-集合函数
$$
m: \mathfrak{F} \to \mathbb{R}
$$
が次の条件を満たすとき, $m$を($\mathfrak{F}$-)**有限加法的測度**と呼ぶ:
1. **非負性**：$ \forall A \in \mathfrak{F}, \; 0 \le m(A) \le \infty$. 特に, $m(\emptyset) = 0$.
2. **加法性**：$A, B \in \mathfrak{F}$かつ$A \cap B = \emptyset$ならば, $m(A \cup B) = m(A) + m(B)$.

上の２つの性質から, 次の性質が導かれる:
- **有限加法性**
    $A_1, A_2, \dots, A_n \in \mathfrak{F}$かつ$A_i \cap A_j = \emptyset$ ($i \neq j$)ならば,
    $$
    m\left(\sum_{i=1}^{n} A_i\right) = \sum_{i=1}^{n} m(A_i)
    $$

- **単調性**
    $A, B \in \mathfrak{F}$かつ$A \subset B$ならば, $m(A) \le m(B)$.
    特に, $m(A) < \infty$ならば, $m(B - A) = m(B) - m(A)$.

- **有限劣加法性**
    $A_1, \cdots, A_n \in \mathfrak{F}$ならば, $m\left(\bigcup_{i=1}^{n} A_i\right) \le \sum_{i=1}^{n} m(A_i)$.


#### 有限加法族上の完全加法性

有限加法族$\mathfrak{F}$上の有限加法的測度$m$が次の条件を満たすとき, 
$m$を(有限加法族$\mathfrak{F}$上の)**完全加法的測度**と呼ぶ:
- **完全加法性**：$A_1, A_2, \dots \in \mathfrak{F}$かつ$A_i \cap A_j = \emptyset$ ($i \neq j$)のとき
$\sum_{i=1}^{\infty} A_i \in \mathfrak{F}$ならば
$$
m\left(\sum_{i=1}^{\infty} A_i\right) = \sum_{i=1}^{\infty} m(A_i)
$$

#### 例
$f_1, \cdots, f_N$を$\mathbb{R}$で単調増加な実数値函数で定数ではないものとしたとき, 以下のように定義される函数$m: \mathfrak{F}_N \to \mathbb{R}$は有限加法族$\mathfrak{F}_N$上の完全加法的測度となる:
- 有界な区間
    $$
    I = [a_1, b_1) \times \cdots \times [a_N, b_N) \in \mathfrak{F}_N
    $$
    に対して
    $$
    m(A) = \prod_{k=1}^{N} \left(f_k(b_k) - f_k(a_k)\right)
    $$
- 有界でない区間$I$に対しては
    $$
    m(I) = \sup\{m(J) \mid J \subset I, J \in \mathfrak{F}_N, J\text{は有界}\}
    $$
- 空集合$\emptyset$に対しては
    $$
    m(\emptyset) = 0
    $$
- 区間塊$E = I_1 + \cdots + I_n \; (I_k \in \mathfrak{F}_N)$に対しては
    $$
    m(E) = \sum_{k=1}^{n} m(I_k)
    $$
と, $m$は有限加法族$\mathfrak{F}$上の完全加法的測度となる.

- 上記のように定義された測度$m$が有限加法族$\mathfrak{F}_N$上の完全加法的測度であるための必要十分条件は, 各函数$f_k$が右連続であることである.
- 特に, $f_k(x) = x$としたとき, $m$は$\mathfrak{F}_N$上の完全加法的測度となる.

---

## 外測度

空間$X$の全ての部分集合$A$に対して定義された集合函数$\Gamma(A)$があって, 
$\Gamma$が次の条件を満たすとき, $\Gamma$を(Carathéodory)**外測度**と呼ぶ:
1. **非負性**：$ \forall A \subset X, \; 0 \le \Gamma(A) \le \infty$. 特に, $\Gamma(\emptyset) = 0$.
2. **単調性**：$A, B \subset X$かつ$A \subset B$ならば, $\Gamma(A) \le \Gamma(B)$.
3. **可算劣加法性**：$A_1, A_2, \dots \subset X$ならば, 
$$
\Gamma\left(\bigcup_{i=1}^{\infty} A_i\right) \le \sum_{i=1}^{\infty} \Gamma(A_i)
$$

このような性質を持つ集合函数$\Gamma$の例は, 次に述べる定理によって
上記例の有限加法的測度から構成することができる.

$\mathfrak{F}$を$X$の部分集合の有限加法族として, $m$を$\mathfrak{F}$上の有限加法的測度とすると, 
- (i) 外測度$\Gamma$を次のように定義できる:
    $$
    \Gamma(A) = \inf\left\{\sum_{i=1}^{\infty} m(E_i) \;\middle|\; A \subset \bigcup_{i=1}^{\infty} E_i, \; E_i \in \mathfrak{F}\right\}, \quad \forall A \subset X.
    $$
- (ii) 特に, $m$が$\mathfrak{F}$上の完全加法的測度であるならば, $E \in \mathfrak{F}$に対して$\Gamma(E) = m(E)$となる.
    - 注: 一般には $\Gamma(E) \le m(E)$ である.

### Lebesgue外測度

$\mathbb{R}^N$において$f_k(x) = x \;(k = 1, \dots, N)$としたとき, 
上記の構成によって得られる外測度を$\mu^*(A)$と書き**Lebesgue外測度**という.
$I = [a_1, b_1) \times \cdots \times [a_N, b_N) \in \mathfrak{F}_N$としたとき, Lebesgue外測度は
$$
\mu^*(I) = \prod_{k=1}^{N} (b_k - a_k)
$$
となる.


---

## 可測性

上の定理の(ii)を満たす$\Gamma$について次の要請を考察する:
(1) 可測な集合の全体が有限加法族をなし, $\Gamma$はその上の有限加法的測度となる.
(2) $A = A_1 + A_2 + \cdots $で各$A_n$が可測ならば$A$も可測である.
(2') (1), (2)より, $A = A_1 \cup A_2 \cup \cdots$で各$A_n$が可測ならば$A$も可測である.
$\because$ $B_1 = A_1, B_n = A_n - \sum_{k=1}^{n-1} A_k$とおくと, $B_n$は可測であり, (2)より$A = \sum_{n=1}^{\infty} B_n$は可測となる.
(3) (ii)を満たす外測度$\Gamma$については$\mathfrak{F}$の全ての集合が可測である.

これらの条件が満たされているとすると, 集合$E$が可測ならば次が成り立つ：
(*) $\forall A \subset X$に対して$\Gamma(A) = \Gamma(A \cap E) + \Gamma(A \cap E^c)$.

$\forall \epsilon > 0, \exists E_1, E_2, \dots \in \mathfrak{F} \text{ such that } A \subset \bigcup_{i=1}^{\infty} E_i \text{ and } \sum_{i=1}^{\infty} m(E_i) \le \Gamma(A) + \epsilon.$
$H = \bigcup_{i=1}^{\infty} E_i$とおくと, 上記の条件(1), (2'), (3)を満たすとき, $H, H \cap A, H \cap A^c$も可測であって
$$
\Gamma(A) + \epsilon \ge \sum_{i=1}^{\infty} \Gamma(E_i) = \Gamma(H) = \Gamma(H \cap E) + \Gamma(H \cap E^c) \ge \Gamma(A \cap E) + \Gamma(A \cap E^c) \ge \Gamma(A).
$$

### Carathéodoryの可測性
空間$X$に外測度$\Gamma$が定義されているとする. 集合$E \subset X$が次の条件を満たすとき, 
$E$を**Carathéodory可測**または$\Gamma$-**可測**であるという:
$$
\forall A \subset X, \quad \Gamma(A) = \Gamma(A \cap E) + \Gamma(A \cap E^c)
$$

$\Gamma$-可測集合の全体を$\mathfrak{M}_\Gamma$と書く.
- $E \in \mathfrak{M}_\Gamma$ならば, $E^c \in \mathfrak{M}_\Gamma$.
- $\Gamma(E) = 0$ならば, $E \in \mathfrak{M}_\Gamma$. 従って特に $\emptyset \in \mathfrak{M}_\Gamma$.
    - $\because \forall A \subset X, \; \Gamma(A \cap E) \le \Gamma(E) = 0$.
    $$
    \Gamma(A) \ge \Gamma(A \cap E^c) = \Gamma(A \cap E) + \Gamma(A \cap E^c)
    $$

### 零集合
$\Gamma(E) = 0$なる集合$E$を ($\Gamma$に関する) **零集合**という. 
- 空集合$\emptyset$は零集合であるが逆は成り立たない.
- 零集合の全体を$\mathfrak{N}_\Gamma$と書く. 


### 性質

- $\mathfrak{F} \subset \mathfrak{M}_\Gamma$: 有限加法族$\mathfrak{F}$の全ての集合は$\Gamma$-可測である.
- $E_k \in \mathfrak{M}_\Gamma (k=1, 2, \cdots), E_i \cap E_j = \emptyset \; (i \ne j)$ならば, 
  $\bigcup_{k=1}^{\infty} E_k \in \mathfrak{M}_\Gamma$, かつ
  $$
  \Gamma\left(\bigcup_{k=1}^{\infty} E_k\right) = \sum_{k=1}^{\infty} \Gamma(E_k).
  $$
- $E, F \in \mathfrak{M}_\Gamma$ならば, $E \cap F, E - F \in \mathfrak{M}_\Gamma$.
$E_k \in \mathfrak{M}_\Gamma (k=1, 2, \cdots, n)$ならば, 
  $$
  \bigcup_{k=1}^{n} E_k, \bigcap_{k=1}^{n} E_k \in \mathfrak{M}_\Gamma.
  $$
- $E_n \in \mathfrak{M}_\Gamma (n=1, 2, \cdots)$ならば,
  $$
  \bigcup_{n=1}^{\infty} E_n \in \mathfrak{M}_\Gamma.
  $$

---

## 測度


### 可算加法族

空間$X$の部分集合の族$\mathfrak{B}$があって, 次の3つの条件を満たすとき, 
集合族$\mathfrak{B}$を**完全加法族**, **可算加法族**, **σ加法族**, または単に**加法族**という:
(1) **空集合**: $\emptyset \in \mathfrak{B}$.
(2) **補集合**: $A \in \mathfrak{B}$ならば, $A^c \in \mathfrak{B}$.
(3) **可算和**: $A_1, A_2, \dots \in \mathfrak{B}$ならば, $\bigcup_{n=1}^{\infty} A_n \in \mathfrak{B}$.

#### 性質
- **全体集合**: $X \in \mathfrak{B}$.
- **可算回演算**: $\mathfrak{B}$に属する集合の可算回の和・差・積の演算により得られる集合もまた$\mathfrak{B}$に属する.
- **有限加法族**: 可算加法族$\mathfrak{B}$は有限加法族である.

### 測度

空間$X$とその部分集合の可算加法族$\mathfrak{B}$があって, $\mathfrak{B}$-集合函数
$$
\mu: \mathfrak{B} \to \mathbb{R}
$$
が次の条件を満たすとき, 集合函数$\mu$を可算加法族$\mathfrak{B}$で定義された**測度**という:
(1) **非負性**: $ \forall A \in \mathfrak{B}, \; 0 \le \mu(A) \le \infty$. 特に, $\mu(\emptyset) = 0$.
(2) **可算加法性**: $A_1, A_2, \dots \in \mathfrak{B}$かつ$A_i \cap A_j = \emptyset$ ($i \neq j$)ならば,
$$
\mu\left(\bigcup_{n=1}^{\infty} A_n\right) = \sum_{n=1}^{\infty} \mu(A_n).
$$

#### 性質
- **有限加法性**: 完全加法性から得られることは明らかである.
- **単調性**: 
    $A, B \in \mathfrak{B}$かつ$A \subset B$ならば, $\mu(A) \le \mu(B)$. 
    特に, $\mu(A) < \infty$ならば, $\mu(B - A) = \mu(B) - \mu(A)$.
- **劣加法性**: 
    $A_1, A_2, \dots \in \mathfrak{B}$ならば, $\mu\left(\bigcup_{n=1}^{\infty} A_n\right) \le \sum_{n=1}^{\infty} \mu(A_n)$.

- $A_n \in \mathfrak{B} (n=1, 2, \cdots)$とする. 集合列 $\{A_n\}$が (i)単調増加, (ii)単調減少のいずれかであり, $\mu(A_1) < \infty$のとき, 次が成り立つ:
$$
\mu\left(\lim_{n \to \infty} A_n\right) = \lim_{n \to \infty} \mu(A_n).
$$
(iii) 一般には
- $\mu\left(\underline{\lim}_{n \to \infty} A_n\right) \le \underline{\lim}_{n \to \infty} \mu(A_n)$
- $\mu\left(\bigcup_{n=1}^\infty A_n\right) < \infty$ ならば$\mu(\overline{\lim}_{n \to \infty} A_n) \ge \overline{\lim}_{n \to \infty} \mu(A_n)$
- $\mu\left( \bigcup_{n=1}^\infty A_n \right) < \infty$で$\lim_{n \to \infty}  A_n$が存在するならば$\mu\left(\lim_{n \to \infty}  A_n\right) = \lim_{n \to \infty} \mu(A_n)$


### 測度空間

空間$X$とその部分集合の可算加法族$\mathfrak{B}$と測度$\mu$の組を**測度空間**といい,
$(X, \mathfrak{B}, \mu)$または$X(\mathfrak{B}, \mu)$と書く.

- $\Gamma$を空間$X$で定義された外測度とすると, 
    $\Gamma$-可測集合の全体$\mathfrak{M}_\Gamma$は可算加法族であり, 
    $\Gamma$は$\mathfrak{M}_\Gamma$上で定義された測度となる.

- 特に, Euclid空間$\mathbb{R}^n$における外測度$\Gamma$がLebesgue外測度$\mu^*$であるとき, 
    $\mathfrak{M}_{\mu^*}$に属する集合を**Lebesgue可測集合**という.
    $\mu^*$は$\mathfrak{M}_{\mu^*}$上で定義された測度となり, これを**Lebesgue測度**といい, 単に$\mu$と書くことにする.
    - 区間や区間塊はLebesgue可測であり, その測度は普通の意味の(N次元)体積である.
        - 従って, Lebesgue測度は体積の一般化である.
    - 単調増加右連続函数$f_1, \cdots, f_N$に対して構成される測度$m$はLebesgue測度の一般化であり,
      これを**Lebesgue-Stieltjes測度**と呼ぶ.


### ほとんど至る所

集合$E\in\mathfrak{B}$の点$x \in E$に関係した命題$P(x)$があって, それが$\mu(E_0) = 0$なる集合$E_0 \subset E$上で成り立つ場合, その命題$P(x)$は集合$E$上で測度$\mu$に関して**ほとんど至る所** (almost everywhere)成り立つという.
または, **ほとんど全ての**(almost every)点$x\in E$に関して命題$P(x)$が成り立つという. これを
$$
\mu\text{-a.e. } x \in E, \quad P(x)
$$
のように書く. 

#### 例： Dirichlet函数
$X = E = \mathbb{R}$とし, $\mu$をLebesgue測度とする. Dirichlet函数
$$
D(x) = \begin{cases}
1, & x \in \mathbb{Q} \\
0, & x \in \mathbb{R} - \mathbb{Q}
\end{cases}
$$
は, $\mathbb{Q}$がLebesgue測度に関して零集合であるため, $D(x) = 0$がほとんど至る所成り立つ. すなわち, 
$$
D(x) = 0 \quad \mu\text{-a.e. } x \in \mathbb{R}
$$
