# Random DNA Read Reconstruction Report

## Problem

We generate a random DNA reference sequence using `A`, `T`, `C`, and `G`.
Short reads of length 30 to 45 are sampled from the reference, then mismatch
noise is added. The goal is to compare reconstruction algorithms by accuracy
and runtime.

## Algorithms

1. Trivial reference matching
2. Position table index matching
3. K-mer hash index matching
4. BWT/FM-index seed matching
5. Greedy overlap assembly
6. De Bruijn graph assembly

## Experiments

Main variables:

- Coverage: `1x`, `2x`, `5x`, `10x`, `20x`
- Noise rate: `0%`, `1%`, `3%`, `5%`
- Reference length: `1,000`, `5,000`, `10,000`, `50,000`

Main metrics:

- Accuracy
- Runtime
- Reconstructed sequence length
- Mismatch count
