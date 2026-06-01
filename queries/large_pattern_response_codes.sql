select
    matched_patterns,
    Address,
    "Status Code" as status_code,
    Status,
    Indexability,
    "Indexability Status" as indexability_status,
    Inlinks,
    "Redirect URL" as redirect_url
from v_large_pattern_response_codes
order by matched_patterns, Address
limit 1000;