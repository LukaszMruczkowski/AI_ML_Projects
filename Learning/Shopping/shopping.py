import csv
import sys

from sklearn.model_selection import train_test_split
from sklearn.neighbors import KNeighborsClassifier

TEST_SIZE = 0.4


def main():

    # Check command-line arguments
    if len(sys.argv) != 2:
        sys.exit("Usage: python shopping.py data")

    # Load data from spreadsheet and split into train and test sets
    evidence, labels = load_data(sys.argv[1])
    X_train, X_test, y_train, y_test = train_test_split(
        evidence, labels, test_size=TEST_SIZE
    )

    # Train model and make predictions
    model = train_model(X_train, y_train)
    predictions = model.predict(X_test)
    sensitivity, specificity = evaluate(y_test, predictions)

    # Print results
    print(f"Correct: {(y_test == predictions).sum()}")
    print(f"Incorrect: {(y_test != predictions).sum()}")
    print(f"True Positive Rate: {100 * sensitivity:.2f}%")
    print(f"True Negative Rate: {100 * specificity:.2f}%")

# Converts month string into corresponding value
def convert_month(month):
    months = ["Jan", "Feb", "Mar", "Apr", "May", "June", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
    
    return months.index(month)



def load_data(filename):
    """
    Load shopping data from a CSV file `filename` and convert into a list of
    evidence lists and a list of labels. Return a tuple (evidence, labels).

    evidence should be a list of lists, where each list contains the
    following values, in order:
        - Administrative, an integer
        - Administrative_Duration, a floating point number
        - Informational, an integer
        - Informational_Duration, a floating point number
        - ProductRelated, an integer
        - ProductRelated_Duration, a floating point number
        - BounceRates, a floating point number
        - ExitRates, a floating point number
        - PageValues, a floating point number
        - SpecialDay, a floating point number
        - Month, an index from 0 (January) to 11 (December)
        - OperatingSystems, an integer
        - Browser, an integer
        - Region, an integer
        - TrafficType, an integer
        - VisitorType, an integer 0 (not returning) or 1 (returning)
        - Weekend, an integer 0 (if false) or 1 (if true)

    labels should be the corresponding list of labels, where each label
    is 1 if Revenue is true, and 0 otherwise.
    """
    with open(filename) as f:
        reader = csv.DictReader(f)

        # All data structures needed 
        evidences = list()
        labels = list()
        
        # Loop through all rows of csv
        for row in reader:

            # Adjust requirements by converting csv values
            row["Administrative"] = int(row["Administrative"])
            row["Administrative_Duration"] = float(row["Administrative_Duration"])
            row["Informational"] = int(row["Informational"])
            row["Informational_Duration"] = float(row["Informational_Duration"])
            row["ProductRelated"] = int(row["ProductRelated"])
            row["ProductRelated_Duration"] = float(row["ProductRelated_Duration"])
            row["BounceRates"] = float(row["BounceRates"])
            row["ExitRates"] = float(row["ExitRates"])
            row["PageValues"] = float(row["PageValues"])
            row["SpecialDay"] = float(row["SpecialDay"])
            row["Month"] = convert_month(row["Month"])
            row["OperatingSystems"] = int(row["OperatingSystems"])
            row["Browser"] = int(row["Browser"])
            row["Region"] = int(row["Region"])
            row["TrafficType"] = int(row["TrafficType"])
            row["VisitorType"] = 1 if row["VisitorType"] == "Returning_Visitor" else 0
            row["Weekend"] = 0 if row["Weekend"] == "FALSE" else 1
            row["Revenue"] = 0 if row["Revenue"] == "FALSE" else 1

            # List of row evidence
            evidence = list()

            # Group evidences and labels in each row
            for key, value in row.items():

                # If value is label append it to labels list
                if key == "Revenue":
                    labels.append(value)
                # Else append one of evidence to evidence list
                else:
                    evidence.append(value)

            # Append list of evidence to evidences list
            evidences.append(evidence)

    return (evidences, labels)

def train_model(evidence, labels):
    """
    Given a list of evidence lists and a list of labels, return a
    fitted k-nearest neighbor model (k=1) trained on the data.
    """
    model = KNeighborsClassifier(n_neighbors=1)
    model.fit(evidence, labels)
    return model


def evaluate(labels, predictions):
    """
    Given a list of actual labels and a list of predicted labels,
    return a tuple (sensitivity, specificity).

    Assume each label is either a 1 (positive) or 0 (negative).

    `sensitivity` should be a floating-point value from 0 to 1
    representing the "true positive rate": the proportion of
    actual positive labels that were accurately identified.

    `specificity` should be a floating-point value from 0 to 1
    representing the "true negative rate": the proportion of
    actual negative labels that were accurately identified.
    """ 
    sensitivity = 0
    specificity = 0

    # Count actual positive labels and negative ones
    positive_count = 0
    negative_count = 0

    for label in labels:
        if label == 1:
            positive_count += 1
        else:
            negative_count += 1

    for actual, predicted in zip(labels, predictions):
        
        # If actual value is same as predicted by AI check if it is positive or negative label
        if actual == predicted:
            if actual == 1:
                sensitivity += 1
            else:
                specificity += 1

    sensitivity /= positive_count
    specificity /= negative_count

    return (sensitivity, specificity)
            


if __name__ == "__main__":
    main()
