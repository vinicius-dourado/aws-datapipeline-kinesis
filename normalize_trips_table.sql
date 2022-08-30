with dataset(value)
 AS (
  select 
  ticker_symbol
  from trips_table
  ),
  parsed(entries) AS (
  SELECT cast(json_parse(value) AS array(row(region varchar, origin_coord varchar, destination_coord varchar, datetime varchar, datasource varchar, id integer)))
  FROM dataset
)
SELECT  ordinal,
        ticker_symbol.region,
        ticker_symbol.origin_coord,
        ticker_symbol.destination_coord,
        date_parse(ticker_symbol.datetime,'%Y-%m-%d %k:%i:%s'),
        ticker_symbol.datasource,
        cast(ticker_symbol.id as integer)
FROM parsed, UNNEST(entries) WITH ORDINALITY t(ticker_symbol, ordinal)
