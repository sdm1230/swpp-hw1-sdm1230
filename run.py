#!/usr/bin/python
# Copyright 2010 Google Inc.
# Licensed under the Apache License, Version 2.0
# http://www.apache.org/licenses/LICENSE-2.0

# Google's Python Class
# http://code.google.com/edu/languages/google-python-class/

# Modified by Alchan Kim at SNU Software Platform Lab for
# SWPP fall 2020 lecture

import sys
import os

from babyname_parser import BabynameParser

"""
Parse html files where the popular baby names are listed for each year,
collect records and save them into "babydata/" as a csv format.
The name of the output CSV file is "babyname.report.csv".
"""

class BabyRecord:
    def __init__(self, year, rank, name, gender, rank_change=None):
        """
        Args:
            year: The corresponding year of the data in integer.
            rank: The rank of the data in integer.
            name: The name of the data in string.
            gender: The gender of the data, either 'M' or 'F'.
            rank_change: The change of the rank compared to the previous year. `None` if no comparison possible.
        """
        self.year = year
        self.rank = rank
        self.name = name
        self.gender = gender
        self.rank_change = rank_change
    
    def to_csv_record(self):
        """
        (1 point)
        Convert the record into a comma-seperated string line, as format of "year,rank,name,gender(M/F),rank_change".
        The return value is a line of body of CSV file output.
        If rank_change is None, save it as blank ("").

        e.g. 2018,1,Joan,F,-2
        """
        # TODO: Implment this function
        line= "{},{},{},{},{}".format(self.year,self.rank,self.name,self.gender,(self.rank_change if self.rank_change!=None else ""))
        return line


    def __repr__(self):
        """
        NOTE: This method is provided for debugging. You don't need to modify this.
        """
        return "<BabyRecord year={} rank={} name={} gender={} rank_change={}>".format(
            self.year,
            self.rank,
            self.name,
            self.gender,
            self.rank_change,
        )

def save(filename, records):
    """
    NOTE: DO NOT change this function.
    This function saves the parsed records in csv format.

    Args:
        filename: The name of the output file.
        records: The list of records.
    """
    with open(filename, "w") as f:
        f.write("year,rank,name,gender,rank_change\n")
        for record in records:
            f.write(record.to_csv_record())
            f.write("\n")


def main():
    """
    (5 points)
    """
    args = sys.argv[1:]

    if len(args) < 2:
        print('usage: python run.py `starting year` `ending year`')
        sys.exit(1)

    year1, year2 = int(args[0]), int(args[1])

    records = [] # list of BabyRecord objects
    prev_male_ranking = {} # use this to calculate the rank if you need
    prev_female_ranking = {}

    for year in range(year1, year2 + 1):
        parser = BabynameParser("babydata", year)

        # TODO: In the following two lines, change `None` to your lambda function to parse baby name records.
        # By using the lambda function, `parse` method should return a list of `BabyRecord` objects
        # that contain year, rank, name, and gender data.
        male_records = parser.parse(lambda x:BabyRecord(year,x[0],x[1],'M')) # Parse the male ranks and store them as a list of `BabyRecord` objects.
        female_records = parser.parse(lambda x:BabyRecord(year,x[0],x[2],'F')) # Parse the female ranks and store it as a list of `BabyRecord` objects.
        
        # TODO: Calculate the rank change for each of `male_records` and `female_records`.
        # For example, if the rank of the previous year is 8 and the rank of the current year is 5,
        # -3 is the rank change. (Beware the sign of the value. Rank-up is respresented with a negative value!)
        # If the rank of previous year is not available, set `rank_change` to `None`.
        if year>year1:
            prev_parser = BabynameParser("babydata", year-1)
            prev_male_ranking = prev_parser.parse(lambda x:x[1])
            prev_female_ranking = prev_parser.parse(lambda  x:x[2])

            for i in range(0,1000):
                if male_records[i].name in prev_male_ranking:
                    male_records[i].rank_change = int(male_records[i].rank) - prev_male_ranking.index(male_records[i].name) - 1
                if female_records[i].name in prev_female_ranking:
                    female_records[i].rank_change = int(female_records[i].rank) - prev_female_ranking.index(female_records[i].name) - 1

        records = records + male_records + female_records
    # TODO: Save the result as a csv file named `babyname.report.csv` under `babydata/` directory.
    # The example output of `babyname.report.csv` is provided in `babydata/` folder.
    # You should make the same result with the example file.
    
    save(os.path.join("babydata", "babyname.report.csv"), records)

if __name__ == '__main__':
    main()
