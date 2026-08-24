select
    成交日期,
    sum(六一成交额) 四分位成交总额,
    sum(六一成交额)/max(全天总成交额) '前25%占比',
    sum(复购数)/count(*) 复购率
from
(
    select
        substring(fullbid_date,1,10) 成交日期,
        user_id,
        sum(amount) 六一成交额,
        cume_dist() over (order by sum(amount) desc) 排名,
        sum(sum(amount)) over () as 全天总成交额
    from edw.dsx_listing_info
    where substring(fullbid_date,1,10)='2020-06-01'
    group by 1,2
) a
left join
(
    select
        user_id,
        1 复购数
    from edw.dsx_listing_info
    where substring(fullbid_date,1,7)='2020-06' and substring(fullbid_date,1,10)!='2020-06-01'
    group by 1
) b
on a.user_id=b.user_id
where 排名 <= 0.25
group by 1