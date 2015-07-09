###############################################################################
# Copyright 2015 Kansas Healthcare Collaborative. All rights reserved.
# This file is part of the BlueButton.py project.
# Use of this source code is governed by the license found in the LICENSE file.
###############################################################################

from ._c32.allergies import allergies
from ._c32.demographics import demographics
from ._c32.document import document
from ._c32.encounters import encounters
from ._c32.immunizations import immunizations
from ._c32.medications import medications
from ._c32.problems import problems
from ._c32.procedures import procedures
from ._c32.results import results
from ._c32.vitals import vitals
from ..core import wrappers


def run(c32):
    data = wrappers.ObjectWrapper()

    data.document = document(c32)
    data.allergies = allergies(c32)
    data.demographics = demographics(c32)
    data.encounters = encounters(c32)
    data.immunizations = immunizations(c32).administered
    data.immunization_declines = immunizations(c32).declined
    data.results = results(c32)
    data.medications = medications(c32)
    data.problems = problems(c32)
    data.procedures = procedures(c32)
    data.vitals = vitals(c32)

    """
    Some sections are in the CCDA but not the C32,
    maintain consistent API by adding null/None/empty entries.
    """
    data.smoking_status = wrappers.ObjectWrapper(
        date=None,
        name=None,
        code=None,
        code_system=None,
        code_system_name=None
    )

    data.chief_complaint = wrappers.ObjectWrapper(
        text = None
    )

    data.care_plan = wrappers.ListWrapper([])
    data.instructions = wrappers.ListWrapper([])
    data.functional_statuses = wrappers.ListWrapper([])

    return data