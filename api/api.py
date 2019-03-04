import math


def validate_data(data):
    if not math.isnan(data):
        data = int(data)
        return data
    else:
        return 0


def check_columns(data):
    columns = data.columns.to_list()
    if(columns[0] != "Date" or len(columns) == 1):
        return 0
    for i in range(1, len(columns)):
        asset_name = ("Asset" + str(i))
        if(columns[i] != asset_name):
            return 0
        else:
            try:
                (data[asset_name]).apply(validate_data)
            except ValueError:
                return 0
    return 1


def check_null_data(data):
    null_data = []
    columns = data.columns.to_list()
    for i in range(1, len(columns)):
        null_dict = {}
        asset_name = ("Asset" + str(i))
        if(columns[i] != asset_name):
            return 0
        else:
            query = data.query(asset_name + ' != ' + asset_name)
            if not query.empty and not query["Date"].empty:
                query = query["Date"].to_list()
                query_list = [date.strftime("%m/%d/%y") for date in query]
                null_dict["asset" + str(i)] = query_list
                null_data.append(null_dict)
    return null_data
