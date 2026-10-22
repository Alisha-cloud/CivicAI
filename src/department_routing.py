CATEGORY_TO_DEPARTMENT = {
    "Water Supply": "Water Supply Department",
    "Electricity": "Electricity Department",
    "Roads & Infrastructure": "Public Works Department",
    "Waste Management": "Waste Management Department",
    "Sanitation": "Sanitation Department",
    "Public Transport": "Public Transport Department",
    "Street Lighting": "Electrical Maintenance Department",
    "Healthcare": "Public Health Department",
    "Public Safety": "Public Safety Department",
    "Environment": "Environment Department",
    "Housing": "Housing Department",
    "Government Services": "General Administration Department",
}

def route_department(category: str) -> str:
    return CATEGORY_TO_DEPARTMENT.get(category, "General Administration Department")
