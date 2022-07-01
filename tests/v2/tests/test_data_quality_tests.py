import pandas as pd

from evidently.pipeline.column_mapping import ColumnMapping
from evidently.v2.tests import TestConflictTarget
from evidently.v2.tests import TestConflictPrediction
from evidently.v2.tests import TestTargetPredictionCorrelation
from evidently.v2.tests import TestFeatureValueMin
from evidently.v2.tests import TestFeatureValueMax
from evidently.v2.tests import TestFeatureValueMean
from evidently.v2.tests import TestFeatureValueMedian
from evidently.v2.tests import TestFeatureValueStd
from evidently.v2.tests import TestNumberOfUniqueValues
from evidently.v2.tests import TestUniqueValuesShare
from evidently.v2.tests import TestMostCommonValueShare
from evidently.v2.tests import TestMeanInNSigmas
from evidently.v2.tests import TestValueRange
from evidently.v2.tests import TestNumberOfOutRangeValues
from evidently.v2.tests import TestShareOfOutRangeValues
from evidently.v2.tests import TestValueList
from evidently.v2.tests import TestNumberOfOutListValues
from evidently.v2.tests import TestShareOfOutListValues
from evidently.v2.tests import TestValueQuantile
from evidently.v2.test_suite import TestSuite


def test_data_quality_test_min() -> None:
    test_dataset = pd.DataFrame(
        {
            "category_feature": ["n", "d", "p", "n"],
            "numerical_feature": [0, 1, 2, 5],
            "target": [0, 0, 0, 1]
        }
    )
    suite = TestSuite(tests=[TestFeatureValueMin(feature_name="numerical_feature", gte=10)])
    suite.run(current_data=test_dataset, reference_data=None, column_mapping=ColumnMapping())
    assert not suite

    suite = TestSuite(tests=[TestFeatureValueMin(feature_name="numerical_feature", eq=0)])
    suite.run(current_data=test_dataset, reference_data=None, column_mapping=ColumnMapping())
    assert suite


def test_data_quality_test_max() -> None:
    test_dataset = pd.DataFrame(
        {
            "category_feature": ["n", "d", "p", "n"],
            "numerical_feature": [0, 1, 2, 5],
            "target": [0, 0, 0, 1]
        }
    )
    suite = TestSuite(tests=[TestFeatureValueMax(feature_name="numerical_feature", gt=10)])
    suite.run(current_data=test_dataset, reference_data=None, column_mapping=ColumnMapping())
    assert not suite

    suite = TestSuite(tests=[TestFeatureValueMax(feature_name="numerical_feature", eq=5)])
    suite.run(current_data=test_dataset, reference_data=None, column_mapping=ColumnMapping())
    assert suite


def test_data_quality_test_mean() -> None:
    test_dataset = pd.DataFrame(
        {
            "category_feature": ["n", "d", "p", "n"],
            "numerical_feature": [0, 1, 2, 5],
            "target": [0, 0, 0, 1]
        }
    )
    suite = TestSuite(tests=[TestFeatureValueMean(feature_name="numerical_feature", eq=5)])
    suite.run(current_data=test_dataset, reference_data=None, column_mapping=ColumnMapping())
    assert not suite

    suite = TestSuite(tests=[TestFeatureValueMean(feature_name="numerical_feature", gt=0, lt=10)])
    suite.run(current_data=test_dataset, reference_data=None, column_mapping=ColumnMapping())
    assert suite

    suite = TestSuite(tests=[TestFeatureValueMean(feature_name="numerical_feature", eq=2)])
    suite.run(current_data=test_dataset, reference_data=None, column_mapping=ColumnMapping())
    assert suite


def test_data_quality_test_conflict_target() -> None:
    test_dataset = pd.DataFrame(
        {
            "category_feature": ["n", "n", "p", "n"],
            "numerical_feature": [0, 0, 2, 5],
            "target": [0, 1, 0, 1]
        }
    )
    suite = TestSuite(tests=[TestConflictTarget()])
    suite.run(current_data=test_dataset, reference_data=None, column_mapping=ColumnMapping())
    assert not suite

    test_dataset = pd.DataFrame(
        {
            "category_feature": ["n", "d", "p", "n"],
            "numerical_feature": [0, 1, 2, 5],
            "target": [0, 0, 0, 1]
        }
    )
    suite = TestSuite(tests=[TestConflictTarget()])
    suite.run(current_data=test_dataset, reference_data=None, column_mapping=ColumnMapping())
    assert suite


def test_data_quality_test_conflict_prediction() -> None:
    test_dataset = pd.DataFrame(
        {
            "category_feature": ["n", "n", "p", "n"],
            "numerical_feature": [0, 0, 2, 5],
            "prediction": [0, 1, 0, 1]
        }
    )
    suite = TestSuite(tests=[TestConflictPrediction()])
    suite.run(current_data=test_dataset, reference_data=None, column_mapping=ColumnMapping())
    assert not suite

    test_dataset = pd.DataFrame(
        {
            "category_feature": ["n", "d", "p", "n"],
            "numerical_feature": [0, 1, 2, 5],
            "prediction": [0, 0, 0, 1]
        }
    )
    suite = TestSuite(tests=[TestConflictPrediction()])
    suite.run(current_data=test_dataset, reference_data=None, column_mapping=ColumnMapping())
    assert suite


def test_data_quality_test_target_prediction_correlation() -> None:
    test_dataset = pd.DataFrame(
        {
            "category_feature": ["n", "d", "p", "n"],
            "numerical_feature": [0, 1, 2, 5],
            "target": [0, 0, 0, 1],
            "prediction": [0, 0, 1, 1],
        }
    )
    suite = TestSuite(tests=[TestTargetPredictionCorrelation(gt=0.5)])
    suite.run(current_data=test_dataset, reference_data=None, column_mapping=ColumnMapping())
    assert suite


def test_data_quality_test_median() -> None:
    test_dataset = pd.DataFrame(
        {
            "feature1": [0, 1, 2, 5],
            "target": [0, 0, 0, 1],
            "prediction": [0, 0, 1, 1],
        }
    )
    suite = TestSuite(tests=[TestFeatureValueMedian(feature_name="no_existing_feature", eq=1.5)])
    suite.run(current_data=test_dataset, reference_data=None, column_mapping=ColumnMapping())
    assert not suite
    suite = TestSuite(tests=[TestFeatureValueMedian(feature_name="feature1", eq=1.5)])
    suite.run(current_data=test_dataset, reference_data=None, column_mapping=ColumnMapping())
    assert suite


def test_data_quality_test_std() -> None:
    test_dataset = pd.DataFrame(
        {
            "feature1": [0, 1, 2, 5],
            "target": [0, 0, 0, 1],
            "prediction": [0, 0, 1, 1],
        }
    )
    suite = TestSuite(tests=[TestFeatureValueStd(feature_name="no_existing_feature", eq=1.5)])
    suite.run(current_data=test_dataset, reference_data=None, column_mapping=ColumnMapping())
    assert not suite
    suite = TestSuite(tests=[TestFeatureValueStd(feature_name="feature1", lt=2)])
    suite.run(current_data=test_dataset, reference_data=None, column_mapping=ColumnMapping())
    assert not suite
    suite = TestSuite(tests=[TestFeatureValueStd(feature_name="feature1", gt=2, lt=3)])
    suite.run(current_data=test_dataset, reference_data=None, column_mapping=ColumnMapping())
    assert suite


def test_data_quality_test_unique_number() -> None:
    test_dataset = pd.DataFrame(
        {
            "feature1": [0, 1, 2, 5],
            "target": [0, 0, 0, 1],
            "prediction": [0, 0, 1, 1],
        }
    )
    suite = TestSuite(tests=[TestNumberOfUniqueValues(feature_name="no_existing_feature", eq=4)])
    suite.run(current_data=test_dataset, reference_data=None, column_mapping=ColumnMapping())
    assert not suite
    suite = TestSuite(tests=[TestNumberOfUniqueValues(feature_name="feature1", lt=2)])
    suite.run(current_data=test_dataset, reference_data=None, column_mapping=ColumnMapping())
    assert not suite
    suite = TestSuite(tests=[TestNumberOfUniqueValues(feature_name="feature1", eq=4)])
    suite.run(current_data=test_dataset, reference_data=None, column_mapping=ColumnMapping())
    assert suite


def test_data_quality_test_unique_share() -> None:
    test_dataset = pd.DataFrame(
        {
            "feature1": [0, 1, 2, 5],
            "target": [0, 0, 0, 1],
            "prediction": [0, 0, 1, 1],
        }
    )
    suite = TestSuite(tests=[TestUniqueValuesShare(feature_name="no_existing_feature", eq=1.5)])
    suite.run(current_data=test_dataset, reference_data=None, column_mapping=ColumnMapping())
    assert not suite
    suite = TestSuite(tests=[TestUniqueValuesShare(feature_name="feature1", lt=0.5)])
    suite.run(current_data=test_dataset, reference_data=None, column_mapping=ColumnMapping())
    assert not suite
    suite = TestSuite(tests=[TestUniqueValuesShare(feature_name="feature1", eq=1)])
    suite.run(current_data=test_dataset, reference_data=None, column_mapping=ColumnMapping())
    assert suite


def test_data_quality_test_most_common_value_share() -> None:
    test_dataset = pd.DataFrame(
        {
            "feature1": [0, 1, 1, 5],
            "target": [0, 0, 0, 1],
            "prediction": [0, 0, 1, 1],
        }
    )
    suite = TestSuite(tests=[TestMostCommonValueShare(feature_name="no_existing_feature", eq=0.5)])
    suite.run(current_data=test_dataset, reference_data=None, column_mapping=ColumnMapping())
    assert not suite
    suite = TestSuite(tests=[TestMostCommonValueShare(feature_name="feature1", lt=0.5)])
    suite.run(current_data=test_dataset, reference_data=None, column_mapping=ColumnMapping())
    assert not suite
    suite = TestSuite(tests=[TestMostCommonValueShare(feature_name="feature1", eq=0.5)])
    suite.run(current_data=test_dataset, reference_data=None, column_mapping=ColumnMapping())
    assert suite


def test_data_quality_test_value_in_n_sigmas() -> None:
    test_dataset = pd.DataFrame(
        {
            "feature1": [0, 1, 1, 20],
            "target": [0, 0, 0, 1],
            "prediction": [0, 0, 1, 1],
        }
    )
    reference_dataset = pd.DataFrame(
        {
            "feature1": [0, 1, 1, 3],
            "target": [0, 0, 0, 1],
            "prediction": [0, 0, 1, 1],
        }
    )
    suite = TestSuite(tests=[TestMeanInNSigmas(column="feature1")])
    suite.run(current_data=test_dataset, reference_data=reference_dataset, column_mapping=ColumnMapping())
    assert not suite

    suite = TestSuite(tests=[TestMeanInNSigmas(column="not_exist_feature", n_sigmas=3)])
    suite.run(current_data=test_dataset, reference_data=reference_dataset, column_mapping=ColumnMapping())
    assert not suite

    suite = TestSuite(tests=[TestMeanInNSigmas(column="feature1", n_sigmas=4)])
    suite.run(current_data=test_dataset, reference_data=reference_dataset, column_mapping=ColumnMapping())
    assert suite


def test_data_quality_test_value_in_range() -> None:
    test_dataset = pd.DataFrame(
        {
            "feature1": [0, 1, 1, 20],
            "target": [0, 0, 0, 1],
            "prediction": [0, 0, 1, 1],
        }
    )
    suite = TestSuite(tests=[TestValueRange(column="feature1", left=0, right=10)])
    suite.run(current_data=test_dataset, reference_data=None, column_mapping=ColumnMapping())
    assert not suite

    suite = TestSuite(tests=[TestValueRange(column="feature1", left=0, right=100)])
    suite.run(current_data=test_dataset, reference_data=None, column_mapping=ColumnMapping())
    assert suite

    reference_dataset = pd.DataFrame(
        {
            "feature1": [0, 1, 1, 3],
            "target": [0, 0, 0, 1],
            "prediction": [0, 0, 1, 1],
        }
    )
    suite = TestSuite(tests=[TestValueRange(column="feature1")])
    suite.run(current_data=test_dataset, reference_data=reference_dataset, column_mapping=ColumnMapping())
    assert not suite

    suite = TestSuite(tests=[TestValueRange(column="feature1", right=100)])
    suite.run(current_data=test_dataset, reference_data=reference_dataset, column_mapping=ColumnMapping())
    assert suite


def test_data_quality_test_number_of_values_not_in_range() -> None:
    test_dataset = pd.DataFrame(
        {
            "feature1": [0, 1, 1, 15],
            "target": [0, 0, 5, 1],
        }
    )
    suite = TestSuite(tests=[TestNumberOfOutRangeValues(column="feature1", left=0, right=10, lt=1)])
    suite.run(current_data=test_dataset, reference_data=None, column_mapping=ColumnMapping())
    assert not suite

    suite = TestSuite(tests=[TestNumberOfOutRangeValues(column="feature1", left=0, right=10, lte=1)])
    suite.run(current_data=test_dataset, reference_data=None, column_mapping=ColumnMapping())
    assert suite

    reference_dataset = pd.DataFrame(
        {
            "feature1": [0, 1, 1, 3],
            "target": [0, 0, 0, 1],
            "prediction": [0, 0, 1, 1],
        }
    )
    suite = TestSuite(tests=[TestNumberOfOutRangeValues(column="feature1", lt=1)])
    suite.run(current_data=test_dataset, reference_data=reference_dataset, column_mapping=ColumnMapping())
    assert not suite

    suite = TestSuite(tests=[TestNumberOfOutRangeValues(column="feature1", lte=1)])
    suite.run(current_data=test_dataset, reference_data=reference_dataset, column_mapping=ColumnMapping())
    assert suite


def test_data_quality_test_share_of_values_not_in_range() -> None:
    test_dataset = pd.DataFrame(
        {
            "feature1": [0, 1, 1, 15],
            "target": [0, 0, 5, 1],
        }
    )
    suite = TestSuite(tests=[TestShareOfOutRangeValues(column="feature1", left=0, right=10, lt=0.2)])
    suite.run(current_data=test_dataset, reference_data=None, column_mapping=ColumnMapping())
    assert not suite

    suite = TestSuite(tests=[TestShareOfOutRangeValues(column="feature1", left=0, right=10, lt=0.5)])
    suite.run(current_data=test_dataset, reference_data=None, column_mapping=ColumnMapping())
    assert suite

    reference_dataset = pd.DataFrame(
        {
            "feature1": [0, 1, 1, 3],
            "target": [0, 0, 0, 1],
            "prediction": [0, 0, 1, 1],
        }
    )
    suite = TestSuite(tests=[TestShareOfOutRangeValues(column="feature1", lt=0.2)])
    suite.run(current_data=test_dataset, reference_data=reference_dataset, column_mapping=ColumnMapping())
    assert not suite

    suite = TestSuite(tests=[TestShareOfOutRangeValues(column="feature1", lte=0.5)])
    suite.run(current_data=test_dataset, reference_data=reference_dataset, column_mapping=ColumnMapping())
    assert suite


def test_data_quality_test_value_in_list() -> None:
    test_dataset = pd.DataFrame(
        {
            "feature1": [0, 1, 1, 20],
            "target": [0, 0, 0, 1],
            "prediction": [0, 0, 1, 1],
        }
    )
    reference_dataset = pd.DataFrame(
        {
            "feature1": [0, 1, 1, 0],
            "target": [0, 0, 0, 1],
            "prediction": [0, 0, 1, 1],
        }
    )
    suite = TestSuite(tests=[TestValueList(column="feature1")])
    suite.run(current_data=test_dataset, reference_data=reference_dataset, column_mapping=ColumnMapping())
    assert not suite

    suite = TestSuite(tests=[TestValueList(column="target")])
    suite.run(current_data=test_dataset, reference_data=reference_dataset, column_mapping=ColumnMapping())
    assert suite


def test_data_quality_test_number_of_values_not_in_list() -> None:
    test_dataset = pd.DataFrame(
        {
            "feature1": [2, 4, 4, 20],
            "target": [0, 0, 0, 1],
            "prediction": [0, 0, 1, 1],
        }
    )
    reference_dataset = pd.DataFrame(
        {
            "feature1": [2, 4, 4, 2],
            "target": [0, 0, 0, 1],
            "prediction": [0, 0, 1, 1],
        }
    )
    suite = TestSuite(tests=[TestNumberOfOutListValues(column="feature1", gt=10)])
    suite.run(current_data=test_dataset, reference_data=reference_dataset, column_mapping=ColumnMapping())
    assert not suite

    suite = TestSuite(tests=[TestNumberOfOutListValues(column="feature1", lt=2)])
    suite.run(current_data=test_dataset, reference_data=reference_dataset, column_mapping=ColumnMapping())
    assert suite


def test_data_quality_test_share_of_values_not_in_list() -> None:
    test_dataset = pd.DataFrame(
        {
            "feature1": [0, 1, 1, 20],
            "target": [0, 0, 0, 1],
            "prediction": [0, 0, 1, 1],
        }
    )

    suite = TestSuite(tests=[TestShareOfOutListValues(column="feature1", values=[0], lt=0.5)])
    suite.run(current_data=test_dataset, reference_data=None, column_mapping=ColumnMapping())
    assert not suite

    suite = TestSuite(tests=[TestShareOfOutListValues(column="feature1", values=[0, 1], lt=0.5)])
    suite.run(current_data=test_dataset, reference_data=None, column_mapping=ColumnMapping())
    assert suite


def test_data_quality_test_value_quantile() -> None:
    test_dataset = pd.DataFrame(
        {
            "feature1": [0, 1, 2, 3],
            "target": [0, 0, 0, 1],
            "prediction": [0, 0, 1, 1],
        }
    )

    suite = TestSuite(tests=[TestValueQuantile(column="feature1", quantile=0.7, lt=1)])
    suite.run(current_data=test_dataset, reference_data=None, column_mapping=ColumnMapping())
    assert not suite

    suite = TestSuite(tests=[TestValueQuantile(column="feature1", quantile=0.2, lt=0.7)])
    suite.run(current_data=test_dataset, reference_data=None, column_mapping=ColumnMapping())
    assert suite