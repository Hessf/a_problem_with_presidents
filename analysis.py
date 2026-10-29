import pandas as pd #For data analysis
from dateutil.relativedelta import relativedelta #For improving accuracy of lifespan calculations
import numpy as np
from scipy import stats #For mathematical calculations (mean, median, etc.)
import matplotlib.pyplot as plt #For creating visual plots of data points

df = pd.read_csv('U.S. Presidents Birth and Death Information - Sheet1.csv') #Reads the CSV

df['BIRTH DATE'] = pd.to_datetime(df['BIRTH DATE'],format='mixed')
df['DEATH DATE'] = pd.to_datetime(df['DEATH DATE'],format='mixed') #Reformats the birth and death dates

df['year_of_birth'] = df['BIRTH DATE'].dt.year #Gets year of birth

df['lifespan_in_days']= (df['DEATH DATE'] - df['BIRTH DATE']).dt.days #Gets lifespan in days (for sorting)
df['lifespan_in_years']= df['lifespan_in_days']/365.2425 #Gets lifespan in years (for plotting)

def get_ymd_lived(row): #Gets lifespan in years, months, days
    if pd.isna(row['DEATH DATE']) or pd.isna(row['BIRTH DATE']): #Ignores presidents that are still alive (no death dates)
        return pd.Series([None, None, None], index=['years_lived', 'months_lived', 'days_lived'])
    lifespan = relativedelta(row['DEATH DATE'], row['BIRTH DATE'])
    return pd.Series([lifespan.years, lifespan.months, lifespan.days],
                     index=['years_lived', 'months_lived', 'days_lived'])

df[['years_lived','months_lived','days_lived']] = df.apply(get_ymd_lived, axis=1)

df_alive_removed=df.dropna(subset=['DEATH DATE']) #Creates a version of the table with living presidents removed (to sort by lifespan)

df_sorted_top = df_alive_removed.sort_values(by=['lifespan_in_days'],ascending=False) #Creates table sorted by lifespan (long -> short)
df_sorted_btm = df_alive_removed.sort_values(by=['lifespan_in_days'],ascending=True) #Creates table sorted by lifespan (short -> long)

longest  = df_sorted_top.head(10)[['PRESIDENT', 'years_lived', 'months_lived', 'days_lived']].copy() #Gets 10 longest lifespans
shortest  = df_sorted_btm.head(10)[['PRESIDENT', 'years_lived', 'months_lived', 'days_lived']].copy() #Gets 10 shortest lifespans

print("#### 10 Longest Lifespans\n")
print(longest.to_markdown(index=False))
print("\n#### 10 Shortest Lifespans\n")
print(shortest.to_markdown(index=False)) #Prints the two tables

mean_lifespan_days = np.round((np.mean(df_alive_removed['lifespan_in_days'])),0) #Gets the mean lifespan in days
med_lifespan_days = np.round((np.median(df_alive_removed['lifespan_in_days'])),0) #Gets the median lifespan in days
mode_lifespan_days = np.round((stats.mode(df_alive_removed['years_lived'])),0) #Gets the most common age of death
max_lifespan_days = np.round((np.max(df_alive_removed['lifespan_in_days'])),0) #Gets the max lifespan in days
min_lifespan_days = np.round((np.min(df_alive_removed['lifespan_in_days'])),0) #Gets the min lifespan in days
std_lifespan_days = np.round((np.std(df_alive_removed['lifespan_in_days'])),0) #Gets the standard deviation in days

def to_ymd_approx(days):
    y = int(days//365)
    m = int((days//30)%12)
    d = int((days%365)%30)
    return f'~{y} year(s), {m} month(s), {d} day(s)' #Converts days to approximate length in ymd (using rough estimates of 30 d/m, 365 d/y) to improve readability

val_table = pd.DataFrame(data={
    "Calculation" : ["Mean","Median","Mode","Max","Min","StdDev"],
    "Value" : [to_ymd_approx(mean_lifespan_days),to_ymd_approx(med_lifespan_days),f'{int(mode_lifespan_days[0])} years',
                   to_ymd_approx(max_lifespan_days),to_ymd_approx(min_lifespan_days),to_ymd_approx(std_lifespan_days)],
    },
    index=[1,2,3,4,5,6]
) #Creates a new table with the mean, median, etc.

print("\n#### Statistics\n")
print(val_table.to_markdown(index=False)) #Displays these statistical values in a format consistent with the previous table

plt.figure(figsize = (10,10)) #Creates the visual plot of lifespans
plt.barh(df_sorted_btm["PRESIDENT"], df_sorted_btm["lifespan_in_years"],color='lightblue',height=0.8)
plt.axvline(x=float(mean_lifespan_days/365.2425),color='red',linewidth=2,label='Average lifespan') #Adds a vertical line showing the average lifespan
plt.axvline(x=float(med_lifespan_days/365.2425),color='black',linewidth=2,label='Median lifespan') #Does the same, with median lifespan
plt.xlabel('President')
plt.ylabel('Lifespan (years)') #Labels the axes of the graph
plt.title('Lifespans of Deceased Presidents')
plt.tight_layout()
plt.legend()
plt.show() #Displays the graph