"""Data profile of Sicily.csv  ->  Data_Profile_Sicily.xlsx
Run:  python data_profile.py  (set SICILY_CSV to the path of the raw file)"""
import os, re
import numpy as np, pandas as pd
from openpyxl import Workbook
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from openpyxl.utils import get_column_letter
from openpyxl.formatting.rule import CellIsRule, DataBarRule
from openpyxl.comments import Comment

SRC = os.environ.get("SICILY_CSV", "data/raw/Sicily.csv")
OUT = os.environ.get("PROFILE_OUT", "Data_Profile_Sicily.xlsx")
df = pd.read_csv(SRC, low_memory=False)
N, C = df.shape

USED = ["id","neighbourhood_cleansed","latitude","longitude","property_type","room_type","accommodates",
        "bathrooms_text","bedrooms","amenities","price","minimum_nights","number_of_reviews","review_scores_rating"]
DATE_COLS = ["last_scraped","calendar_last_scraped","first_review","last_review",
             "price_quote_checkin_date","price_quote_checkout_date"]
ID_COLS = ["id","scrape_id","host_id","host_profile_id"]
HOST_PERSONAL = ["host_id","host_url","host_profile_id","host_profile_url","host_name","host_picture_url",
                 "host_thumbnail_url","host_about","host_location","host_since","host_neighbourhood"]

price_num = pd.to_numeric(df["price"].astype(str).str.replace(r"[\$,]", "", regex=True), errors="coerce")

def friendly_dtype(s):
    d = str(s.dtype)
    return "object (text)" if d in ("str", "object", "string") else d

def logical_type(c, s):
    if s.isna().all(): return "Empty (100% missing)"
    if c in ID_COLS: return "Identifier"
    if c == "price": return "Currency (stored as text)"
    if c == "amenities": return "List (stored as text)"
    if c == "price_quote_raw": return "JSON (stored as text)"
    if c in DATE_COLS: return "Date (stored as text)"
    if s.dtype.kind in "if":
        return "Numeric (integer)" if s.dtype.kind == "i" or (s.dropna() % 1 == 0).all() else "Numeric (decimal)"
    vals = set(s.dropna().unique())
    if vals <= {"t", "f"}: return "Boolean (t/f as text)"
    if c.endswith("_url") or c == "picture_url": return "URL"
    nun = s.nunique()
    if nun <= 400 and nun / max(s.notna().sum(), 1) < 0.02: return "Category"
    return "Free text"

def fmt_top(s):
    vc = s.value_counts(dropna=True)
    if vc.empty or vc.iloc[0] == 1: return "—"
    v = str(vc.index[0]).replace("\n", " ")
    return f"{v[:38]}{'…' if len(v) > 38 else ''} ({vc.iloc[0]:,})"

def min_max(c, s):
    if c == "price": return price_num.min(), price_num.max()
    if c in ID_COLS: return str(int(s.min())), str(int(s.max()))      # 19-digit ids exceed Excel's 15-digit precision -> keep as text
    if c in DATE_COLS:
        d = pd.to_datetime(s, errors="coerce").dropna()
        return (d.min().strftime("%Y-%m-%d"), d.max().strftime("%Y-%m-%d")) if len(d) else ("—", "—")
    if s.dtype.kind in "if" and s.notna().any(): return s.min(), s.max()
    return "—", "—"

def mean_median(c, s):
    if c == "price": return price_num.mean(), price_num.median()
    if s.dtype.kind in "if" and s.notna().any() and c not in ID_COLS: return s.mean(), s.median()
    return None, None

# ---- facts used in notes / issues
n_zero_reviews = int((df.number_of_reviews == 0).sum())
rating_zero_ids = df.loc[df.review_scores_rating == 0, "id"].tolist()
mn_gt365 = int((df.minimum_nights > 365).sum())
empty_cols = [c for c in df.columns if df[c].isna().all()]
const_cols = [c for c in df.columns if df[c].nunique(dropna=True) == 1]
ppg = price_num / df["accommodates"]
bt = df["bathrooms_text"].dropna()
half_no_number = int((~bt.str.contains(r"\d")).sum())
dup_rows = int(df.duplicated().sum())

NOTES = {
 "id": "Primary key. All 56,873 values are unique (no duplicate listings).",
 "price": f"Stored as TEXT with $ and commas (e.g. \"$1,250.00\"); must be converted to a number. Min/Max shown after parsing. Extremes: max {price_num.max():,.2f}, min {price_num.min():,.2f}.",
 "bathrooms": "Numeric version already in the file but has far more gaps (8,847) than bathrooms_text (63).",
 "bathrooms_text": f"Text such as \"1 shared bath\". {half_no_number} values have no number (\"Half-bath\", \"Shared half-bath\"...).",
 "bedrooms": "15.0% missing; cannot be inferred from other columns.",
 "beds": "12.0% missing.",
 "amenities": "List stored as one text string (JSON-like); needs json.loads to count items. No missing values; 49 are empty lists (44 after dropping rows without a price).",
 "accommodates": "Number of guests. Used to compute price per guest = price / accommodates.",
 "minimum_nights": f"{mn_gt365} listings above 365 nights (long stays, not short-term rentals). 1 value missing.",
 "review_scores_rating": f"Missing exactly where the listing has no reviews ({n_zero_reviews:,} listings with number_of_reviews = 0). {len(rating_zero_ids)} listings have an invalid rating of 0.0 (ids {', '.join(map(str, rating_zero_ids))}); scale is 1–5.",
 "number_of_reviews": f"{n_zero_reviews:,} listings ({n_zero_reviews/N:.1%}) have 0 reviews.",
 "neighbourhood_cleansed": "372 areas. Name \"Cefal\" is truncated in the source file (probably Cefalù).",
 "latitude": f"Range {df.latitude.min():.2f} to {df.latitude.max():.2f}; consistent with Sicily and its islands (Lampedusa ≈ 35.5).",
 "longitude": f"Range {df.longitude.min():.2f} to {df.longitude.max():.2f}; consistent with Sicily and its islands.",
 "room_type": "4 values: Entire home/apt, Private room, Hotel room, Shared room.",
 "property_type": "99 values; top 10 cover most listings.",
 "scrape_id": "Constant value for every row: carries no information.",
 "last_scraped": "2 scrape dates only.",
 "price_quote_raw": "Raw JSON of a price quote; not needed for the price comparison.",
 "price_quote_price_per_night": "Quote for one sample stay; has 1 more missing value than price.",
 "estimated_revenue_l365d": "Missing for the same 5,009 listings that have no price.",
 "host_is_superhost": "Evaluative label about a host (t/f). Excluded: project does not profile hosts.",
}
rows = []
for c in df.columns:
    s = df[c]
    lt = logical_type(c, s)
    mn, mx = min_max(c, s)
    mean, med = mean_median(c, s)
    miss = int(s.isna().sum())
    note = NOTES.get(c, "")
    if lt.startswith("Empty"): note = "Column is completely empty: no usable information."
    elif c in HOST_PERSONAL and not note: note = "Host personal / identifying data; not needed for the project."
    elif lt.startswith("Boolean") and not note: note = "Values t / f stored as text."
    elif lt.startswith("URL") and not note: note = "Link; not needed for analysis."
    elif lt.startswith("Date") and not note: note = "Date stored as text; parse with pd.to_datetime if needed."
    rows.append(dict(col=c, dtype=friendly_dtype(s), logical=lt, miss=miss, uniq=int(s.nunique(dropna=True)),
                     mn=mn, mx=mx, mean=mean, med=med, top=fmt_top(s) if not lt.startswith("Empty") and lt not in ("List (stored as text)","JSON (stored as text)") else "—",
                     used="Yes" if c in USED else "No", note=note))

# ================= workbook =================
wb = Workbook()
AR = "Arial"
f_norm = Font(name=AR, size=10); f_bold = Font(name=AR, size=10, bold=True)
f_hdr = Font(name=AR, size=10, bold=True, color="FFFFFF"); f_title = Font(name=AR, size=14, bold=True, color="1F3864")
f_input = Font(name=AR, size=10, color="0000FF"); f_link = Font(name=AR, size=10, color="008000")
fill_hdr = PatternFill("solid", fgColor="1F3864"); fill_zebra = PatternFill("solid", fgColor="F3F6FB")
fill_used = PatternFill("solid", fgColor="E7F4EA"); fill_red = PatternFill("solid", fgColor="F8D7DA"); fill_amb = PatternFill("solid", fgColor="FFF4D6")
thin = Side(style="thin", color="C9D3E3"); box = Border(left=thin, right=thin, top=thin, bottom=thin)
wrap = Alignment(wrap_text=True, vertical="top"); center = Alignment(horizontal="center", vertical="top")

def header(ws, row, labels, widths=None):
    for i, l in enumerate(labels, 1):
        c = ws.cell(row=row, column=i, value=l); c.font = f_hdr; c.fill = fill_hdr; c.border = box
        c.alignment = Alignment(wrap_text=True, vertical="center", horizontal="center")
    if widths:
        for i, w in enumerate(widths, 1): ws.column_dimensions[get_column_letter(i)].width = w
    ws.row_dimensions[row].height = 30

# ---------- Sheet 1: Data Profile ----------
ws = wb.active; ws.title = "Data Profile"
ws["A1"] = "Data Profile – Sicily Airbnb listings (raw file Sicily.csv)"; ws["A1"].font = f_title
ws["A2"] = ("One row per column of the raw file (90 columns, 56,873 rows). Missing % = Missing Count ÷ total rows (Summary!B4). "
            "Min/Max are shown for numeric and date columns; \"—\" means not applicable. Mean/Median and Most Frequent are static values computed with pandas.")
ws["A2"].font = Font(name=AR, size=9, italic=True); ws["A2"].alignment = wrap; ws.merge_cells("A2:M2"); ws.row_dimensions[2].height = 28
HR = 4
labels = ["Column","Data Type","Logical Type","Missing Count","Missing %","Unique Values","Min","Max","Mean","Median","Most Frequent Value (count)","Used in Project","Notes"]
header(ws, HR, labels, [30,14,24,12,10,12,14,14,12,12,34,10,80])
first = HR + 1
for i, r in enumerate(rows):
    rr = first + i
    vals = [r["col"], r["dtype"], r["logical"], r["miss"], f"=D{rr}/Summary!$B$4", r["uniq"], r["mn"], r["mx"], r["mean"], r["med"], r["top"], r["used"], r["note"]]
    for j, v in enumerate(vals, 1):
        if isinstance(v, (np.integer,)): v = int(v)
        if isinstance(v, (np.floating,)): v = None if np.isnan(v) else float(v)
        c = ws.cell(row=rr, column=j, value=v); c.font = f_norm; c.border = box; c.alignment = wrap
        if i % 2 == 1: c.fill = fill_zebra
    ws.cell(row=rr, column=1).font = f_bold
    ws.cell(row=rr, column=4).number_format = "#,##0"; ws.cell(row=rr, column=5).number_format = "0.0%"
    ws.cell(row=rr, column=6).number_format = "#,##0"
    for col in (7, 8, 9, 10):
        c = ws.cell(row=rr, column=col)
        if isinstance(c.value, (int, float)): c.number_format = "#,##0.00" if not float(c.value).is_integer() else "#,##0"
        c.alignment = Alignment(horizontal="right", vertical="top")
    ws.cell(row=rr, column=12).alignment = center
    if r["used"] == "Yes": ws.cell(row=rr, column=12).fill = fill_used
last = first + len(rows) - 1
ws.conditional_formatting.add(f"E{first}:E{last}", CellIsRule(operator="greaterThanOrEqual", formula=["0.5"], fill=fill_red))
ws.conditional_formatting.add(f"E{first}:E{last}", CellIsRule(operator="between", formula=["0.1", "0.4999"], fill=fill_amb))
ws.freeze_panes = ws.cell(row=first, column=2); ws.auto_filter.ref = f"A{HR}:M{last}"
ws.cell(row=last + 2, column=1, value="Legend").font = f_bold
ws.cell(row=last + 3, column=1, value="Missing % ≥ 50%").fill = fill_red; ws.cell(row=last + 4, column=1, value="Missing % 10%–50%").fill = fill_amb
ws.cell(row=last + 5, column=1, value="Used in Project = Yes").fill = fill_used
for k in (3, 4, 5): ws.cell(row=last + k, column=1).font = f_norm
ws.cell(row=last + 6, column=1, value="Used in Project = the 14 columns kept in the cleaning log (column selection).").font = Font(name=AR, size=9, italic=True)
rng = lambda col: f"'Data Profile'!${col}${first}:${col}${last}"

# ---------- Sheet 2: Summary ----------
sm = wb.create_sheet("Summary")
sm["A1"] = "Dataset summary"; sm["A1"].font = f_title
header(sm, 3, ["Metric", "Value", "How it is obtained"], [46, 16, 80])
srows = [
 ("Total rows (listings)", N, "Input: row count of Sicily.csv (counted with pandas).", "input"),
 ("Total columns", f"=COUNTA({rng('A')})", "Number of rows in the Data Profile sheet.", "f"),
 ("Columns used in the project", f'=COUNTIF({rng("L")},"Yes")', "Column selection in the cleaning log (14 of 90).", "f"),
 ("Columns completely empty (100% missing)", f"=COUNTIF({rng('E')},1)", "Missing % = 100%.", "f"),
 ("Columns with more than 50% missing", f'=COUNTIF({rng("E")},">0.5")', "Includes the completely empty columns.", "f"),
 ("Columns with 10%–50% missing", f'=COUNTIFS({rng("E")},">=0.1",{rng("E")},"<=0.5")', "Between 10% and 50% inclusive.", "f"),
 ("Columns with no missing values", f"=COUNTIF({rng('E')},0)", "Missing count = 0.", "f"),
 ("Constant columns (1 unique value)", f"=COUNTIF({rng('F')},1)", "Same value in every row: no information.", "f"),
 ("Numeric columns (int64 + float64)", f'=COUNTIF({rng("B")},"int64")+COUNTIF({rng("B")},"float64")', "Data Type = int64 or float64 (includes completely empty ones, which pandas reads as float64).", "f"),
 ("Text columns (object)", f'=COUNTIF({rng("B")},"object (text)")', "Data Type = object (text).", "f"),
 ("Total missing cells", f"=SUM({rng('D')})", "Sum of Missing Count.", "f"),
 ("Total cells", "=B4*B5", "Rows × columns.", "f"),
 ("Overall missing %", "=B14/B15", "Missing cells ÷ total cells.", "f"),
 ("Duplicate listing ids", int(df["id"].duplicated().sum()), "Input: counted with pandas (id.duplicated().sum()).", "input"),
 ("Fully duplicated rows", dup_rows, "Input: counted with pandas (df.duplicated().sum()).", "input"),
 ("Listings with a price", int(price_num.notna().sum()), "Input: counted after converting price text to number.", "input"),
 ("Listings without a price (missing)", "=B4-B19", "Rows − listings with a price.", "f"),
 ("Share of listings without a price", "=B20/B4", "Missing price ÷ total rows.", "f"),
 ("Listings with 0 reviews", n_zero_reviews, "Input: counted with pandas (number_of_reviews == 0).", "input"),
 ("Share of listings with 0 reviews", "=B22/B4", "", "f"),
 ("Latitude range", f"{df.latitude.min():.2f} to {df.latitude.max():.2f}", "Input: min/max of latitude.", "input"),
 ("Longitude range", f"{df.longitude.min():.2f} to {df.longitude.max():.2f}", "Input: min/max of longitude.", "input"),
 ("Scrape dates (last_scraped)", " / ".join(sorted(df["last_scraped"].unique())), "Input: unique values of last_scraped.", "input"),
]
for i, (m, v, h, kind) in enumerate(srows):
    r = 4 + i
    sm.cell(row=r, column=1, value=m).font = f_norm
    c = sm.cell(row=r, column=2, value=v); c.font = f_input if kind == "input" else f_norm
    c.alignment = Alignment(horizontal="right"); sm.cell(row=r, column=3, value=h).font = Font(name=AR, size=9, italic=True)
    for col in (1, 2, 3): sm.cell(row=r, column=col).border = box
    if isinstance(v, str) and v.startswith("=") and ("/" in v) and ("B4" in v or "B14" in v or "B15" in v or "B20" in v or "B22" in v) and m.lower().startswith(("overall","share")):
        c.number_format = "0.0%"
    elif isinstance(v, (int, str)) and not (isinstance(v, str) and not v.startswith("=")): c.number_format = "#,##0"
sm.cell(row=4+len(srows)+1, column=1, value="Blue = input typed from pandas results; black = formula over the Data Profile sheet.").font = Font(name=AR, size=9, italic=True)

# ---------- Sheet 3: Numeric Stats ----------
ns = wb.create_sheet("Numeric Stats")
ns["A1"] = "Descriptive statistics of numeric columns (non-empty, identifiers excluded)"; ns["A1"].font = f_title
header(ns, 3, ["Column","Count (non-missing)","Mean","Std","Min","25%","Median (50%)","75%","Max"], [38,14,14,14,14,14,14,14,16])
num_cols = [c for c in df.columns if df[c].dtype.kind in "if" and df[c].notna().any() and c not in ID_COLS]
series = {c: df[c] for c in num_cols}; series["price (parsed from text)"] = price_num
r = 4
for c, s in series.items():
    d = s.describe()
    vals = [c, int(d["count"]), d["mean"], d["std"], d["min"], d["25%"], d["50%"], d["75%"], d["max"]]
    for j, v in enumerate(vals, 1):
        cell = ns.cell(row=r, column=j, value=(float(v) if j > 1 and not isinstance(v, int) else v)); cell.font = f_bold if j == 1 else f_norm; cell.border = box
        if j > 1: cell.number_format = "#,##0" if j == 2 else "#,##0.00"
        if r % 2 == 1: cell.fill = fill_zebra
    r += 1
ns.freeze_panes = "B4"
ns.cell(row=r + 1, column=1, value="Static values computed with pandas describe().").font = Font(name=AR, size=9, italic=True)

# ---------- Sheet 4: Category Counts ----------
cc = wb.create_sheet("Category Counts")
cc["A1"] = "Frequency of the main categorical columns"; cc["A1"].font = f_title
header(cc, 3, ["Column","Value","Count","% of all listings"], [28,42,12,16])
r = 4
for col, top in [("room_type", None), ("property_type", 15), ("neighbourhood_cleansed", 15), ("source", None), ("last_scraped", None)]:
    vc = df[col].value_counts(dropna=False)
    if top: vc = vc.head(top)
    for k, v in vc.items():
        vals = [col, "(missing)" if pd.isna(k) else str(k), int(v), f"=C{r}/Summary!$B$4"]
        for j, x in enumerate(vals, 1):
            cell = cc.cell(row=r, column=j, value=x); cell.font = f_bold if j == 1 else f_norm; cell.border = box
        cc.cell(row=r, column=3).number_format = "#,##0"; cc.cell(row=r, column=4).number_format = "0.0%"
        r += 1
    r += 1
cc.cell(row=r, column=1, value="property_type and neighbourhood_cleansed show only the 15 most frequent values (99 and 372 values in total).").font = Font(name=AR, size=9, italic=True)
cc.freeze_panes = "A4"

# ---------- Sheet 5: Issues Found ----------
isu = wb.create_sheet("Issues Found")
isu["A1"] = "Data quality issues found while profiling"; isu["A1"].font = f_title
header(isu, 3, ["#","Area","Finding","Evidence","Why it matters","Suggested handling","Where handled in cleaning log"], [5,18,46,48,42,42,28])
mn = lambda v: f"{v:,}"
issues = [
 ("Structure", f"{len(empty_cols)} columns are completely empty", ", ".join(empty_cols), "No information; waste space and can mislead summaries.", "Exclude from the working dataset.", "Column selection (A–C)"),
 ("Structure", "1 constant column", ", ".join(const_cols), "Same value in every row.", "Exclude.", "Column selection (C)"),
 ("Privacy", "Host-identifying and host-evaluating columns", "host_id, host_name, host_url, host_picture_url, host_about, host_is_superhost…", "Personal data not needed for a price study.", "Exclude.", "Column selection (A, B)"),
 ("Price", "price is stored as text with $ and commas", "Example: \"$262.00\"", "Cannot compute averages or compare as text.", "Remove $ and commas, convert to float.", "Step 2"),
 ("Price", f"{mn(int(price_num.isna().sum()))} listings have no price ({price_num.isna().mean():.1%})", f"Also missing: estimated_revenue_l365d ({mn(int(df.estimated_revenue_l365d.isna().sum()))})", "A listing without a price cannot be compared.", "Remove these rows.", "Step 3"),
 ("Price", "Extreme prices", f"max {price_num.max():,.2f} USD per night, min {price_num.min():,.2f}; price per guest up to {ppg.max():,.0f}", "Likely data-entry errors or special listings; distort averages.", "Flag with IQR rules instead of deleting.", "Steps 12–14"),
 ("Bathrooms", "bathrooms_text is text; numeric bathrooms has many gaps", f"bathrooms missing {mn(int(df.bathrooms.isna().sum()))} vs bathrooms_text missing {int(df.bathrooms_text.isna().sum())}; {half_no_number} values without a number (half-baths)", "Need a usable number of bathrooms.", "Extract number from text; half-bath = 0.5.", "Step 4"),
 ("Amenities", "amenities is one text string holding a list", "Example: [\"Hair dryer\", \"Coffee maker\", …]", "Cannot analyse directly.", "Parse with json.loads and count items.", "Step 5"),
 ("Missing", f"bedrooms missing in {mn(int(df.bedrooms.isna().sum()))} listings ({df.bedrooms.isna().mean():.1%})", f"beds missing {mn(int(df.beds.isna().sum()))}", "Many rows would be lost if removed; value cannot be inferred.", "Keep as NaN; exclude explicitly in size-based comparisons.", "Step 6"),
 ("Reviews", f"{mn(int(df.review_scores_rating.isna().sum()))} listings have no rating ({df.review_scores_rating.isna().mean():.1%})", f"Exactly the listings with 0 reviews ({mn(n_zero_reviews)}); every listing with at least one review has a rating", "A missing rating means \"not rated yet\", not a bad rating.", "Keep as NaN; never fill with 0.", "Step 8"),
 ("Reviews", "Invalid ratings", f"{len(rating_zero_ids)} listings with rating 0.0 (ids {', '.join(map(str, rating_zero_ids))}); scale is 1–5", "Out-of-range values.", "Set to NaN.", "Step 7"),
 ("Stay rules", "Very long minimum stays", f"{mn_gt365} listings with minimum_nights > 365 (max {int(df.minimum_nights.max())}); 1 missing", "Not short-term rentals; price not comparable.", "Add a flag column.", "Steps 9–10"),
 ("Location", "Coordinates inside the expected range", f"lat {df.latitude.min():.2f}–{df.latitude.max():.2f}, lon {df.longitude.min():.2f}–{df.longitude.max():.2f}", "Checks that all listings belong to Sicily and its islands.", "No action needed.", "Step 11"),
 ("Location", "Truncated area name", "neighbourhood_cleansed contains \"Cefal\" (probably Cefalù)", "Name is cut in the source; area-level tables show \"Cefal\".", "Report to data owner; not changed.", "Not covered"),
 ("Types", "Dates and booleans stored as text", "first_review, last_review, last_scraped… (text); host_is_superhost, has_availability… (t/f)", "Must be converted before date or logical operations.", "Convert only if the column is used.", "Not needed (columns excluded)"),
 ("Duplicates", "No duplicate listings", f"Duplicate ids: {int(df['id'].duplicated().sum())}; fully duplicated rows: {dup_rows}", "Duplicates would be counted twice.", "No action needed.", "Step 1"),
]
for i, (area, finding, evidence, why, action, where) in enumerate(issues, 1):
    r = 3 + i
    for j, v in enumerate([i, area, finding, evidence, why, action, where], 1):
        c = isu.cell(row=r, column=j, value=v); c.font = f_bold if j == 3 else f_norm; c.alignment = wrap; c.border = box
        if i % 2 == 0: c.fill = fill_zebra
isu.freeze_panes = "A4"

for w in wb.worksheets: w.sheet_view.showGridLines = False
wb.save(OUT); print("saved", OUT, "| rows profiled:", len(rows))
