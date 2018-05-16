import argparse
import os
import shutil
import sys
from data.util import geocode_address

#pass path to create in into a argument
#test with small csv for crashes and concerns
#Mount and test with changes in 

#todo check how to pass this then, actually, not in test
BASE_DIR = os.path.dirname(
    os.path.dirname(
        os.path.abspath(__file__)))


def make_config_file(yml_file, city, folder, crash, concern):

    f = open(yml_file, 'w+')

    address = geocode_address(city)
    f.write(
        "# City name\n" +
        "city: {}\n".format(city) +
        "# The folder under data where this city's data is stored\n" +
        "name: {}\n".format(folder) +
        "city_latitude: {}\n".format(address[1]) +
        "city_longitude: {}\n".format(address[2]) +
        "# If given, limit crashes to after start_year and before end_year\n" +
        "# Recommended to limit to just a few years for now\n" +
        "start_year: \n" +
        "end_year: \n\n\n" +
        "#################################################################\n" +
        "# Configuration for data transformation\n\n" +
        "# crash file configurations\n" +
        "crashes_files:\n" +
        "  {}:\n".format(crash) +
        "    required:\n" +
        "      id: \n" +
        "      latitude: \n" +
        "      longitude: \n" +
        "      date: \n" +
        "      # Time is only required if date and time" +
        " are in different columns\n" +
        "      time: \n" +
        "    optional:\n" +
        "      summary: \n" +
        "      address: \n\n"
    )

    if concern:
        f.write(
            "# List of concern type information" +
            "concern_files:\n" +
            "- name: concern\n" +
            "filename: {}\n".format(concern) +
            "latitude: \n" +
            "longitude: \n" +
            "time: \n\n\n"
        )
    f.write(
        "# week on which to predict crashes (week, year)\n" +
        "# will output predictions for all weeks up to this week\n" +
        "# Choose a week towards the end of your crash data set\n" +
        "# in format [month, year]\n" +
        "time_target: [30, 2017]\n"
    )
    f.close()
    print "Wrote new configuration file in {}".format(yml_file)


if __name__ == '__main__':

    parser = argparse.ArgumentParser()
    parser.add_argument("-city", "--city", type=str,
                        help="city name")
    parser.add_argument("-f", "--folder", type=str,
                        help="folder name")
    parser.add_argument('-crash', '--crash_file', type=str,
                        help="crash file path")
    parser.add_argument('-concern', '--concern_file', type=str,
                        help="concern file path")
    parser.add_argument('-basePath', '--base_path', type=str,
                        help="base file path")
    parser.add_argument('-configPath', '--config_path', type=str,
                        help="base file path")
    args = parser.parse_args()
    if not args.city:
        print "city required"
        sys.exit()
    if not args.folder:
        print "folder required"
        sys.exit()
    if not args.crash_file:
        print "crash file required"
        sys.exit()
    if not args.base_path:
        print "base path for files required"
        sys.exit()
    if not args.config_path:
        print "config path for files required"
        sys.exit()        
    print "in init city..."
    #DATA_FP = os.path.join(BASE_DIR, 'data', args.folder)
    DATA_FP = args.base_path+ '/data'+ args.folder
    print "args are"
    print args
    print "data_fp is " + args.base_path+ '/data'+ args.folder

    crash = args.crash_file.split('/')[-1]
    crash_dir = os.path.join(DATA_FP, 'raw', 'crashes')
    concern = None
    if args.concern_file:
        concern = args.concern_file.split('/')[-1]

    # Check to see if the directory exists
    # if it does, it's already been initialized, so do nothing
    if not os.path.exists(DATA_FP):
        os.makedirs(DATA_FP)
        os.makedirs(os.path.join(DATA_FP, 'raw'))
        os.makedirs(crash_dir)
        concern_dir = os.path.join(DATA_FP, 'raw', 'concerns')
        os.makedirs(concern_dir)
        os.makedirs(os.path.join(DATA_FP, 'processed'))
        os.makedirs(os.path.join(DATA_FP, 'standardized'))
        shutil.copyfile(args.crash_file, os.path.join(crash_dir, crash))

        if args.concern_file:
            shutil.copyfile(args.concern_file, os.path.join(
                concern_dir, concern))

    else:
        print args.folder + " already initialized, skipping"

    #actually should pass in 'src/config/config_'
    yml_file = os.path.join(
        args.config_path + args.folder + '.yml')
    print "yml path is: " + yml_file

    if not os.path.exists(yml_file):
        make_config_file(yml_file, args.city, args.folder, crash, concern)

