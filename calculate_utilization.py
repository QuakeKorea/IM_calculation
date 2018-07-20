import os
import datetime
import calendar
import argparse
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.dates as mdates


CALENDAR = {s: n for n, s in enumerate(calendar.month_abbr)}


def get_datetime(time_string):
    try:
        date, time = time_string.split('_')
        try:
            year, month, day = map(int, date.split('-'))  # 2018-07-10_00:08:27 run_emod3d.MaungatiE01_HYP09-17_S1324.20180710_000823.out
        except ValueError:  # 09:20:52_03/07/2018 run_emod3d.EdgecumbCS_HYP02-14_S1254.20180703_092031.out
            date, time = time, date
            day, month, year = map(int, date.split('/'))
    except ValueError:
        _, month, day, time, _, year = time_string.split()
        month = CALENDAR[month]
        day = int(day)
        year = int(year)
    hour, minute, second = map(int, time.split(':'))
    datetime_obj = datetime.datetime(year, month, day, hour, minute, second)
    return datetime_obj


def get_fraction_dict(dir_path, file_pattern=''):
    fraction_dict = {}
    for f in os.listdir(dir_path):
        if not f.startswith('post') and f.startswith(file_pattern):
            file_path = os.path.join(dir_path, f)
            with open(file_path, 'r') as sim_file:
                buf = sim_file.readlines()
                start_time = get_datetime(buf[0].strip())
                end_time = get_datetime(buf[-1].strip())
                calc_fraction(fraction_dict, start_time, end_time)
    return fraction_dict


def populate_dict(fraction_dict, time, duration):
    if time not in fraction_dict.keys():
        fraction_dict[time] = duration / 3600.
    else:
        fraction_dict[time] += duration / 3600.


def calc_fraction(fraction_dict, start_time, end_time):
    duration = (end_time - start_time).total_seconds()
    # print(start_time, end_time, duration)
    diff_start = 3600 - (start_time.minute * 60 + start_time.second)
    if diff_start >= duration:    # if the job is completed within an complete hour, eg 8:00-9:00
        populate_dict(fraction_dict, start_time, duration)
    else:  # if the job is completed over 8:56-9:15, 8:00-10:00 etc
        diff_end = end_time.minute * 60 + end_time.second
        hours_between = (duration - diff_start - diff_end) // 3600
        populate_dict(fraction_dict, start_time, diff_start)
        if hours_between != 0:
            for i in range(int(hours_between)):
                new_time = start_time + datetime.timedelta(hours=i+1)
                populate_dict(fraction_dict, new_time, 3600)
        populate_dict(fraction_dict, end_time, diff_end)


def df_to_csv(df, index_colname, value_colname, csv_name):
    df.columns=[value_colname]
    df.index.name = index_colname
    df.to_csv('~/{}'.format(csv_name))


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('dir_path', type=str,
                        help='abs path to *.out folder')
    parser.add_argument('-f', '--file_pattern', type=str, default='sim_bb', help='what file pattern the bb file startswith. eg.sim_bb')
    args = parser.parse_args()

    fraction_dict = get_fraction_dict(args.dir_path)
    df = pd.DataFrame.from_dict(fraction_dict, orient='index')
    df = df.groupby(pd.Grouper(freq='H')).sum()
    num_of_dates = float(len(df.index))
    
    plt.style.use('ggplot')
    fig, ax = plt.subplots(figsize=(15, 7))
    
    ax.bar(df.index, df.values, width=15/num_of_dates/24 * 3, align='center')
    
    # uncomment the 3 lines below and comment out 'set major and minor x ticks' for another x-axis date formatter
    # ax.set_xticks(df.index)
    # ax.xaxis.set_major_formatter(mdates.DateFormatter("%b-%d-%H"))
    # _ = plt.xticks(rotation=90)

    # set major and minor x ticks
    ax.xaxis.set_major_locator(mdates.DayLocator())
    ax.xaxis.set_major_formatter(mdates.DateFormatter('%b-%d'))
    ax.xaxis.set_minor_locator(mdates.HourLocator())
    ax.xaxis.set_minor_formatter(mdates.DateFormatter('%H'))
    ax.xaxis.set_tick_params(which='major', pad=15)
    # plt.setp(ax.get_xticklabels(which='minor'), rotation=90, horizontalalignment='right')
 

    # count total of BB jobs
    bb_fraction_dict = get_fraction_dict(args.dir_path, args.file_pattern)
    bb_df = pd.DataFrame.from_dict(bb_fraction_dict, orient='index')
    bb_df = bb_df.groupby(pd.Grouper(freq='D')).count()
    bb_per_day = np.divide(np.sum(bb_df.values), np.size(bb_df.values))
    bb_text = 'Average bb jobs run per day is {}'.format(bb_per_day)
    
    ax.set_title('Kupe core hour utilized per realtime hour')
    ax.set_xlabel('datetime')
    ax.set_ylabel('core hour utilized')
    plt.text(0.9, 0.9, bb_text, horizontalalignment='center', verticalalignment='center', transform=ax.transAxes)

    df_to_csv(df, 'datetime', 'core_hour_utilized', 'all_jobs.csv')
    df_to_csv(bb_df, 'datetime', 'number_of_bb_jobs_running', 'bb_jobs.csv')

    fig.tight_layout()
    plt.show()


if __name__ == '__main__':
   main()

