class Projection:
    def __init__(self,ref_tab,dem_tabl,wb,reg_tabl):
        self.reference_table = ref_tab
        self.demand_table = dem_tabl
        self.workbook = wb
        self.regression = reg_tabl
        #self.indirect_costs = {}
        #self.direct_costs = {}
    
    def periodical_projection(self,period):
        base = self.reference_table
        initial_period = base
        quarterly = initial_period.loc[initial_period["Periodicity"] == "quarter"]
        yearly = initial_period.loc[initial_period["Periodicity"] == "yearly"]
        monthly = initial_period.loc[initial_period["Periodicity"] == "month"]
        one_time_costs = reference_table.loc[reference_table["Periodicity"] == "one-time"]
        one_time_costs.reset_index(drop=True, inplace=True)

        local_var = initial_period
        for i in range(int(period)):
            
            if i == 0:
                print(i,"iteration which == 0")
            #MONTHLY RESIDUAL COSTS 
            elif i != 0: #or i % 3 == 0 or i % 12 == 0:
                print(i,"iteration which != 0")
                monthly.append(monthly) 
                local_var = pd.concat([local_var,monthly])
                
                if i % 3 == 0:
                    print(i,"True 3")
                    quarterly.append(local_var.loc[local_var["Periodicity"] == "quarter"])
                    local_var = pd.concat([local_var,quarterly])
                    
                if i % 12 == 0:
                    yearly.append(local_var.loc[local_var["Periodicity"] == "yearly"])
                    local_var = pd.concat([local_var,yearly])
                    print(i,"True 12")
            else:
                print("Condition finished")
                    
            #ONE-TIME COSTS
            print("Condition finished 1")
            if i != 0:    
                iteration_onetime_costs = one_time_costs
                for j in range(len(one_time_costs)):
                    b = input("Zadaj množstvo " + one_time_costs["object"][j])
                    print(f"Zadané množstvo je {b}")
                    one_time_costs.at[j,"Amount"] = int(b)
                    iteration_onetime_costs = pd.concat([one_time_costs])
                output = pd.concat([iteration_onetime_costs,local_var])
            else:
                output = local_var
                
            local_var = output
            indirect_costs = local_var[local_var["Amount"]>0]
            indirect_costs.reset_index(drop=True, inplace=True)

        return(indirect_costs)