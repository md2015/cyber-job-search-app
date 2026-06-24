from fuzzywuzzy import fuzz

DEGREE_TIERS = {
    "high school": 1, "ged": 1,
    "associate": 2, "aas": 2, "aa": 2,
    "bachelor": 3, "bs": 3, "ba": 3, "bsc": 3,
    "master": 4, "ms": 4, "mba": 4,
    "phd": 5, "doctorate": 5,
}

CERT_ALIASES = {
    "security+": ["security plus", "comptia security+", "sec+"],
    "network+": ["network plus", "comptia network+", "net+"],
    "a+": ["comptia a+", "a plus"],
    "linux+": ["comptia linux+"],
    "ceh": ["certified ethical hacker", "ec-council ceh"],
    "cissp": ["certified information systems security professional"],
    "ccna": ["cisco certified network associate"],
}

def match_job(job, profile):
    degree_score, degree_detail = _match_degree(job.get("education_required", ""), profile)
    cert_score, cert_detail = _match_certs(job.get("certifications_required", ""), profile)
    skill_score, skill_detail = _match_skills(job.get("skills_required", "") + " " + job.get("description", ""), profile)

    total = round((degree_score * 0.35) + (cert_score * 0.30) + (skill_score * 0.35))

    if total >= 75:
        status = "✅ Yes"
    elif total >= 45:
        status = "⚠️ Partial Match"
    else:
        status = "❌ No"

    return {
        **job,
        "match_status": status,
        "match_score": total,
        "degree_score": degree_score,
        "cert_score": cert_score,
        "skill_score": skill_score,
        "match_detail": {"degree": degree_detail, "certs": cert_detail, "skills": skill_detail},
    }

def _match_degree(required, profile):
    if not required or required.strip().lower() in ["", "not specified", "none"]:
        return 100, "No degree requirement listed."
    req_lower = required.lower()
    req_tier = 0
    for keyword, tier in DEGREE_TIERS.items():
        if keyword in req_lower:
            req_tier = max(req_tier, tier)
    user_tier = 0
    user_highest = ""
    for deg in profile.get("degrees", []):
        deg_lower = deg.lower()
        for keyword, tier in DEGREE_TIERS.items():
            if keyword in deg_lower and tier > user_tier:
                user_tier = tier
                user_highest = deg
    if req_tier == 0:
        return 80, f"Unclear requirement. You have: {user_highest}."
    if user_tier >= req_tier:
        return 100, f"✔ Your {user_highest} meets requirement."
    elif user_tier == req_tier - 1:
        return 50, f"⚠ Job wants higher degree. You have {user_highest}."
    else:
        return 0, f"✘ Degree gap. You have {user_highest}."

def _match_certs(required, profile):
    if not required or required.strip().lower() in ["", "none specified", "none"]:
        return 100, "No certifications required."
    user_certs = [c.lower() for c in profile.get("certifications", [])]
    required_items = [r.strip() for r in required.split(",") if r.strip()]
    matched, missing = [], []
    for req_cert in required_items:
        req_lower = req_cert.lower()
        found = any(req_lower in uc or uc in req_lower for uc in user_certs)
        if not found:
            for canonical, aliases in CERT_ALIASES.items():
                if req_lower in [canonical] + aliases:
                    found = any(canonical in uc or any(a in uc for a in aliases) for uc in user_certs)
                    break
        if not found:
            found = any(fuzz.partial_ratio(req_lower, uc) >= 80 for uc in user_certs)
        (matched if found else missing).append(req_cert)
    if not required_items:
        return 100, "No certs required."
    score = round(len(matched) / len(required_items) * 100)
    detail = ""
    if matched:
        detail += f"✔ Have: {', '.join(matched)}. "
    if missing:
        detail += f"✘ Missing: {', '.join(missing)}."
    return score, detail.strip()

def _match_skills(text, profile):
    user_skills = [s.lower() for s in profile.get("skills", [])]
    text_lower = text.lower()
    matched = [s for s in user_skills if s in text_lower]
    score = min(100, round(len(matched) / max(len(user_skills), 1) * 120))
    detail = f"✔ Matched: {', '.join(matched[:5])}." if matched else "No skill overlap found."
    return score, detail

def batch_match(jobs, profile):
    return [match_job(job, profile) for job in jobs]
