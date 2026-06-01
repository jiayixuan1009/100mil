select
    health_class,
    status,
    count(*) as urls,
    sum(case when status_ok = 'True' then 1 else 0 end) as status_ok_urls,
    sum(case when title_ok = 'True' then 1 else 0 end) as title_ok_urls,
    sum(case when meta_ok = 'True' then 1 else 0 end) as meta_ok_urls,
    sum(case when canonical_ok = 'True' then 1 else 0 end) as canonical_ok_urls,
    sum(case when robots_ok = 'True' then 1 else 0 end) as robots_ok_urls,
    sum(case when h1_ok = 'True' then 1 else 0 end) as h1_ok_urls
from read_csv_auto('docs/phase3_compare_live_regression_current.csv', header=true, all_varchar=true)
group by 1,2
order by health_class, status;