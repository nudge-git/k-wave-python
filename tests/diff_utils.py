import os
from pprint import pprint
from warnings import warn

import h5py

from tests.h5_summary import H5Summary


def compare_against_ref(reference: str, h5_path, eps=1e-8, precision=8):
    summary_ref = H5Summary.load(reference)
    summary_new = H5Summary.from_h5(h5_path)

    print('Comparing Summary files ...')
    diff = summary_ref.get_diff(summary_new, eps=eps, precision=precision)
    if len(diff) != 0:
        warn('H5Summary files do not match! Printing the difference:')
        pprint(diff)
    return len(diff) == 0


def check_h5_equality(path_a, path_b):
    # H5DIFF doesn't support excluding attributes from comparison
    # Therefore we remove them manually
    # Don't apply this procedure in the final version!
    for path in [path_a, path_b]:
        with h5py.File(path, "a") as f:
            for attr in ['creation_date', 'file_description', 'created_by']:
                if attr in f.attrs:
                    del f.attrs[attr]

    cmd = f'h5diff -c -d 0.00000001 {path_a} {path_b}'
    print(cmd)
    res = os.system(cmd)
    return res == 0
