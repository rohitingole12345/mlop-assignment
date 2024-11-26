from fastapi import FastAPI, Query, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
import pandas as pd
import matplotlib.pyplot as plt
import os
import math

# Initialize FastAPI app
app = FastAPI()

# Load templates
templates = Jinja2Templates(directory="templates")

# Load the Iris dataset
iris_data = pd.read_csv("Iris.csv")  # Ensure the file path is correct

class IrisDataFilter:
    def __init__(self, data: pd.DataFrame):
        self.data = data

    def filter_by_species(self, species: str) -> pd.DataFrame:
        """Filter data based on the selected species."""
        if species:
            return self.data[self.data["Species"] == species]
        return self.data

@app.get("/", response_class=HTMLResponse)
def home(request: Request):
    """Serve the homepage."""
    return templates.TemplateResponse("index.html", {"request": request})

@app.get("/filter", response_class=HTMLResponse)
def filter_iris(
    request: Request,
    species: str = Query(None),
    page: int = Query(1),
    page_size: int = Query(10)
):
    """
    Filter Iris dataset based on species and visualize feature distribution.
    Includes paginated display of filtered data and graph.
    """
    # Filter data based on species
    filter_instance = IrisDataFilter(iris_data)
    filtered_data = filter_instance.filter_by_species(species)

    # Pagination logic
    total_records = len(filtered_data)
    total_pages = math.ceil(total_records / page_size)
    start_idx = (page - 1) * page_size
    end_idx = start_idx + page_size
    paginated_data = filtered_data.iloc[start_idx:end_idx]

    # Visualization logic (Graph for filtered data)
    image_path = f"static/{species}_features_distribution.png"
    os.makedirs("static", exist_ok=True)
    plt.figure(figsize=(12, 8))
    features = ["SepalLengthCm", "SepalWidthCm", "PetalLengthCm", "PetalWidthCm"]
    for i, feature in enumerate(features):
        plt.subplot(2, 2, i + 1)
        plt.hist(filtered_data[feature], bins=10, color="skyblue", edgecolor="black")
        plt.title(f"{feature} Distribution")
        plt.xlabel(feature)
        plt.ylabel("Frequency")
        plt.tight_layout()
    plt.savefig(image_path)
    plt.close()

    # Render paginated data to HTML
    return templates.TemplateResponse(
        "filter.html",
        {
            "request": request,
            "species": species or "All Species",
            "image_path": image_path,
            "paginated_data_html": paginated_data.to_html(index=False),
            "page": page,
            "page_size": page_size,
            "total_pages": total_pages,
        },
    )
