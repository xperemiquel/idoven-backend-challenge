from uuid import UUID
import logging
from database import Session
from models.models import ECG, Lead, LeadAnalysis
import numpy as np

logger = logging.getLogger("__name__")


def calculate_zero_crossings(signal: list) -> int:
    """
    Calculates the zero crossings of a given signal.

    We assume that a zero value is not relevant for our solution, so we remove all 0 from the signal to simplify
    the solution. In addition, we are using Numpy to optimize efficiency.

    Then we create 2 arrays one without the first item, and another one without the last item of teh original array.
    This way can easily multiply each number in the array for their adjacent one and get the product.
    If the product is negative it mean we detected a zero crossing, then whe sum them all.
    """

    np_array = np.array(signal)
    np_array = np_array[np_array != 0]
    return int(((np_array[:-1] * np_array[1:]) < 0).sum())


def process_ecg(ecg_id: UUID):
    """
    Process all leads of an ECG: calculate zero crossings and update the database.

    Assumes `ecg_id` is a UUID.

    Parameters:
    - ecg_id (UUID): The UUID of the ECG to process.
    """
    db = Session()

    try:
        ecg = db.query(ECG).filter(ECG.id == ecg_id).first()
        leads = db.query(Lead).filter(Lead.ecg == ecg).all()
        for lead in leads:
            num_zero_crosses = calculate_zero_crossings(lead.signal)
            analysis = LeadAnalysis(id=lead.id, num_zero_crosses=num_zero_crosses)
            db.add(analysis)
        ecg.processed = True
        db.commit()
    except Exception as e:
        db.rollback()
        logger.error(e)
    finally:
        db.close()
