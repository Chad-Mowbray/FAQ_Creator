### Purpose
This is a tool for providing an overview of who our clients are and what their problems are.

### Usage
1. Clone this repo
2. Create a virtual environment (optional)
3. Install requirements.txt (pip install -r requirements.txt)
4. Put the csv file in /input
5. From the command line run:

```bash
python main.py -input myCsvFile.csv
```

This will produce four text files in the /output folder.

If you would like to see graphs, add the "-plot" flag to the command.