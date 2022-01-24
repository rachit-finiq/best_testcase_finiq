import pandas as pd

file_name = input("Enter Product Name (input file): ")

# load the data
df = pd.read_excel("./data/test.xlsx",
                   header=[0, 1], sheet_name=file_name, engine='openpyxl')


# stores final objects
S = []

# store filters for different products
AC = ["Std. AutoCall", "Fixed Coupon AC",
      "Phoenix AC with Memory", "Phoenix AC Wo Memory"]
PC1 = ["Fixed Coupon AC"]
PC2 = [" Phoenix AC with Memory", "Phoenix AC Wo Memory"]
YE1 = ["YC_Fixed Unconditional"]
YE2 = ["YC_Cond with Memory", "YC_Cond Wo Memory"]

st_list = []

for i in range(len(df["General Terms"]["Format"])):
    ac = True if file_name in AC else False
    pc1 = True if file_name in PC1 else False
    pc2 = True if file_name in PC2 else False
    ye1 = True if file_name in YE1 else False
    ye2 = True if file_name in YE2 else False

    # general tags
    st = df["General Terms"]["Solve For"][i]+","+df["General Terms"]["Public/Private"][i] + \
        ","+df["Dates"]["Strike Shift"][i]+"," + \
        df["Dates"]["Issue Date Offset"][i]+","
    a, pc, ye = ",,,,", ",,,", ",,,"

    # autocall tags
    if ac:
        a = df["AutoCall"]["Type"][i]+","+df["AutoCall"]["Autocall Freq. "][i] + \
            ","+df["AutoCall"]["AC From"][i]+"," + \
            df["AutoCall Coupon"]["Type"][i]+","

    # phoenix tags
    if pc1:
        pc = df["Periodic Coupon"]["Coupon Type"][i] + \
            ",,"+df["Periodic Coupon"]["Coupon Freq"][i]+","

    # phoenix tags
    if pc2:
        pc = df["Periodic Coupon"]["Coupon Type"][i]+"," + \
            df["Periodic Coupon"]["Coupon Barrier Type"][i] + \
            ","+df["Periodic Coupon"]["Coupon Freq"][i]+","

    # yield enchancement tags
    if ye1:
        ye = df["Yield Enhancement"]["Coupon Type"][i] + \
            ",,"+df["Yield Enhancement"]["Coupon Freq"][i]+","

    # yield enchancement tags
    if ye2:
        ye = df["Yield Enhancement"]["Coupon Type"][i]+"," + \
            df["Yield Enhancement"]["Coupon Barrier Type"][i] + \
            ","+df["Yield Enhancement"]["Coupon Freq"][i]+","

    st = st + a + pc + ye
    st += df["Payoff at Maturity"]["Prot. Type"][i]
    st_list.append(st)