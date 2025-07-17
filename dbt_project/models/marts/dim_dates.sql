with all_dates as (
    select message_date::date as date from {{ ref('stg_lobelia4cosmetics') }}
    union
    select message_date::date as date from {{ ref('stg_tikvahpharma') }}
),
distinct_dates as (
    select distinct date from all_dates
)
select
    row_number() over (order by date) as date_id,
    date,
    extract(year from date) as year,
    extract(month from date) as month,
    extract(day from date) as day,
    extract(dow from date) as weekday
from distinct_dates
order by date 