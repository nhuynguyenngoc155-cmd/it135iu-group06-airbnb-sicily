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

## References

- Inside Airbnb. (n.d.). Get the Data. https://insideairbnb.com/get-the-data/
- Inside Airbnb. (n.d.). Data Policies. https://insideairbnb.com/data-policies/
- Inside Airbnb. (n.d.). Data Requests. https://insideairbnb.com/data-requests/
- Creative Commons. (n.d.). Attribution 4.0 International (CC BY 4.0). https://creativecommons.org/licenses/by/4.0/
