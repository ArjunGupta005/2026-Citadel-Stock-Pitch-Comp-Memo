"""GEV: reconstruct quarterly FCF from operating components and isolate customer deposits (contract liabilities).

FCF (company definition) = cash from operating activities - additions to PP&E and internal-use software.
Deposit contribution = cash-flow-statement change in contract liabilities (IncreaseDecreaseInContractWithCustomerLiability).
Normalized FCF (zero incremental deposits) = FCF - deposit contribution.
All values from SEC XBRL (first-filed, point-in-time); YTD cash flows differenced into quarters.
Output: framework_B/gev_fcf_decomposition.csv, printed table.
"""

import pandas as pd

from common import ROOT, xbrl_quarterly, xbrl_ytd_quarterly
from valuation_history import instant

T = "GEV"
CF = {
    "ocf": ["NetCashProvidedByUsedInOperatingActivities"],
    "capex": ["PaymentsToAcquireProductiveAssets"],
    "d_contract_liab": ["IncreaseDecreaseInContractWithCustomerLiability"],
    "d_contract_asset": ["IncreaseDecreaseInContractWithCustomerAsset"],
    "d_inventory": ["IncreaseDecreaseInInventories"],
    "d_receivables": ["IncreaseDecreaseInOtherReceivables", "IncreaseDecreaseInAccountsReceivable"],
    "d_payables": ["IncreaseDecreaseInAccountsPayableAndAccruedLiabilities"],
    "d_other_cur_liab": ["IncreaseDecreaseInOtherCurrentLiabilities"],
    "depreciation": ["Depreciation", "DepreciationDepletionAndAmortization"],
    "buybacks": ["PaymentsForRepurchaseOfCommonStock"],
    "dividends": ["PaymentsOfDividends"],
}


def build():
    q = {k: xbrl_ytd_quarterly(T, v)["val"] / 1e9 for k, v in CF.items()}
    df = pd.DataFrame(q)
    df["net_income"] = xbrl_quarterly(T, ["NetIncomeLoss", "ProfitLoss"])["val"] / 1e9
    df["revenue"] = xbrl_quarterly(T, ["Revenues", "RevenueFromContractWithCustomerExcludingAssessedTax"])["val"] / 1e9
    df["op_income"] = xbrl_quarterly(T, ["OperatingIncomeLoss"])["val"] / 1e9
    cl = instant(T, ["ContractWithCustomerLiability"])["val"] / 1e9
    df["contract_liab_bs"] = cl.reindex(df.index)
    df = df.loc["2024-01-01":]
    df["fcf"] = df["ocf"] - df["capex"]
    # sign convention: in XBRL, IncreaseDecreaseIn...Liability is positive when the liability (cash inflow) grows;
    # IncreaseDecreaseIn...Asset / Inventories / Receivables are positive when the asset grows (cash outflow).
    df["deposit_contrib"] = df["d_contract_liab"]
    df["fcf_ex_deposits"] = df["fcf"] - df["deposit_contrib"]
    df["deposit_share_of_fcf"] = df["deposit_contrib"] / df["fcf"]
    df["bs_check_d_contract_liab"] = df["contract_liab_bs"].diff()
    return df


if __name__ == "__main__":
    d = build()
    d.to_csv(ROOT / "framework_B" / "gev_fcf_decomposition.csv")
    pd.set_option("display.width", 250)
    cols = ["revenue", "op_income", "net_income", "depreciation", "ocf", "capex", "fcf", "d_contract_liab",
            "bs_check_d_contract_liab", "d_contract_asset", "d_inventory", "d_receivables", "d_payables",
            "fcf_ex_deposits", "deposit_share_of_fcf", "buybacks", "dividends"]
    print(d[[c for c in cols if c in d]].round(2).T.to_string())
