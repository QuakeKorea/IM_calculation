from rrup import rrup as rrup
import argparse

DEFAULT_N_PROCESSES = 4


def write_and_calculate_rrups(station_file, srf_file, stations=None, processes=DEFAULT_N_PROCESSES):
    rrups = rrup.computeRrup(station_file, srf_file, stations, processes)
    fname = args.output
    with open(fname, 'w') as f:
        f.write("Station_name, lon, lat, r_rup, r_jbs, r_x\n")
        for values in rrups:
            name, lat, lon, (r_rups, r_jbs, r_x) = values
            f.write("%s,%s,%s,%s,%s,%s\n" % (name, lon, lat, r_rups, r_jbs, r_x))


# /nesi/nobackup/nesi00213/RunFolder/Cybershake/v18p6/Runs/Kelly/fd_rt01-h0.400.ll
# /scale_akl_nobackup/filesets/transit/nesi00213/StationInfo/non_uniform_whole_nz_with_real_stations-hh400_v18p6.ll
def get_fd_stations(fd_ll):
    """
    :param fd_ll: path to fd_ll station file
    :return: a list of useful stations
    """
    stations = []
    with open(fd_ll, 'r') as fd:
        lines = fd.readlines()
        for line in lines:
            station = line.strip().split()[-1]
            stations.append(station)
    print("stations",len(stations))
    return stations


def get_match_stations(parser, arg_fd, arg_stations):
    """
    :param parser:
    :param arg_fd: input fd_station_file_path
    :param arg_stations: input space delimited list of stations
    :return: None or a list of match stations
    """
    match_stations = None

    if arg_fd is not None and arg_stations is not None:
        parser.error("'-fd and -s options are mutually exclusive.")

    if arg_fd is not None:
        match_stations = get_fd_stations(arg_fd)

    if arg_stations is not None:
        match_stations = arg_stations

    return match_stations


if __name__ == "__main__":
    parser = argparse.ArgumentParser('calculate_rrups.py')
    parser.add_argument('station_file', type=str)
    parser.add_argument('srf_file', type=str)
    parser.add_argument('-np', '--processes', type=int, default=DEFAULT_N_PROCESSES)
    parser.add_argument('-s', '--stations', nargs='+', help="space delimited list of stations", default=None)
    parser.add_argument('-o', '--output', type=str, default='rrups.csv')
    parser.add_argument('-fd' 'fd_station_file', type=str, default=None)

    args = parser.parse_args()

    match_stations = get_match_stations(parser, args.fd_station_file, args.stations)

    write_and_calculate_rrups(args.station_file, args.srf_file, stations=match_stations, processes=args.processes)
