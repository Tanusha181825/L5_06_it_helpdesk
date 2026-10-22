# Static Code Analysis — Issues Identified

**Initial Pylint Score:** 5.53/10

**Initial Bandit Findings:** 1 High, 3 Low

**Initial Flake8 Findings:** 15 violations

| Issue | Type | Line(s) | Description | Fix Approach |
|---|---|---|---|---|
| Command injection (B602) | Security - High | 38 | `shell=True` executes a command constructed using untrusted hostname input. | Use a subprocess argument list without a shell. |
| Hardcoded password (B105) | Security - Low | 8, 54 | Admin password is stored directly in source code. | Read the password securely from an environment variable. |
| Mutable default argument (W0102) | Bug | 10 | `audit_trail=[]` is shared between function calls. | Use `None` and initialize a new list inside the function. |
| Bare exception (W0702, E722, B110) | Error handling | 21–24 | `except: pass` silently ignores errors. | Check ticket existence and handle invalid IDs explicitly. |
| Invalid urgency | Logical bug | 13, 49 | Negative or out-of-range urgency values are accepted. | Validate that urgency is an integer between 1 and 5. |
| Unsafe file handling (R1732, W1514) | Code quality | 41–43 | File is opened without a context manager or explicit encoding. | Use `with open(..., encoding="utf-8")`. |
| Incorrect naming (C0103) | Style | 7, 30 | Variable and function names do not follow recommended conventions. | Use appropriate constant naming and snake_case functions. |
| Incorrect None comparison (C0121, E711) | Style | 33 | Uses `== None` instead of `is None`. | Replace with `is None`. |
| Missing docstrings (C0114, C0116) | Documentation | 1, 10–45 | Module and functions lack documentation. | Add concise module and function docstrings. |
| Formatting violations (E302, E305, E501) | Style | Multiple | Missing blank lines and excessive line lengths. | Format code according to PEP 8. |
| Unused variable (W0612, F841) | Code quality | 47 | `t2` is assigned but never used. | Remove the unnecessary assignment. |
| Subprocess import warning (B404) | Security - Low | 2 | Bandit warns that subprocess usage can be dangerous. | Replace unsafe subprocess usage with a safer implementation and verify the warning is resolved. |
