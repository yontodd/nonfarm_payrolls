# nonfarm-payrolls

Uses the Bureau of Labor Statistics (BLS) API, pulls the most recent month's Nonfarm Payrolls report.

Latest update - May 10, 2021

## Inputs:
- Prior two months of headline data - to calculate revisions from most recent report
- Consensus estimate to compare headline nonfarm payrolls data to Street estimates

## Output:
- Table of most recent 12 months data (set in DataFrame)
- Text update from report:
  - Headline payrolls number and how it compared to consensus estimates
  - Revisions for prior two months

## To-dos:
- Update with other key data from the payrolls report, including:
  - Private payrolls
  - Manufacturing payrolls
  - Average hourly earnings
  - Average workweek
  - Unemployment rate
  - Participation rate
  - Employment-to-population ratio
