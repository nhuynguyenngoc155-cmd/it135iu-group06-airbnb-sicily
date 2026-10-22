# it135iu-group06-airbnb-sicily

Data Science project - Airbnb Sicily

## Project Topic

Which listings on a room-rental platform are overpriced for their area?

## Dataset

The project uses the Sicily Airbnb Listings Dataset and review data from Inside Airbnb.

### Files used

- `listings.csv` - detailed Airbnb listing information.
- `reviews.csv` - review data used to create review summaries.

The data files are not included in this repository in accordance with Inside Airbnb's data policy.

## License and Data Policy

The Airbnb data used in this project is provided by Inside Airbnb and is licensed under the Creative Commons Attribution 4.0 International (CC BY 4.0) License.

According to the Inside Airbnb Data Policies:

- The data should be appropriately attributed and cited.
- The data should not be republished.
- Only the data needed for the project should be used.
- Data should be downloaded once rather than repeatedly when running analysis scripts.

For more information, please refer to:

- Inside Airbnb - Get the Data: https://insideairbnb.com/get-the-data/
- Inside Airbnb - Data Policies: https://insideairbnb.com/data-policies/
- Inside Airbnb - Data Requests: https://insideairbnb.com/data-requests/
- Creative Commons - CC BY 4.0: https://creativecommons.org/licenses/by/4.0/

## Project Notebook

The main notebook is:

`notebooks/D2_group06_notebook.ipynb`

The notebook includes the following main sections:

1. Data source, loading and column selection
2. Data profiling
3. Data cleaning
4. Data operations
5. Data analysis

The project also includes a data cleaning log:

`cleaning_log.ipynb`

## Requirements

The project uses the following Python libraries:

- pandas
- numpy
- matplotlib
- seaborn
- jupyter

To install the required libraries:

```bash
pip install -r requirements.txt
```

## Reproducibility

A random seed of 42 is used to make the results reproducible.
