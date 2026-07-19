"""Quick check of today's tasks."""
import httpx

r = httpx.post('http://localhost:8000/auth/login', json={'email': 'neharsha@planner.local', 'password': 'planner123'})
token = r.json()['access_token']
h = {'Authorization': f'Bearer {token}'}

r = httpx.get('http://localhost:8000/tasks?view=today', headers=h)
tasks = r.json()
print(f"TODAY ({len(tasks)} tasks):")
for t in tasks:
    print(f"  [{t['priority']}] {t['title']}  ({t['estimated_minutes']}min)")

r = httpx.get('http://localhost:8000/tasks?view=backlog', headers=h)
print(f"\nBACKLOG: {len(r.json())} tasks (future scheduled)")
