# VAHAN Monthly Vehicle Sales by Motor Company

VAHAN (Vehicle Registration) data is published by the Ministry of Road Transport
at https://vahan.parivahan.gov.in/vahan4dashboard

## How to get monthly sales filtered by motor company

1. Go to https://vahan.parivahan.gov.in/vahan4dashboard
2. Select **"Comparative Report"** from the top menu
3. Under filters:
   - **Year**: select the target year (e.g. 2024–25)
   - **Month**: select the target month
   - **Maker**: type the company name (e.g. MARUTI, HYUNDAI, TATA, MAHINDRA)
   - **Vehicle Class**: leave as ALL or narrow to Cars / Two Wheelers etc.
4. Click **"Refresh"** — the table shows registrations for that maker

## Month-over-Month (MoM) comparison

- Select **two consecutive months** in the filter (the report supports a range)
- The table will show both months side by side with a % change column
- Alternatively export both months separately and compute:
  `MoM % = ((current_month - previous_month) / previous_month) * 100`

## Year-over-Year (YoY) comparison

- Use the **"Year Wise" tab** in the Comparative Report
- Select the same month across two financial years (e.g. April 2023 vs April 2024)
- The dashboard renders a bar chart and table with absolute and % difference

## MoM within a year (full year trend)

- Select **"Monthly Trend"** report type
- Set the full financial year range (April to March)
- Filter by Maker — the chart shows all 12 months for that OEM in one view

## Exporting data

- Click the **Excel icon** on the top-right of any report table to download as .xlsx
- The downloaded file includes maker, state, vehicle class, and count columns

## Notes

- Data reflects **registrations** (vehicles registered with RTO), not factory dispatches
- There is typically a 2–4 week lag before the current month appears
- VAHAN data excludes vehicles registered under temporary permits
