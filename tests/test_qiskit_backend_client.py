"""
\********************************************************************************
* Copyright (c) 2023 the Qrisp authors
*
* This program and the accompanying materials are made available under the
* terms of the Eclipse Public License 2.0 which is available at
* http://www.eclipse.org/legal/epl-2.0.
*
* This Source Code may also be made available under the following Secondary
* Licenses when the conditions for such availability set forth in the Eclipse
* Public License, v. 2.0 are satisfied: GNU General Public License, version 2
* with the GNU Classpath Exception which is
* available at https://www.gnu.org/software/classpath/license.html.
*
* SPDX-License-Identifier: EPL-2.0 OR GPL-2.0 WITH Classpath-exception-2.0
********************************************************************************/
"""

# Created by ann81984 at 23.05.2022
import numpy as np

from qrisp import QuantumCircuit
from qrisp.interface.backends import VirtualBackend
from qrisp.interface.backends import VirtualQiskitBackend



def test_qiskit_backend_client():
    
    try:
        from qiskit import Aer
        backend = Aer.get_backend("qasm_simulator")
    except ImportError:
        from qiskit.providers.basic_provider import BasicProvider
        backend = BasicProvider().get_backend('basic_simulator')

    # Create QuantumCricuit
    qc = QuantumCircuit()

    qc.add_qubit()
    qc.add_qubit()
    

    qc.h(0)

    qc.rz(np.pi / 2, 0)

    qc.x(0)
    qc.cx(0, 1)
    

    qc.append(qc.to_op("composed_op"), qc.qubits, qc.clbits)

    qc.append(qc.to_op("multi_composed_op"), qc.qubits, qc.clbits)

    qc.add_clbit()
    qc.measure(1, 0)    
    print(qc)

    ###################

    # Create VirtualBackend
    def sample_run_func(qc, shots, token):
        print("Executing Circuit")
        return {"0": shots}

    test_virtual_backend = VirtualBackend(sample_run_func)

    print(test_virtual_backend.run(qc, 100))
    assert str(test_virtual_backend.run(qc, 100)) == "{'0': 100}"
    assert test_virtual_backend.run(qc, 100)["0"] == 100

    ###################

    # Create Qiskit Backend
    test_qiskit_backend = VirtualQiskitBackend()

    qc = QuantumCircuit(4, 1)
    qc.x(0)
    qc.measure(0, 0)

    print(test_qiskit_backend.run(qc, 2000))
    # status = test_qiskit_backend.ping()
    assert str(test_qiskit_backend.run(qc, 2000)) == "{'1': 2000}"