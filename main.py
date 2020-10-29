"""
Entrypoint for the FAQ application
"""

import sys
import argparse
from components.helpers.Logger import Logger
from components.helpers.Runner import Runner


if __name__ == "__main__":
    Logger.log_message(Logger.INFO, "Starting FAQ creator...")

    parser = argparse.ArgumentParser()
    parser.add_argument('-plot', action="store_true", default=False)
    parser.add_argument('-input', action="store")
    parser.add_argument('-quick', action="store_true", default=False)
    results = parser.parse_args()

    input_file, should_plot, quick_run = results.input, results.plot, results.quick

    if quick_run:
        runner = Runner("test_VOH_CSV.csv", True, quick_run)
        runner.main()

    else:
        if input_file is None or input_file[-4:] != ".csv":
            Logger.log_message(
                Logger.ERROR,
                "You must provide an input csv file as an argument.\
                Example: python main.py -input myFile.csv"
                )
            sys.exit(1)

        runner = Runner(input_file, should_plot, quick_run)
        runner.main()
