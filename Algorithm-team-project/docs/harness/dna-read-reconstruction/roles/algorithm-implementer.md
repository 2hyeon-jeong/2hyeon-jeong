# Algorithm Implementer Role

## Responsibility

Implement one assigned string-search algorithm and make it comparable with the shared benchmark.

Final implementations belong in `cpp/algorithms/` and should follow the project stdin/stdout protocol documented in `AGENTS.md`.

## Required Notes

For each algorithm, record:

- algorithm name
- preprocessing/index construction
- read or seed search method
- mismatch verification method
- complexity
- validation command
- known limitations

## Quality Bar

The algorithm should be deterministic on the same input and should run on synthetic `A/T/C/G` reads with mismatch noise.
