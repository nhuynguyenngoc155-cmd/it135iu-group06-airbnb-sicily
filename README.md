# it135iu-group06-airbnb-sicily

Data Science Project - Airbnb Sicily

## Project Topic

**Which listings on a room-rental platform are overpriced for their area?**

This project analyzes Airbnb listings in Sicily, Italy, to identify listings with potentially unusually high prices compared with similar listings in the same area.

## Dataset

The project uses the Sicily Airbnb Listings Dataset from Inside Airbnb.

### Files Used

- `Sicily.csv` - the input dataset used by the main analysis notebook.

### Data Source

- **Source:** Inside Airbnb
- **Snapshot date:** July 1–2, 2026
- **Download date:** September 27, 2026

The dataset is not included in this repository in accordance with Inside Airbnb's data policy. Users must obtain the dataset from the original source.

## License and Data Policy

### License

The data is licensed under a Creative Commons Attribution 4.0 International License (CC BY 4.0).

### Data Policies

Inside Airbnb is a mission-driven activist project that provides data to quantify the impact of short-term rentals on housing and residential communities and supports advocacy for policies that protect cities from the impacts of short-term rentals.

### Community Policies

When using Inside Airbnb data, the following policies should be followed:

- Only take the data you need.
- Do not scrape data from the site. If you would like to subscribe to the data directly, please contact Inside Airbnb.
- Do not republish the data.
- When writing data analysis scripts, download the data once rather than downloading it each time the analysis is run.
- Inside Airbnb data should be appropriately attributed and cited.
- Users are encouraged to consider how their use of the data can contribute to the mission of Inside Airbnb and local communities.
- Do good with the data.

### Free vs Archived Data Policy

The Inside Airbnb Free vs Archived Data Policy provides a reasonable amount of free data from the last 12 months to meet the immediate needs of its intended audience, including housing and community activists and journalists.

Other data may be archived and must be requested through an Archived Data Request.

### Archived Data Requests Policy

Requests for archived data are assessed based on:

- The amount of data requested across time and space.
- The intended use of the data.
- The identity of the requestor.

Requests for larger amounts of data, historical data, or uses outside the project's mission may be refused or may require payment to help sustain the project.

Where possible, archived data is available to housing and community activists and journalists.

### New Data Policy

Inside Airbnb aims to add more data over time. However, adding data depends on the project's capacity, demand for the data, strategic considerations, and opportunities to support its mission.

### New Data Requests

Due to limited resources, Inside Airbnb generally cannot respond to most requests to add data for new cities or other locations.

Exceptions may be considered when the requested data could result in meaningful change for residents and communities affected by Airbnb and short-term rentals. Such requests may come from residents, activists, or city administrators who are studying the impact of or regulating short-term rentals.

For other requests, commissioned data requests may be considered. These requests can add data to the project while also helping to sustain and support Inside Airbnb.

## Project Notebook

The main notebook is:

`notebooks/D3_Topic06_Triet_Huy_Doanh_Tan_Phuong_Nguyen_Thien.ipynb`

The notebook includes the following main sections:

1. Data loading and reconstruction of `df_clean`
2. Filtering
3. Group-by and aggregation
4. Sensitivity analysis
5. Expected price, price gap, and flag status
6. Statistical relationship analysis
7. Interpretation of results
8. Saving summary tables

The project also includes a data cleaning log:

`cleaning_log.ipynb`

## Project Structure

```text
it135iu-group06-airbnb-sicily/
├── notebooks/
│   └── D3_Topic06_Triet_Huy_Doanh_Tan_Phuong_Nguyen_Thien.ipynb
├── data/
│   └── raw/
│       └── Sicily.csv
├── outputs/
│   └── tables/
├── cleaning_log.ipynb
├── requirements.txt
└── README.md
```

## Requirements

The project uses Python and the libraries listed in `requirements.txt`.

To install the required libraries:

```bash
pip install -r requirements.txt
```

## How to Run

1. Clone or download the repository.
2. Place `Sicily.csv` in the `data/raw/` directory.
3. Install the required libraries:

   ```bash
   pip install -r requirements.txt
   ```

4. Open the main notebook from the `notebooks/` directory.
5. Run all cells from beginning to end.

The notebook reads the input dataset from `data/raw/Sicily.csv` by default and saves generated summary tables to `outputs/tables/`.

The notebook also checks the reconstructed dataset against the cleaning log. It stops if the expected number of rows, columns, or flag counts do not match.

## Reproducibility

A fixed random seed of 42 is used for reproducibility.

The notebook includes validation checks to ensure that the reconstructed dataset matches the cleaning log.

## Limitations

The analysis uses a single data snapshot. Advertised prices may differ from the actual prices paid by guests. Listings with missing prices were excluded, which may introduce bias.

The analysis identifies potentially unusually high-priced listings compared with similar listings. It does not prove that a listing is incorrectly priced.

The results describe statistical associations and do not establish causal relationships.

## References

- Inside Airbnb. (n.d.). Get the Data. https://insideairbnb.com/get-the-data/
- Inside Airbnb. (n.d.). Data Policies. https://insideairbnb.com/data-policies/
- Inside Airbnb. (n.d.). Data Requests. https://insideairbnb.com/data-requests/
- Creative Commons. (n.d.). Attribution 4.0 International (CC BY 4.0). https://creativecommons.org/licenses/by/4.0/
