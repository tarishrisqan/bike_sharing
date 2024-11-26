import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st
import matplotlib.ticker as ticker

sns.set(style='dark')

#filter dataframe dari 1-January-2011 sampai 31-desember-2012
def total_day_sidebar(day_df):
    total_day_df = day_df.query(str('dteday >= "2011-01-01" and dteday < "2012-12-31"'))
    return total_day_df

def total_hour(hour_df):
    total_hours_df = hour_df.groupby(by="hour").agg({"count_ttl": ["sum"]})
    return total_hours_df

#mengambil data dari dteday dan meng computes total member yang ada pertanggal itu dan mengganti value menjadi register_sum
def total_member_df(day_df):
    member_df = day_df.groupby(by="dteday").agg({
        "member": "sum"
    })
    member_df = member_df.reset_index()
    member_df.rename(columns={
        "member": "register_sum"
    }, inplace=True)
    return member_df

def total_non_member_df(day_df):
    nonmember_df = day_df.groupby(by="dteday").agg({
        "non_member": ["sum"]
    })
    nonmember_df = nonmember_df.reset_index()
    nonmember_df.rename(columns={
        "non_member": "non_member_sum"
    }, inplace=True)
    return nonmember_df

def four_season (day_df):
    four_seasons_df = day_df.groupby(by="season").count_ttl.sum().reset_index()
    return  four_seasons_df

def hour_order (hour_df):
    hour_order_df = hour_df.groupby("hour").count_ttl.sum().sort_values(ascending=False).reset_index
    return hour_order_df

dayc_df = pd.read_csv("day_confirm.csv")
hourc_df= pd.read_csv("hour_confirm.csv")

datetime_columns = ["dteday"]
dayc_df.reset_index(inplace=True)
dayc_df.sort_values(by="dteday", inplace=True)

hourc_df.reset_index(inplace=True)
hourc_df.sort_values(by="dteday", inplace=True)

for column in datetime_columns:
    hourc_df[column] = pd.to_datetime(hourc_df[column])
    dayc_df[column] = pd.to_datetime((dayc_df[column]))

min_date_dayc = dayc_df["dteday"].min()
max_date_dayc = dayc_df["dteday"].min()

min_date_hourc = hourc_df["dteday"].min()
max_date_hourc =  hourc_df["dteday"].min()

with st.sidebar:
    st.image("https://github.com/tarishrisqan/Dicoding_Deco/blob/main/bike.jpg?raw=true")

    # Mengambil start_date & end_date dari date_input
    start_date, end_date = st.date_input(
        label='Rentang Waktu',
        min_value=min_date_dayc,
        max_value=max_date_dayc,
        value=[min_date_dayc, max_date_dayc])

    hourc_main_df = hourc_df[(hourc_df["dteday"] >= str(start_date)) &
                     (hourc_df["dteday"] <= str(end_date))]

    dayc_main_df = dayc_df[(dayc_df["dteday"] >= str(start_date)) &
                (dayc_df["dteday"] <= str(end_date))]

    total_day_sidebar_df = total_day_sidebar(dayc_main_df)
    total_hours_df= total_hour(hourc_main_df)
    member_df = total_member_df(dayc_main_df)
    non_member_df = total_non_member_df(dayc_main_df)
    four_season_df = four_season(hourc_main_df)
    hour_order_df = hour_order(hourc_main_df)

st.header('Bike Rent :sparkles')
st.subheader('Daily Rent')

col1, col2, col3= st.columns(3)

with col1:
    total_orders = total_day_sidebar_df.count_ttl.sum()
    st.metric("Total rent bike", value=total_orders)

with col2:
    total_sum = member_df.register_sum.sum()
    st.metric("Total Member", value=total_sum)

with col3:
    total_sum =non_member_df.non_member_sum.sum()
    st.metric("Total Non Member", value=total_sum)

fig, ax = plt.subplots(figsize=(16, 8))
ax.plot(
    dayc_df["dteday"],
    dayc_df["count_ttl"],
    marker='o',
    linewidth=2,
    color="#90CAF9"
)
ax.tick_params(axis='y', labelsize=20)
ax.tick_params(axis='x', labelsize=15)

st.pyplot(fig)

#Pertanyaan 1

#Membuat Sub Judul
st.subheader("Kondisi Cuaca Apa yang mendorong pelanggan untuk menyewa sepeda?")
#membuat Kelompok
weather_df = dayc_df.groupby("weather_condition").count_ttl.mean().reset_index()
#membuat gambar dan ukuran menjadi 16, 8 inci
fig, ax = plt.subplots(figsize=(16, 8))
#membuat barplot
sns.barplot(data=weather_df, x="weather_condition", y="count_ttl", ax=ax, palette="pastel")
ax.set_title('Rata rata penyewaan sepeda', fontsize=20)
ax.set_xlabel('Kondisi cuaca', fontsize=15)
ax.set_ylabel('Rata rata penyewaan sepeda', fontsize=15)
ax.yaxis.set_major_locator(ticker.MaxNLocator(integer=True))
ax.tick_params(axis='y', labelsize=12)
ax.tick_params(axis='x', labelsize=12)
#print Plot
st.pyplot(fig)

#Pertanyaan 2 dan 3

st.subheader(" Hari dan musim apa dalam seminggu  puncak penyewaan sepeda terjadi?")
dayc_df["weekday"] = dayc_df["dteday"].dt.day_name()

weekday_season_df = dayc_df.groupby(["weekday", "season"]).agg({"count_ttl": "sum"}).unstack().fillna(0)
weekday_season_df.columns = [f'{col[1]}' for col in weekday_season_df.columns]
weekday_order = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
weekday_season_df = weekday_season_df.reindex(weekday_order)

fig, ax = plt.subplots(figsize=(16, 8))

weekday_season_df.plot(kind='barh', stacked=True, ax=ax,)

ax.set_title('Performa Penyewaan Sepeda berdasarkan  musim dan hari dalam seminggu', fontsize=20)
ax.set_xlabel('Total Penyewaan', fontsize=15)
ax.set_ylabel('Hari Dalam Seminggu', fontsize=15)
ax.yaxis.set_major_locator(ticker.MaxNLocator(integer=True))
ax.tick_params(axis='y', labelsize=12)
ax.tick_params(axis='x', labelsize=12)

st.pyplot(fig)

#pertanyaan 4
st.subheader("Bagaimana performa penyewaan sepeda di tahun terakhir?")

latest_date = dayc_df["dteday"].max()
last_year_start = latest_date - pd.DateOffset(years=1)
last_year_df = dayc_df[(dayc_df["dteday"] >= last_year_start)]
fig, ax = plt.subplots(figsize=(16, 8))
ax.plot(
    last_year_df["dteday"],
    last_year_df["count_ttl"],
    marker='o',
    linewidth=2,
    color="#90CAF9"
)
ax.set_title("Bagaimana performa penyewaan sepeda di tahun terakhir?", fontsize=20)
ax.set_xlabel("Bulan", fontsize=15)
ax.set_ylabel("Angka Pencapaian", fontsize=15)
ax.tick_params(axis='y', labelsize=12)
ax.tick_params(axis='x', labelsize=12)
ax.grid(True)

st.pyplot(fig)


#Pertanyaan 5 "perbedaan member dan non-member"
st.subheader("Perbandingan Member dan non member setiap tahun nya")
dayc_df['year'] = dayc_df['dteday'].dt.year
yearly_comparison_df = dayc_df.groupby('year').agg({'member': 'sum', 'non_member': 'sum'}).reset_index()
fig, ax = plt.subplots(figsize=(16, 8))

yearly_comparison_df.plot(kind='barh',stacked=True, x='year', y=['member', 'non_member'], color=['#f47e7a', '#b71f5c'], ax=ax, alpha=0.7, width=0.8)
ax.set_title('Perbandingan Member Dan Non Member', fontsize=20)
ax.set_xlabel('Tahun', fontsize=15)
ax.set_ylabel('total Member', fontsize=15)
ax.tick_params(axis='y', labelsize=12)
ax.tick_params(axis='x', labelsize=12)
ax.legend(['Member', 'Non-Member'],frameon=False, fontsize=12)

st.pyplot(fig)

