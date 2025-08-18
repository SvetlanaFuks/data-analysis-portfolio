--Project: Yandex Real Estate
-- Author: Svetlana Fuks
--Date: 08.08.2025

--Task 1. Ad activity time
with limits as (
       SELECT  
        PERCENTILE_DISC(0.99) WITHIN GROUP (ORDER BY total_area) AS total_area_limit,
        PERCENTILE_DISC(0.99) WITHIN GROUP (ORDER BY rooms) AS rooms_limit,
        PERCENTILE_DISC(0.99) WITHIN GROUP (ORDER BY balcony) AS balcony_limit,
        PERCENTILE_DISC(0.99) WITHIN GROUP (ORDER BY ceiling_height) AS ceiling_height_limit_h,
        PERCENTILE_DISC(0.01) WITHIN GROUP (ORDER BY ceiling_height) AS ceiling_height_limit_l
    FROM real_estate.flats),
cleaned as (
         SELECT id
    FROM real_estate.flats  
    WHERE 
        total_area < (SELECT total_area_limit FROM limits)
        AND (rooms < (SELECT rooms_limit FROM limits) OR rooms IS NULL)
        AND (balcony < (SELECT balcony_limit FROM limits) OR balcony IS NULL)
        AND ((ceiling_height < (SELECT ceiling_height_limit_h FROM limits)
            AND ceiling_height > (SELECT ceiling_height_limit_l FROM limits)) OR ceiling_height IS NULL)),              
category as (
select f.id,
       balcony,
       floor,
       rooms,
       last_price,
       total_area,
       type,
case
       	when c.city = 'Санкт-Петербург' then 'Санкт-Петербург' else 'ЛенОбл'
          end as city_category,
       case
       	when a.days_exposition < 31 then 'месяц'
       	when a.days_exposition >= 31 and days_exposition <= 90 then 'квартал'
       	when a.days_exposition >=91 and  days_exposition <= 180   then 'полгода'
       	when a.days_exposition>181 then 'больше полугода'
       	else 'еще активно'
       end as days_category       
from real_estate.flats f
left join real_estate.city c using (city_id)
left join real_estate.advertisement  a using (id)
left join real_estate.type t using (type_id)
where f.id IN (select * from cleaned) and  type ='город'),
calculus as (
       select city_category,
              days_category,
              count (id) as total_ads,
              ROUND ((select count (id) from category where city_category ='ЛенОбл')::numeric/(select count(id) from category),2) as ads_num_L,
              ROUND ((select count (id) from category where city_category ='Санкт-Петербург')::numeric/ (select count(id) from category),2) as ads_num_S,
              round (avg (last_price /total_area)::numeric,2) as avg_price_sqm,
              round (avg (total_area)::numeric,2) as avg_total_area,
              PERCENTILE_DISC(0.5) within Group (Order by balcony) as median_balcony,
              PERCENTILE_DISC(0.5) within Group (Order by rooms) as median_rooms,
              PERCENTILE_DISC(0.99) within Group (Order by floor) as median_floor        
from category
group by city_category,days_category)
select *
from calculus;

--Task 2. Ad seasonality
with limits as (
       SELECT  
        PERCENTILE_DISC(0.99) WITHIN GROUP (ORDER BY total_area) AS total_area_limit,
        PERCENTILE_DISC(0.99) WITHIN GROUP (ORDER BY rooms) AS rooms_limit,
        PERCENTILE_DISC(0.99) WITHIN GROUP (ORDER BY balcony) AS balcony_limit,
        PERCENTILE_DISC(0.99) WITHIN GROUP (ORDER BY ceiling_height) AS ceiling_height_limit_h,
        PERCENTILE_DISC(0.01) WITHIN GROUP (ORDER BY ceiling_height) AS ceiling_height_limit_l
    FROM real_estate.flats),
cleaned as (
         SELECT id
    FROM real_estate.flats  
    WHERE 
        total_area < (SELECT total_area_limit FROM limits)
        AND (rooms < (SELECT rooms_limit FROM limits) OR rooms IS NULL)
        AND (balcony < (SELECT balcony_limit FROM limits) OR balcony IS NULL)
        AND ((ceiling_height < (SELECT ceiling_height_limit_h FROM limits)
            AND ceiling_height > (SELECT ceiling_height_limit_l FROM limits)) OR ceiling_height IS NULL)),
dates as (select *,
       to_char(date_trunc('month', (first_day_exposition::date + days_exposition * INTERVAL '1 day')::timestamp), 'Month') AS sold_month,       --создаем колонку даты продажы и округляем до месяца
       to_char(date_trunc('month', first_day_exposition), 'Month') AS publishing_month 
from real_estate.advertisement
left join real_estate.flats using (id)
left join real_estate.type using (type_id)
where id in (select * from cleaned) and type = 'город' and EXTRACT(YEAR FROM first_day_exposition) BETWEEN 2015 AND 2018),
published_data as (
                   select publishing_month as ac_month,
                   count (d.id) as total_published,
                   round(avg (last_price /total_area)::numeric,2)  as published_avg_price_sqm,
                   round (avg ((total_area)::numeric)::numeric,2) as published_avg_total_area,
                   round ((count (d.id)::numeric/(select count (*) from dates))*100,2) as share_published,
                   dense_rank() over (order by count (d.id) asc ) as published_rank
                   from dates as d
group by publishing_month
order by publishing_month asc),
sold_data as (select sold_month as ac_month,
                   count (days_exposition) as total_sold,
                   round(avg (last_price /total_area)::numeric,2)  as avg_price_sqm,
                   round (avg ((total_area)::numeric)::numeric,2) as avg_total_area,
                   round ((count (d.id)::numeric/(select count (*) from dates  where days_exposition IS NOT null))*100,2) as share_sold,
                   dense_rank () over (order by count (days_exposition) asc ) as sold_rank
                   from dates as d
where days_exposition IS NOT null
group by sold_month
order by sold_month asc)
select *
from published_data
full join sold_data using (ac_month)
order by published_rank asc;


--Task 3. Analysis of the Leningrad Region real estate market
with limits as (
       SELECT  
        PERCENTILE_DISC(0.99) WITHIN GROUP (ORDER BY total_area) AS total_area_limit,
        PERCENTILE_DISC(0.99) WITHIN GROUP (ORDER BY rooms) AS rooms_limit,
        PERCENTILE_DISC(0.99) WITHIN GROUP (ORDER BY balcony) AS balcony_limit,
        PERCENTILE_DISC(0.99) WITHIN GROUP (ORDER BY ceiling_height) AS ceiling_height_limit_h,
        PERCENTILE_DISC(0.01) WITHIN GROUP (ORDER BY ceiling_height) AS ceiling_height_limit_l
    FROM real_estate.flats),
cleaned as (
         SELECT id
    FROM real_estate.flats  
    WHERE 
        total_area < (SELECT total_area_limit FROM limits)
        AND (rooms < (SELECT rooms_limit FROM limits) OR rooms IS NULL)
        AND (balcony < (SELECT balcony_limit FROM limits) OR balcony IS NULL)
        AND ((ceiling_height < (SELECT ceiling_height_limit_h FROM limits)
            AND ceiling_height > (SELECT ceiling_height_limit_l FROM limits)) OR ceiling_height IS NULL)),
city_len as (
            select city,
                   type,
                   ceiling(avg (a.days_exposition)) as avg_days_exposition,
                   min (a.days_exposition) as min_days_exposition,
                   max (a.days_exposition) as max_days_exposition,
                   count (first_day_exposition) as total_published_ads,
                   count(days_exposition) as total_sold,
                   round ((select count (id) from real_estate.advertisement where days_exposition IS NOT null)::numeric /(select count (*) from real_estate.advertisement  where days_exposition IS NOT null))*100,2) as ratio_sold_ads,
                   round(avg (last_price /total_area)::numeric, 2) AS avg_price,
                   round(avg(total_area)::numeric, 2) AS avg_area
             from real_estate.advertisement as a
             left join real_estate.flats as f using (id)
             left join real_estate.city as c using (city_id)
             left join real_estate.type as t using (type_id)
             where f.id in (select * from cleaned) and f.city_id != '6X8I'
             group by city, type)
select*
from city_len
where total_published_ads >100
order by total_published_ads desc;         


             

                   
            




