select
    source_kind,
    matched_patterns,
    rows
from v_large_pattern_summary
order by rows desc;