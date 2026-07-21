from seeds.private_roadmap_v2 import get_curriculum
c = get_curriculum()
print(f"Total days: {len(c)}")
print(f"Day 1: {c[0]['topic']}")
print(f"Day 15: {c[14]['topic']}")
print(f"Day 40: {c[39]['topic']}")
print(f"Day 85: {c[84]['topic']}")
print(f"Last day: Day {c[-1]['day']} - {c[-1]['topic']}")
