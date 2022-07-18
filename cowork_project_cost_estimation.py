import pandas as pd
import random
from bank_statement_process import pre_processed
import xlrd

def project_one_time_costs():
    one_time_costs = reference_table.loc[reference_table["Periodicity"] == "one-time"]
    one_time_costs.reset_index(drop=True, inplace=True)
    for item in range(len(one_time_costs)):
        #print(item)
        a = input("Zadaj množstvo " + one_time_costs["object"][item])
        one_time_costs.at[item,"Amount"] = float(a)
    return(one_time_costs)

def project_monthly_residuals(column):
    return(reference_table.loc[reference_table[str(column)] == "month"])
    #return pd.concat([reference_table,another_month],axis=0,ignore_index=True)

def project_quarterly_residuals(month):
    if month % 3 == 0:
        return(reference_table.loc[reference_table["Periodicity"] == "quarter"])
        #return pd.concat([reference_table,quarterly_costs], axis=0,ignore_index=True)

def project_yearly_residuals(month):        
    if month % 12 == 0:
        return(reference_table.loc[reference_table["Periodicity"] == "yearly"])
        #return pd.concat([reference_table,yearly_costs], axis=0,ignore_index=True)

def project_cog_produced(obdobie):
    #Divides demand_table on individual monthly demands for particular products
    NEx_demanded = demand_table.loc[demand_table["Product"]=="NEx"]
    NEx_demanded.reset_index(drop=True, inplace=True)
    NIn_demanded = demand_table.loc[demand_table["Product"]=="NIn"]
    NIn_demanded.reset_index(drop=True, inplace=True)
    P3_demanded = demand_table.loc[demand_table["Product"]=="P3"]
    P3_demanded.reset_index(drop=True, inplace=True)

    #Load a share of individual products on overall production in defined month/period (obdobie)
    worksheet = workbook.sheet_by_name("O"+str(obdobie))
    NEx_share_of_demand = float(worksheet.cell(12, 6).value)#share of Product1
    NIn_share_of_demand = float(worksheet.cell(13, 6).value)#share of Product2
    P3_share_of_demand = float(worksheet.cell(14, 6).value)#share of Product3

    #Converts string from table on TOTAL price (float) of production in regression table
    BreakEven_prices = []
    for string in production_regression["Demand from customer/s (in EUR)"]:
        BreakEven_prices.append(float(string.replace(',','')))

    #Adds shares of TOTAL production to lists of individual products
    NEx_produced = []
    NIn_produced = []
    P3_produced = []
    for price in BreakEven_prices:
        NEx_produced.append(price * NEx_share_of_demand)
        NIn_produced.append(price * NIn_share_of_demand)
        P3_produced.append(price * P3_share_of_demand)

    #Creates DataFrame from prices of production for individual products
    data = {"object":["NEx", "NIn", "P3"],
    "Periodicity":["on-demand", "on-demand", "on-demand"],
    "Price per Unit": [NEx_produced[obdobie]/float(NEx_demanded["Q (in Units)"][obdobie].replace(',','')),
    NIn_produced[obdobie]/float(NIn_demanded["Q (in Units)"][obdobie].replace(',','')),
    P3_produced[obdobie]/float(P3_demanded["Q (in Units)"][obdobie].replace(',',''))],
    "Amount": [NEx_demanded["Q (in Units)"][obdobie],NIn_demanded["Q (in Units)"][obdobie],P3_demanded["Q (in Units)"][obdobie]]}
    
    return(pd.DataFrame(data))