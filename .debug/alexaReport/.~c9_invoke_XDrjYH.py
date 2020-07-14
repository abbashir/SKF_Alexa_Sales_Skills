import json
import boto3
import pandas as pd
import datetime




# -----------------------Function for own library ------------------------------
def get_time_stamp():
    client = boto3.client('s3')
    path = 's3://erpalexa/TimeStamp.xlsx'
    df = pd.read_excel(path, header=None)
    return str((df.loc[1,0]))
def get_days_of_month(month, year):
    if(int(year) % 4) == 0:
        if month == "01":
            return 31
        elif month == "02":
            return 29
        elif month == "03":
            return 31
        elif month == "04":
            return 30
        elif month == "05":
            return 31
        elif month == "06":
            return 30
        elif month == "07":
            return 31
        elif month == "08":
            return 31
        elif month == "09":
            return 30
        elif month == "10":
            return 31
        elif month == "11":
            return 30
        elif month == "12":
            return 31
    else:
        if month == "01":
            return 31
        elif month == "02":
            return 28
        elif month == "03":
            return 31
        elif month == "04":
            return 30
        elif month == "05":
            return 31
        elif month == "06":
            return 30
        elif month == "07":
            return 31
        elif month == "08":
            return 31
        elif month == "09":
            return 30
        elif month == "10":
            return 31
        elif month == "11":
            return 30
        elif month == "12":
            return 31
def get_year(year):
    if year == "2017":
        return 201700
    elif year == "2018":
        return 201800
    elif year == "2019":
        return 201900
    elif year == "2020":
        return 202000
    elif year == "2021":
        return 202100
    elif year == "2022":
        return 202200
def get_month(month):
    if month == "01":
        return 1
    elif month == "02":
        return 2
    elif month == "03":
        return 3
    elif month == "04":
        return 4
    elif month == "05":
        return 5
    elif month == "06":
        return 6
    elif month == "07":
        return 7
    elif month == "08":
        return 8
    elif month == "09":
        return 9
    elif month == "10":
        return 10
    elif month == "11":
        return 11
    elif month == "12":
        return 12
def get_unit(value):
    if value >= 10000000:
        string = str(value)
        unit = str(string[0:len(string) - 7] + " crore " + string[len(string) - 7:len(string) - 5] + " lakh " + string[
                                                                                                                len(
                                                                                                                    string) - 5:len(
                                                                                                                    string) - 3] + " thousand")
        return unit
    elif value >= 100000:
        string = str(value)
        unit = str(
            string[0:len(string) - 5] + " lakh " + string[len(string) - 5:len(string) - 3] + " thousand")
        return unit
    elif value >= 1000:
        string = str(value)
        unit = str(string[0:len(string) - 3] + " thousand")
        return unit
    else:
        return (value)
# ------------------------------Global Variables -------------------------------
startTime = 9
now = datetime.datetime.now()
currentTime = (int(str(now.strftime('%H:%M:%S'))[0:2])) + 7
endTime = 21
format = '%H:%M:%S'
salesDuration = currentTime - startTime
salesHour = endTime - startTime
trendTime = (salesHour / salesDuration)
year = str(pd.datetime.today())[0:4]
month = str(pd.datetime.today())[5:7]
yearmonth = get_year(year) + get_month(month)
days = get_days_of_month(month,year)
today = int(datetime.datetime.today().day)
# ---------------------Function that returns data from excel -------------------
# # Branch Name
# def get_branch_name(intentname):
#     name = intentname
#     sname = name[0:6]
#     client = boto3.client('s3')
#     path = 's3://erpalexa/Branch.xlsx'
#     data = pd.read_excel(path)
#     rows = data['skf'].tolist()
#     y = rows.index(sname)
#     branch = data.iloc[y, 2]
#     return branch

# Sales - Live
def get_sales():
    client = boto3.client('s3')
    path = 's3://erpalexa/BranchSales.xlsx'
    data = pd.read_excel(path)
    sales = data['sales'].sum()
    return sales

# Sales - MTD
def get_mtd_sales():
    global yearmonth
    client = boto3.client('s3')
    path = 's3://erpalexa/NSM' + str(yearmonth) + 'Sales.xlsx'
    data = pd.read_excel(path)
    sales = data['sales'].sum()
    return sales

# Sales - YTD
def get_ytd_sales():
    global year
    client = boto3.client('s3')
    path = 's3://erpalexa/Branch' + str(year) + 'Sales.xlsx'
    data = pd.read_excel(path)
    sales = data['sales'].sum()
    return sales

# Sales - Branch wise
def get_branch_sales(branch):
    client = boto3.client('s3')
    path = 's3://erpalexa/BranchSales.xlsx'
    data = pd.read_excel(path)
    sales = data.loc[data.branch == branch, "sales"].sum()
    return sales

# Sales - MTD wise
def get_branch_mtd_sales(branch):
    global yearmonth
    client = boto3.client('s3')
    path = 's3://erpalexa/Branch' + str(yearmonth) + 'Sales.xlsx'
    data = pd.read_excel(path)
    sales = data.loc[data.branch == branch, "sales"].sum()
    return sales

# Sales - YTD Sales
def get_branch_ytd_sales(branch):
    global year
    client = boto3.client('s3')
    path = 's3://erpalexa/Branch' + str(year) + 'Sales.xlsx'
    data = pd.read_excel(path)
    sales = data.loc[data.branch == branch, "sales"].sum()
    return sales

# Sales - Brand wise
def get_brand_sales(brand):
    client = boto3.client('s3')
    path = 's3://erpalexa/BranchSales.xlsx'
    data = pd.read_excel(path)
    sales = data.loc[data.brand == brand, "sales"].sum()
    return sales

# Sales - Branch & Brand wise sales
def get_branch_brand_sales(branch, brand):
    client = boto3.client('s3')
    path = 's3://erpalexa/BranchSales.xlsx'
    data = pd.read_excel(path)
    sales = data.loc[(data['branch'] == branch) & (data['brand'] == brand), "sales"].sum()
    return sales

# Sales - Branch & YearMonth Wise Sales
def get_branch_month_sales(branch, year_month):
    date = year_month
    yearmonth = int(date)
    client = boto3.client('s3')
    path = 's3://erpalexa/Branch' + str(date) + 'Sales.xlsx'
    data = pd.read_excel(path)
    sales = data.loc[data.branch == branch, "sales"].sum()
    return sales

# Sales - Brand & YearMonth Wise Sales
def get_brand_month_sales(brand, year_month):
    date = year_month
    yearmonth = int(date)
    client = boto3.client('s3')
    path = 's3://erpalexa/Branch' + str(date) + 'Sales.xlsx'
    data = pd.read_excel(path)
    sales = data.loc[data.brand == brand, "sales"].sum()
    return sales

# Sales - Branch, Brand & YearMonth Wise sales
def get_branch_brand_month_sales(branch, brand, year_month):
    date = year_month
    yearmonth = int(date)
    client = boto3.client('s3')
    path = 's3://erpalexa/Branch' + str(date) + 'Sales.xlsx'
    data = pd.read_excel(path)
    sales = data.loc[(data['branch'] == branch) & (data['brand'] == brand), "sales"].sum()
    return sales

# Sales - NSM wise
def get_nsm_sales(nsmid):
    client = boto3.client('s3')
    path = 's3://erpalexa/NSMSales.xlsx'
    data = pd.read_excel(path)
    sales = data.loc[data.nsmid == nsmid, "sales"].sum()
    return sales

# Sales - NSM MTD sales
def get_nsm_mtd_sales(nsmid):
    global yearmonth
    client = boto3.client('s3')
    path = 's3://erpalexa/NSM' + str(yearmonth) + 'Sales.xlsx'
    data = pd.read_excel(path)
    sales = data.loc[data.nsmid == nsmid, "sales"].sum()
    return sales

# Sales - NSM YTD sales
def get_nsm_ytd_sales(nsmid):
    global yearmonth
    client = boto3.client('s3')
    path = 's3://erpalexa/NSM' + str(year) + 'Sales.xlsx'
    data = pd.read_excel(path)
    sales = data.loc[data.nsmid == nsmid, "sales"].sum()
    return sales

# Sales - NSM & YearMonth Wise
def get_nsm_month_sales(nsmid, year_month):
    date = year_month
    yearmonth = int(date)
    client = boto3.client('s3')
    path = 's3://erpalexa/NSM' + str(date) + 'Sales.xlsx'
    data = pd.read_excel(path)
    sales = data.loc[data.nsmid == nsmid, "sales"].sum()
    return sales

# Sales - NSM & Brand wise sales
def get_nsm_brand_sales(nsmid, brand):
    client = boto3.client('s3')
    path = 's3://erpalexa/NSMSales.xlsx'
    data = pd.read_excel(path)
    sales = data.loc[(data['nsmid'] == nsmid) & (data['brand'] == brand), "sales"].sum()
    return sales

# Sales - NSM & Brand MTD sales
def get_nsm_brand_mtd_sales(nsmid, brand):
    global yearmonth
    client = boto3.client('s3')
    path = 's3://erpalexa/NSM' + str(yearmonth) + 'Sales.xlsx'
    data = pd.read_excel(path)
    sales = data.loc[(data['nsmid'] == nsmid) & (data['brand'] == brand), "sales"].sum()
    return sales

# Sales - NSM & Brand YTD sales
def get_nsm_brand_ytd_sales(nsmid, brand):
    global year
    client = boto3.client('s3')
    path = 's3://erpalexa/NSM' + str(year) + 'Sales.xlsx'
    data = pd.read_excel(path)
    sales = data.loc[(data['nsmid'] == nsmid) & (data['brand'] == brand), "sales"].sum()
    return sales

# Sales - NSM , Brand & YearMonth Wise Sales
def get_nsm_brand_month_sales(nsmid, brand, year_month):
    date = year_month
    yearmonth = int(date)
    client = boto3.client('s3')
    path = 's3://erpalexa/NSM' + str(date) + 'Sales.xlsx'
    data = pd.read_excel(path)
    sales = data.loc[(data['nsmid'] == nsmid) & (data['brand'] == brand), "sales"].sum()
    return sales

# Sales - RSM wise
def get_rsm_sales(rsmid):
    client = boto3.client('s3')
    path = 's3://erpalexa/RSMSales.xlsx'
    data = pd.read_excel(path)
    sales = data.loc[data.rsmid == rsmid, "sales"].sum()
    return sales

# Sales - RSM MTD sales
def get_rsm_mtd_sales(rsmid):
    global yearmonth
    client = boto3.client('s3')
    path = 's3://erpalexa/RSM' + str(yearmonth) + 'Sales.xlsx'
    data = pd.read_excel(path)
    sales = data.loc[data.rsmid == rsmid, "sales"].sum()
    return sales

# Sales - RSM YTD sales
def get_rsm_ytd_sales(rsmid):
    global year
    client = boto3.client('s3')
    path = 's3://erpalexa/RSM' + str(year) + 'Sales.xlsx'
    data = pd.read_excel(path)
    sales = data.loc[data.rsmid == rsmid, "sales"].sum()
    return sales

# Sales - RSM & YearMonth Wise Sales
def get_rsm_month_sales(rsmid, year_month):
    date = year_month
    yearmonth = int(date)
    client = boto3.client('s3')
    path = 's3://erpalexa/RSM' + str(date) + 'Sales.xlsx'
    data = pd.read_excel(path)
    sales = data.loc[data.rsmid == rsmid, "sales"].sum()
    return sales

# Sales - RSM & Brand wise sales
def get_rsm_brand_sales(rsmid, brand):
    client = boto3.client('s3')
    path = 's3://erpalexa/RSMSales.xlsx'
    data = pd.read_excel(path)
    sales = data.loc[(data['rsmid'] == rsmid) & (data['brand'] == brand), "sales"].sum()
    return sales

# Sales - RSM & Brand MTD sales
def get_rsm_brand_mtd_sales(rsmid, brand):
    global yearmonth
    client = boto3.client('s3')
    path = 's3://erpalexa/RSM' + str(yearmonth) + 'Sales.xlsx'
    data = pd.read_excel(path)
    sales = data.loc[(data['rsmid'] == rsmid) & (data['brand'] == brand), "sales"].sum()
    return sales

# Sales - RSM & Brand YTD sales
def get_rsm_brand_ytd_sales(rsmid, brand):
    global year
    client = boto3.client('s3')
    path = 's3://erpalexa/RSM' + str(year) + 'Sales.xlsx'
    data = pd.read_excel(path)
    sales = data.loc[(data['rsmid'] == rsmid) & (data['brand'] == brand), "sales"].sum()
    return sales

# Sales - RSM , Brand & YearMonth Wise Sales
def get_rsm_brand_month_sales(rsmid, brand, year_month):
    date = year_month
    yearmonth = int(date)
    client = boto3.client('s3')
    path = 's3://erpalexa/RSM' + str(date) + 'Sales.xlsx'
    data = pd.read_excel(path)
    sales = data.loc[(data['rsmid'] == rsmid) & (data['brand'] == brand), "sales"].sum()
    return sales

# Sales - FM wise
def get_fm_sales(fmid):
    client = boto3.client('s3')
    path = 's3://erpalexa/FMSales.xlsx'
    data = pd.read_excel(path)
    sales = data.loc[data.fmid == fmid, "sales"].sum()
    return sales

# Sales - FM MTD sales
def get_fm_mtd_sales(fmid):
    global yearmonth
    client = boto3.client('s3')
    path = 's3://erpalexa/FM' + str(yearmonth) + 'Sales.xlsx'
    data = pd.read_excel(path)
    sales = data.loc[data.fmid == fmid, "sales"].sum()
    return sales

# Sales - FM YTD sales
def get_fm_ytd_sales(fmid):
    global year
    client = boto3.client('s3')
    path = 's3://erpalexa/FM' + str(year) + 'Sales.xlsx'
    data = pd.read_excel(path)
    sales = data.loc[data.fmid == fmid, "sales"].sum()
    return sales

# Sales - FM & YearMonth Wise Sales
def get_fm_month_sales(fmid, year_month):
    date = year_month
    yearmonth = int(date)
    client = boto3.client('s3')
    path = 's3://erpalexa/FM' + str(date) + 'Sales.xlsx'
    data = pd.read_excel(path)
    sales = data.loc[data.fmid == fmid, "sales"].sum()
    return sales

# Sales - FM & Brand wise sales
def get_fm_brand_sales(fmid, brand):
    client = boto3.client('s3')
    path = 's3://erpalexa/FMSales.xlsx'
    data = pd.read_excel(path)
    sales = data.loc[(data['fmid'] == fmid) & (data['brand'] == brand), "sales"].sum()
    return sales

# Sales - FM & Brand mtd sales
def get_fm_brand_mtd_sales(fmid, brand):
    global yearmonth
    client = boto3.client('s3')
    path = 's3://erpalexa/FM' + str(yearmonth) + 'Sales.xlsx'
    data = pd.read_excel(path)
    sales = data.loc[(data['fmid'] == fmid) & (data['brand'] == brand), "sales"].sum()
    return sales

# Sales - FM & Brand ytd sales
def get_fm_brand_ytd_sales(fmid, brand):
    global year
    client = boto3.client('s3')
    path = 's3://erpalexa/FM' + str(year) + 'Sales.xlsx'
    data = pd.read_excel(path)
    sales = data.loc[(data['fmid'] == fmid) & (data['brand'] == brand), "sales"].sum()
    return sales

# Sales - FM , Brand & YearMonth Wise Sales
def get_fm_brand_month_sales(fmid, brand, year_month):
    date = year_month
    yearmonth = int(date)
    client = boto3.client('s3')
    path = 's3://erpalexa/RSM' + str(date) + 'Sales.xlsx'
    data = pd.read_excel(path)
    sales = data.loc[(data['fmid'] == fmid) & (data['brand'] == brand), "sales"].sum()
    return sales

# Stock - Branch wise
def get_branch_stock(branch):
    client = boto3.client('s3')
    path = 's3://erpalexa/Stock.xlsx'
    data = pd.read_excel(path)
    rows = data['branch'].tolist()
    y = rows.index(branch)
    stock = data.iloc[y, 2]
    return stock

# Outstanding - All Branch
def get_outstanding():
    client = boto3.client('s3')
    path = 's3://erpalexa/BranchOutstanding.xlsx'
    data = pd.read_excel(path)
    sales = data['outstanding'].sum()
    return sales

# Outstanding - Branch wise
def get_branch_outstanding(branch):
    client = boto3.client('s3')
    path = 's3://erpalexa/BranchOutstanding.xlsx'
    data = pd.read_excel(path)
    sales = data.loc[data.branch == branch, "outstanding"].sum()
    return sales

# Traget - All Branches Monthly
def get_mTarget():
    global yearmonth
    path = 's3://erpalexa/BranchTarget.xlsx'
    data = pd.read_excel(path)
    target = int(data.loc[data['yearmonth'] == yearmonth, "target"].sum())
    return target

# Traget - Branches Monthly
def get_branch_mTarget(branch):
    global yearmonth
    path = 's3://erpalexa/BranchTarget.xlsx'
    data = pd.read_excel(path)
    mTarget = int(data.loc[(data['branch'] == branch) & (data['yearmonth'] == yearmonth), "target"].sum())
    return mTarget

# Traget - Branches yearly
def get_branch_yTarget(branch):
    global year
    path = 's3://erpalexa/BranchTarget.xlsx'
    data = pd.read_excel(path)
    yTarget = int(data.loc[(data['branch'] == branch) & (data['yearmonth'] >= get_year(year)), "target"].sum())
    return yTarget

# Traget - NSM Monthly
def get_nsm_mTarget(nsmid):
    global yearmonth
    path = 's3://erpalexa/FieldForce.xlsx'
    data = pd.read_excel(path)
    mTarget = int(data.loc[(data['nsmid'] == nsmid) & (data['yearmonth'] == yearmonth), "target"].sum())
    return mTarget

# Traget - NSM yearly
def get_nsm_yTarget(nsmid):
    global year
    path = 's3://erpalexa/FieldForce.xlsx'
    data = pd.read_excel(path)
    yTarget = int(data.loc[(data['nsmid'] == nsmid) & (data['yearmonth'] >= get_year(year)), "target"].sum())
    return yTarget

# Traget - RSM Monthly
def get_rsm_mTarget(rsmid):
    global yearmonth
    path = 's3://erpalexa/FieldForce.xlsx'
    data = pd.read_excel(path)
    mTarget = int(data.loc[(data['rsmid'] == rsmid) & (data['yearmonth'] == yearmonth), "target"].sum())
    return mTarget

# Traget - RSM yearly
def get_rsm_yTarget(rsmid):
    global year
    path = 's3://erpalexa/FieldForce.xlsx'
    data = pd.read_excel(path)
    yTarget = int(data.loc[(data['rsmid'] == rsmid) & (data['yearmonth'] >= get_year(year)), "target"].sum())
    return yTarget

# Traget - FM Monthly
def get_fm_mTarget(fmid):
    global yearmonth
    path = 's3://erpalexa/FieldForce.xlsx'
    data = pd.read_excel(path)
    mTarget = int(data.loc[(data['fmid'] == fmid) & (data['yearmonth'] == yearmonth), "target"].sum())
    return mTarget

# Traget - FM yearly
def get_fm_yTarget(fmid):
    global year
    path = 's3://erpalexa/FieldForce.xlsx'
    data = pd.read_excel(path)
    yTarget = int(data.loc[(data['fmid'] == fmid) & (data['yearmonth'] >= get_year(year)), "target"].sum())
    return yTarget

# --------------- Helpers that build all of the responses ----------------------

def build_speechlet_response(title, output, reprompt_text, should_end_session):
    return {
        'outputSpeech': {
            'type': 'PlainText',
            'text': output
        },
        'card': {
            'type': 'Simple',
            'title': "AI Report- " + title,
            'content': "Alexa- " + output
        },
        'reprompt': {
            'outputSpeech': {
                'type': 'PlainText',
                'text': reprompt_text
            }
        },
        'shouldEndSession': should_end_session
    }
def build_response(session_attributes, speechlet_response):
    return {
        'version': '1.0',
        'sessionAttributes': session_attributes,
        'response': speechlet_response
    }

# --------------- Functions that control the skill's behavior ------------------

# Sales - Total Sales
def sales_intent_response():
    """ An example of a custom intent. Same structure as welcome message, just make sure to add this intent
    in your alexa skill in order for it to work.
    """
    global days, trendTime, salesDuration, currentTime
    sales = get_sales()
    mTarget = get_mTarget()
    
    dTarget = int(mTarget / days)
    trend = int(sales * trendTime)
    achievement = int((sales / dTarget) * 100)
    trendAchievement = int((trend / dTarget) * 100)
    
   # print("mTarget",mTarget,"dTarget",dTarget,"trend",trend,"achievement",achievement,"trendAchievement",trendAchievement)

    session_attributes = {}
    card_title = "Live Sales"
    speech_output = "Your today's sales as of "+str(get_time_stamp())+" in TDCL Nation wide is " + str(
        get_unit(sales)) + " taka . \n \n \n . . . . . . . . . . . . .. . . .  " \
                          "Today's sales target is " + str(
        get_unit(dTarget)) + " taka . . . . . . . . . . . . \n \n \n.. . . . . . . ." \
                             "Today's sales trend is " + str(
        get_unit(trend)) + " taka. . . . . . . .   .. . . . . .\n \n \n .. . . . . ." \
                          "Today's achievement till now is " + str(
        achievement) + " % . . . . .  .  . . . . . . .. \n \n \n. . . . . . ..  " \
                      "Today's achievement according to trend will be " + str(trendAchievement) + " % ."
    reprompt_text = "if you want to know more you can say month to date sales , year to date sales etc."
    should_end_session = False
    return build_response(session_attributes, build_speechlet_response(
        card_title, speech_output, reprompt_text, should_end_session))

# Sales - MTD Sales
def mtd_sales_intent_response():
    """ An example of a custom intent. Same structure as welcome message, just make sure to add this intent
    in your alexa skill in order for it to work.
    """
    global days, trendTime, salesDuration, currentTime, today
    sales = get_mtd_sales()
    mTarget = get_mTarget()
    trend = int((sales / today) * days)
    achievement = int((sales / mTarget) * 100)
    trendAchievement = int((trend / mTarget) * 100)

    session_attributes = {}
    card_title = "Month to Date Sales"
    speech_output = "Your Month to Date sales as of "+str(get_time_stamp())+" in TDCL Nation wide branch is " + str(
        get_unit(sales)) + " taka . \n \n \n . . . . . . . . . . . . .. . . . .. . " \
                           "Month end sales target is " + str(
        get_unit(mTarget)) + " taka .  \n \n \n . . . . . . . . . . . . .. . . .  .. .  ." \
                             "Month to Date sales trend is " + str(
        get_unit(trend)) + " taka. \n \n \n . . . . . . . . . . . . .. . . .  . . . .. . . . . .. . . . " \
                           "Month to Date achievement till now is " + str(
        achievement) + " %  \n \n \n . . . . . . . . . . . . .. . . . . . . . . .. . . . . . " \
                       "Month to Date achievement according to trend will be " + str(trendAchievement) + " % ."
    reprompt_text = "if you want to know more you can say live sales , year to date sales etc."
    should_end_session = False
    return build_response(session_attributes, build_speechlet_response(
        card_title, speech_output, reprompt_text, should_end_session))

# Sales - YTD Sales
def ytd_sales_intent_response():
    """ An example of a custom intent. Same structure as welcome message, just make sure to add this intent
    in your alexa skill in order for it to work.
    """
    global days, trendTime, salesDuration, currentTime, today
    sales = get_ytd_sales()

    session_attributes = {}
    card_title = "Year to Date Sales"
    speech_output = "Your Year to Date sales as of "+str(get_time_stamp())+" in TDCL Nation wide is " + str(get_unit(sales)) + " taka . . . . . . . "
    reprompt_text = "if you want to know more you can say live sales , month to date sales etc."
    should_end_session = False
    return build_response(session_attributes, build_speechlet_response(
        card_title, speech_output, reprompt_text, should_end_session))

# Sales - Branch wise
def branch_sales_intent_response(intent):
    """ An example of a custom intent. Same structure as welcome message, just make sure to add this intent
    in your alexa skill in order for it to work.
    """
    global days, trendTime

    branch = intent['slots']['branch']['resolutions']['resolutionsPerAuthority'][0]['values'][0]['value']['id']
    branch_name = intent['slots']['branch']['resolutions']['resolutionsPerAuthority'][0]['values'][0]['value']['name']
    sales = get_branch_sales(branch)
    mTarget = get_branch_mTarget(branch)
    dTarget = int(mTarget / days)
    trend = int(sales * trendTime)
    achievement = int((sales / dTarget) * 100)
    trendAchievement = int((trend / dTarget) * 100)

    session_attributes = {}
    card_title = "Branch Sales"
    speech_output = "Your today's total sales in " + branch_name + " branch as of "+str(get_time_stamp())+" is " + str(
        get_unit(sales)) + " taka . \n \n \n . . . . . . . . . . . . .. . . .  . . . . ." \
                           "Today's " + branch_name + " sales target is " + str(
        get_unit(dTarget)) + " taka . \n \n \n . . . . . . . . . . . . .. . . .  . . . . . ." \
                             "Today's " + branch_name + " sales trend is " + str(get_unit(trend)) + " taka . . \n \n \n . . . . . . . . . . . . .. . . .  . . . " \
                                                                                                    "Today's " + branch_name + " achievement till now is " + str(
        achievement) + " % . \n \n \n . . . . . . . . . . . . .. . . .  . . . .  . " \
                       "Today's " + branch_name + " achievement according to trend will be " + str(
        trendAchievement) + " % .  . . . ."

    reprompt_text = "For brand wise sales report say brand name and then say sales , like Losictil Sales "
    should_end_session = False
    return build_response(session_attributes,
                          build_speechlet_response(card_title, speech_output, reprompt_text, should_end_session))

# Sales - Branch MTD
def branch_mtd_sales_intent_response(intent):
    """ An example of a custom intent. Same structure as welcome message, just make sure to add this intent
    in your alexa skill in order for it to work.
    """
    global days, today

    branch = intent['slots']['branch']['resolutions']['resolutionsPerAuthority'][0]['values'][0]['value']['id']
    branch_name = intent['slots']['branch']['resolutions']['resolutionsPerAuthority'][0]['values'][0]['value']['name']
    sales = get_branch_mtd_sales(branch)
    mTarget = get_branch_mTarget(branch)
    trend = int((sales / today) * days)
    achievement = int((sales / mTarget) * 100)
    trendAchievement = int((trend / mTarget) * 100)

    session_attributes = {}
    card_title = "Branch Month to Date Sales"
    speech_output = "Your Month to Date total sales in " + branch_name + " branch as of "+str(get_time_stamp())+" is " + str(
        get_unit(sales)) + " taka . \n \n \n . . . . . . . . . . . . .. . . .  . . . . ." \
                           "Month to Date " + branch_name + " sales target is " + str(
        get_unit(mTarget)) + " taka . \n \n \n . . . . . . . . . . . . .. . . .  . . . . . ." \
                             "Month to Date " + branch_name + " sales trend is " + str(
        get_unit(trend)) + " taka . \n \n \n . . . . . . . . . . . . .. . . .  . . . . " \
                           "Month to Date " + branch_name + " achievement till now is " + str(
        achievement) + " %  \n \n \n . . . . . . . . . . . . .. . . . . . . . .  . " \
                       "Month to Date " + branch_name + " achievement according to trend will be " + str(
        trendAchievement) + " % .  . . . ."

    reprompt_text = "For brand wise sales report say brand name and then say sales , like Losictil Sales "
    should_end_session = False
    return build_response(session_attributes,
                          build_speechlet_response(card_title, speech_output, reprompt_text, should_end_session))

# Sales - Branch YTD
def branch_ytd_sales_intent_response(intent):
    """ An example of a custom intent. Same structure as welcome message, just make sure to add this intent
    in your alexa skill in order for it to work.
    """
    global days, today

    branch = intent['slots']['branch']['resolutions']['resolutionsPerAuthority'][0]['values'][0]['value']['id']
    branch_name = intent['slots']['branch']['resolutions']['resolutionsPerAuthority'][0]['values'][0]['value']['name']
    sales = get_branch_ytd_sales(branch)
    yTarget = get_branch_yTarget(branch)

    session_attributes = {}
    card_title = "Branch Year to Date Sales"
    speech_output = "Your Year to Date total sales in " + branch_name + " branch as of "+str(get_time_stamp())+" is " + str(
        get_unit(sales)) + " taka . . . . . ." \
                           "Year to Date " + branch_name + " sales target is " + str(
        get_unit(yTarget)) + " taka . . . . . . ."
    reprompt_text = "For brand wise sales report say brand name and then say sales , like Losictil Sales "
    should_end_session = False
    return build_response(session_attributes,
                          build_speechlet_response(card_title, speech_output, reprompt_text, should_end_session))

# Sales - Brand wise
def brand_sales_intent_response(intent):
    """ An example of a custom intent. Same structure as welcome message, just make sure to add this intent
    in your alexa skill in order for it to work.
    """
    brand = intent['slots']['brand']['resolutions']['resolutionsPerAuthority'][0]['values'][0]['value']['name']
    sales = get_brand_sales("apenda")
    

    session_attributes = {}
    card_title = "Brand Sales"
    speech_output = "Your " + str(brand) + " sales as of "+str(get_time_stamp())+" is " + str(get_unit(sales)) + " taka "
    reprompt_text = "Would you like to know any other report, like outstanding or stock"
    should_end_session = False
    return build_response(session_attributes, build_speechlet_response(
        card_title, speech_output, reprompt_text, should_end_session))
   

# Sales - Brand & YearMonth Wise Sales
def brand_month_sales_intent_response(intent):
    """ An example of a custom intent. Same structure as welcome message, just make sure to add this intent
    in your alexa skill in order for it to work.
    """
    brand = intent['slots']['brand']['resolutions']['resolutionsPerAuthority'][0]['values'][0]['value']['name']
    month = intent['slots']['month']['resolutions']['resolutionsPerAuthority'][0]['values'][0]['value']['id']
    month_name = intent['slots']['month']['resolutions']['resolutionsPerAuthority'][0]['values'][0]['value']['name']
    year = intent['slots']['year']['resolutions']['resolutionsPerAuthority'][0]['values'][0]['value']['id']
    year_month = year + month
    session_attributes = {}
    sales = get_brand_month_sales(brand, year_month)

    card_title = "Sales"
    speech_output = "Your " + str(brand) + " " + str(month_name) + " " + str(year) + " sales was " + str(
        get_unit(sales)) + " Taka"
    reprompt_text = "Would you like to know any other report, like outstanding or sales"
    should_end_session = False
    return build_response(session_attributes, build_speechlet_response(
        card_title, speech_output, reprompt_text, should_end_session))

# Sales - Branch & YearMonth Wise Sales
def branch_month_sales_intent_response(intent):
    """ An example of a custom intent. Same structure as welcome message, just make sure to add this intent
    in your alexa skill in order for it to work.
    """
    branch = intent['slots']['branch']['resolutions']['resolutionsPerAuthority'][0]['values'][0]['value']['id']
    branch_name = intent['slots']['branch']['resolutions']['resolutionsPerAuthority'][0]['values'][0]['value']['name']
    month = intent['slots']['month']['resolutions']['resolutionsPerAuthority'][0]['values'][0]['value']['id']
    month_name = intent['slots']['month']['resolutions']['resolutionsPerAuthority'][0]['values'][0]['value']['name']
    year = intent['slots']['year']['resolutions']['resolutionsPerAuthority'][0]['values'][0]['value']['id']
    year_month = year + month
    session_attributes = {}
    sales = get_branch_month_sales(branch, year_month)

    card_title = "Sales"
    speech_output = "Your " + str(branch_name) + " " + str(month_name) + " " + str(year) + " sales was " + str(
        get_unit(sales)) + " Taka"
    reprompt_text = "Would you like to know any other report, like outstanding or sales"
    should_end_session = False
    return build_response(session_attributes, build_speechlet_response(
        card_title, speech_output, reprompt_text, should_end_session))

# Sales - Branch & Brand wise sales
def branch_brand_sales_intent_response(intent):
    """ An example of a custom intent. Same structure as welcome message, just make sure to add this intent
    in your alexa skill in order for it to work.
    """
    branch = intent['slots']['branch']['resolutions']['resolutionsPerAuthority'][0]['values'][0]['value']['id']
    branch_name = intent['slots']['branch']['resolutions']['resolutionsPerAuthority'][0]['values'][0]['value']['name']
    brand = intent['slots']['brand']['resolutions']['resolutionsPerAuthority'][0]['values'][0]['value']['name']
    session_attributes = {}
    sales = get_branch_brand_sales(branch, brand)

    card_title = "Sales"
    speech_output = "Your " + str(branch_name) + " " + str(brand) + " sales as of "+str(get_time_stamp())+" is " + str(get_unit(sales)) + " Taka"
    reprompt_text = "Would you like to know any other report, like outstanding or sales"
    should_end_session = False
    return build_response(session_attributes, build_speechlet_response(
        card_title, speech_output, reprompt_text, should_end_session))

# Sales - Branch, Brand & YearMonth Wise sales
def branch_brand_month_sales_intent_response(intent):
    """ An example of a custom intent. Same structure as welcome message, just make sure to add this intent
    in your alexa skill in order for it to work.
    """
    branch = intent['slots']['branch']['resolutions']['resolutionsPerAuthority'][0]['values'][0]['value']['id']
    branch_name = intent['slots']['branch']['resolutions']['resolutionsPerAuthority'][0]['values'][0]['value']['name']
    brand = intent['slots']['brand']['resolutions']['resolutionsPerAuthority'][0]['values'][0]['value']['name']
    month = intent['slots']['month']['resolutions']['resolutionsPerAuthority'][0]['values'][0]['value']['id']
    month_name = intent['slots']['month']['resolutions']['resolutionsPerAuthority'][0]['values'][0]['value']['name']
    year = intent['slots']['year']['resolutions']['resolutionsPerAuthority'][0]['values'][0]['value']['id']
    year_month = year + month
    session_attributes = {}
    sales = get_branch_brand_month_sales(branch, brand, year_month)

    card_title = "Sales"
    speech_output = "Your " + str(branch_name) + " " + str(brand) + " " + str(month_name) + " " + str(
        year) + " sales was " + str(get_unit(sales)) + " Taka"
    reprompt_text = "Would you like to know any other report, like outstanding or sales"
    should_end_session = False
    return build_response(session_attributes, build_speechlet_response(
        card_title, speech_output, reprompt_text, should_end_session))

# Sales - NSM wise
def nsm_sales_intent_response(intent):
    """ An example of a custom intent. Same structure as welcome message, just make sure to add this intent
    in your alexa skill in order for it to work.
    """

    nsmid = int(intent['slots']['nsm']['resolutions']['resolutionsPerAuthority'][0]['values'][0]['value']['id'])
    nsm_name = intent['slots']['nsm']['resolutions']['resolutionsPerAuthority'][0]['values'][0]['value']['name']
    sales = get_nsm_sales(nsmid)
    mTarget = get_nsm_mTarget(nsmid)
    dTarget = int(mTarget / days)
    trend = int(sales * trendTime)
    achievement = int((sales / dTarget) * 100)
    trendAchievement = int((trend / dTarget) * 100)

    session_attributes = {}
    card_title = "Brand Sales"
    speech_output = "Your NSM " + str(nsm_name) + " sales as of "+str(get_time_stamp())+" is " + str(get_unit(sales)) + " taka "\
                    "Today's sales target is " + str(get_unit(dTarget)) + " taka . . . . . . . . . . . . \n \n \n.. . . . . . . ." \
                             "Today's sales trend is " + str(
        get_unit(trend)) + " taka. . . . . . . .   .. . . . . .\n \n \n .. . . . . ." \
                           "Today's achievement till now is " + str(
        achievement) + " % . . . . .  .  . . . . . . .. \n \n \n. . . . . . ..  " \
                       "Today's achievement according to trend will be " + str(trendAchievement) + " % ."
    # speech_output = "Your NSM " + str(nsm_name) + "sales is 1000 taka "
    reprompt_text = "Would you like to know any other report, like outstanding or stock"
    should_end_session = False
    return build_response(session_attributes, build_speechlet_response(
        card_title, speech_output, reprompt_text, should_end_session))

# Sales - NSM MTD
def nsm_mtd_sales_intent_response(intent):
    """ An example of a custom intent. Same structure as welcome message, just make sure to add this intent
    in your alexa skill in order for it to work.
    """

    nsmid = int(intent['slots']['nsm']['resolutions']['resolutionsPerAuthority'][0]['values'][0]['value']['id'])
    nsm_name = intent['slots']['nsm']['resolutions']['resolutionsPerAuthority'][0]['values'][0]['value']['name']
    sales = get_nsm_mtd_sales(nsmid)

    session_attributes = {}
    card_title = "Brand Sales"
    speech_output = "Your NSM " + str(nsm_name) + " month to date sales as of "+str(get_time_stamp())+" is " + str(get_unit(sales)) + " taka "
    reprompt_text = "Would you like to know any other report, like outstanding or stock"
    should_end_session = False
    return build_response(session_attributes, build_speechlet_response(
        card_title, speech_output, reprompt_text, should_end_session))

# Sales - NSM YTD
def nsm_ytd_sales_intent_response(intent):
    """ An example of a custom intent. Same structure as welcome message, just make sure to add this intent
    in your alexa skill in order for it to work.
    """

    nsmid = int(intent['slots']['nsm']['resolutions']['resolutionsPerAuthority'][0]['values'][0]['value']['id'])
    nsm_name = intent['slots']['nsm']['resolutions']['resolutionsPerAuthority'][0]['values'][0]['value']['name']
    sales = get_nsm_ytd_sales(nsmid)

    session_attributes = {}
    card_title = "Brand Sales"
    speech_output = "Your NSM " + str(nsm_name) + " year to date sales as of "+str(get_time_stamp())+" is " + str(get_unit(sales)) + " taka "
    reprompt_text = "Would you like to know any other report, like outstanding or stock"
    should_end_session = False
    return build_response(session_attributes, build_speechlet_response(
        card_title, speech_output, reprompt_text, should_end_session))

# Sales - NSM & YearMonth Wise
def nsm_month_sales_intent_response(intent):
    """ An example of a custom intent. Same structure as welcome message, just make sure to add this intent
    in your alexa skill in order for it to work.
    """

    nsmid = int(intent['slots']['nsm']['resolutions']['resolutionsPerAuthority'][0]['values'][0]['value']['id'])
    nsm_name = intent['slots']['nsm']['resolutions']['resolutionsPerAuthority'][0]['values'][0]['value']['name']
    month = intent['slots']['month']['resolutions']['resolutionsPerAuthority'][0]['values'][0]['value']['id']
    month_name = intent['slots']['month']['resolutions']['resolutionsPerAuthority'][0]['values'][0]['value']['name']
    year = intent['slots']['year']['resolutions']['resolutionsPerAuthority'][0]['values'][0]['value']['id']
    year_month = year + month
    sales = get_nsm_month_sales(nsmid, year_month)

    session_attributes = {}
    card_title = "Brand Sales"
    speech_output = "Your NSM " + str(nsm_name) + " " + str(month_name) + " " + str(year) + "sales was " + str(
        get_unit(sales)) + " taka "
    # speech_output = "Your NSM " + str(nsm_name) + "sales is 1000 taka "
    reprompt_text = "Would you like to know any other report, like outstanding or stock"
    should_end_session = False
    return build_response(session_attributes, build_speechlet_response(
        card_title, speech_output, reprompt_text, should_end_session))

# Sales - NSM & Brand  Wise
def nsm_brand_sales_intent_response(intent):
    """ An example of a custom intent. Same structure as welcome message, just make sure to add this intent
    in your alexa skill in order for it to work.
    """
    nsm = int(intent['slots']['nsm']['resolutions']['resolutionsPerAuthority'][0]['values'][0]['value']['id'])
    nsm_name = intent['slots']['nsm']['resolutions']['resolutionsPerAuthority'][0]['values'][0]['value']['name']
    brand = intent['slots']['brand']['resolutions']['resolutionsPerAuthority'][0]['values'][0]['value']['name']
    session_attributes = {}
    sales = get_nsm_brand_sales(nsm, brand)

    card_title = "Sales"
    speech_output = "Your  NSM " + str(nsm_name) + " " + str(brand) + " sales as of "+str(get_time_stamp())+" is " + str(get_unit(sales)) + " Taka"
    reprompt_text = "Would you like to know any other report, like outstanding or sales"
    should_end_session = False
    return build_response(session_attributes, build_speechlet_response(
        card_title, speech_output, reprompt_text, should_end_session))

# Sales - NSM & Brand MTD sales
def nsm_brand_mtd_sales_intent_response(intent):
    """ An example of a custom intent. Same structure as welcome message, just make sure to add this intent
    in your alexa skill in order for it to work.
    """
    nsm = int(intent['slots']['nsm']['resolutions']['resolutionsPerAuthority'][0]['values'][0]['value']['id'])
    nsm_name = intent['slots']['nsm']['resolutions']['resolutionsPerAuthority'][0]['values'][0]['value']['name']
    brand = intent['slots']['brand']['resolutions']['resolutionsPerAuthority'][0]['values'][0]['value']['name']
    session_attributes = {}
    sales = get_nsm_brand_mtd_sales(nsm, brand)

    card_title = "Sales"
    speech_output = "Your  NSM " + str(nsm_name) + " " + str(brand) + " month to date sales as of "+str(get_time_stamp())+" is " + str(
        get_unit(sales)) + " Taka"
    reprompt_text = "Would you like to know any other report, like outstanding or sales"
    should_end_session = False
    return build_response(session_attributes, build_speechlet_response(
        card_title, speech_output, reprompt_text, should_end_session))

# Sales - NSM & Brand YTD sales
def nsm_brand_ytd_sales_intent_response(intent):
    """ An example of a custom intent. Same structure as welcome message, just make sure to add this intent
    in your alexa skill in order for it to work.
    """
    nsm = int(intent['slots']['nsm']['resolutions']['resolutionsPerAuthority'][0]['values'][0]['value']['id'])
    nsm_name = intent['slots']['nsm']['resolutions']['resolutionsPerAuthority'][0]['values'][0]['value']['name']
    brand = intent['slots']['brand']['resolutions']['resolutionsPerAuthority'][0]['values'][0]['value']['name']
    session_attributes = {}
    sales = get_nsm_brand_ytd_sales(nsm, brand)

    card_title = "Sales"
    speech_output = "Your  NSM " + str(nsm_name) + " " + str(brand) + " year to date sales as of "+str(get_time_stamp())+" is " + str(
        get_unit(sales)) + " Taka"
    reprompt_text = "Would you like to know any other report, like outstanding or sales"
    should_end_session = False
    return build_response(session_attributes, build_speechlet_response(
        card_title, speech_output, reprompt_text, should_end_session))

# Sales - NSM , Brand & YearMonth Wise
def nsm_brand_month_sales_intent_response(intent):
    """ An example of a custom intent. Same structure as welcome message, just make sure to add this intent
    in your alexa skill in order for it to work.
    """

    nsmid = int(intent['slots']['nsm']['resolutions']['resolutionsPerAuthority'][0]['values'][0]['value']['id'])
    nsm_name = intent['slots']['nsm']['resolutions']['resolutionsPerAuthority'][0]['values'][0]['value']['name']
    brand = intent['slots']['brand']['resolutions']['resolutionsPerAuthority'][0]['values'][0]['value']['name']
    month = intent['slots']['month']['resolutions']['resolutionsPerAuthority'][0]['values'][0]['value']['id']
    month_name = intent['slots']['month']['resolutions']['resolutionsPerAuthority'][0]['values'][0]['value']['name']
    year = intent['slots']['year']['resolutions']['resolutionsPerAuthority'][0]['values'][0]['value']['id']
    year_month = year + month
    sales = get_nsm_brand_month_sales(nsmid, brand, year_month)

    session_attributes = {}
    card_title = "Brand Sales"
    speech_output = "Your NSM " + str(nsm_name) + " " + str(brand) + " " + str(month_name) + " " + str(
        year) + "sales was " + str(get_unit(sales)) + " taka "
    # speech_output = "Your NSM " + str(nsm_name) + "sales is 1000 taka "
    reprompt_text = "Would you like to know any other report, like outstanding or stock"
    should_end_session = False
    return build_response(session_attributes, build_speechlet_response(
        card_title, speech_output, reprompt_text, should_end_session))

# Sales - RSM wise
def rsm_sales_intent_response(intent):
    """ An example of a custom intent. Same structure as welcome message, just make sure to add this intent
    in your alexa skill in order for it to work.
    """

    # rsm = int(intent['slots']['rsm']['resolutions']['resolutionsPerAuthority'][0]['values'][0]['value']['id'])
    # rsm_name = intent['slots']['rsm']['resolutions']['resolutionsPerAuthority'][0]['values'][0]['value']['name']
    sales = get_rsm_sales(2320)
    mTarget = get_rsm_mTarget(2320)
    # dTarget = int(mTarget / days)
    # trend = int(sales * trendTime)
    # achievement = int((sales / dTarget) * 100)
    # trendAchievement = int((trend / dTarget) * 100)
    
    print("Helo......................",sales,'------',sales)

    # session_attributes = {}
    # card_title = "Brand Sales"
    # speech_output = "Your RSM " + str(rsm_name) + " sales as of "+str(get_time_stamp())+" is " + str(get_unit(sales)) + " taka .............. . .. . . .\n \n \n "\
    #                       "Today's sales target is " + str(
    #     get_unit(dTarget)) + " taka . . . . . . . . . . . . \n \n \n.. . . . . . . ." \
    #                          "Today's sales trend is " + str(
    #     get_unit(trend)) + " taka. . . . . . . .   .. . . . . .\n \n \n .. . . . . ." \
    #                       "Today's achievement till now is " + str(
    #     achievement) + " % . . . . .  .  . . . . . . .. \n \n \n. . . . . . ..  " \
    #                   "Today's achievement according to trend will be " + str(trendAchievement) + " % ."
    # reprompt_text = "Would you like to know any other report, like outstanding or stock"
    # should_end_session = False
    # return build_response(session_attributes, build_speechlet_response(
    #     card_title, speech_output, reprompt_text, should_end_session))
    
rsm_sales_intent_response(444)

# Sales - RSM MTD
def rsm_mtd_sales_intent_response(intent):
    """ An example of a custom intent. Same structure as welcome message, just make sure to add this intent
    in your alexa skill in order for it to work.
    """

    rsm = int(intent['slots']['rsm']['resolutions']['resolutionsPerAuthority'][0]['values'][0]['value']['id'])
    rsm_name = intent['slots']['rsm']['resolutions']['resolutionsPerAuthority'][0]['values'][0]['value']['name']
    sales = get_rsm_mtd_sales(rsm)

    session_attributes = {}
    card_title = "Brand Sales"
    speech_output = "Your RSM " + str(rsm_name) + " month to date sales as of "+str(get_time_stamp())+" is " + str(get_unit(sales)) + " taka "
    reprompt_text = "Would you like to know any other report, like outstanding or stock"
    should_end_session = False
    return build_response(session_attributes, build_speechlet_response(
        card_title, speech_output, reprompt_text, should_end_session))

# Sales - RSM YTD
def rsm_ytd_sales_intent_response(intent):
    """ An example of a custom intent. Same structure as welcome message, just make sure to add this intent
    in your alexa skill in order for it to work.
    """

    rsm = int(intent['slots']['rsm']['resolutions']['resolutionsPerAuthority'][0]['values'][0]['value']['id'])
    rsm_name = intent['slots']['rsm']['resolutions']['resolutionsPerAuthority'][0]['values'][0]['value']['name']
    sales = get_rsm_ytd_sales(rsm)

    session_attributes = {}
    card_title = "Brand Sales"
    speech_output = "Your RSM " + str(rsm_name) + " year to date sales as of "+str(get_time_stamp())+" is " + str(get_unit(sales)) + " taka "
    reprompt_text = "Would you like to know any other report, like outstanding or stock"
    should_end_session = False
    return build_response(session_attributes, build_speechlet_response(
        card_title, speech_output, reprompt_text, should_end_session))

# Sales - RSM & YearMonth Wise
def rsm_month_sales_intent_response(intent):
    """ An example of a custom intent. Same structure as welcome message, just make sure to add this intent
    in your alexa skill in order for it to work.
    """

    rsmid = int(intent['slots']['rsm']['resolutions']['resolutionsPerAuthority'][0]['values'][0]['value']['id'])
    rsm_name = intent['slots']['rsm']['resolutions']['resolutionsPerAuthority'][0]['values'][0]['value']['name']
    month = intent['slots']['month']['resolutions']['resolutionsPerAuthority'][0]['values'][0]['value']['id']
    month_name = intent['slots']['month']['resolutions']['resolutionsPerAuthority'][0]['values'][0]['value']['name']
    year = intent['slots']['year']['resolutions']['resolutionsPerAuthority'][0]['values'][0]['value']['id']
    year_month = year + month
    sales = get_rsm_month_sales(rsmid, year_month)

    session_attributes = {}
    card_title = "Brand Sales"
    speech_output = "Your RSM " + str(rsm_name) + " " + str(month_name) + " " + str(year) + " sales was " + str(
        get_unit(sales)) + " taka "
    # speech_output = "Your NSM " + str(nsm_name) + "sales is 1000 taka "
    reprompt_text = "Would you like to know any other report, like outstanding or stock"
    should_end_session = False
    return build_response(session_attributes, build_speechlet_response(
        card_title, speech_output, reprompt_text, should_end_session))

# Sales - RSM & Brand Wise sales
def rsm_brand_sales_intent_response(intent):
    """ An example of a custom intent. Same structure as welcome message, just make sure to add this intent
    in your alexa skill in order for it to work.
    """
    rsm = int(intent['slots']['rsm']['resolutions']['resolutionsPerAuthority'][0]['values'][0]['value']['id'])
    rsm_name = intent['slots']['rsm']['resolutions']['resolutionsPerAuthority'][0]['values'][0]['value']['name']
    brand = intent['slots']['brand']['resolutions']['resolutionsPerAuthority'][0]['values'][0]['value']['name']
    session_attributes = {}
    sales = get_rsm_brand_sales(rsm, brand)

    card_title = "Sales"
    speech_output = "Your RSM " + str(rsm_name) + " " + str(brand) + " sales as of "+str(get_time_stamp())+" is " + str(get_unit(sales)) + " Taka"
    reprompt_text = "Would you like to know any other report, like outstanding or sales"
    should_end_session = False
    return build_response(session_attributes, build_speechlet_response(
        card_title, speech_output, reprompt_text, should_end_session))

# Sales - RSM & Brand MTD sales
def rsm_brand_mtd_sales_intent_response(intent):
    """ An example of a custom intent. Same structure as welcome message, just make sure to add this intent
    in your alexa skill in order for it to work.
    """
    rsm = int(intent['slots']['rsm']['resolutions']['resolutionsPerAuthority'][0]['values'][0]['value']['id'])
    rsm_name = intent['slots']['rsm']['resolutions']['resolutionsPerAuthority'][0]['values'][0]['value']['name']
    brand = intent['slots']['brand']['resolutions']['resolutionsPerAuthority'][0]['values'][0]['value']['name']
    session_attributes = {}
    sales = get_rsm_brand_mtd_sales(rsm, brand)

    card_title = "Sales"
    speech_output = "Your RSM " + str(rsm_name) + " " + str(brand) + " month to date sales as of "+str(get_time_stamp())+" is " + str(
        get_unit(sales)) + " Taka"
    reprompt_text = "Would you like to know any other report, like outstanding or sales"
    should_end_session = False
    return build_response(session_attributes, build_speechlet_response(
        card_title, speech_output, reprompt_text, should_end_session))

# Sales - RSM & Brand YTD sales
def rsm_brand_ytd_sales_intent_response(intent):
    """ An example of a custom intent. Same structure as welcome message, just make sure to add this intent
    in your alexa skill in order for it to work.
    """
    rsm = int(intent['slots']['rsm']['resolutions']['resolutionsPerAuthority'][0]['values'][0]['value']['id'])
    rsm_name = intent['slots']['rsm']['resolutions']['resolutionsPerAuthority'][0]['values'][0]['value']['name']
    brand = intent['slots']['brand']['resolutions']['resolutionsPerAuthority'][0]['values'][0]['value']['name']
    session_attributes = {}
    sales = get_rsm_brand_ytd_sales(rsm, brand)

    card_title = "Sales"
    speech_output = "Your RSM " + str(rsm_name) + " " + str(brand) + " year to date sales as of "+str(get_time_stamp())+" is " + str(
        get_unit(sales)) + " Taka"
    reprompt_text = "Would you like to know any other report, like outstanding or sales"
    should_end_session = False
    return build_response(session_attributes, build_speechlet_response(
        card_title, speech_output, reprompt_text, should_end_session))

# Sales - RSM , Brand & YearMonth Wise
def rsm_brand_month_sales_intent_response(intent):
    """ An example of a custom intent. Same structure as welcome message, just make sure to add this intent
    in your alexa skill in order for it to work.
    """

    rsmid = int(intent['slots']['rsm']['resolutions']['resolutionsPerAuthority'][0]['values'][0]['value']['id'])
    rsm_name = intent['slots']['rsm']['resolutions']['resolutionsPerAuthority'][0]['values'][0]['value']['name']
    brand = intent['slots']['brand']['resolutions']['resolutionsPerAuthority'][0]['values'][0]['value']['name']
    month = intent['slots']['month']['resolutions']['resolutionsPerAuthority'][0]['values'][0]['value']['id']
    month_name = intent['slots']['month']['resolutions']['resolutionsPerAuthority'][0]['values'][0]['value']['name']
    year = intent['slots']['year']['resolutions']['resolutionsPerAuthority'][0]['values'][0]['value']['id']
    year_month = year + month
    sales = get_rsm_brand_month_sales(rsmid, brand, year_month)

    session_attributes = {}
    card_title = "Brand Sales"
    speech_output = "Your RSM " + str(rsm_name) + " " + str(brand) + " " + str(month_name) + " " + str(
        year) + "sales was " + str(get_unit(sales)) + " taka "
    # speech_output = "Your NSM " + str(nsm_name) + "sales is 1000 taka "
    reprompt_text = "Would you like to know any other report, like outstanding or stock"
    should_end_session = False
    return build_response(session_attributes, build_speechlet_response(
        card_title, speech_output, reprompt_text, should_end_session))

# Sales - FM wise
def fm_sales_intent_response(intent):
    """ An example of a custom intent. Same structure as welcome message, just make sure to add this intent
    in your alexa skill in order for it to work.
    """

    fm = int(intent['slots']['fm']['resolutions']['resolutionsPerAuthority'][0]['values'][0]['value']['id'])
    fm_name = intent['slots']['fm']['resolutions']['resolutionsPerAuthority'][0]['values'][0]['value']['name']
    sales = get_fm_sales(fm)
    mTarget = get_fm_mTarget(fm)
    dTarget = int(mTarget / days)
    trend = int(sales * trendTime)
    achievement = int((sales / dTarget) * 100)
    trendAchievement = int((trend / dTarget) * 100)

    session_attributes = {}
    card_title = "Brand Sales"
    speech_output = "Your FM " + str(fm_name) + " sales as of "+str(get_time_stamp())+" is " + str(get_unit(sales)) + " taka "\
                    "Today's sales target is " + str(
                        get_unit(dTarget)) + " taka . . . . . . . . . . . . \n \n \n.. . . . . . . ." \
                                             "Today's sales trend is " + str(
                        get_unit(trend)) + " taka. . . . . . . .   .. . . . . .\n \n \n .. . . . . ." \
                                           "Today's achievement till now is " + str(
                        achievement) + " % . . . . .  .  . . . . . . .. \n \n \n. . . . . . ..  " \
                                       "Today's achievement according to trend will be " + str(trendAchievement) + " % ."
    reprompt_text = "Would you like to know any other report, like outstanding or stock"
    should_end_session = False
    return build_response(session_attributes, build_speechlet_response(
        card_title, speech_output, reprompt_text, should_end_session))

# Sales - FM MTD
def fm_mtd_sales_intent_response(intent):
    """ An example of a custom intent. Same structure as welcome message, just make sure to add this intent
    in your alexa skill in order for it to work.
    """

    fm = int(intent['slots']['fm']['resolutions']['resolutionsPerAuthority'][0]['values'][0]['value']['id'])
    fm_name = intent['slots']['fm']['resolutions']['resolutionsPerAuthority'][0]['values'][0]['value']['name']
    sales = get_fm_mtd_sales(fm)

    session_attributes = {}
    card_title = "Brand Sales"
    speech_output = "Your FM " + str(fm_name) + " month to date sales as of "+str(get_time_stamp())+" is " + str(get_unit(sales)) + " taka "
    reprompt_text = "Would you like to know any other report, like outstanding or stock"
    should_end_session = False
    return build_response(session_attributes, build_speechlet_response(
        card_title, speech_output, reprompt_text, should_end_session))

# Sales - FM YTD
def fm_ytd_sales_intent_response(intent):
    """ An example of a custom intent. Same structure as welcome message, just make sure to add this intent
    in your alexa skill in order for it to work.
    """

    fm = int(intent['slots']['fm']['resolutions']['resolutionsPerAuthority'][0]['values'][0]['value']['id'])
    fm_name = intent['slots']['fm']['resolutions']['resolutionsPerAuthority'][0]['values'][0]['value']['name']
    sales = get_fm_ytd_sales(fm)

    session_attributes = {}
    card_title = "Brand Sales"
    speech_output = "Your FM " + str(fm_name) + " year to date sales as of "+str(get_time_stamp())+" is " + str(get_unit(sales)) + " taka "
    reprompt_text = "Would you like to know any other report, like outstanding or stock"
    should_end_session = False
    return build_response(session_attributes, build_speechlet_response(
        card_title, speech_output, reprompt_text, should_end_session))

# Sales - FM & YearMonth Wise
def fm_month_sales_intent_response(intent):
    """ An example of a custom intent. Same structure as welcome message, just make sure to add this intent
    in your alexa skill in order for it to work.
    """

    fmid = int(intent['slots']['fm']['resolutions']['resolutionsPerAuthority'][0]['values'][0]['value']['id'])
    fm_name = intent['slots']['fm']['resolutions']['resolutionsPerAuthority'][0]['values'][0]['value']['name']
    month = intent['slots']['month']['resolutions']['resolutionsPerAuthority'][0]['values'][0]['value']['id']
    month_name = intent['slots']['month']['resolutions']['resolutionsPerAuthority'][0]['values'][0]['value']['name']
    year = intent['slots']['year']['resolutions']['resolutionsPerAuthority'][0]['values'][0]['value']['id']
    year_month = year + month
    sales = get_fm_month_sales(fmid, year_month)

    session_attributes = {}
    card_title = "Brand Sales"
    speech_output = "Your FM " + str(fm_name) + " " + str(month_name) + " " + str(year) + "sales was " + str(
        get_unit(sales)) + " taka "
    # speech_output = "Your NSM " + str(nsm_name) + "sales is 1000 taka "
    reprompt_text = "Would you like to know any other report, like outstanding or stock"
    should_end_session = False
    return build_response(session_attributes, build_speechlet_response(
        card_title, speech_output, reprompt_text, should_end_session))

# Sales - FM & Brand Wise
def fm_brand_sales_intent_response(intent):
    """ An example of a custom intent. Same structure as welcome message, just make sure to add this intent
    in your alexa skill in order for it to work.
    """
    fm = int(intent['slots']['fm']['resolutions']['resolutionsPerAuthority'][0]['values'][0]['value']['id'])
    fm_name = intent['slots']['fm']['resolutions']['resolutionsPerAuthority'][0]['values'][0]['value']['name']
    brand = intent['slots']['brand']['resolutions']['resolutionsPerAuthority'][0]['values'][0]['value']['name']
    session_attributes = {}
    sales = get_fm_brand_sales(fm, brand)

    card_title = "Sales"
    speech_output = "Your FM " + str(fm_name) + " " + str(brand) + " sales as of "+str(get_time_stamp())+" is " + str(get_unit(sales)) + " Taka"
    reprompt_text = "Would you like to know any other report, like outstanding or sales"
    should_end_session = False
    return build_response(session_attributes, build_speechlet_response(
        card_title, speech_output, reprompt_text, should_end_session))

# Sales - FM & Brand MTD Sales
def fm_brand_mtd_sales_intent_response(intent):
    """ An example of a custom intent. Same structure as welcome message, just make sure to add this intent
    in your alexa skill in order for it to work.
    """
    fm = int(intent['slots']['fm']['resolutions']['resolutionsPerAuthority'][0]['values'][0]['value']['id'])
    fm_name = intent['slots']['fm']['resolutions']['resolutionsPerAuthority'][0]['values'][0]['value']['name']
    brand = intent['slots']['brand']['resolutions']['resolutionsPerAuthority'][0]['values'][0]['value']['name']
    session_attributes = {}
    sales = get_fm_brand_mtd_sales(fm, brand)

    card_title = "Sales"
    speech_output = "Your FM " + str(fm_name) + " " + str(brand) + " month to date sales as of "+str(get_time_stamp())+" is " + str(
        get_unit(sales)) + " Taka"
    reprompt_text = "Would you like to know any other report, like outstanding or sales"
    should_end_session = False
    return build_response(session_attributes, build_speechlet_response(
        card_title, speech_output, reprompt_text, should_end_session))

# Sales - FM & Brand YTD Sales
def fm_brand_ytd_sales_intent_response(intent):
    """ An example of a custom intent. Same structure as welcome message, just make sure to add this intent
    in your alexa skill in order for it to work.
    """
    fm = int(intent['slots']['fm']['resolutions']['resolutionsPerAuthority'][0]['values'][0]['value']['id'])
    fm_name = intent['slots']['fm']['resolutions']['resolutionsPerAuthority'][0]['values'][0]['value']['name']
    brand = intent['slots']['brand']['resolutions']['resolutionsPerAuthority'][0]['values'][0]['value']['name']
    session_attributes = {}
    sales = get_fm_brand_ytd_sales(fm, brand)

    card_title = "Sales"
    speech_output = "Your FM " + str(fm_name) + " " + str(brand) + " year to date sales is " + str(
        get_unit(sales)) + " Taka"
    reprompt_text = "Would you like to know any other report, like outstanding or sales"
    should_end_session = False
    return build_response(session_attributes, build_speechlet_response(
        card_title, speech_output, reprompt_text, should_end_session))

# Sales - FM , Brand & YearMonth Wise
def fm_brand_month_sales_intent_response(intent):
    """ An example of a custom intent. Same structure as welcome message, just make sure to add this intent
    in your alexa skill in order for it to work.
    """

    fmid = int(intent['slots']['fm']['resolutions']['resolutionsPerAuthority'][0]['values'][0]['value']['id'])
    fm_name = intent['slots']['fm']['resolutions']['resolutionsPerAuthority'][0]['values'][0]['value']['name']
    brand = intent['slots']['brand']['resolutions']['resolutionsPerAuthority'][0]['values'][0]['value']['name']
    month = intent['slots']['month']['resolutions']['resolutionsPerAuthority'][0]['values'][0]['value']['id']
    month_name = intent['slots']['month']['resolutions']['resolutionsPerAuthority'][0]['values'][0]['value']['name']
    year = intent['slots']['year']['resolutions']['resolutionsPerAuthority'][0]['values'][0]['value']['id']
    year_month = year + month
    sales = get_fm_brand_month_sales(fmid, brand, year_month)

    session_attributes = {}
    card_title = "Brand Sales"
    speech_output = "Your RSM " + str(fm_name) + " " + str(brand) + " " + str(month_name) + " " + str(
        year) + "sales was " + str(get_unit(sales)) + " taka "
    # speech_output = "Your NSM " + str(nsm_name) + "sales is 1000 taka "
    reprompt_text = "Would you like to know any other report, like outstanding or stock"
    should_end_session = False
    return build_response(session_attributes, build_speechlet_response(
        card_title, speech_output, reprompt_text, should_end_session))

# Stock - Branch wise
def branch_stock_intent_response(intent):
    """ An example of a custom intent. Same structure as welcome message, just make sure to add this intent
    in your alexa skill in order for it to work.
    """
    branch = intent['slots']['branch']['resolutions']['resolutionsPerAuthority'][0]['values'][0]['value']['id']
    branch_name = intent['slots']['branch']['resolutions']['resolutionsPerAuthority'][0]['values'][0]['value']['name']
    session_attributes = {}
    stock = get_branch_stock(branch)
    card_title = "Stock"
    speech_output = "Your " + str(branch_name) + " stock as of "+str(get_time_stamp())+" is " + str(stock) + " unit"
    reprompt_text = "Would you like to know any other report, like outstanding or sales"
    should_end_session = False
    return build_response(session_attributes, build_speechlet_response(
        card_title, speech_output, reprompt_text, should_end_session))

# Outstanding - All branches
def outstanding_intent_response():
    """ An example of a custom intent. Same structure as welcome message, just make sure to add this intent
    in your alexa skill in order for it to work.
    """
    session_attributes = {}
    # name = intent['slots']['name']['value']
    card_title = "Outstanding"
    outstanding = get_outstanding()
    speech_output = "Your outstanding as of yesterday is " + str(get_unit(outstanding)) + " taka"
    reprompt_text = "Would you like to know any other report, like sales or stock"
    should_end_session = False
    return build_response(session_attributes, build_speechlet_response(
        card_title, speech_output, reprompt_text, should_end_session))

# Outstanding - Branch Wise
def branch_outstanding_intent_response(intent):
    """ An example of a custom intent. Same structure as welcome message, just make sure to add this intent
    in your alexa skill in order for it to work.
    """
    branch = intent['slots']['branch']['resolutions']['resolutionsPerAuthority'][0]['values'][0]['value']['id']
    branch_name = intent['slots']['branch']['resolutions']['resolutionsPerAuthority'][0]['values'][0]['value']['name']
    session_attributes = {}
    outstanding = get_branch_outstanding(branch)

    card_title = "Outstanding"
    speech_output = "Your " + str(branch_name) + " outstanding as of "+str(get_time_stamp())+" is " + str(get_unit(outstanding)) + " Taka"
    reprompt_text = "Would you like to know any other report, like outstanding or sales"
    should_end_session = False
    return build_response(session_attributes, build_speechlet_response(
        card_title, speech_output, reprompt_text, should_end_session))

# Welcome Responce
def get_welcome_response():
    """ If we wanted to initialize the session to have some attributes we could
    add those here
    """
    session_attributes = {}
    card_title = "Welcome"
    speech_output = "Welcome to the Report. Which report you want to know?"
    # If the user either does not reply to the welcome message or says something
    # that is not understood, they will be prompted again with this text.
    reprompt_text = "you can say sales, stock or outstanding to know the reports."
    should_end_session = False
    return build_response(session_attributes, build_speechlet_response(
        card_title, speech_output, reprompt_text, should_end_session))

# Good Bye Response
def handle_session_end_request():
    card_title = "Session Ended"
    speech_output = "Thank you for trying the Report . " \
                    "Have a nice day! "
    # Setting this to true ends the session and exits the skill.
    should_end_session = True
    return build_response({}, build_speechlet_response(
        card_title, speech_output, None, should_end_session))

# --------------- Events -------------------------------------------------------
def on_session_started(session_started_request, session):
    """ Called when the session starts.
        One possible use of this function is to initialize specific
        variables from a previous state stored in an external database
    """
    # Add additional code here as needed
    pass
def on_launch(launch_request, session):
    """ Called when the user launches the skill without specifying what they
    want
    """
    # Dispatch to your skill's launch message
    return get_welcome_response()
def on_intent(intent_request, session):
    """ Called when the user specifies an intent for this skill """

    intent = intent_request['intent']
    intent_name = intent_request['intent']['name']
    # intentcode = intent_name[len(intent_name)-14:len(intent_name)]

    # Dispatch to your skill's intent handlers

    # Sales - All Branch
    if intent_name == "ALLBLSSLIntent":
        return sales_intent_response()

    # Sales - MTD Sales
    elif intent_name == "ALLBMTDSIntent":
        return mtd_sales_intent_response()

    # Sales - YTD Sales
    elif intent_name == "ALLBYTDSIntent":
        return ytd_sales_intent_response()

    # Sales - Branch Wise
    elif intent_name == "BNCHLSSLIntent":
        return branch_sales_intent_response(intent)

    # Sales - Branch MTD
    elif intent_name == "BNCHMTDSIntent":
        return branch_mtd_sales_intent_response(intent)

    # Sales - Branch YTD
    elif intent_name == "BNCHYTDSIntent":
        return branch_ytd_sales_intent_response(intent)

    # Stock - Branch Wise
    elif intent_name == "BNCHCSSTIntent":
        return branch_stock_intent_response(intent)

    # Sales - Brand Wise
    elif intent_name == "BRNDLSSLIntent":
        return brand_sales_intent_response(intent)

    # Sales - Branch & Brand Wise
    elif intent_name == "BHBDLSSLIntent":
        return branch_brand_sales_intent_response(intent)

    # Sales - NSM Wise
    elif intent_name == "NSMWLSSLIntent":
        return nsm_sales_intent_response(intent)

    # Sales - NSM MTD
    elif intent_name == "NSMWMTDSIntent":
        return nsm_mtd_sales_intent_response(intent)

    # Sales - NSM YTD
    elif intent_name == "NSMWYTDSIntent":
        return nsm_ytd_sales_intent_response(intent)

    # Sales - NSM & YearMonth Wise
    elif intent_name == "NSMMMYYSIntent":
        return nsm_month_sales_intent_response(intent)

        # Sales - NSM & Brand Wise
    elif intent_name == "NSMBDWLSIntent":
        return nsm_brand_sales_intent_response(intent)

    # Sales - NSM & Brand MTD
    elif intent_name == "NSMBDMDSIntent":
        return nsm_brand_mtd_sales_intent_response(intent)

    # Sales - NSM & Brand YTD
    elif intent_name == "NSMBDYDSIntent":
        return nsm_brand_ytd_sales_intent_response(intent)

    # Sales - NSM, Brand & YearMonth Wise
    elif intent_name == "NSMBDMYSIntent":
        return nsm_brand_month_sales_intent_response(intent)

    # Sales - RSM Wise
    elif intent_name == "RSMWLSSLIntent":
        return rsm_sales_intent_response(intent)

    # Sales - RSM MTD
    elif intent_name == "RSMWMTDSIntent":
        return rsm_mtd_sales_intent_response(intent)

    # Sales - RSM YTD
    elif intent_name == "RSMWYTDSIntent":
        return rsm_ytd_sales_intent_response(intent)

    # Sales - RSM & YearMonth Wise
    elif intent_name == "RSMMMYYSIntent":
        return rsm_month_sales_intent_response(intent)

    # Sales - RSM & Brand Wise
    elif intent_name == "RSMBDWLSIntent":
        return rsm_brand_sales_intent_response(intent)

    # Sales - RSM & Brand MTD
    elif intent_name == "RSMBDMDSIntent":
        return rsm_brand_mtd_sales_intent_response(intent)

    # Sales - RSM & Brand YTD
    elif intent_name == "RSMBDYDSIntent":
        return rsm_brand_ytd_sales_intent_response(intent)

    # Sales - RSM, Brand & YearMonth Wise
    elif intent_name == "RSMBDMYSIntent":
        return rsm_brand_month_sales_intent_response(intent)

    # Sales - FM Wise
    elif intent_name == "FFMWLSSLIntent":
        return fm_sales_intent_response(intent)

    # Sales - FM MTD
    elif intent_name == "FFMWMTDSIntent":
        return fm_mtd_sales_intent_response(intent)

    # Sales - FM YTD
    elif intent_name == "FFMWYTDSIntent":
        return fm_ytd_sales_intent_response(intent)

    # Sales - FM & YearMonth Wise
    elif intent_name == "FFMMMYYSIntent":
        return fm_month_sales_intent_response(intent)

    # Sales - FM & Brand Wise
    elif intent_name == "FFMBDWLSIntent":
        return fm_brand_sales_intent_response(intent)

    # Sales - FM & Brand MTD
    elif intent_name == "FFMBDMDSIntent":
        return fm_brand_mtd_sales_intent_response(intent)

    # Sales - FM & Brand YTD
    elif intent_name == "FFMBDYDSIntent":
        return fm_brand_ytd_sales_intent_response(intent)

    # Sales - FM, Brand & YearMonth Wise
    elif intent_name == "FFMBDMYSIntent":
        return fm_brand_month_sales_intent_response(intent)

    # Sales - Brand , Branch , MonthYear Wise
    elif intent_name == "BBMMYYSLIntent":
        return branch_brand_month_sales_intent_response(intent)

    # Sales - Branch & MonthYear Wise
    elif intent_name == "BHMMYYSLIntent":
        return branch_month_sales_intent_response(intent)

    # Sales - Brand & MonthYear Wise
    elif intent_name == "BDMMYYSLIntent":
        return brand_month_sales_intent_response(intent)

    # Outstanding - Branch Outstanding Till today
    elif intent_name == "BNCHAFOTIntent":
        return branch_outstanding_intent_response(intent)

    # Outstanding - Total
    elif intent_name == "OutstandingIntent":
        return outstanding_intent_response()

    elif intent_name == "AMAZON.HelpIntent":
        return get_welcome_response()

    elif intent_name == "AMAZON.CancelIntent" or intent_name == "AMAZON.StopIntent":
        return handle_session_end_request()

    else:
        raise ValueError("Invalid intent")
def on_session_ended(session_ended_request, session):
    """ Called when the user ends the session.
    Is not called when the skill returns should_end_session=true
    """
    print("on_session_ended requestId=" + session_ended_request['requestId'] +
          ", sessionId=" + session['sessionId'])
    # add cleanup logic here

# --------------- Main handler -------------------------------------------------


def lambda_handler(event, context):
    """ Route the incoming request based on type (LaunchRequest, IntentRequest,
    etc.) The JSON body of the request is provided in the event parameter.
    """
    print("Incoming requests ...")

    """
    Uncomment this if statement and populate with your skill's application ID to
    prevent someone else from configuring a skill that sends requests to this
    function.
    """
    # if (event['session']['application']['applicationId'] !=
    #         "amzn1.echo-sdk-ams.app.[unique-value-here]"):
    #     raise ValueError("Invalid Application ID")

    # if event['session']['new']:
    #     on_session_started({'requestId': event['request']['requestId']},event['session'])

    # if event['request']['type'] == "LaunchRequest":
    #     return on_launch(event['request'], event['session'])
    # elif event['request']['type'] == "IntentRequest":
    #     return on_intent(event['request'], event['session'])
    # elif event['request']['type'] == "SessionEndedRequest":
    #     return on_session_ended(event['request'], event['session'])
        
    if ('session' in event):
        print("event.session.application.applicationId=" +
              event['session']['application']['applicationId'])
        if event['session']['new']:
            on_session_started({'requestId': event['request']['requestId']},
                           event['session'])
    if ('request' in event):                       
        if event['request']['type'] == "LaunchRequest":
            return on_launch(event['request'], event['session'])
        elif event['request']['type'] == "IntentRequest":
            return on_intent(event['request'], event['session'])
        elif event['request']['type'] == "SessionEndedRequest":
            return on_session_ended(event['request'], event['session'])        
