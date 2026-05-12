# Code References

- `src/auth/token.py` — JWT issue and verification logic, TTL constant defined here
- `src/middleware/auth.py` — middleware that validates tokens on every request
- `src/routes/auth.py` — `/auth/refresh` endpoint implementation
