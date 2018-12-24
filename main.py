# TODO add python3.7.1 hashbang

import collections
import csv

Address = collections.namedtuple('Address', 'street_1 street_2 city state zip_code')
Node = collections.namedtuple('Node', 'client_name booked_amount reservice address')

def read_input(filename):
    """Convert each row of the input csv into a dictionary"""
    with open(filename, newline='\n') as csvfile:
        reader = csv.DictReader(csvfile)
        rows = list(reader)
    return rows


def create_nodes(rows):
    """
    Takes each csv input row and create a Node object representation.

    Returns a dict of nodes ordered by their `slot_end`. We do this as an
    optimization to avoid storing the nodes in a list and scanning the list for
    a "next" node when trying to build a route.

    For example:

    We expect a job to complete by 11:30pm. Taking into account available slots:
    {8-10, 9-12, 10-13, ...} it's clear that the "next" node in the scheduling
    sequence could NOT be in the 8-10 slot. Therefore, we'd look only for
    available nodes in slots ending > 11:30pm, i.e. {9-12, 10-13, ...}. This way
    there's a chance that the driver could make it to the next node within the
    time range, accounting for travel time.

    It's possible that some nodes in the 9-12 range will not be possible if the
    driver leaves at 11:30pm and needs >= 30min of travel time. This is can be
    accounted for later and the Node can be removed from the list of possible
    "next" Nodes for the current Node.
    """
    nodes = collections.defaultdict(list)
    for row in rows:
        # hardcode these for now
        slot_start = 8
        slot_end = 10
        # slot_start = row['Slot Start'] # TODO add column for this to csv
        # slot_end = row['Slot End'] # TODO add column for this to csv
        address = Address(
            street_1 = row['Street 1'],
            street_2 = row['Street 2'],
            city = row['City'],
            state = row['State'],
            zip_code = row['Zip Code'])
        node = Node(
            client_name = row['Client Name'],
            booked_amount = row['Booked Amount'],
            reservice = False,
            address = address)
        nodes[slot_end].append(node)
    return nodes


if __name__ == "__main__":
    report_rows = read_input('inputs/report.csv')
    nodes = create_nodes(report_rows)
    print(nodes.keys())
