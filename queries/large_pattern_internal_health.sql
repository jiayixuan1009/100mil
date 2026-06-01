select
    source_kind,
    matched_patterns,
    Address,
    "Status Code" as status_code,
    Status,
    Indexability,
    "Indexability Status" as indexability_status,
    "Title 1" as title,
    "Canonical Link Element 1" as canonical,
    Inlinks
from v_large_pattern_internal_all
order by matched_patterns, Address
limit 1000;