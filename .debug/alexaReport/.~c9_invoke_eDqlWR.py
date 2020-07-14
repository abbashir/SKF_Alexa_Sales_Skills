import json
import boto3
import pandas as pd
import pytz
from datetime import datetime

# S3 Bucket Selector
bucket_name = 's3://erpalexa/'

bucket_fixed = 's3://skffixed/'
bucket_primary = 's3://skfliveprimary/'
bucket_secondary = 's3://skflivesecondary/'

bucket_live = 's3://skfliveprimary/'

# SELECT LIVE BUCKET
try:
    client = boto3.resource('dynamodb')
    table = client.Table("alexa_status")
    response = table.get_item(Key={'id': 1})
    status = response['Item']['status']
    status = int(status)
    upload_time = response['Item']['upload_end_time']
    
    
    now = datetime.now()
    fmt = '%Y-%m-%d %H:%M:%S'
    upload_end_time = datetime.strptime(upload_time, fmt)
    
    now_time = now.strftime(fmt)
    now_time = datetime.strptime(upload_end_time, fmt)
    
    time_delta = (now_time - upload_end_time)
    total_seconds = time_delta.total_seconds()
    minutes = total_seconds / 60
    
    print("Time Diff: ",minutes)

    
  
  
    
    

    print('bucket status: ' , status)
    
    if status == 1:
        bucket_live = bucket_primary
    else:
        bucket_live = bucket_secondary
except:
    bucket_live = bucket_secondary

print('Live bucket name: '+ bucket_live)

# -----------------------Function for own library ------------------------------
def get_time_stamp():
    client = boto3.client('s3')
    path = bucket_live + 'TimeStamp.xlsx'
    df = pd.read_excel(path, header=None)
    utime = str((df.loc[1, 0]))
    return str((df.loc[1, 0]))

print(get_time_stamp())

def get_days_of_month(month, year):
    if (int(year) % 4) == 0:
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
        unit = str(string[0:len(string) - 7] + " crore " + string[len(string) - 7:len(string) - 5] + " lakh ")
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
        return value


# ------------------------------Global Variables -------------------------------
startTime = 9
now = datetime.now()
currentTime = (int(str(now.strftime('%H:%M:%S'))[0:2])) + 7
endTime = 21
format = '%H:%M:%S'
salesDuration = currentTime - startTime
salesHour = endTime - startTime
trendTime = (salesHour / salesDuration)
year = str(pd.datetime.today())[0:4]
month = str(pd.datetime.today())[5:7]
yearmonth = get_year(year) + get_month(month)
days = get_days_of_month(month, year)
today = int(datetime.today().day)

# ---------------------Function that returns data from excel -------------------


# ********OVER ALL SALES START**************************************************
# Sales - Overall Live
def get_sales():
    client = boto3.client('s3')
    path = bucket_live +'BranchSales.xlsx'
    data = pd.read_excel(path)
    sales = data['sales'].sum()
    return sales

# Sales - MTD
def get_mtd_sales():
    global yearmonth
    client = boto3.client('s3')
    path = bucket_fixed + 'NSM' + str(yearmonth) + 'Sales.xlsx'
    data = pd.read_excel(path)
    sales = data['sales'].sum()
    sales = sales + get_sales() # mtd sales = fixed_bucket_sale + live_sales
    return sales
    

# Sales - YTD
def get_ytd_sales():
    global year
    client = boto3.client('s3')
    path = bucket_fixed + 'Branch' + str(year) + 'Sales.xlsx'
    data = pd.read_excel(path)
    sales = data['sales'].sum()
    sales = sales + get_sales() # ytd sales = fixed_bucket_sale + live_sales
    return sales
   
# Traget - Overall terget
def get_mTarget():
    global yearmonth
    path = bucket_fixed + 'BranchTarget.xlsx'
    data = pd.read_excel(path)
    target = int(data.loc[data['yearmonth'] == yearmonth, "target"].sum())
    
    if target == 0 :
          target = int(data.loc[data['yearmonth'] == yearmonth-1, "target"].sum())
    return target
    
# ********OVER ALL SALES END****************************************************





# ********BRANCH WISE SALES START***********************************************

# Sales - Branch wise live
def get_branch_sales(branch):
    client = boto3.client('s3')
    path = bucket_live + 'BranchSales.xlsx'
    data = pd.read_excel(path)
    sales = data.loc[data.branch == branch, "sales"].sum()
    return sales


# Sales - MTD wise
def get_branch_mtd_sales(branch):
    global yearmonth
    client = boto3.client('s3')
    path = bucket_fixed + 'Branch' + str(yearmonth) + 'Sales.xlsx'
    data = pd.read_excel(path)
    sales = data.loc[data.branch == branch, "sales"].sum()
    sales = sales + get_branch_sales(branch) # mtd sales = fixed_bucket_sale + live_sales
    return sales
    
    
# Sales - YTD Sales
def get_branch_ytd_sales(branch):
    global year
    client = boto3.client('s3')
    path = bucket_fixed + 'Branch' + str(year) + 'Sales.xlsx'
    data = pd.read_excel(path)
    sales = data.loc[data.branch == branch, "sales"].sum()
    sales = sales + get_branch_sales(branch) # ytd sales = fixed_bucket_sale + live_sales
    return sales

# Sales - Branch & YearMonth Wise Sales
def get_branch_month_sales(branch, year_month):
    date = year_month
    yearmonth = int(date)
    client = boto3.client('s3')
    path = bucket_fixed + 'Branch' + str(date) + 'Sales.xlsx'
    data = pd.read_excel(path)
    sales = data.loc[data.branch == branch, "sales"].sum()
    return sales    
    
# Traget - Branches Monthly
def get_branch_mTarget(branch):
    global yearmonth
    path = bucket_fixed + 'BranchTarget.xlsx'
    data = pd.read_excel(path)
    mTarget = int(data.loc[(data['branch'] == branch) & (data['yearmonth'] == yearmonth), "target"].sum())
    if mTarget == 0 :
          mTarget = int(data.loc[(data['branch'] == branch) & (data['yearmonth'] == yearmonth-1), "target"].sum())
    return mTarget
    

# ********BRANCH WISE SALES END*************************************************




# ********BRAND WISE SALES START************************************************

# Sales - Brand wise live sales
def get_brand_sales(brand):
    path = bucket_live + 'BranchSales.xlsx'
    data = pd.read_excel(path)
    sales = data.loc[data.brand == brand, "sales"].sum()
    return sales
#     print(sales)
# get_brand_sales('Alben')    


# Sales - Branch & Brand wise sales
def get_branch_brand_sales(branch, brand):
    client = boto3.client('s3')
    path = bucket_live + 'BranchSales.xlsx'
    data = pd.read_excel(path)
    sales = data.loc[(data['branch'] == branch) & (data['brand'] == brand), "sales"].sum()
    return sales


# Sales - Brand & YearMonth Wise Sales
def get_brand_month_sales(brand, year_month):
    date = year_month
    yearmonth = int(date)
    client = boto3.client('s3')
    path = bucket_fixed + 'Branch' + str(date) + 'Sales.xlsx'
    data = pd.read_excel(path)
    sales = data.loc[data.brand == brand, "sales"].sum()
    return sales


# Sales - Branch, Brand & YearMonth Wise sales
def get_branch_brand_month_sales(branch, brand, year_month):
    date = year_month
    yearmonth = int(date)
    client = boto3.client('s3')
    path = bucket_fixed + 'Branch' + str(date) + 'Sales.xlsx'
    data = pd.read_excel(path)
    sales = data.loc[(data['branch'] == branch) & (data['brand'] == brand), "sales"].sum()
    return sales
    
# BRAND wise Sales in Box
def today_brand_sales_in_box(brand):
    client = boto3.client('s3')
    path = bucket_live + 'BrandwiseSales.xlsx'
    data = pd.read_excel(path)
    sales = data.loc[data.brand == brand, "sales"].sum()
    return sales   
#     print( sales)
#     print("----")
# today_brand_sales_in_box('Losectil')

# Traget - BRAND Monthly Target in Box
def monthly_brand_target_in_box(brand):
    client = boto3.client('s3')
    path = bucket_fixed + 'BrandwiseTarget.xlsx'
    data = pd.read_excel(path)
    target = data.loc[data.brand == brand, "target"].sum()
    return target
    
#     print(target)
# monthly_brand_target_in_box('Losectil')
    
    
    
# ********BRAND WISE SALES START************************************************




# ********NSM WISE SALES START**************************************************

# Sales - NSM wise live
def get_nsm_sales(nsmid):
    client = boto3.client('s3')
    path = bucket_live + 'NSMSales.xlsx'
    data = pd.read_excel(path)
    sales = data.loc[data.nsmid == nsmid, "sales"].sum()
    return sales
    # print(sales)


# Sales - NSM MTD sales
def get_nsm_mtd_sales(nsmid):
    global yearmonth
    client = boto3.client('s3')
    path = bucket_fixed + 'NSM' + str(yearmonth) + 'Sales.xlsx'
    data = pd.read_excel(path)
    sales = data.loc[data.nsmid == nsmid, "sales"].sum()
    sales = sales + get_nsm_sales(nsmid) # mtd = fixed + live
    return sales


# Sales - NSM YTD sales
def get_nsm_ytd_sales(nsmid):
    global yearmonth
    client = boto3.client('s3')
    path = bucket_fixed + 'NSM' + str(year) + 'Sales.xlsx'
    data = pd.read_excel(path)
    sales = data.loc[data.nsmid == nsmid, "sales"].sum()
    sales = sales + get_nsm_sales(nsmid) # mtd = fixed + live
    return sales


# Sales - NSM & YearMonth Wise
def get_nsm_month_sales(nsmid, year_month):
    date = year_month
    yearmonth = int(date)
    client = boto3.client('s3')
    path = bucket_fixed + 'NSM' + str(date) + 'Sales.xlsx'
    data = pd.read_excel(path)
    sales = data.loc[data.nsmid == nsmid, "sales"].sum()
    return sales


# Sales - NSM & Brand wise live sales
def get_nsm_brand_sales(nsmid, brand):
    client = boto3.client('s3')
    path = bucket_live + 'NSMSales.xlsx'
    data = pd.read_excel(path)
    sales = data.loc[(data['nsmid'] == nsmid) & (data['brand'] == brand), "sales"].sum()
    return sales


# Sales - NSM & Brand MTD sales
def get_nsm_brand_mtd_sales(nsmid, brand):
    global yearmonth
    client = boto3.client('s3')
    path = bucket_fixed + 'NSM' + str(yearmonth) + 'Sales.xlsx'
    data = pd.read_excel(path)
    sales = data.loc[(data['nsmid'] == nsmid) & (data['brand'] == brand), "sales"].sum()
    sales = sales + get_nsm_brand_sales(nsmid, brand) # sales = fixed + live
    return sales


# Sales - NSM & Brand YTD sales
def get_nsm_brand_ytd_sales(nsmid, brand):
    global year
    client = boto3.client('s3')
    path = bucket_fixed + 'NSM' + str(year) + 'Sales.xlsx'
    data = pd.read_excel(path)
    sales = data.loc[(data['nsmid'] == nsmid) & (data['brand'] == brand), "sales"].sum()
    sales = sales + get_nsm_brand_sales(nsmid, brand) # sales = fixed + live
    return sales


# Sales - NSM , Brand & YearMonth Wise Sales
def get_nsm_brand_month_sales(nsmid, brand, year_month):
    date = year_month
    yearmonth = int(date)
    client = boto3.client('s3')
    path = bucket_fixed + 'NSM' + str(date) + 'Sales.xlsx'
    data = pd.read_excel(path)
    sales = data.loc[(data['nsmid'] == nsmid) & (data['brand'] == brand), "sales"].sum()
    return sales
    

# Traget - NSM Monthly
def get_nsm_mTarget(nsmid):
    global yearmonth

    path = bucket_fixed + 'FieldForce.xlsx'
    data = pd.read_excel(path)
    mTarget = int(data.loc[(data['NSMID'] == nsmid) & (data['yearmonth'] == yearmonth), "target"].sum())
    if mTarget == 0:
        mTarget = int(data.loc[(data['NSMID'] == nsmid) & (data['yearmonth'] == yearmonth - 1), "target"].sum())

    return mTarget

    
# ********NSM WISE SALES END****************************************************





# ********RSM WISE SALES START**************************************************

# Sales - RSM wise
def get_rsm_sales(rsmid):
    client = boto3.client('s3')
    path = bucket_live + 'RSMSales.xlsx'
    data = pd.read_excel(path)
    sales = data.loc[data.rsmid == rsmid, "sales"].sum()
    return sales


# Sales - RSM MTD sales
def get_rsm_mtd_sales(rsmid):
    global yearmonth
    client = boto3.client('s3')
    path = bucket_fixed + 'RSM' + str(yearmonth) + 'Sales.xlsx'
    data = pd.read_excel(path)
    sales = data.loc[data.rsmid == rsmid, "sales"].sum()
    sales = sales + get_rsm_sales(rsmid) # sales = fixed + live
    return sales


# Sales - RSM YTD sales
def get_rsm_ytd_sales(rsmid):
    global year
    client = boto3.client('s3')
    path = bucket_fixed + 'RSM' + str(year) + 'Sales.xlsx'
    data = pd.read_excel(path)
    sales = data.loc[data.rsmid == rsmid, "sales"].sum()
    sales = sales + get_rsm_sales(rsmid) # sales = fixed + live
    return sales


# Sales - RSM & YearMonth Wise Sales
def get_rsm_month_sales(rsmid, year_month):
    date = year_month
    yearmonth = int(date)
    client = boto3.client('s3')
    path = bucket_fixed + 'RSM' + str(date) + 'Sales.xlsx'
    data = pd.read_excel(path)
    sales = data.loc[data.rsmid == rsmid, "sales"].sum()
    return sales


# Sales - RSM & Brand wise sales
def get_rsm_brand_sales(rsmid, brand):
    client = boto3.client('s3')
    path = bucket_live + 'RSMSales.xlsx'
    data = pd.read_excel(path)
    sales = data.loc[(data['rsmid'] == rsmid) & (data['brand'] == brand), "sales"].sum()
    return sales


# Sales - RSM & Brand MTD sales
def get_rsm_brand_mtd_sales(rsmid, brand):
    global yearmonth
    client = boto3.client('s3')
    path = bucket_fixed + 'RSM' + str(yearmonth) + 'Sales.xlsx'
    data = pd.read_excel(path)
    sales = data.loc[(data['rsmid'] == rsmid) & (data['brand'] == brand), "sales"].sum()
    sales = sales + get_rsm_brand_sales(rsmid, brand) # sales = fixed + live
    return sales


# Sales - RSM & Brand YTD sales
def get_rsm_brand_ytd_sales(rsmid, brand):
    global year
    client = boto3.client('s3')
    path = bucket_fixed + 'RSM' + str(year) + 'Sales.xlsx'
    data = pd.read_excel(path)
    sales = data.loc[(data['rsmid'] == rsmid) & (data['brand'] == brand), "sales"].sum()
    sales = sales + get_rsm_brand_sales(rsmid, brand) # sales = fixed + live
    return sales


# Sales - RSM , Brand & YearMonth Wise Sales
def get_rsm_brand_month_sales(rsmid, brand, year_month):
    date = year_month
    yearmonth = int(date)
    client = boto3.client('s3')
    path = bucket_fixed + 'RSM' + str(date) + 'Sales.xlsx'
    data = pd.read_excel(path)
    sales = data.loc[(data['rsmid'] == rsmid) & (data['brand'] == brand), "sales"].sum()
    return sales
    
    
# Traget - RSM Monthly
def get_rsm_mTarget(rsmid):
    global yearmonth
    path = bucket_fixed + 'FieldForce.xlsx'
    data = pd.read_excel(path)
    mTarget = int(data.loc[(data['RSMID'] == rsmid) & (data['yearmonth'] == yearmonth), "target"].sum())
    if mTarget == 0 :
        mTarget = int(data.loc[(data['RSMID'] == rsmid) & (data['yearmonth'] == yearmonth-1), "target"].sum())
    return mTarget
    
    
# ********RSM WISE SALES END**************************************************




# ********FM WISE SALES START**************************************************

# Sales - FM wise live
def get_fm_sales(fmid):
    client = boto3.client('s3')
    path = bucket_live + 'FMSales.xlsx'
    data = pd.read_excel(path)
    sales = data.loc[data.fmid == fmid, "sales"].sum()
    return sales


# Sales - FM MTD sales
def get_fm_mtd_sales(fmid):
    global yearmonth
    client = boto3.client('s3')
    path = bucket_fixed + 'FM' + str(yearmonth) + 'Sales.xlsx'
    data = pd.read_excel(path)
    sales = data.loc[data.fmid == fmid, "sales"].sum()
    sales = sales + get_fm_sales(fmid) # sales = fixed + live
    return sales


# Sales - FM YTD sales
def get_fm_ytd_sales(fmid):
    global year
    client = boto3.client('s3')
    path = bucket_fixed + 'FM' + str(year) + 'Sales.xlsx'
    data = pd.read_excel(path)
    sales = data.loc[data.fmid == fmid, "sales"].sum()
    sales = sales + get_fm_sales(fmid) # sales = fixed + live
    return sales


# Sales - FM & YearMonth Wise Sales
def get_fm_month_sales(fmid, year_month):
    date = year_month
    yearmonth = int(date)
    client = boto3.client('s3')
    path = bucket_fixed + 'FM' + str(date) + 'Sales.xlsx'
    data = pd.read_excel(path)
    sales = data.loc[data.fmid == fmid, "sales"].sum()
    return sales


# Sales - FM & Brand wise live sales
def get_fm_brand_sales(fmid, brand):
    client = boto3.client('s3')
    path = bucket_live + 'FMSales.xlsx'
    data = pd.read_excel(path)
    sales = data.loc[(data['fmid'] == fmid) & (data['brand'] == brand), "sales"].sum()
    return sales


# Sales - FM & Brand mtd sales
def get_fm_brand_mtd_sales(fmid, brand):
    global yearmonth
    client = boto3.client('s3')
    path = bucket_fixed + 'FM' + str(yearmonth) + 'Sales.xlsx'
    data = pd.read_excel(path)
    sales = data.loc[(data['fmid'] == fmid) & (data['brand'] == brand), "sales"].sum()
    sales = sales + get_fm_brand_sales(fmid, brand) # sales = fixed + live
    return sales


# Sales - FM & Brand ytd sales
def get_fm_brand_ytd_sales(fmid, brand):
    global year
    client = boto3.client('s3')
    path = bucket_fixed + 'FM' + str(year) + 'Sales.xlsx'
    data = pd.read_excel(path)
    sales = data.loc[(data['fmid'] == fmid) & (data['brand'] == brand), "sales"].sum()
    sales = sales + get_fm_brand_sales(fmid, brand) # sales = fixed + live
    return sales


# Sales - FM , Brand & YearMonth Wise Sales
def get_fm_brand_month_sales(fmid, brand, year_month):
    date = year_month
    yearmonth = int(date)
    client = boto3.client('s3')
    path = bucket_fixed + 'FM' + str(date) + 'Sales.xlsx'
    data = pd.read_excel(path)
    sales = data.loc[(data['fmid'] == fmid) & (data['brand'] == brand), "sales"].sum()
    return sales
    
# Traget - FM Monthly
def get_fm_mTarget(fmid):
    global yearmonth
    path = bucket_fixed + 'FieldForce.xlsx'
    data = pd.read_excel(path)
    mTarget = int(data.loc[(data['FMID'] == fmid) & (data['yearmonth'] == yearmonth), "target"].sum())
    if mTarget == 0 :
        mTarget = int(data.loc[(data['FMID'] == fmid) & (data['yearmonth'] == yearmonth-1), "target"].sum())
    return mTarget    
    
# ********FM WISE SALES END**************************************************



# Stock - Branch wise
def get_branch_stock(branch):
    client = boto3.client('s3')
    path = bucket_live + 'Stock.xlsx'
    data = pd.read_excel(path)
    rows = data['branch'].tolist()
    y = rows.index(branch)
    stock = data.iloc[y, 2]
    return stock


# Outstanding - All Branch
def get_outstanding():
    client = boto3.client('s3')
    path = bucket_live + 'BranchOutstanding.xlsx'
    data = pd.read_excel(path)
    sales = data['outstanding'].sum()
    return sales


# Outstanding - Branch wise
def get_branch_outstanding(branch):
    client = boto3.client('s3')
    path = bucket_live + 'BranchOutstanding.xlsx'
    data = pd.read_excel(path)
    sales = data.loc[data.branch == branch, "outstanding"].sum()
    return sales




# Traget - Branches yearly
def get_branch_yTarget(branch):
    global year
    path = bucket_name + 'BranchTarget.xlsx'
    data = pd.read_excel(path)
    yTarget = int(data.loc[(data['branch'] == branch) & (data['yearmonth'] >= get_year(year)), "target"].sum())
    return yTarget



# Traget - NSM yearly
def get_nsm_yTarget(nsmid):
    global year
    path = bucket_name + 'FieldForce.xlsx'
    data = pd.read_excel(path)
    yTarget = int(data.loc[(data['nsmid'] == nsmid) & (data['yearmonth'] >= get_year(year)), "target"].sum())
    return yTarget




# Traget - RSM yearly
def get_rsm_yTarget(rsmid):
    global year
    path = bucket_name + 'FieldForce.xlsx'
    data = pd.read_excel(path)
    yTarget = int(data.loc[(data['rsmid'] == rsmid) & (data['yearmonth'] >= get_year(year)), "target"].sum())
    return yTarget





# Traget - FM yearly
def get_fm_yTarget(fmid):
    global year
    path = bucket_name + 'FieldForce.xlsx'
    data = pd.read_excel(path)
    yTarget = int(data.loc[(data['fmid'] == fmid) & (data['yearmonth'] >= get_year(year)), "target"].sum())
    return yTarget