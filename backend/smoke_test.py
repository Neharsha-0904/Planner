"""Quick smoke test — run with: python smoke_test.py"""
import httpx

BASE = "http://localhost:8000"

# Health
r = httpx.get(f"{BASE}/health")
print("Health:", r.json())

# Login
r = httpx.post(f"{BASE}/auth/login", json={"email": "neharsha@planner.local", "password": "planner123"})
token = r.json()["access_token"]
headers = {"Authorization": f"Bearer {token}"}
print("Login: OK")

# Today's tasks
r = httpx.get(f"{BASE}/tasks?view=today", headers=headers)
print(f"\nToday response: {r.status_code}")
if r.status_code != 200:
    print("  Error:", r.text[:500])
else:
    tasks = r.json()
    print(f"  {len(tasks)} task(s)")
    for t in tasks:
        print(f"  [{t['priority']}] {t['title']}  (rolled over {t['rolled_over_count']}x)")

# Backlog
r = httpx.get(f"{BASE}/tasks?view=backlog", headers=headers)
print(f"\nBacklog response: {r.status_code}")
if r.status_code != 200:
    print("  Error:", r.text[:500])
else:
    tasks = r.json()
    print(f"  {len(tasks)} task(s)")
    for t in tasks:
        print(f"  [{t['priority']}] {t['title']}")

# Done
r = httpx.get(f"{BASE}/tasks?view=done", headers=headers)
print(f"\nDone: {len(r.json())} task(s)")
