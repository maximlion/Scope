import pandas as pd
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from .api import check_columns, check_null_data


class AcceptView(APIView):
    def post(self, request, format='csv'):
        aggregation = request.data['aggregation']
        data_dict = {
            "code": 1,
            "error": "Wrong format"
        }
        response = {"data": data_dict,
                    "status": status.HTTP_422_UNPROCESSABLE_ENTITY}
        df = pd.read_csv(request.data['data'], delimiter=",")
        if check_columns(df):
            try:
                df['Date'] = pd.to_datetime(df['Date'])
            except ValueError:
                return Response(response['data'], status=response['status'])
            start_date = df['Date'].iloc[0]
            end_date = df['Date'].iloc[-1]
            missing_dates = pd.date_range(start=start_date,
                                          end=end_date).difference(df['Date'])
            missing_dates = [date.date().strftime("%m/%d/%y")
                             for date in missing_dates]
            null_list = check_null_data(df)
            missing_assets = []
            if len(null_list) != 0:
                missing_assets = null_list
            if len(missing_dates) != 0:
                response['data']['code'] = 2
                response['data']['error'] = "Missing dates"
                response['data']['details'] = missing_dates
                return Response(response['data'], status=response['status'])
            if len(missing_assets) != 0:
                response['data']['code'] = 2
                response['data']['error'] = "Missing assets"
                response['data']['details'] = missing_assets
                return Response(response['data'], status=response['status'])
        else:
            return Response(response['data'], status=response['status'])
        if aggregation == "quarterly":
            # Use %W to stop the spillover from one week to another
            df['Range_identifier'] = df['Date'].dt.strftime('%W')
            df2 = df.set_index(["Date"]).resample('Q').sum()
            return Response(df2)
        elif aggregation == "monthly":
            df['Range_identifier'] = df['Date'].dt.strftime('%m')
        elif aggregation == "weekly":
            df['Range_identifier'] = df['Date'].dt.strftime('%W')
        elif aggregation == "yearly":
            df['Range_identifier'] = df['Date'].dt.strftime('%y')
        df['Year'] = df['Date'].dt.year
        df2 = df.groupby(['Year', 'Range_identifier']).sum()

        return Response(df2)
