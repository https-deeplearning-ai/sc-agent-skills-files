# Initial Conversation

## Part 1

I'm attaching my weekly campaign data that I'd like to analyze its performance.

INPUT DATA
The csv file has campaign performance across Facebook, Google, TikTok, and Email
Columns: date, campaign_Name, channel, segment, impressions, clicks, conversions, spend, revenue, orders.

DATA QUALITY
Check for any missing data or any anomalies.

FUNNEL ANALYSIS
For each channel compute these two metrics:

* CTR (Click Through Rate) = Clicks/Impressions
* CVR (Conversion Rate) = Conversions/Clicks

and compare them to these historical benchmarks:

Channel, CTR, CVR 
Facebook_Ads, 2.5%, 3.8%  
Google_Ads, 5.0%, 4.5%  
TikTok_Ads,  2.0%, 0.9%  
Email, 15.0%, 2.1%

## Part 2

EFFICIENCY ANALYSIS 
For each channel, compute these additional metrics: 

* ROAS (Return on Ad Spend) = Revenue/Spend
* CPA (Cost Per Acquisition) = Spend / Conversions
* Net profit = Revenue - Total Costs:
  - Total Costs = Spend  + (Orders × Shipping Cost) + (Revenue × Product Cost Percentage)
  - Assume Shipping Cost is 8 dollars on average per order, and Product Cost Percentage is 35%
  
and compare them to the targets:
Target ROAS: 4.0x minimum  
Max CPA: $50 
Net profit should be positive

OUTPUT FORMAT
* Table summarizing showing the metrics (columns) for each channel and indicating whether the ROAS are above the target ROAS, if CPA is below the MAX CPA and if net profit is positive

## Part 3
I've attached the best practices for budget reallocation, how should I reallocate my budget? I can shift up to $10k between channels, and limit increases to 15% per channel.
