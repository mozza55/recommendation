"""Hello Analytics Reporting API V4."""

from googleapiclient.discovery import build
from oauth2client.service_account import ServiceAccountCredentials
import pandas as pd


SCOPES = ['https://www.googleapis.com/auth/analytics.readonly']
KEY_FILE_LOCATION = './omega-fabric-257807-0e78d8aa0187.json'
VIEW_ID = '204713676'


def initialize_analyticsreporting():
  """Initializes an Analytics Reporting API V4 service object.

  Returns:
    An authorized Analytics Reporting API V4 service object.
  """
  credentials = ServiceAccountCredentials.from_json_keyfile_name(
      KEY_FILE_LOCATION, SCOPES)

  # Build the service object.
  analytics = build('analyticsreporting', 'v4', credentials=credentials)

  return analytics


def get_report(analytics):
  """Queries the Analytics Reporting API V4.

  Args:
    analytics: An authorized Analytics Reporting API V4 service object.
  Returns:
    The Analytics Reporting API V4 response.
  """
  return analytics.reports().batchGet(
      body={
        'reportRequests': [
        {
          'viewId': VIEW_ID,
          'dateRanges': [{'startDate': '1daysAgo', 'endDate': 'today'}],
          'metrics': [{'expression': 'ga:totalEvents'}],
          'dimensions': [{'name': 'ga:dimension1'},
                         {"name": "ga:eventCategory"},
                         {"name": "ga:eventAction"},
                         {"name": "ga:eventLabel"}]
        }]
      }
  ).execute()


def print_response(response):
  """Parses and prints the Analytics Reporting API V4 response.
  Args:
    response: An Analytics Reporting API V4 response.
  """
  df = pd.DataFrame(columns=['shop_id','category','action','label','cnt'])
  cnt =0
  for report in response.get('reports', []):
    columnHeader = report.get('columnHeader', {})
    dimensionHeaders = columnHeader.get('dimensions', [])
    metricHeaders = columnHeader.get('metricHeader', {}).get('metricHeaderEntries', [])

    for row in report.get('data', {}).get('rows', []):
      dimensions = row.get('dimensions', [])
      dateRangeValues = row.get('metrics', [])
      #t = dateRangeValues[0].keys()
      #print(dateRangeValues[0]['values'][0])
      #df.loc[cnt] = [dimensions[0],dimensions[1],dimensions[2],dimensions[3]]
      df.loc[cnt] = [dimensions[0],dimensions[1],dimensions[2],dimensions[3],dateRangeValues[0]['values'][0]]
      cnt +=1
      """
      for header, dimension in zip(dimensionHeaders, dimensions):
        print(header + ': ' + dimension)
      for i, values in enumerate(dateRangeValues):
        #print('Date range: ' + str(i))
        for metricHeader, value in zip(metricHeaders, values.get('values')):
          print(metricHeader.get('name') + ': ' + value)
      """
  print(df)

def main():
  analytics = initialize_analyticsreporting()
  response = get_report(analytics)
  print_response(response)

if __name__ == '__main__':
  main()
