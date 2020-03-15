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

from floe.api import BooleanParameter, ComputeCube
from orionplatform.mixins import RecordPortsMixin
from openeye import oeomega, oechem
import quacpac
# TODO: shall we generate graphs at the same time?
# import hgfp
# import dgl

from floe.api.cubes import ComputeCube, ParallelMixin
from floe.api.parameter import IntegerParameter, StringParameter, DecimalParameter, BooleanParameter
from orionplatform.mixins import RecordPortsMixin
from datarecord import OERecord, Types, OEPrimaryMolField, OEField
from orionplatform.parameters import FieldParameter
from orionplatform.ports import RecordInputPort, RecordOutputPort


class AM1BCCCharge(RecordPortsMixin, ComputeCube):
    title = "AM1BCC Charge"
    classification = [["charge"]]
    tags = ["AM1BCC", "charge"]
    description = "A cube that assigns partial charges via quacpac AM1BCC"

    # now we only specify parameters for omega
    max_confs = IntegerParameter(
        'max_confs',
        default=10,
        help_text='Maximum number of conformers.')

    max_search_time = IntegerParameter(
        'max_search_time',
        default=2,
        help_text = 'Maiximum search time.')

    energy_window = IntegerParameter(
        'energy_window',
        default=15,
        help_text='Energy window.')

    # ports
    in_port = RecordInputPort('in_port')
    out_port = RecordOutputPort('out_port')

    def begin(self):

        omegaOpts = oeomega.OEOmegaOptions()
        omega = oeomega.OEOmega(omegaOpts)

        omega = oeomega.OEOmega()
        omega.SetIncludeInput(False)
        omega.SetCanonOrder(False)
        omega.SetSampleHydrogens(True)
        omega.SetStrictStereo(False) # JDC
        omega.SetMaxSearchTime(self.args.max_search_time) # maximum omega search time
        omega.SetEnergyWindow(self.args.energy_window)
        omega.SetMaxConfs(self.args.max_confs)
        omega.SetRMSThreshold(1.0)
        self.omega = omega

    # Records are passed to this function for processing.
    def process(self, record, port):
        mols = [_record.get_value(OEPrimaryMolField()) for _record in self.in_port]
        if len(mols) != 1:
            raise Exception('Too many mols.')


        if omega(mol):
            mol, logs = run_elf10(mol)
            mol = mol[0]
            self.log.debug(logs)
            record.set_value(self.out_port, mol)
            self.success.emit(record)

        # TODO: not sure where this should go:
        # g = hgfp.graph.from_oemol(mol)
        # g.ndata['am1_charge'] = torch.Tensor([x.GetDoubleData("AM1Charge") for x in mol.GetAtoms()])
        # g.ndata['bcc_charge'] = torch.Tensor([x.GetDoubleData("BCCCharge") for x in mol.GetAtoms()])
        # bond_orders = np.zeros((g.number_of_edges(), ))
        # for bond in mol.GetBonds():
        #     bond_start = bond.GetBgnIdx()
        #     bond_end = bond.GetEndIdx()
        #     bond_order = bond.GetDoubleData("BondOrder")
        #     bond_orders[g.edge_id(bond_start, bond_end)] = bond_order
        #     bond_orders[g.edge_id(bond_end, bond_start)] = bond_order
