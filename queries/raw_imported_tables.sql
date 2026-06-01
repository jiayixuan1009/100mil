select
    source_group,
    table_name,
    relative_path,
    imported_rows,
    size_mb
from v_raw_imported_tables
order by source_group, size_mb desc;