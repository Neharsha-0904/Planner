# Design System

## Principle
Surfaces stay dark and neutral; color is reserved for meaning. Priority uses a heat scale (red → amber → fades to gray, not blue). Status uses one distinct violet accent that never overlaps with priority, so "urgent" and "interactive" never compete for the same color. Aging escalates via a badge + dot color, not by repainting the whole card.

## Surfaces
| Token | Hex | Use |
|---|---|---|
| `bg-app` | `#0F1117` | page background |
| `bg-sidebar` | `#161B27` | sidebar panel |
| `bg-card` | `#1A2130` | task cards |
| `bg-card-muted` | `#151A26` | done/archived cards |
| `border` | `#2A3346` | card/panel borders |

## Text
| Token | Hex | Use |
|---|---|---|
| `text-primary` | `#E7EAF0` | titles, active text |
| `text-secondary` | `#9AA3B2` | tags, metadata |
| `text-muted` | `#6B7486` | done-task text, disabled nav |

## Accent (brand — never used for priority)
| Token | Hex | Use |
|---|---|---|
| `accent` | `#7C6BF0` | active nav item, primary buttons, "in progress" pill |
| `accent-hover` | `#8E7FF3` | hover state |

## Priority (heat scale — quiet at the bottom)
| Token | Hex | Use |
|---|---|---|
| `priority-p0` | `#EF4E52` | urgent — dot, badge, border accents |
| `priority-p1` | `#F5A524` | medium |
| `priority-p2` | `#6B7486` | low — same as muted gray, deliberately quiet |

## Status
| Token | Hex | Use |
|---|---|---|
| `status-in-progress` | `#7C6BF0` | same as accent |
| `status-done` | `#34D399` | check icon, done pill |
| `status-backlog` | `#6B7486` | same as muted gray |

## Aging (backlog escalation)
- `rolled_over_count` 1–2: no visual change beyond normal card.
- `rolled_over_count` 3+: dot switches to `priority-p0` red (`#EF4E52`) regardless of actual priority, plus a small badge "rolled over N×" in a red-tinted pill (`bg: rgba(239,78,82,0.16)`, `text: #F2888A`).
- Never darken/tint the whole card background for aging — keep that signal to the dot + badge only, so the card grid stays calm and scannable.

## Pill background formula (used for P0/P1/status pills)
Take the solid hex, render the pill background at ~16% opacity of that color, and use a lighter tint of the same hue for the pill text (not the solid hex) so it's legible on the tinted background — e.g. P0 pill: bg `rgba(239,78,82,0.16)`, text `#F2888A`.

## Light mode (when you get to it)
Flip only the surface/text tokens; keep accent, priority, and status hues identical:
- `bg-app` → `#F7F8FA`, `bg-sidebar` → `#FFFFFF`, `bg-card` → `#FFFFFF`, `border` → `#E2E5EA`
- `text-primary` → `#1A2130`, `text-secondary` → `#5A6273`, `text-muted` → `#9AA3B2`
