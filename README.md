# Bitcoin block lookup
A python script to locate the bitcoin block which was created just before a requested timestamp.


##  Prerequisites
python version  >= 3.9

Install requirements.txt packages:
`pip -r requirements.txt`

Recommended using virtual environment.

## Usage
./lookup.py \<timestamp> [--log loglevel]

(timestamp is an Epoch timestamp)

For more info:
./lookup.py -h

### Example
./lookup.py 1232103989 --log info

