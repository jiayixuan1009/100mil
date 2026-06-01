select
    source_group,
    files,
    size_mb,
    imported_rows,
    imported_files,
    failed_files
from v_raw_source_inventory
order by size_mb desc;