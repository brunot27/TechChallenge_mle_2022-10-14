import logging
import traceback
import os
from typing import Any
import pandas as pd
from datetime import datetime

from sklearn.linear_model import LogisticRegression, LinearRegression
from sklearn.preprocessing import PolynomialFeatures
from sklearn.tree import DecisionTreeClassifier
from sklearn.neighbors import KNeighborsClassifier
from sklearn.cluster import AgglomerativeClustering
from sklearn.naive_bayes import GaussianNB
from sklearn.cluster import KMeans
from sklearn.svm import SVC


# Set the log and model path
LOGS_DIR = os.path.join(os.path.dirname(__file__), "../logs/")
LOG_FILEMAME = os.path.join(
    LOGS_DIR, (datetime.now().strftime("%Y-%m-%d-%H-%M-%S") + ".log")
)
MODEL_DIR = os.path.join(os.path.dirname(__file__), "../models/")

# Create directories if not exist
for dirpath in [LOGS_DIR, MODEL_DIR]:
    if not os.path.exists(dirpath):
        os.makedirs(dirpath)


# Configuring logging
logger = logging.getLogger(__name__)
logging.basicConfig(
    filename=LOG_FILEMAME,
    filemode="a",
    level=logging.INFO,
    format="%(asctime)-15s | %(threadName)-11s | %(levelname)-5s | %(message)s",
)


class MLEModel:
    # init model
    model = None  # the model itself

    def linear_regression(self) -> Any:
        model_ = LinearRegression()
        return model_

    def logistic_regression(self) -> Any:
        model_ = LogisticRegression
        return model_

    def poly_regression(self, degree) -> Any:
        model_ = PolynomialFeatures(degree=degree)
        return model_

    def decison_tree(self, criterion: str) -> Any:
        model_ = DecisionTreeClassifier(criterion=criterion)
        return model_

    def knn(self, n_neighbors: int) -> Any:
        model_ = KNeighborsClassifier(n_neighbors=n_neighbors)
        return model_

    def svm(self, shape: str) -> Any:
        model_ = SVC(decision_function_shape=shape)
        return model_

    def agglo_cluster(self, n_clusters: int) -> Any:
        model_ = AgglomerativeClustering(n_clusters=n_clusters)
        return model_

    def naive_bayes(self) -> Any:
        model_ = GaussianNB()
        return model_

    def k_means(self, init: str, n_clusters: int) -> Any:
        model_ = (KMeans(init=init, n_clusters=n_clusters),)
        return model_

    def predict_with_logging(
        self,
        features: pd.DataFrame,
    ) -> None:
        """Predicts model with logging"""
        logger.info("--- Generating Prediction ---")
        # The SimpleModel has a predict method that we will use
        label = self.model.predict(features)
        logger.info(f"Predicted label: {label}")
        return label

    def trigger_retraining(
        self,
        features: pd.DataFrame,
        dataset: Any,
        new_dataset: Any,
    ) -> Any:
        """Compare the output and trigger"""
        try:
            # Read and fetch the last log
            with open(LOG_FILEMAME, "r") as f:
                log = f.read()
            last_log = max(os.listdir(LOGS_DIR))
            last_log = os.path.join(LOGS_DIR, last_log)

            # take the most current label from the last log
            to_check = "Predicted label:"
            last_line_log = [i for i in log.split("\n") if str(to_check) in i][-1]
            last_log_label = (
                last_line_log.split("|")[-1].replace(str(to_check), "").strip()
            )

            # Fit the model with the current dataset
            self.model.fit(dataset, 1)

            # Predict the dataset and compare the label
            current_label = self.model.predict(features)
            if current_label - last_log_label < 0.5:

                logger.info("Apply a partial fit to retrain the model")
                self.model.fit(new_dataset, 2)
                self.model.save(MODEL_DIR)

                logger.info(f"New model saved at {MODEL_DIR}")
                self.predict_with_logging(features)
            else:
                logger.info("No changes on the model")

            return LOG_FILEMAME

        except Exception:
            logger.error(traceback.format_exc())
            return
