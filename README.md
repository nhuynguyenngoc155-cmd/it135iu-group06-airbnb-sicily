# it135iu-group06-airbnb-sicily

Data Science Project - Airbnb Sicily

## Project Topic

**Which listings on a room-rental platform are overpriced for their area?**

This project analyzes Airbnb listings in Sicily, Italy, to identify listings with potentially unusually high prices compared with similar listings in the same area.

## Dataset

The project uses the Sicily Airbnb Listings Dataset from Inside Airbnb.

### Files Used

The notebook uses two data files from Inside Airbnb. They are **not** included in this repository.

- `listings.csv` - the Detailed Listings file (90 columns, 56,873 listings). The notebook reads only the 14 columns needed for the price comparison.
- `reviews.csv` - the reviews file (one row per review, with `listing_id` and `date` only). It is used to add the number of reviews and the first and latest review date to each listing.

The notebook also reads three supporting files that are included in this repository:

- `Data_Profile.csv` - profile of the 90 original columns, displayed in the data profile section.
- `groups_below_thresholds.csv` - table used for Chart 1.
- `descriptive_price_distribution.csv` - table used for Chart 3.

### Data Source

- **Source:** Inside Airbnb
- **Snapshot date:** July 1-2, 2026
- **Download date:** September 27, 2026

The dataset is not included in this repository in accordance with Inside Airbnb's data policy. Users must obtain the dataset from the original source.

To download the data, go to https://insideairbnb.com/get-the-data/, find Sicily, and download:

1. **Detailed Listings** (`listings.csv.gz`). Unzip it to get `listings.csv`. Do not use the summary listings file: it has only about 19 columns and lacks columns the notebook needs, such as `amenities`, `bedrooms` and `bathrooms_text`.
2. **Reviews** (`reviews.csv`).

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

It contains the D2 part first and the D3 part after it, in one file.

**D2 part:**

1. Data source, loading and column selection
2. Merging the review table
3. Data profile
4. Data cleaning log
5. Loading data and rebuilding `df_clean`
6. Filtering
7. Group-by and aggregation
8. Sensitivity check
9. Key takeaways
10. Saving outputs

**D3 part:**

1. Decision question, user and success criteria
2. Loading `df_clean`
3. Descriptive statistics by area and room type
4. Expected price, price gap and flag status
5. Statistical relationship analysis
6. Charts
7. Licence, attribution and AI use
8. Session information

### Data Cleaning Log

The data cleaning log (column selection and 14 cleaning steps) is part of the notebook, in the D2 part, in the section **Data Cleaning Log**. There is no separate cleaning log notebook.

## Project Structure

```text
it135iu-group06-airbnb-sicily/
├── notebooks/
│   └── D3_Topic06_Triet_Huy_Doanh_Tan_Phuong_Nguyen_Thien.ipynb
├── Output_tables/                          # summary tables
├── Data_Profile.csv                        # read by the notebook
├── groups_below_thresholds.csv             # read by the notebook (Chart 1)
├── descriptive_price_distribution.csv      # read by the notebook (Chart 3)
├── listings.csv                            # NOT in the repository: download from Inside Airbnb
├── reviews.csv                             # NOT in the repository: download from Inside Airbnb
├── requirements.txt
└── README.md
```

`listings.csv` and `reviews.csv` appear in the tree only to show where to place them after downloading. They are not stored on GitHub.

## Requirements

The project uses Python and the libraries listed in `requirements.txt`.

To install the required libraries:

```bash
pip install -r requirements.txt
```

## How to Run

1. Clone or download the repository.
2. Download `listings.csv` and `reviews.csv` from Inside Airbnb (see Data Source) and place both files in the root folder of the repository, next to `Data_Profile.csv`.
3. Install the required libraries:

   ```bash
   pip install -r requirements.txt
   ```

4. Open the main notebook from the `notebooks/` directory.
5. Run all cells from beginning to end (Restart & Run All).

The notebook looks for `listings.csv` and `reviews.csv` in its working folder first and then one folder above it. To use another location, set the environment variable `PROJECT_ROOT`, or `LISTINGS_CSV` and `REVIEWS_CSV`. The first cell prints the paths it found. If it shows `exists: False`, the files are in the wrong place.

The chart cells read `groups_below_thresholds.csv` and `descriptive_price_distribution.csv` and write to `outputs/` relative to the folder the notebook is run from. Run the notebook with the repository root as the working folder (in VS Code, set `jupyter.notebookFileRoot` to `${workspaceFolder}`), or keep the notebook and the CSV files in the same folder.

The notebook saves generated files to `outputs/` (created automatically and not committed): summary tables in `outputs/tables/`, the table with one row per listing in `outputs/local/`, and the charts in `outputs/images/`.

The notebook also checks the reconstructed dataset against the cleaning log. It stops if the expected number of rows, columns, or flag counts do not match.

## Reproducibility

A random seed is not used. The notebook has no random sampling, train/test split or model fitting, so the results are the same on every run. The last cell of the notebook prints the library versions.

The notebook was run with Python 3.13.7, pandas 3.1.0, numpy 2.5.4 and matplotlib 3.11.2.

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
