select
    page_type_guess,
    source,
    count(*) as orphan_urls
from v_raw_www_orphan_pages_0518
group by page_type_guess, source
order by orphan_urls desc;