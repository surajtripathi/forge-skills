# VAHAN State-wise Vehicle Registration Breakdown

## How to get state-wise data

1. Go to https://vahan.parivahan.gov.in/vahan4dashboard
2. Select **"State/RTO Wise"** from the report menu
3. Apply filters:
   - **Year + Month** (or a date range)
   - **Maker**: filter to a specific OEM if needed
   - **Vehicle Class**: Cars, Two Wheelers, Three Wheelers, etc.
4. The table shows each state as a row with total registrations

## Drilling down to RTO level

- Click any **state row** to expand it to individual RTO offices
- Useful for understanding city-level demand (e.g. Delhi RTO vs Gurugram RTO)

## Comparing states MoM or YoY

- Apply the same state filter across two time periods and export both
- Compute % change per state:
  `MoM % = ((current - previous) / previous) * 100`

## Market share by state

VAHAN does not compute market share directly. To get OEM share in a state:
1. Pull total registrations for all makers in that state and month
2. Pull registrations for your target OEM in that state and month
3. `Share % = (OEM registrations / total registrations) * 100`

## Notes

- Some states (especially smaller UTs) have reporting delays up to 30 days
- RTO-level data can have gaps if the RTO has not synced to VAHAN centrally
- For bulk downloads select the Excel export; the API is not publicly documented
