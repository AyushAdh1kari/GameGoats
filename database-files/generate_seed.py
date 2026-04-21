#!/usr/bin/env python3
"""
Generates realistic mock seed data for the GameGoats database.
Outputs SQL INSERT statements to 02_gamegoats_seed_data.sql.

Usage:  python3 generate_seed.py
"""

import hashlib, random
from datetime import datetime, timedelta
from pathlib import Path

from faker import Faker

fake = Faker()
Faker.seed(42)
random.seed(42)

OUT_PATH = Path(__file__).resolve().parent / "02_gamegoats_seed_data.sql"

REGIONS = ["NA-East", "NA-West", "EU-Central", "EU-West", "AP-South", "LATAM"]
PLATFORMS = ["PC", "PlayStation", "Xbox", "Nintendo", "Mobile"]
GENRES = ["Shooter", "RPG", "Strategy", "Simulation", "Sports", "Adventure",
          "Puzzle", "Platformer", "Racing", "Horror"]
LIFECYCLE = ["active", "maintenance", "sunset"]

TAG_NAMES = [
    "open-world", "co-op", "roguelike", "battle-royale", "pixel-art",
    "story-driven", "sandbox", "turn-based", "pvp", "crafting",
    "survival", "stealth", "base-building", "deckbuilder", "metroidvania",
    "souls-like", "mmorpg", "speedrun-friendly", "procedural", "moddable",
    "retro", "vr-compatible", "cross-platform", "early-access",
    "free-to-play", "esports", "local-multiplayer", "narrative",
    "hack-and-slash", "tower-defense", "city-builder", "dungeon-crawler",
    "bullet-hell", "idle", "rhythm",
]

TITLE_ADJ = [
    "Crimson", "Neon", "Shattered", "Solar", "Frozen", "Phantom",
    "Iron", "Mystic", "Void", "Ember", "Silent", "Dark", "Astral",
    "Hollow", "Infinite",
]
TITLE_NOUN = [
    "Frontier", "Dominion", "Odyssey", "Crusade", "Chronicle", "Legacy",
    "Uprising", "Vanguard", "Rift", "Bastion", "Throne", "Forge",
    "Eclipse", "Horizon", "Legends",
]

STUDIO_ADJ = [
    "Phantom", "Nebula", "Iron", "Pixel", "Crystal", "Ember", "Lunar",
    "Storm", "Nova", "Apex", "Crimson", "Obsidian", "Hyper", "Verdant",
    "Echo", "Frost", "Drift", "Titan", "Shadow", "Quantum",
]
STUDIO_NOUN = [
    "Forge", "Works", "Labs", "Games", "Interactive", "Studios",
    "Digital", "Entertainment", "Collective", "Assembly", "Dynamics",
    "Ventures", "Creations", "Productions", "Network",
]

DEV_ROLES = ["Lead Design", "Backend Engineering", "UI/UX", "QA", "Tools",
             "Gameplay Programming", "Audio", "Narrative", "Art Direction",
             "Level Design"]

COMMENT_TEMPLATES = [
    "Gameplay loop feels very polished this season.",
    "The latest patch really improved matchmaking quality.",
    "UI still needs better inventory sorting options.",
    "Performance was rock-solid during my last session.",
    "Co-op mode had occasional desync issues on cross-play.",
    "Difficulty curve feels well-balanced overall.",
    "Love the new map — great level design.",
    "Audio design is top-tier, especially the ambient tracks.",
    "Progression system feels rewarding without being grindy.",
    "Hit detection could use some work in PvP.",
    "Story DLC was worth every penny.",
    "Frame rate drops on older hardware during boss fights.",
    "Crafting system is surprisingly deep once you get into it.",
    "Matchmaking times are way better after the server update.",
    "Netcode improvements really show in ranked matches.",
    "Character customization options are fantastic.",
    "End-game content keeps me coming back every week.",
    "Loading times improved dramatically with the latest hotfix.",
    "The community events this month were really fun.",
    "Voice acting quality is excellent for an indie title.",
]

THREAD_TITLES = [
    "Patch {v} Notes — What Changed?",
    "Best Builds for Season {v}",
    "Ranked Mode Feedback Thread",
    "Meta Discussion: Current Tier List",
    "Bug Report Megathread (v{v})",
    "New Player Tips & Tricks",
    "Suggestions for Next Update",
    "Weekend Event Impressions",
    "Balancing Discussion: {class_name} Too Strong?",
    "Performance Optimization Guide",
    "Community Highlight Reel Thread",
    "Controller vs. M&KB Debate",
]

THREAD_CLASSES = ["Ranger", "Mage", "Tank", "Support", "Assassin", "Berserker"]

ALERT_TYPES = {
    "latency-spike": "Latency exceeded {val}ms threshold on endpoint {ep}.",
    "cpu-saturation": "CPU utilization at {pct}% — above target ceiling.",
    "memory-pressure": "Memory usage hit {pct}% — OOM risk rising.",
    "disk-watermark": "Disk usage crossed {pct}% watermark on volume {vol}.",
    "matchmaking-delay": "Matchmaking queue p95 at {val}s — above SLA target.",
    "connection-pool-exhaustion": "Connection pool {pct}% utilized — near saturation.",
    "error-rate-spike": "5xx error rate spiked to {pct}% of requests.",
    "ssl-cert-expiry": "SSL certificate for {ep} expires in {val} days.",
    "replication-lag": "DB replica lag reached {val}s.",
    "gc-pause": "GC pause exceeded {val}ms on worker pod.",
}

REPORT_TEMPLATES = [
    "Player was using abusive language in voice chat during a ranked match.",
    "Suspected wallhack — player consistently tracks opponents through walls.",
    "Account appears to be boosted — stats jumped overnight.",
    "Offensive username violating community guidelines.",
    "Spam messages flooding the game chat channel.",
    "Team-killing repeatedly in competitive mode.",
    "Exploiting a map glitch to get out of bounds.",
    "Toxic behavior in forum thread, harassing other users.",
    "Bot account farming in-game currency.",
    "Impersonating a developer or moderator in chat.",
    "Inappropriate content in user-generated level.",
    "Match manipulation — both teams appear coordinated.",
    "Advertising third-party services in comment section.",
    "Racist imagery in custom avatar/banner.",
    "Griefing newer players repeatedly in tutorial zone.",
]

RECOMMENDATION_REASONS = [
    "Matches your top-rated genre preferences.",
    "Popular among players you follow.",
    "Similar gameplay loop to your most-played title.",
    "Trending this week in your region.",
    "Recommended based on recent forum activity.",
    "High retention rate among comparable player profiles.",
    "Strong co-op features — pairs well with your friend list.",
    "New release from a studio you have favorited.",
    "Highly rated by the community this season.",
    "Shares multiple tags with your favorite games.",
]

RESOLUTION_NOTES = [
    "Warning issued to offending user.",
    "Temporary 7-day suspension applied.",
    "Content removed, no further action needed.",
    "Permanent ban applied after repeated violations.",
    "No violation found after investigation.",
    "Duplicate report — already handled under report #{rid}.",
    "Forwarded to anti-cheat team for deeper analysis.",
    "User apologized, informal warning issued.",
]

# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def esc(s: str) -> str:
    return s.replace("\\", "\\\\").replace("'", "\\'").replace(";", ",")

def ts(dt: datetime) -> str:
    return dt.strftime("%Y-%m-%d %H:%M:%S")

def date_str(dt: datetime) -> str:
    return dt.strftime("%Y-%m-%d")

def sha_hash() -> str:
    return hashlib.sha256(fake.binary(length=32)).hexdigest()

def pick(lst):
    return random.choice(lst)

now = datetime(2026, 4, 20, 12, 0, 0)

def past(max_days=300, min_days=1):
    return now - timedelta(days=random.randint(min_days, max_days))

def unique_pairs(pool_a, pool_b, n, *, no_self=False):
    pairs = set()
    attempts = 0
    while len(pairs) < n and attempts < n * 20:
        a = random.choice(pool_a)
        b = random.choice(pool_b)
        if no_self and a == b:
            attempts += 1
            continue
        if (a, b) not in pairs:
            pairs.add((a, b))
        attempts += 1
    return list(pairs)

# ---------------------------------------------------------------------------
# Data generation
# ---------------------------------------------------------------------------

lines = ["USE gamegoats_db;\n"]

# --- roles (4 fixed) ---
lines.append("-- roles")
lines.append("INSERT INTO roles (role_name) VALUES ('player'), ('recommender'), ('developer'), ('admin');\n")
ROLE_IDS = {"player": 1, "recommender": 2, "developer": 3, "admin": 4}

# --- users (40) ---
lines.append("-- users")
usernames = set()
users = []
for i in range(1, 41):
    while True:
        base = fake.user_name()
        uname = f"{base}{random.randint(10, 99)}"
        if uname not in usernames and len(uname) <= 64:
            usernames.add(uname)
            break
    domain = pick(["gmail.com", "outlook.com", "proton.me", "yahoo.com", "gamegoats.dev"])
    email = f"{uname}@{domain}"
    pwd = sha_hash()
    region = pick(REGIONS)
    created = past(360, 60)
    users.append({"id": i, "username": uname, "email": email,
                  "password_hash": pwd, "region": region, "created_at": created})

lines.append("INSERT INTO users (username, email, password_hash, region, created_at) VALUES")
vals = []
for u in users:
    vals.append(f"  ('{esc(u['username'])}', '{esc(u['email'])}', '{u['password_hash']}', "
                f"'{u['region']}', '{ts(u['created_at'])}')")
lines.append(",\n".join(vals) + ";\n")

# --- user_roles (target ≥130) ---
# Allocation: users 1-30 get player, 10-30 get recommender, 24-38 get developer, 39-40 get admin
# Many users get multiple roles to push count past 125
lines.append("-- user_roles")
ur_pairs = set()
# Every user is a player
for uid in range(1, 41):
    ur_pairs.add((uid, ROLE_IDS["player"]))
# All 40 users also get recommender (power users who leave reviews)
for uid in range(1, 41):
    ur_pairs.add((uid, ROLE_IDS["recommender"]))
# Users 24-38 are developers (15 devs)
for uid in range(24, 39):
    ur_pairs.add((uid, ROLE_IDS["developer"]))
# Users 39-40 are admins (also devs for elevated privileges)
for uid in [39, 40]:
    ur_pairs.add((uid, ROLE_IDS["admin"]))
    ur_pairs.add((uid, ROLE_IDS["developer"]))
# Give users 1-23 developer role too (community modders / contributors)
for uid in range(1, 24):
    ur_pairs.add((uid, ROLE_IDS["developer"]))
# Give some users admin role (senior community moderators)
for uid in range(35, 39):
    ur_pairs.add((uid, ROLE_IDS["admin"]))

ur_list = sorted(ur_pairs)
player_ids = sorted({uid for uid, rid in ur_list if rid == ROLE_IDS["player"]})
recommender_ids = sorted({uid for uid, rid in ur_list if rid == ROLE_IDS["recommender"]})
developer_ids = sorted({uid for uid, rid in ur_list if rid == ROLE_IDS["developer"]})
admin_ids = sorted({uid for uid, rid in ur_list if rid == ROLE_IDS["admin"]})

lines.append("INSERT INTO user_roles (user_id, role_id) VALUES")
vals = [f"  ({uid}, {rid})" for uid, rid in ur_list]
lines.append(",\n".join(vals) + ";\n")

# --- studios (35) ---
lines.append("-- studios")
studio_names_used = set()
studios = []
for i in range(1, 36):
    while True:
        sname = f"{pick(STUDIO_ADJ)} {pick(STUDIO_NOUN)}"
        if sname not in studio_names_used:
            studio_names_used.add(sname)
            break
    studios.append({"id": i, "name": sname, "region": pick(REGIONS),
                    "created_at": past(500, 90)})

lines.append("INSERT INTO studios (studio_name, headquarters_region, created_at) VALUES")
vals = [f"  ('{esc(s['name'])}', '{s['region']}', '{ts(s['created_at'])}')" for s in studios]
lines.append(",\n".join(vals) + ";\n")

# --- developer_profiles (15 devs — users 24-38 who are "real" devs with profiles) ---
lines.append("-- developer_profiles")
dev_ids = list(range(24, 39))
lines.append("INSERT INTO developer_profiles (developer_id, dev_handle, portfolio_url, years_experience) VALUES")
handles_used = set()
vals = []
for did in dev_ids:
    while True:
        handle = f"dev_{fake.lexify('????')}{random.randint(1,99)}"
        if handle not in handles_used and len(handle) <= 64:
            handles_used.add(handle)
            break
    url = f"https://portfolio.dev/{handle}"
    yrs = random.randint(1, 12)
    vals.append(f"  ({did}, '{esc(handle)}', '{url}', {yrs})")
lines.append(",\n".join(vals) + ";\n")

# --- studio_memberships (target ≥130) ---
# Each dev joins 8-10 studios; first membership is owner
lines.append("-- studio_memberships")
sm_pairs = set()
studio_id_pool = [s["id"] for s in studios]
for did in dev_ids:
    n_studios = random.randint(8, 10)
    chosen = random.sample(studio_id_pool, min(n_studios, len(studio_id_pool)))
    for idx, sid in enumerate(chosen):
        sm_pairs.add((sid, did, idx == 0))

sm_list = sorted(sm_pairs, key=lambda x: (x[0], x[1]))
lines.append("INSERT INTO studio_memberships (studio_id, developer_id, is_owner, joined_on) VALUES")
vals = []
for sid, did, is_owner in sm_list:
    joined = past(400, 30)
    vals.append(f"  ({sid}, {did}, {1 if is_owner else 0}, '{date_str(joined)}')")
lines.append(",\n".join(vals) + ";\n")

# --- games (40) ---
lines.append("-- games")
game_titles_used = set()
games = []
for i in range(1, 41):
    while True:
        title = f"{pick(TITLE_ADJ)} {pick(TITLE_NOUN)}"
        plat = pick(PLATFORMS)
        if (title, plat) not in game_titles_used:
            game_titles_used.add((title, plat))
            break
    genre = pick(GENRES)
    yr = random.randint(2012, 2026)
    rating = round(random.uniform(2.50, 4.99), 2)
    status = random.choices(LIFECYCLE, weights=[70, 20, 10])[0]
    pub_studio = pick(studio_id_pool) if random.random() < 0.85 else None
    created = past(450, 30)
    updated = created + timedelta(days=random.randint(1, 60))
    games.append({"id": i, "title": title, "platform": plat, "genre": genre,
                  "release_year": yr, "rating": rating, "status": status,
                  "studio": pub_studio, "created": created, "updated": updated})

lines.append("INSERT INTO games (title, description, genre, platform, release_year, "
             "average_rating, lifecycle_status, published_by_studio_id, created_at, updated_at) VALUES")
vals = []
for g in games:
    desc = esc(fake.sentence(nb_words=18)[:499])
    studio_val = str(g["studio"]) if g["studio"] else "NULL"
    vals.append(
        f"  ('{esc(g['title'])}', '{desc}', '{g['genre']}', '{g['platform']}', "
        f"{g['release_year']}, {g['rating']:.2f}, '{g['status']}', {studio_val}, "
        f"'{ts(g['created'])}', '{ts(g['updated'])}')"
    )
lines.append(",\n".join(vals) + ";\n")

game_ids = [g["id"] for g in games]

# --- game_developers (130) ---
lines.append("-- game_developers")
gd_pairs = unique_pairs(game_ids, dev_ids, 130)
lines.append("INSERT INTO game_developers (game_id, developer_id, contribution_role) VALUES")
vals = [f"  ({gid}, {did}, '{pick(DEV_ROLES)}')" for gid, did in sorted(gd_pairs)]
lines.append(",\n".join(vals) + ";\n")

# --- tags (35) ---
lines.append("-- tags")
lines.append("INSERT INTO tags (tag_name) VALUES")
vals = [f"  ('{esc(t)}')" for t in TAG_NAMES[:35]]
lines.append(",\n".join(vals) + ";\n")
tag_ids = list(range(1, 36))

# --- game_tags (140) ---
lines.append("-- game_tags")
gt_pairs = unique_pairs(game_ids, tag_ids, 140)
lines.append("INSERT INTO game_tags (game_id, tag_id) VALUES")
vals = [f"  ({gid}, {tid})" for gid, tid in sorted(gt_pairs)]
lines.append(",\n".join(vals) + ";\n")

# --- comments (70) ---
lines.append("-- comments")
lines.append("INSERT INTO comments (game_id, created_by_user_id, comment_text, rating, created_at, updated_at) VALUES")
vals = []
for _ in range(70):
    gid = pick(game_ids)
    uid = pick(player_ids)
    txt = esc(pick(COMMENT_TEMPLATES))
    rating = random.randint(1, 5)
    created = past(120, 1)
    updated = created + timedelta(hours=random.randint(0, 48))
    vals.append(f"  ({gid}, {uid}, '{txt}', {rating}, '{ts(created)}', '{ts(updated)}')")
lines.append(",\n".join(vals) + ";\n")

# --- forum_threads (60) ---
lines.append("-- forum_threads")
lines.append("INSERT INTO forum_threads (game_id, title, thread_text, created_by_user_id, created_at, updated_at) VALUES")
vals = []
forum_ids_range = list(range(1, 61))
for i in range(60):
    gid = pick(game_ids)
    tmpl = pick(THREAD_TITLES)
    title = tmpl.format(v=f"{random.randint(1,9)}.{random.randint(0,9)}",
                        class_name=pick(THREAD_CLASSES))
    if len(title) > 180:
        title = title[:180]
    body = esc(fake.paragraph(nb_sentences=4)[:999])
    uid = pick(player_ids + recommender_ids)
    created = past(90, 1)
    updated = created + timedelta(hours=random.randint(0, 72))
    vals.append(f"  ({gid}, '{esc(title)}', '{body}', {uid}, '{ts(created)}', '{ts(updated)}')")
lines.append(",\n".join(vals) + ";\n")

# --- forum_thread_contributions (70) ---
lines.append("-- forum_thread_contributions")
lines.append("INSERT INTO forum_thread_contributions (forum_id, contributed_by_user_id, contribution_text, created_at) VALUES")
vals = []
for _ in range(70):
    fid = pick(forum_ids_range)
    uid = pick(player_ids + recommender_ids)
    txt = esc(fake.paragraph(nb_sentences=2)[:499])
    created = past(60, 1)
    vals.append(f"  ({fid}, {uid}, '{txt}', '{ts(created)}')")
lines.append(",\n".join(vals) + ";\n")

# --- user_follows (130, no self-follows) ---
lines.append("-- user_follows")
all_user_ids = list(range(1, 41))
uf_pairs = unique_pairs(all_user_ids, all_user_ids, 130, no_self=True)
lines.append("INSERT INTO user_follows (follower_user_id, followed_user_id, followed_at) VALUES")
vals = [f"  ({a}, {b}, '{ts(past(200, 1))}')" for a, b in sorted(uf_pairs)]
lines.append(",\n".join(vals) + ";\n")

# --- favorites (150, unique player+game) ---
lines.append("-- favorites")
fav_pairs = unique_pairs(player_ids, game_ids, 150)
lines.append("INSERT INTO favorites (player_user_id, game_id, priority, added_at) VALUES")
vals = [f"  ({pid}, {gid}, {random.randint(1, 5)}, '{ts(past(180, 1))}')"
        for pid, gid in sorted(fav_pairs)]
lines.append(",\n".join(vals) + ";\n")

# --- recommendations (65, unique player+game) ---
lines.append("-- recommendations")
rec_pairs = unique_pairs(player_ids, game_ids, 65)
lines.append("INSERT INTO recommendations (player_user_id, game_id, recommender_user_id, "
             "recommendation_reason, match_score, is_saved, recommendation_status, "
             "generated_at, refreshed_at) VALUES")
vals = []
rec_statuses = ["new", "accepted", "dismissed", "hidden"]
for pid, gid in sorted(rec_pairs):
    rec_uid = pick(recommender_ids) if random.random() < 0.7 else "NULL"
    reason = esc(pick(RECOMMENDATION_REASONS))
    score = round(random.uniform(55.0, 99.99), 2)
    saved = 1 if random.random() < 0.2 else 0
    status = random.choices(rec_statuses, weights=[50, 25, 15, 10])[0]
    gen_at = past(60, 1)
    ref_at = gen_at + timedelta(hours=random.randint(1, 48))
    rec_uid_str = str(rec_uid) if rec_uid != "NULL" else "NULL"
    vals.append(
        f"  ({pid}, {gid}, {rec_uid_str}, '{reason}', {score:.2f}, {saved}, "
        f"'{status}', '{ts(gen_at)}', '{ts(ref_at)}')"
    )
lines.append(",\n".join(vals) + ";\n")

# --- servers (30) ---
lines.append("-- servers")
lines.append("INSERT INTO servers (server_name, region, environment, status, "
             "capacity_percent, last_heartbeat, created_at) VALUES")
vals = []
server_names_used = set()
server_envs = []
for i in range(1, 31):
    env = "production" if i <= 24 else "staging"
    prefix = "gg-prod" if env == "production" else "gg-stage"
    region = REGIONS[(i - 1) % len(REGIONS)]
    sname = f"{prefix}-{region.lower()}-{i:02d}"
    status = random.choices(["healthy", "degraded", "down"], weights=[75, 18, 7])[0]
    cap = round(random.uniform(15.0, 95.0), 2)
    hb = now - timedelta(minutes=random.randint(1, 120))
    created = past(300, 60)
    server_envs.append(env)
    vals.append(
        f"  ('{sname}', '{region}', '{env}', '{status}', {cap:.2f}, "
        f"'{ts(hb)}', '{ts(created)}')"
    )
lines.append(",\n".join(vals) + ";\n")
server_ids = list(range(1, 31))

# --- alerts (60) ---
lines.append("-- alerts")
alert_type_keys = list(ALERT_TYPES.keys())
lines.append("INSERT INTO alerts (server_id, alert_severity, alert_type, alert_message, "
             "alert_status, recorded_at, acknowledged_by_admin_id, acknowledged_at, resolved_at) VALUES")
vals = []
severities = ["low", "medium", "high", "critical"]
alert_statuses = ["active", "acknowledged", "resolved"]
for _ in range(60):
    sid = pick(server_ids)
    sev = random.choices(severities, weights=[35, 30, 25, 10])[0]
    atype_key = pick(alert_type_keys)
    msg = esc(ALERT_TYPES[atype_key].format(
        val=random.randint(100, 9999), pct=random.randint(70, 99),
        ep=f"/api/{fake.word()}", vol=f"/data/vol-{random.randint(1,8)}"))
    if len(msg) > 255:
        msg = msg[:255]
    astatus = random.choices(alert_statuses, weights=[50, 30, 20])[0]
    recorded = past(100, 1)
    ack_admin = "NULL"
    ack_at = "NULL"
    res_at = "NULL"
    if astatus in ("acknowledged", "resolved"):
        ack_admin = str(pick(admin_ids))
        ack_at = f"'{ts(recorded + timedelta(hours=random.randint(1, 24)))}'"
    if astatus == "resolved":
        res_at = f"'{ts(recorded + timedelta(hours=random.randint(25, 72)))}'"
    vals.append(
        f"  ({sid}, '{sev}', '{esc(atype_key)}', '{msg}', '{astatus}', "
        f"'{ts(recorded)}', {ack_admin}, {ack_at}, {res_at})"
    )
lines.append(",\n".join(vals) + ";\n")

# --- reports (55) ---
lines.append("-- reports")
offender_types = ["user", "game", "comment", "thread", "server", "studio", "other"]
report_statuses = ["open", "in_review", "resolved", "rejected"]
ref_id_pools = {
    "user": all_user_ids,
    "game": game_ids,
    "comment": list(range(1, 71)),
    "thread": forum_ids_range,
    "server": server_ids,
    "studio": [s["id"] for s in studios],
    "other": [None],
}

lines.append("INSERT INTO reports (created_by_user_id, offender_user_id, offender_type, "
             "offender_reference_id, report_text, report_status, handled_by_admin_id, "
             "created_at, resolved_at, resolution_notes) VALUES")
vals = []
for i in range(55):
    creator = pick(all_user_ids)
    otype = pick(offender_types)
    offender_uid = "NULL"
    if otype == "user":
        candidates = [u for u in all_user_ids if u != creator]
        offender_uid = str(pick(candidates))
    ref_pool = ref_id_pools[otype]
    ref_id = str(pick(ref_pool)) if ref_pool[0] is not None else "NULL"
    txt = esc(pick(REPORT_TEMPLATES))
    rstatus = random.choices(report_statuses, weights=[35, 25, 25, 15])[0]
    admin = "NULL"
    created = past(120, 1)
    resolved = "NULL"
    notes = "NULL"
    if rstatus in ("in_review", "resolved", "rejected"):
        admin = str(pick(admin_ids))
    if rstatus in ("resolved", "rejected"):
        resolved = f"'{ts(created + timedelta(days=random.randint(1, 14)))}'"
        note = esc(pick(RESOLUTION_NOTES).format(rid=random.randint(1, 55)))
        notes = f"'{note}'"
    vals.append(
        f"  ({creator}, {offender_uid}, '{otype}', {ref_id}, '{txt}', "
        f"'{rstatus}', {admin}, '{ts(created)}', {resolved}, {notes})"
    )
lines.append(",\n".join(vals) + ";\n")

# ---------------------------------------------------------------------------
# Write output
# ---------------------------------------------------------------------------
sql = "\n".join(lines)
OUT_PATH.write_text(sql, encoding="utf-8")

# Print row-count summary
print(f"Wrote {OUT_PATH}")
print(f"  users:                     {len(users)}")
print(f"  roles:                     4")
print(f"  user_roles:                {len(ur_list)}")
print(f"  studios:                   {len(studios)}")
print(f"  developer_profiles:        {len(dev_ids)}")
print(f"  studio_memberships:        {len(sm_list)}")
print(f"  games:                     {len(games)}")
print(f"  game_developers:           {len(gd_pairs)}")
print(f"  tags:                      {len(TAG_NAMES[:35])}")
print(f"  game_tags:                 {len(gt_pairs)}")
print(f"  comments:                  70")
print(f"  forum_threads:             60")
print(f"  forum_thread_contributions:70")
print(f"  user_follows:              {len(uf_pairs)}")
print(f"  favorites:                 {len(fav_pairs)}")
print(f"  recommendations:           {len(rec_pairs)}")
print(f"  servers:                   30")
print(f"  alerts:                    60")
print(f"  reports:                   55")
