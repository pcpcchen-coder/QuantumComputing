# Q001 來源筆記（逐字引文）

查核日：2026-11-07。arXiv 三頁由研究子代理開啟並回報逐字引文；Aaronson 兩篇 PDF 由製作代理下載後用 `pdftotext` 讀原文。

## Aaronson, "The Limits of Quantum Computers", Scientific American, March 2008

取得：https://www.scottaaronson.com/papers/limitsam.pdf 回 404；改用 https://www.cs.virginia.edu/~robins/The_Limits_of_Quantum_Computers.pdf（雜誌版 PDF，頁面標示 © 2008 Scientific American）。

- 「Quantum computers would be exceptionally fast at a few specific tasks, but it appears that for most problems they would outclass today's computers only modestly.」
- 「When the particles are measured (as is necessary to read out their final state), the rules of quantum mechanics dictate that the measurement will pick out just one of the 10^300 possibilities at random」
- 「…seem to be no better off than if we used a classical computer and tried out one randomly chosen」（可能解）
- 「So a good quantum computer algorithm would ensure that computational paths leading to a wrong answer would cancel out in this way.」「…which yields constructive interference and thereby boosts the probability of finding them when the particles are measured at the end.」
- 「…would, like Shor's algorithm, have to exploit the problems' structure」

## Aaronson, "Read the fine print", Nature Physics 11 (2015)

取得：https://www.scottaaronson.com/papers/qml.pdf（作者版，標題 Quantum Machine Learning Algorithms: Read the Fine Print）。

- 「(1) The vector b … somehow needs to be loaded quickly into the quantum computer's memory」
- 「…one faces the problem of how to load a large amount of classical data into a quantum computer (or else compute the data "on-the-fly"), in a way that is efficient enough to preserve the quantum speedup.」

## Shor, arXiv:quant-ph/9508027（1995／1996；SIAM J. Comput. 1997）

- 「Efficient randomized algorithms are given for these two problems on a hypothetical quantum computer.」
- 「These algorithms take a number of steps polynomial in the input size」
- 「two problems which are generally thought to be hard on a classical computer」

## Grover, arXiv:quant-ph/9605043（STOC 1996）

- 「any classical algorithm (whether deterministic or probabilistic) will need to look at a minimum of N/2 names」（以 50% 機率找到為條件）
- 「the desired phone number can be obtained in only O(sqrt(N)) steps」

## Preskill, "Quantum computing 40 years later", arXiv:2106.10522

- 「In May 1981, Feynman spoke at a conference on the topic "Simulating physics with computers."」
- 「There he proposed the idea of using quantum computers to simulate quantum systems that are too hard to simulate」
