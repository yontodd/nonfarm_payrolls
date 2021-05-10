# -*- coding: utf-8 -*-
"""BLS - Nonfarm payrolls.ipynb

# Monthly Nonfarm Payrolls Data
"""

import pandas as pd
import numpy as np
import requests

report_series = "CES0000000001" # Total nonfarm employment
base_url = 'https://api.bls.gov/publicAPI/v1/timeseries/data/'
series = {'id':report_series,
          'name':"Total nonfarm employment"}
data_url = '{}{}'.format(base_url,series['id'])
print(data_url)
data = requests.get(data_url).json()

"""# Test connection"""

print('Status: ' + data['status'])

"""# Inputs **Before** report"""

report_series = "CES0000000001" # Total nonfarm employment
base_url = 'https://api.bls.gov/publicAPI/v1/timeseries/data/'
series = {'id':report_series,
          'name':"Total nonfarm employment"}
data_url = '{}{}'.format(base_url,series['id'])
data = requests.get(data_url).json()
data = data["Results"]["series"][0]["data"]

payrolls = pd.DataFrame(data[0:14])
payrolls["period"] = payrolls["period"].map(lambda x: x.lstrip("M"))
payrolls["value"] = payrolls["value"].map(lambda x: int(x))
payrolls["payrolls_chg"] = payrolls["value"].diff(periods = -1)
payrolls = payrolls[0:13]
payrolls["payrolls_chg"] = payrolls["payrolls_chg"].map(lambda x: int(x))
payrolls = payrolls.drop(columns = ["footnotes"])

# Enter before report print
prior1 = int(input("{} print (in Ks, before revision): ".format(payrolls["periodName"][1])))
prior2 = int(input("{} print (in Ks, before revision): ".format(payrolls["periodName"][2])))
payrolls_estimate = int(input("{} headlines payrolls consensus estimate (in Ks): ".format(payrolls["periodName"][0])))

def conditions(df, df_chg_col):
  conditions = [
    (df_chg_col > 0),
    (df_chg_col == 0),
    (df_chg_col < 0)
  ]
  values = ["up", "unchanged", "down"]
  col_name = list(payrolls.columns)[-1] + "_up_down"
  df[col_name] = np.select(conditions,values)

conditions(payrolls, payrolls["payrolls_chg"])

print(payrolls)

headline_nfp = int(payrolls["payrolls_chg"][0])

def payrolls_statement(headline_nfp, payrolls_estimate):
  if headline_nfp > payrolls_estimate:
    print("{} nonfarm payrolls were {} {}K, beating estimates for {}K.".format(payrolls["periodName"][0], payrolls["payrolls_chg_up_down"][0],headline_nfp, payrolls_estimate))
  else:
    print("{} nonfarm payrolls were {} {}K, missing estimates for {}K.".format(payrolls["periodName"][0], payrolls["payrolls_chg_up_down"][0],headline_nfp,payrolls_estimate))

payrolls_rev1 = int(payrolls["payrolls_chg"][1])
payrolls_rev2 = int(payrolls["payrolls_chg"][2])
total_revision = (payrolls_rev1 - prior1) + (payrolls_rev2 - prior2)

def revision_statement(prior1, prior2):
  if payrolls_rev1 > prior1:
    print("{} was revised up {}K to {}K".format(payrolls["periodName"][1], abs((payrolls_rev1 - prior1)), payrolls_rev1))
  elif payrolls_rev1 < prior1:
    print("{} was revised down {}K to {}K".format(payrolls["periodName"][1], abs((payrolls_rev1 - prior1)), payrolls_rev1))
  elif payrolls_rev1 - prior1 == 0:
    print("{} was unrevised at {}K".format(payrolls["periodName"][1], payrolls_rev1))

  if payrolls_rev2 > prior2:
    print("{} was revised up {}K to {}K".format(payrolls["periodName"][2], abs((payrolls_rev2 - prior2)), payrolls_rev2))
  elif payrolls_rev2 < prior2:
    print("{} was revised down {}K to {}K".format(payrolls["periodName"][1], abs((payrolls_rev2 - prior2)), payrolls_rev2))
  elif payrolls_rev2 - prior2 == 0:
    print("{} was unrevised at {}K".format(payrolls["periodName"][1], payrolls_rev1))
  
  if total_revision > 0:
    print("Prior two months were revised up {}K".format(abs(total_revision)))
  elif total_revision <0:
    print("Prior two months were revised down {}K".format(abs(total_revision)))

payrolls_statement(headline_nfp, payrolls_estimate)
revision_statement(prior1, prior2)
