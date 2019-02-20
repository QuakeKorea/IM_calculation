import sys
import numpy as np
import argparse
import pickle
import pytest
import shutil
import calculate_ims
import os
import getpass
import sys
from qcore import shared

#sys.path.insert(0, '../../')

PARSER = argparse.ArgumentParser()
BSC_PERIOD = [0.05, 0.1,  5.0, 10.0]
TEST_IMS = ['PGA', 'PGV', 'Ds575', 'pSA']


@pytest.mark.parametrize(
    "test_comp, expected_comp", [('ellipsis', 'ellipsis'), ('000', '000'), ('090', '090'), ('ver', 'ver'), ('geom', 'ellipsis')]
)
def test_validate_comp(test_comp, expected_comp):
    assert calculate_ims.validate_comp(PARSER, test_comp)[0] == expected_comp


@pytest.mark.parametrize("test_comp_fail", ["adsf"])
def test_validate_comp_fail(test_comp_fail):
    with pytest.raises(SystemExit):
         calculate_ims.validate_comp(PARSER, test_comp_fail)


@pytest.mark.parametrize(
    "test_period, test_extended, test_im, expected_period", [(BSC_PERIOD, False, TEST_IMS, np.array(BSC_PERIOD)), (BSC_PERIOD, True, TEST_IMS, np.unique(np.append(BSC_PERIOD, calculate_ims.EXT_PERIOD)))]
)
def test_validate_period(test_period, test_extended, test_im, expected_period):
    assert all(np.equal(calculate_ims.validate_period(PARSER, test_period, test_extended, test_im), expected_period))


@pytest.mark.parametrize(
    "test_period, test_extended, test_im", [(BSC_PERIOD, False, TEST_IMS[:-1]), (BSC_PERIOD, True, TEST_IMS[:-1])]
)
def test_validate_period_fail(test_period, test_extended, test_im):
    with pytest.raises(SystemExit):
        calculate_ims.validate_period(PARSER, test_period, test_extended, test_im)

class TestPickleTesting():

    REALISATIONS = [('PangopangoF29_HYP01-10_S1244',"https://www.dropbox.com/sh/dgpfukqd01zucjv/AAA8iMASZWn5vbr0PdDCgTG3a?dl=0")]
    test_data_save_dirs = []

    # Run this once, but run it for any test/collection of tests that is run in this class
    @pytest.fixture(scope='class', autouse=True)
    def set_up(self):
        for i, (REALISATION, DATA_DOWNLOAD_PATH) in enumerate(self.REALISATIONS):
            DATA_STORE_PATH = os.path.join(".", "sample"+str(i))
            os.mkdir(DATA_STORE_PATH)

            ZIP_DOWNLOAD_PATH = os.path.join(DATA_STORE_PATH, REALISATION+".zip")
            OUTPUT_DIR_PATH = os.path.join(DATA_STORE_PATH, "input")
            os.mkdir(OUTPUT_DIR_PATH)

            DOWNLOAD_CMD = "wget -O {} {}".format(ZIP_DOWNLOAD_PATH, DATA_DOWNLOAD_PATH)
            UNZIP_CMD = "unzip {} -d {}".format(ZIP_DOWNLOAD_PATH, OUTPUT_DIR_PATH)

            self.test_data_save_dirs.append(OUTPUT_DIR_PATH)
            if not os.path.isfile(OUTPUT_DIR_PATH):
                out, err = shared.exe(DOWNLOAD_CMD, debug=False)
                if b"failed" in err:
                    os.remove(ZIP_DOWNLOAD_PATH)
                    sys.exit("{} failed to download data folder".format(err))
                else:
                    print("Successfully downloaded benchmark data folder")

                out, err = shared.exe(UNZIP_CMD, debug=False)
                os.remove(ZIP_DOWNLOAD_PATH)
                if b"error" in err:
                    shutil.rmtree(OUTPUT_DIR_PATH)
                    sys.exit("{} failed to extract data folder".format(err))
            else:
                print("Benchmark data folder already exits")

        # Run all tests
        yield

        # Remove the test data directory
        for _, PATH in self.REALISATIONS:
            shutil.rmtree(PATH)

    def test_convert_str_comp(self):

        function = 'convert_str_comp'
        for root_path in self.test_data_save_dirs:

            with open(os.path.join(root_path, function + '_comp.P'), 'rb') as load_file:
                comp = pickle.load(load_file)

            print(comp)
            value_to_test = calculate_ims.convert_str_comp(comp)

            with open(os.path.join(root_path, function + '_converted_comp.P'), 'rb') as load_file:
                converted_comp = pickle.load(load_file)
            print(converted_comp)

            assert value_to_test == converted_comp

    def test_get_comp_name_and_list(self):

        function = 'get_comp_name_and_list'
        for root_path in self.test_data_save_dirs:
            with open(os.path.join(root_path, function + '_comp.P'), 'rb') as load_file:
                comp = pickle.load(load_file)
            with open(os.path.join(root_path, function + '_geom_only.P'), 'rb') as load_file:
                geom_only = pickle.load(load_file)

            value1_to_test, value2_to_test = calculate_ims.get_comp_name_and_list(comp, geom_only)

            with open(os.path.join(root_path, function + '_converted_comp.P'), 'rb') as load_file:
                converted_comp = pickle.load(load_file)
            with open(os.path.join(root_path, function + '_converted_comp.P'), 'rb') as load_file:
                converted_comp2 = pickle.load(load_file)

            assert value1_to_test == converted_comp
            assert value2_to_test == converted_comp2

