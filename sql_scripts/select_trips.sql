with dataset(value) AS (
	select content
	from trips_tbl
),
parsed(entries) AS (
	SELECT cast(
			json_parse(value) AS array(
				row(
					region varchar,
					origin_coord varchar,
					destination_coord varchar,
					datetime varchar,
					datasource varchar,
					id integer,
					city_ori varchar,
					state_ori varchar,
					country_ori varchar,
					city_dest varchar,
					state_dest varchar,
					country_dest varchar
					
				)
			)
		)
	FROM dataset
)
SELECT content.region,
	content.origin_coord,
	content.destination_coord,
	--date_parse(content.datetime, '%Y-%m-%d %k:%i:%s'),
	content.datetime, 
	content.datasource,
	cast(content.id as integer) as id,
	content.city_ori,
	content.state_ori,
	content.country_ori,
	content.city_dest,
	content.state_dest,
	content.country_dest	
FROM parsed,
	UNNEST(entries) WITH ORDINALITY t(content, id);
