
import pytest
from pyspark.sql import SparkSession
from pyspark_job import clean_data
@pytest.fixture(scope="session")
def spark():
    spark = (
        SparkSession.builder
        .master("local[2]")
        .appName("test-clean-data")
        .getOrCreate()
    )

    yield spark

    spark.stop()


def test_clean_data(spark):
    data = [
        ("alice", 150.0),
        ("bob", -20.0),
        ("charlie", 0.0),
        (None, 100.0),
    ]

    df = spark.createDataFrame(
        data,
        ["name", "amount"]
    )

    result = clean_data(df).collect()

    assert len(result) == 1

    assert result[0]["name"] == "alice"
    assert result[0]["amount"] == 150.0
    assert result[0]["amount_with_tax"] == 180.0
