import os
import pickle
import numpy as np

from IM import read_waveform
from test.test_common_set_up import (
    TEST_DATA_SAVE_DIRS,
    INPUT,
    OUTPUT,
    set_up,
    compare_dicts,
)


def get_common_waveform_values(root_path, function_name):
    with open(
        os.path.join(root_path, INPUT, function_name + "_bbseis.P"), "rb"
    ) as load_file:
        bbseis = pickle.load(load_file)
    with open(
        os.path.join(root_path, INPUT, function_name + "_comp.P"), "rb"
    ) as load_file:
        comp = pickle.load(load_file)
    with open(
        os.path.join(root_path, INPUT, function_name + "_wave_type.P"), "rb"
    ) as load_file:
        wave_type = pickle.load(load_file)
    with open(
        os.path.join(root_path, INPUT, function_name + "_file_type.P"), "rb"
    ) as load_file:
        file_type = pickle.load(load_file)

    return bbseis, comp, wave_type, file_type




def get_common_bbseis_values(root_path, function_name):
    with open(
        os.path.join(root_path, INPUT, function_name + "_station_names.P"), "rb"
    ) as load_file:
        station_names = pickle.load(load_file)

    with open(
        os.path.join(root_path, INPUT, function_name + "_units.P"), "rb"
    ) as load_file:
        units = pickle.load(load_file)
    return station_names, units


def compare_waveforms(bench_waveform, test_waveform):
    vars_test = vars(test_waveform)
    vars_bench = vars(bench_waveform)
    for k in vars_bench.keys():
        if isinstance(vars_bench[k], np.ndarray):
            assert np.isclose(vars_test[k], vars_bench[k]).all()
        else:
            assert vars_test[k] == vars_bench[k]


def test_calculate_timesteps():
    function = "calculate_timesteps"
    for root_path in TEST_DATA_SAVE_DIRS:
        with open(
            os.path.join(root_path, INPUT, function + "_NT.P"), "rb"
        ) as load_file:
            NT = pickle.load(load_file)
        with open(
            os.path.join(root_path, INPUT, function + "_DT.P"), "rb"
        ) as load_file:
            DT = pickle.load(load_file)

        test_output = read_waveform.calculate_timesteps(NT, DT)

        with open(
            os.path.join(root_path, OUTPUT, function + "_ret_val.P"), "rb"
        ) as load_file:
            bench_output = pickle.load(load_file)

        assert np.isclose(test_output, bench_output).all()


def test_read_waveforms():
    function = "read_waveforms"
    for root_path in TEST_DATA_SAVE_DIRS:
        station_names, units = get_common_bbseis_values(root_path, function)
        bbseis, comp, wave_type, file_type = get_common_waveform_values(
            root_path, function
        )

        # only test for binary, path to ascii folder is not needed
        test_output = read_waveform.read_waveforms(
            None, bbseis, station_names, comp, wave_type, file_type, units
        )

        with open(
            os.path.join(root_path, OUTPUT, function + "_ret_val.P"), "rb"
        ) as load_file:
            bench_output = pickle.load(load_file)
        for i in range(len(bench_output)):  # a list of waveform tuples
            for j in range(2):  # (waveform_acc, waveform_vel)
                compare_waveforms(bench_output[i][j], test_output[i][j])


def test_read_one_station_from_bbseis():  # station name not the same
    function = "read_one_station_from_bbseries"
    for root_path in TEST_DATA_SAVE_DIRS:
        print("root_path", root_path)
        with open(
            os.path.join(root_path, INPUT, function + "_station_name.P"), "rb"
        ) as load_file:
            station_name = pickle.load(load_file)
            print("station_name from pikle", station_name)

        bbseis, comp, wave_type, file_type = get_common_waveform_values(
            root_path, function
        )

        test_output = read_waveform.read_one_station_from_bbseries(
            bbseis, station_name, comp, wave_type, file_type
        )

        with open(
            os.path.join(root_path, OUTPUT, function + "_waveform.P"), "rb"
        ) as load_file:
            bench_output = pickle.load(load_file)

        compare_waveforms(bench_output, test_output)


def test_read_binary_file():
    function = "read_binary_file"
    for root_path in TEST_DATA_SAVE_DIRS:
        station_names, units = get_common_bbseis_values(root_path, function)
        bbseis, comp, wave_type, file_type = get_common_waveform_values(
            root_path, function
        )

        test_output = read_waveform.read_binary_file(
            bbseis, comp, station_names, wave_type, file_type, units
        )

        with open(
            os.path.join(root_path, OUTPUT, function + "_waveforms.P"), "rb"
        ) as load_file:
            bench_output = pickle.load(load_file)

        for i in range(len(bench_output)):
            for j in range(2):
                compare_waveforms(bench_output[i][j], test_output[i][j])
