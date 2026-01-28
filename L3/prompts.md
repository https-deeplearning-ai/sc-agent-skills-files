# Prompts 

## Part 1: Updating the Marketing Skill

- List the tables in BigQuery that exist
- Show me the schema of the table
- To update the skill:

    I want to update the `analyzing-marketing-campaign-csv` skill so that instead of expecting a CSV upload, it pulls data directly from BigQuery.
    It should include the information about the BigQuery table:
    -**Dataset:** `marketing` 
    - **Table:** `campaign_performance`
    - **Schema** SEE ABOVE

    **Requirements:**
    1. The user must specify which week to analyze (e.g., "Dec 9-15" or "2024-12-09 to 2024-12-15")
    2. Always filter by date range in the SQL query, never pull the entire table
    3. Keep all the same analysis logic (funnel metrics, efficiency metrics, budget reallocation rules)
    4. Keep the existing `references/budget_reallocation_rules.md` file

    The skill should instruct Claude on how to query the data, not hardcode the SQL. Make sure to follow best practices for skill creation.

## Part 2:  Creating the Brand Guideline Skill

Create a brand guidelines skill from these files so I can apply our branding to future presentations and documents.

## Part 3: Implementing the Entire Workflow

First, analyze my marketing data from BigQuery for the week December 16–22, 2024, so that I see how each channel is doing. 

Then, generate a presentation with 4 slides for CraftedWell: 
- Slide 1: Title Slide (Title: "Weekly Report", subtitle: week date range)
- Slide 2: Executive Summary with key findings
- Slide 3: Funnel Analysis table (CTR/CVR vs benchmarks) 
- Slide 4: Efficiency Analysis table (ROAS, CPA, Net Profit)

For slides 3 and 4, use native PowerPoint tables