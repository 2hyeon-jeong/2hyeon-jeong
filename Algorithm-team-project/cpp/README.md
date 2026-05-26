# C++ Algorithm Interface

Place final team algorithms in `cpp/algorithms/`.

Each `.cpp` file is compiled by:

```powershell
.\.venv\Scripts\python.exe scripts\build_cpp.py
```

The output executable is written to `build/algorithms/` and is automatically included in Python benchmark runs with the `cpp_` prefix.

## Required Protocol

Input from `stdin`:

```text
reference
read_count
read_1
read_2
...
```

Output to `stdout`:

```text
reconstructed_sequence
```

Only print the final reconstructed sequence during benchmark runs. Extra debug output will break CSV results.

