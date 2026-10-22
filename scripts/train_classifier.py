from src.classification import train_classifier
if __name__ == "__main__":
    model = train_classifier(force=True)
    print("Baseline classifier trained and saved.")
    print(f"Model classes: {list(model.classes_)}")
