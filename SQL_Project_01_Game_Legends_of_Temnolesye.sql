/* Project «Legends of Temnolesye»
 * Goal: Study the influence of players’ characteristics and their in-game characters on the purchase of the in-game currency "Paradise Petals," as well as assess players’ activity when making in-game purchases.

 * Author: Svetlana Fuks
 * Date: 15.07.2025
*/

-- Part 1. Exploratory Data Analysis" (EDA): Analysis of the share of paying players

-- 1.1. Share of paying users across all data:

select count(id) as total_users,
       count(case when payer =1 then payer end) as total_payers,
       ROUND ((count(case when payer =1 then payer end)::numeric/count(id)),2) as payer_share
     from fantasy.users;


--/*total_users	total_payers	payer_share
--   22 214    |	3 929	 |   0,18*/

-- 1.2. Share of paying users by character race:

select r.race,
count(u.id) as total_users_by_race,
count(case when u.payer =1 then payer end) as total_paying_race,
ROUND ((count(case when u.payer =1 then payer end)::numeric/ count(id)),2) as race_payer_share
from fantasy.users as u
left join fantasy.race as r on u.race_id = r.race_id
group by r.race;

/*race	total_users_by_race	total_paying_species	race_payer_share
Elf	    2 501	               427                  	0,17
Human	6 328                1 114	                    0,18
Orc	    3 619	               636	                    0,18
Hobbit	3 648	               659	                    0,18
Northman 3 562                 626	                    0,18
Angel	1 327	               229	                    0,17
Demon	1 229	               238	                    0,19*/

-- task 2. Analysis of in-game purchases
-- 2.1. Statistical indicators for the amount field:

select count (transaction_id) as total_transactions,
          sum (amount) as total_revenue,
          min (amount) as min_amount,
          max (amount) as max_amount,
          ROUND(avg (amount)::numeric,2) as avg_amount,
         PERCENTILE_DISC(0.5) within group (order by amount) as median_amount,
         stddev (amount) as amount_stddev
from fantasy.events;
 
/*--total_transactions	total_revenue	min_amount	max_amount	avg_amount	median_amount	amount_stddev
--1 307 678	            686 615 040	         0	     486 615,1	525,69	      74,86	          2 517,3454444278
   */


--Statistical indicators for the amount field without anomalies (zeros filtered out)
select count (transaction_id) as filtered_total_transactions,
          sum (amount) as filtered_total_revenue,
          min (amount) as filtered_min_amount,
          max (amount) as filtered_max_amount,
          ROUND(avg (amount)::numeric,2) as filtered_avg_amount,
         PERCENTILE_DISC(0.5) within group (order by amount) as filtered_median_amount,
         stddev (amount) as filtered_amount_stddev
from fantasy.events
 where amount <> 0;

/*
total_transactions	total_revenue	min_amount	max_amount	avg_amount	median_amount	amount_stddev
1 306 771	        686 615 040     	0,01	486 615,1	526,06	     74,86	        2 518,1807984988
*/

-- 2.2: Abnormal zero purchases:

with empty_amount as (
         select count (transaction_id) as total_empty_count
         from fantasy.events
         where amount =0)
select total_empty_count,
       total_empty_count::numeric /(select count (transaction_id) from fantasy.events) as share_empty_amount
from empty_amount;

/*--  total_empty_count              share_empty_amount
--      907                             0,0006935958*/

-- 2.3: Popular epic items:

with stats_per_item as (
         select item_code,
         count (distinct id) as total_item_users,
         count (transaction_id) as total_item_transactions 
         from fantasy.events
         left join fantasy.users using (id)
         where amount > 0 
         group by item_code),
desc_stats as (
        select count (distinct id) as total_users,
               count (transaction_id) as total_transactions 
        from fantasy.events
        left join fantasy.users using (id)
        where amount > 0 )
select item_code,
       game_items,
       total_item_transactions,
       ROUND (total_item_transactions::numeric/(select total_transactions from desc_stats),2) as share_trans,
       ROUND (total_item_users::numeric /(select total_users from desc_stats),2) as share_users   
from stats_per_item 
left join fantasy.items as i using (item_code)
order by share_users desc
limit 5;

/*item_code	game_items	total_item_transactions	share_trans	share_users
6 010	Book of Legends	   1004516	                0,77      	0,88
6 011	Bag of Holding	   271875                	0,21	    0,87
6 012	Necklace of Wisdom 13828	                0,01	    0,12
6 536	Gems of Insight	    3833	                0	         0,07
5 411	Silver Flask	    795	                     0	        0,05*/

-- Task: Dependence of player activity on character race:
with totals as (
      select race_id,
      count (*) as total_users_by_race
from fantasy.users
group by race_id),
totals_by_race as (
select u.race_id,
       count (distinct e.id)filter (where amount >0) as total_buyers,
       count (distinct e.id) filter (where amount >0 and payer = 1) as payers
from fantasy.events as e
left join fantasy.users as u on u.id=e.id
group by race_id),
descriptives_by_race as (
select u.race_id,
       count (e.transaction_id) filter (where amount >0) as total_purchase_number_by_race,
       sum (e.amount) as total_amount_by_race
from fantasy.events as e
left join fantasy.users as u on u.id=e.id
group by race_id)
select r.race,
       total_users_by_race,
       total_buyers,
       total_buyers::numeric/total_users_by_race as share_buyers,
       payers::numeric/total_buyers as share_payers,
       total_purchase_number_by_race::numeric/total_buyers as avg_purchase_number,
       total_amount_by_race::numeric/total_purchase_number_by_race as avg_amount_per_user,
       total_amount_by_race::numeric/total_buyers as avg_sum_per_user
 from totals as t
 left join totals_by_race as tr on t.race_id= tr.race_id
 left join descriptives_by_race as de  on t.race_id=de.race_id
 left join fantasy.race as r on t.race_id=r.race_id;    

/*
 race      | total_users_by_race | total_buyers | share_buyers | share_payers | avg_purchase_number | avg_amount_per_user | avg_sum_per_user
------------------------------------------------------------------------------------------------------------------------------------
 Elf       |               2 501 |        1 543 |       0,6170 |       0,1627 |             78,7907 |             682,3301 |           53 761,2443
 Northman  |               3 562 |        2 229 |       0,6258 |       0,1821 |             82,1018 |             761,4819 |           62 519,0668
 Angel     |               1 327 |          820 |       0,6179 |       0,1671 |            106,8049 |             455,6406 |           48 664,6341
 Orc       |               3 619 |        2 276 |       0,6289 |       0,1740 |             81,7381 |             510,9205 |           41 761,6872
 Hobbit    |               3 648 |        2 266 |       0,6212 |       0,1770 |             86,1289 |             552,9134 |           47 621,8005
 Human     |               6 328 |        3 921 |       0,6196 |       0,1801 |            121,4022 |             403,0709 |           48 933,6904
 Demon     |               1 229 |          737 |       0,5997 |       0,1995 |             77,8697 |             529,0173 |           41 194,4369
*/
