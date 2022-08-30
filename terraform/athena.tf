resource "aws_athena_database" "trips" {
  name   = "trips_database"
  bucket = "trips-landing-zone-dev"
  force_destroy = true
}

resource "aws_athena_named_query" "query_trips_top_2" {
  name      = "query_trips_top_2"
  database  = aws_athena_database.trips.name
  query = <<EOF
        with counter as(
            select region, count(*) as counting from AwsDataCatalog.trips_database.vwcte
            group by region order by count(*) desc
            limit 2
            ),
            row_n as (
            select * ,row_number() over(partition by region order by datetime desc) rn 
            from AwsDataCatalog.trips_database.vwcte 
            where region in (select region from counter)
            )
            select * from row_n;

  EOF
}


