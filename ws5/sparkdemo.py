import sys

from pyspark.sql import SparkSession
from pyspark.ml import Pipeline
from pyspark.ml.feature import VectorAssembler
from pyspark.ml.regression import LinearRegression
from pyspark.ml.evaluation import RegressionEvaluator


# A1: Create a SparkSession named ws5-regression
spark = (
    SparkSession.builder
    .appName("ws5-regression")
    .getOrCreate()
)


# A2: Read the CSV path passed through the command line
input_path = sys.argv[1]

data = (
    spark.read
    .option("header", True)
    .option("inferSchema", True)
    .csv(input_path)
)

print("Dataset:")
data.show()


# A3: Combine total_bill and size into a features vecto
assembler = VectorAssembler(
    inputCols=["total_bill", "size"],
    outputCol="features"
)


# A4: Split the data into 80% training and 20% testing
train_data, test_data = data.randomSplit(
    [0.8, 0.2],
    seed=42
)


# A5: Define the linear regression model and pipeline
regression = LinearRegression(
    featuresCol="features",
    labelCol="tip"
)

pipeline = Pipeline(
    stages=[assembler, regression]
)

pipeline_model = pipeline.fit(train_data)


# A6: Make predictions using the test data
predictions = pipeline_model.transform(test_data)

print("Predictions:")
predictions.select(
    "total_bill",
    "size",
    "tip",
    "prediction"
).show()


# A7: Evaluate the predictions using RMSE and R-squared
evaluator = RegressionEvaluator(
    labelCol="tip",
    predictionCol="prediction"
)

evaluator.setMetricName("rmse")
rmse = evaluator.evaluate(predictions)

evaluator.setMetricName("r2")
r2 = evaluator.evaluate(predictions)


# A8: Get the fitted regression model from the pipeline
fitted_model = pipeline_model.stages[-1]

print("----- MODEL RESULTS -----")
print(f"Coefficients: {fitted_model.coefficients}")
print(f"Intercept: {fitted_model.intercept}")
print(f"RMSE: {rmse}")
print(f"R-squared: {r2}")
print("-------------------------")


spark.stop()
