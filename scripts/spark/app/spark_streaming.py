from pyspark.sql import SparkSession, DataFrame
from pyspark.sql.types import StructType, StringType, StructField
from pyspark.sql.functions import col, from_json
from psycopg2 import connect


def create_spark_session() -> SparkSession:
    """Initialize and return a Spark Session with Cassandra support."""
    builder: SparkSession.Builder = SparkSession.builder
    spark_session: SparkSession = builder.appName(
        "KafkaToCassandraStreaming"
    ).getOrCreate()

    spark_session.sparkContext.setLogLevel("ERROR")

    return spark_session


def read_from_kafka(
    spark: SparkSession, bootstrap_servers: str, topic: str
) -> DataFrame:
    """Read streaming data from Kafka topic."""
    return (
        spark.readStream.format("kafka")
        .option("kafka.bootstrap.servers", bootstrap_servers)
        .option("subscribe", topic)
        .option("startingOffsets", "earliest")
        .load()
        .selectExpr("CAST(value AS STRING) as message")
    )


def parse_stream_data(dataframe: DataFrame) -> DataFrame:
    """Parse JSON data from Kafka stream."""
    schema = StructType(
        [
            StructField("id", StringType(), False),
            StructField("name", StringType(), False),
            StructField("email", StringType(), False),
            StructField("gender", StringType(), False),
            StructField("address", StringType(), True),
            StructField("phone", StringType(), True),
            StructField("dob", StringType(), True),
        ]
    )

    return dataframe.select(from_json(col("message"), schema).alias("data")).select(
        "data.*"
    )


def write_to_postgres(batch_df: DataFrame, table_name: str) -> None:
    """Write Spark DataFrame batch to PostgreSQL."""
    pgsql_url = "jdbc:postgresql://postgres:5432/postgres"
    pgsql_properties = {
        "user": "postgres",
        "password": "postgres",
        "driver": "org.postgresql.Driver",
    }

    (
        batch_df.write.format("jdbc")
        .option("url", pgsql_url)
        .option("dbtable", table_name)
        .options(**pgsql_properties)
        .mode("append")
        .save()
    )


def create_table(table_name: str) -> None:
    """Ensure the PostgreSQL table exists."""
    conn = connect(
        host="postgres", dbname="postgres", user="postgres", password="postgres"
    )
    cur = conn.cursor()
    cur.execute(
        f"""
        CREATE TABLE IF NOT EXISTS {table_name} (
            id VARCHAR PRIMARY KEY,
            name VARCHAR,
            email VARCHAR,
            gender VARCHAR,
            address VARCHAR,
            phone VARCHAR,
            dob VARCHAR
        );
    """
    )
    conn.commit()
    cur.close()
    conn.close()
    print("✅ Table checked/created.")


def main() -> None:
    """Main entry point for Spark Streaming application."""

    table_name = "fake_users"
    kafka_bootstrap_servers = "kafka:29092"
    kafka_topic = "fake-users"

    create_table(table_name)

    spark = create_spark_session()

    raw_df: DataFrame = read_from_kafka(spark, kafka_bootstrap_servers, kafka_topic)
    dataframe: DataFrame = parse_stream_data(raw_df)

    query = (
        dataframe.writeStream.foreachBatch(
            lambda batch_df, _: write_to_postgres(batch_df, table_name)
        )
        .outputMode("append")
        .start()
    )

    query.awaitTermination()


if __name__ == "__main__":
    main()
