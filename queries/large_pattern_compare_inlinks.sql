select
    Source,
    Destination,
    Anchor,
    "Status Code" as status_code,
    Follow,
    "Link Position" as link_position
from v_large_pattern_inlinks
where matched_patterns like '%compare%'
limit 500;