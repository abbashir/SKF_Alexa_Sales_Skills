import json
import boto3
import pandas as pd
import datetime

# S3 Bucket Selector
bucket_name = 's3://erpalexa/'

bucket_fixed = 's3://skffixed/'
bucket_primary = 's3://skfliveprimary/'
bucket_secondary = 's3://skflivesecondary/'

bucket_live = 's3://erpalexa/'

# SELECT LIVE BUCKET
try:
  client = boto3.client('s3')
  path = bucket_primary + 'flag_status.xlsx'
  df = pd.read_excel(path, header=None)
  status =  str((df.loc[0, 0]))
  print('status: '+status)
  if status == '0' :
      bucket_live = bucket_primary
  else:
     bucket_live = bucket_secondary
except:
  bucket_live = bucket_secondary

print('Live bucket : '+bucket_live)

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
days = get_days_of_month(month, year)
today = int(datetime.datetime.today().day)

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
    path = bucket_name + 'NSM' + str(yearmonth) + 'Sales.xlsx'
    data = pd.read_excel(path)
    sales = data['sales'].sum()
    return sales


# Sales - YTD
def get_ytd_sales():
    global year
    client = boto3.client('s3')
    path = bucket_name + 'Branch' + str(year) + 'Sales.xlsx'
    data = pd.read_excel(path)
    sales = data['sales'].sum()
    return sales
    
# Traget - Overall terget
def get_mTarget():
    global yearmonth
    path = bucket_name + 'BranchTarget.xlsx'
    data = pd.read_excel(path)
    target = int(data.loc[data['yearmonth'] == yearmonth, "target"].sum())
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
    path = bucket_name + 'Branch' + str(yearmonth) + 'Sales.xlsx'
    data = pd.read_excel(path)
    sales = data.loc[data.branch == branch, "sales"].sum()
    return sales


# Sales - YTD Sales
def get_branch_ytd_sales(branch):
    global year
    client = boto3.client('s3')
    path = bucket_name + 'Branch' + str(year) + 'Sales.xlsx'
    data = pd.read_excel(path)
    sales = data.loc[data.branch == branch, "sales"].sum()
    return sales
    
# Traget - Branches Monthly
def get_branch_mTarget(branch):
    global yearmonth
    path = bucket_name + 'BranchTarget.xlsx'
    data = pd.read_excel(path)
    mTarget = int(data.loc[(data['branch'] == branch) & (data['yearmonth'] == yearmonth), "target"].sum())
    return mTarget
    

# ********BRANCH WISE SALES END*************************************************




# ********BRAND WISE SALES START************************************************

# Sales - Brand wise live sales
def get_brand_sales(brand):
    client = boto3.client('s3')
    path = bucket_live + 'BranchSales.xlsx'
    data = pd.read_excel(path)
    sales = data.loc[data.brand == brand, "sales"].sum()
    return sales


# Sales - Branch & Brand wise sales
def get_branch_brand_sales(branch, brand):
    client = boto3.client('s3')
    path = bucket_name + 'BranchSales.xlsx'
    data = pd.read_excel(path)
    sales = data.loc[(data['branch'] == branch) & (data['brand'] == brand), "sales"].sum()
    return sales


# Sales - Branch & YearMonth Wise Sales
def get_branch_month_sales(branch, year_month):
    date = year_month
    yearmonth = int(date)
    client = boto3.client('s3')
    path = bucket_name + 'Branch' + str(date) + 'Sales.xlsx'
    data = pd.read_excel(path)
    sales = data.loc[data.branch == branch, "sales"].sum()
    return sales


# Sales - Brand & YearMonth Wise Sales
def get_brand_month_sales(brand, year_month):
    date = year_month
    yearmonth = int(date)
    client = boto3.client('s3')
    path = bucket_name + 'Branch' + str(date) + 'Sales.xlsx'
    data = pd.read_excel(path)
    sales = data.loc[data.brand == brand, "sales"].sum()
    return sales


# Sales - Branch, Brand & YearMonth Wise sales
def get_branch_brand_month_sales(branch, brand, year_month):
    date = year_month
    yearmonth = int(date)
    client = boto3.client('s3')
    path = bucket_name + 'Branch' + str(date) + 'Sales.xlsx'
    data = pd.read_excel(path)
    sales = data.loc[(data['branch'] == branch) & (data['brand'] == brand), "sales"].sum()
    return sales
    
# ********BRAND WISE SALES START************************************************


# Sales - NSM wise
def get_nsm_sales(nsmid):
    client = boto3.client('s3')
    path = bucket_name + 'NSMSales.xlsx'
    data = pd.read_excel(path)
    sales = data.loc[data.nsmid == nsmid, "sales"].sum()
    return sales


# Sales - NSM MTD sales
def get_nsm_mtd_sales(nsmid):
    global yearmonth
    client = boto3.client('s3')
    path = bucket_name + 'NSM' + str(yearmonth) + 'Sales.xlsx'
    data = pd.read_excel(path)
    sales = data.loc[data.nsmid == nsmid, "sales"].sum()
    return sales


# Sales - NSM YTD sales
def get_nsm_ytd_sales(nsmid):
    global yearmonth
    client = boto3.client('s3')
    path = bucket_name + 'NSM' + str(year) + 'Sales.xlsx'
    data = pd.read_excel(path)
    sales = data.loc[data.nsmid == nsmid, "sales"].sum()
    return sales


# Sales - NSM & YearMonth Wise
def get_nsm_month_sales(nsmid, year_month):
    date = year_month
    yearmonth = int(date)
    client = boto3.client('s3')
    path = bucket_name + 'NSM' + str(date) + 'Sales.xlsx'
    data = pd.read_excel(path)
    sales = data.loc[data.nsmid == nsmid, "sales"].sum()
    return sales


# Sales - NSM & Brand wise sales
def get_nsm_brand_sales(nsmid, brand):
    client = boto3.client('s3')
    path = bucket_name + 'NSMSales.xlsx'
    data = pd.read_excel(path)
    sales = data.loc[(data['nsmid'] == nsmid) & (data['brand'] == brand), "sales"].sum()
    return sales


# Sales - NSM & Brand MTD sales
def get_nsm_brand_mtd_sales(nsmid, brand):
    global yearmonth
    client = boto3.client('s3')
    path = bucket_name + 'NSM' + str(yearmonth) + 'Sales.xlsx'
    data = pd.read_excel(path)
    sales = data.loc[(data['nsmid'] == nsmid) & (data['brand'] == brand), "sales"].sum()
    return sales


# Sales - NSM & Brand YTD sales
def get_nsm_brand_ytd_sales(nsmid, brand):
    global year
    client = boto3.client('s3')
    path = bucket_name + 'NSM' + str(year) + 'Sales.xlsx'
    data = pd.read_excel(path)
    sales = data.loc[(data['nsmid'] == nsmid) & (data['brand'] == brand), "sales"].sum()
    return sales


# Sales - NSM , Brand & YearMonth Wise Sales
def get_nsm_brand_month_sales(nsmid, brand, year_month):
    date = year_month
    yearmonth = int(date)
    client = boto3.client('s3')
    path = bucket_name + 'NSM' + str(date) + 'Sales.xlsx'
    data = pd.read_excel(path)
    sales = data.loc[(data['nsmid'] == nsmid) & (data['brand'] == brand), "sales"].sum()
    return sales


# Sales - RSM wise
def get_rsm_sales(rsmid):
    client = boto3.client('s3')
    path = bucket_name + 'RSMSales.xlsx'
    data = pd.read_excel(path)
    sales = data.loc[data.rsmid == rsmid, "sales"].sum()
    return sales


# Sales - RSM MTD sales
def get_rsm_mtd_sales(rsmid):
    global yearmonth
    client = boto3.client('s3')
    path = bucket_name + 'RSM' + str(yearmonth) + 'Sales.xlsx'
    data = pd.read_excel(path)
    sales = data.loc[data.rsmid == rsmid, "sales"].sum()
    return sales


# Sales - RSM YTD sales
def get_rsm_ytd_sales(rsmid):
    global year
    client = boto3.client('s3')
    path = bucket_name + 'RSM' + str(year) + 'Sales.xlsx'
    data = pd.read_excel(path)
    sales = data.loc[data.rsmid == rsmid, "sales"].sum()
    return sales


# Sales - RSM & YearMonth Wise Sales
def get_rsm_month_sales(rsmid, year_month):
    date = year_month
    yearmonth = int(date)
    client = boto3.client('s3')
    path = bucket_name + 'RSM' + str(date) + 'Sales.xlsx'
    data = pd.read_excel(path)
    sales = data.loc[data.rsmid == rsmid, "sales"].sum()
    return sales


# Sales - RSM & Brand wise sales
def get_rsm_brand_sales(rsmid, brand):
    client = boto3.client('s3')
    path = bucket_name + 'RSMSales.xlsx'
    data = pd.read_excel(path)
    sales = data.loc[(data['rsmid'] == rsmid) & (data['brand'] == brand), "sales"].sum()
    return sales


# Sales - RSM & Brand MTD sales
def get_rsm_brand_mtd_sales(rsmid, brand):
    global yearmonth
    client = boto3.client('s3')
    path = bucket_name + 'RSM' + str(yearmonth) + 'Sales.xlsx'
    data = pd.read_excel(path)
    sales = data.loc[(data['rsmid'] == rsmid) & (data['brand'] == brand), "sales"].sum()
    return sales


# Sales - RSM & Brand YTD sales
def get_rsm_brand_ytd_sales(rsmid, brand):
    global year
    client = boto3.client('s3')
    path = bucket_name + 'RSM' + str(year) + 'Sales.xlsx'
    data = pd.read_excel(path)
    sales = data.loc[(data['rsmid'] == rsmid) & (data['brand'] == brand), "sales"].sum()
    return sales


# Sales - RSM , Brand & YearMonth Wise Sales
def get_rsm_brand_month_sales(rsmid, brand, year_month):
    date = year_month
    yearmonth = int(date)
    client = boto3.client('s3')
    path = bucket_name + 'RSM' + str(date) + 'Sales.xlsx'
    data = pd.read_excel(path)
    sales = data.loc[(data['rsmid'] == rsmid) & (data['brand'] == brand), "sales"].sum()
    return sales


# Sales - FM wise
def get_fm_sales(fmid):
    client = boto3.client('s3')
    path = bucket_name + 'FMSales.xlsx'
    data = pd.read_excel(path)
    sales = data.loc[data.fmid == fmid, "sales"].sum()
    return sales


# Sales - FM MTD sales
def get_fm_mtd_sales(fmid):
    global yearmonth
    client = boto3.client('s3')
    path = bucket_name + 'FM' + str(yearmonth) + 'Sales.xlsx'
    data = pd.read_excel(path)
    sales = data.loc[data.fmid == fmid, "sales"].sum()
    return sales


# Sales - FM YTD sales
def get_fm_ytd_sales(fmid):
    global year
    client = boto3.client('s3')
    path = bucket_name + 'FM' + str(year) + 'Sales.xlsx'
    data = pd.read_excel(path)
    sales = data.loc[data.fmid == fmid, "sales"].sum()
    return sales


# Sales - FM & YearMonth Wise Sales
def get_fm_month_sales(fmid, year_month):
    date = year_month
    yearmonth = int(date)
    client = boto3.client('s3')
    path = bucket_name + 'FM' + str(date) + 'Sales.xlsx'
    data = pd.read_excel(path)
    sales = data.loc[data.fmid == fmid, "sales"].sum()
    return sales


# Sales - FM & Brand wise sales
def get_fm_brand_sales(fmid, brand):
    client = boto3.client('s3')
    path = bucket_name + 'FMSales.xlsx'
    data = pd.read_excel(path)
    sales = data.loc[(data['fmid'] == fmid) & (data['brand'] == brand), "sales"].sum()
    return sales


# Sales - FM & Brand mtd sales
def get_fm_brand_mtd_sales(fmid, brand):
    global yearmonth
    client = boto3.client('s3')
    path = bucket_name + 'FM' + str(yearmonth) + 'Sales.xlsx'
    data = pd.read_excel(path)
    sales = data.loc[(data['fmid'] == fmid) & (data['brand'] == brand), "sales"].sum()
    return sales


# Sales - FM & Brand ytd sales
def get_fm_brand_ytd_sales(fmid, brand):
    global year
    client = boto3.client('s3')
    path = bucket_name + 'FM' + str(year) + 'Sales.xlsx'
    data = pd.read_excel(path)
    sales = data.loc[(data['fmid'] == fmid) & (data['brand'] == brand), "sales"].sum()
    return sales


# Sales - FM , Brand & YearMonth Wise Sales
def get_fm_brand_month_sales(fmid, brand, year_month):
    date = year_month
    yearmonth = int(date)
    client = boto3.client('s3')
    path = bucket_name + 'FM' + str(date) + 'Sales.xlsx'
    data = pd.read_excel(path)
    sales = data.loc[(data['fmid'] == fmid) & (data['brand'] == brand), "sales"].sum()
    return sales


# Stock - Branch wise
def get_branch_stock(branch):
    client = boto3.client('s3')
    path = bucket_name + 'Stock.xlsx'
    data = pd.read_excel(path)
    rows = data['branch'].tolist()
    y = rows.index(branch)
    stock = data.iloc[y, 2]
    return stock


# Outstanding - All Branch
def get_outstanding():
    client = boto3.client('s3')
    path = bucket_name + 'BranchOutstanding.xlsx'
    data = pd.read_excel(path)
    sales = data['outstanding'].sum()
    return sales


# Outstanding - Branch wise
def get_branch_outstanding(branch):
    client = boto3.client('s3')
    path = bucket_name + 'BranchOutstanding.xlsx'
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


# Traget - NSM Monthly
def get_nsm_mTarget(nsmid):
    global yearmonth
    path = bucket_name + 'FieldForce.xlsx'
    data = pd.read_excel(path)
    mTarget = int(data.loc[(data['nsmid'] == nsmid) & (data['yearmonth'] == yearmonth), "target"].sum())
    return mTarget


# Traget - NSM yearly
def get_nsm_yTarget(nsmid):
    global year
    path = bucket_name + 'FieldForce.xlsx'
    data = pd.read_excel(path)
    yTarget = int(data.loc[(data['nsmid'] == nsmid) & (data['yearmonth'] >= get_year(year)), "target"].sum())
    return yTarget


# Traget - RSM Monthly
def get_rsm_mTarget(rsmid):
    global yearmonth
    path = bucket_name + 'FieldForce.xlsx'
    data = pd.read_excel(path)
    mTarget = int(data.loc[(data['rsmid'] == rsmid) & (data['yearmonth'] == yearmonth), "target"].sum())
    return mTarget


# Traget - RSM yearly
def get_rsm_yTarget(rsmid):
    global year
    path = bucket_name + 'FieldForce.xlsx'
    data = pd.read_excel(path)
    yTarget = int(data.loc[(data['rsmid'] == rsmid) & (data['yearmonth'] >= get_year(year)), "target"].sum())
    return yTarget


# Traget - FM Monthly
def get_fm_mTarget(fmid):
    global yearmonth
    path = bucket_name + 'FieldForce.xlsx'
    data = pd.read_excel(path)
    mTarget = int(data.loc[(data['fmid'] == fmid) & (data['yearmonth'] == yearmonth), "target"].sum())
    return mTarget


# Traget - FM yearly
def get_fm_yTarget(fmid):
    global year
    path = bucket_name + 'FieldForce.xlsx'
    data = pd.read_excel(path)
    yTarget = int(data.loc[(data['fmid'] == fmid) & (data['yearmonth'] >= get_year(year)), "target"].sum())
    return yTarget