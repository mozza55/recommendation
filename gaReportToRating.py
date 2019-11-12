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


def return_response_toDataFrame(response):
  """Parses and prints the Analytics Reporting API V4 response.
  Args:
    response: An Analytics Reporting API V4 response.
  """
  weblog = pd.DataFrame(columns=['shop_id','category','action','label','count'])
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
      weblog.loc[cnt] = [dimensions[0],dimensions[1],dimensions[2],dimensions[3],dateRangeValues[0]['values'][0]]
      cnt +=1
      """
      for header, dimension in zip(dimensionHeaders, dimensions):
        print(header + ': ' + dimension)
      for i, values in enumerate(dateRangeValues):
        #print('Date range: ' + str(i))
        for metricHeader, value in zip(metricHeaders, values.get('values')):
          print(metricHeader.get('name') + ': ' + value)
      """
  return weblog

def calculatgeLogRating(weblog):
  ratings = pd.DataFrame(columns=['shop_id','ch_id','rating'])
  cnt = 0
  for idx in weblog.index:
    try:
      ch_id= int(weblog.loc[idx,'label'])
    except ValueError:
      #print(weblog.loc[idx,'label'])
      continue
    ratings.loc[cnt,'ch_id'] = ch_id
    ratings.loc[cnt, 'shop_id'] = weblog.loc[idx,'shop_id']

    action = weblog.loc[idx,'action']
    if action == 'Contact icon Click':
      ratings.loc[cnt, 'rating'] =  2* float(weblog.loc[idx,'count'])
      if ratings.loc[cnt, 'rating'] > 3.5:
        ratings.loc[cnt, 'rating']=3.5
    elif action == 'Contract icon Click':
      ratings.loc[cnt, 'rating'] = 2 * float(weblog.loc[idx,'count'])
      if ratings.loc[cnt, 'rating'] > 3.5:
        ratings.loc[cnt, 'rating']=3.5
    elif action == 'View Details Click':
      ratings.loc[cnt, 'rating'] = 0.2 * float(weblog.loc[idx,'count'])
      if ratings.loc[cnt, 'rating'] > 2:
        ratings.loc[cnt, 'rating']=3
    cnt +=1
  ratings = ratings.groupby(['shop_id','ch_id'], as_index = False)['rating'].sum()
  #print(ratings)
  ratings.to_csv('./data/logRatings.csv',index=False)


def update_logRating():
  analytics = initialize_analyticsreporting()
  response = get_report(analytics)
  log = return_response_toDataFrame(response)
  calculatgeLogRating(log)

if __name__ == '__main__':
  update_logRating()
