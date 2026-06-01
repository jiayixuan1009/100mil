select
    source_kind,
    relative_path,
    scanned_rows,
    matched_rows,
    malformed_rows,
    imported_rows
from v_large_pattern_extract_inventory
order by matched_rows desc;