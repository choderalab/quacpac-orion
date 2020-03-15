# (C) 2018 OpenEye Scientific Software Inc. All rights reserved.
#
# TERMS FOR USE OF SAMPLE CODE The software below ("Sample Code") is
# provided to current licensees or subscribers of OpenEye products or
# SaaS offerings (each a "Customer").
# Customer is hereby permitted to use, copy, and modify the Sample Code,
# subject to these terms. OpenEye claims no rights to Customer's
# modifications. Modification of Sample Code is at Customer's sole and
# exclusive risk. Sample Code may require Customer to have a then
# current license or subscription to the applicable OpenEye offering.
# THE SAMPLE CODE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
# EXPRESS OR IMPLIED.  OPENEYE DISCLAIMS ALL WARRANTIES, INCLUDING, BUT
# NOT LIMITED TO, WARRANTIES OF MERCHANTABILITY, FITNESS FOR A
# PARTICULAR PURPOSE AND NONINFRINGEMENT. In no event shall OpenEye be
# liable for any damages or liability in connection with the Sample Code
# or its use.

from floe.api import WorkFloe
from orionplatform.cubes import DatasetReaderCube, DatasetWriterCube
from am1bcc_charge.am1bcc_charge import AM1BCCCharge


# Declare and document floe
job = WorkFloe("am1bcc_charge", title="am1bcc charge")
job.description = (
    "AM1BCC Charge"
)
job.classification = [["Charge"]]
job.tags = ["Charge"]

# Declare Cubes
input_cube = DatasetReaderCube("input_cube")
charge_cube = MyCube("charge_cube")
output_cube = DatasetWriterCube("output_cube")

# Add cubes to floe
job.add_cube(input_cube)
job.add_cube(charge_cube)
job.add_cube(output_cube)

# Promote parameters
input_cube.promote_parameter(
    "data_in", promoted_name="in", title="Input data set of records"
)

charge_cube.promoted_parameter(
    'max_confs', promoted_name='in', title='Maximum number of conformers.'
)

charge_cube.promoted_parameter(
    'max_search_time', promoted_name='in', title='Search time for conformers.'
)

charge_cube.promote_parameter(
    'energy_window', promoted_name='in', title='Energy window '
)

output_cube.promote_parameter(
    "data_out", promoted_name="out", title="Output File of Molecules"
)


input_cube.success.connect(charge_cube.intake)
charge_cube.success.connect(output_cube.intake)

if __name__ == "__main__":
    job.run()
