from sqlalchemy import Column, Integer, String, Float
from database import Base

# ---------------------------------------------------
# Certification Table
# ---------------------------------------------------

class Certification(Base):

    __tablename__ = "certifications"

    id = Column(Integer, primary_key=True, index=True)

    sn = Column(Integer)

    course = Column(String)

    txn_id = Column(String)

    txn_amount = Column(Float)

    txn_status = Column(String)

    txn_time = Column(String)

    applicant_name = Column(String)

    mobile = Column(String)

    district = Column(String)

    referral_of = Column(String)

    referral_code = Column(String)

    referral_role = Column(String)

# ---------------------------------------------------
# Loan Application Table
# ---------------------------------------------------

class LoanApplication(Base):

    __tablename__ = "loan_applications"

    id = Column(Integer, primary_key=True, index=True)

    applicant_name = Column(String)

    district = Column(String)

    gender = Column(String)

    category = Column(String)

    sector = Column(String)

    loan_amount = Column(Float)

    status = Column(String)

# ---------------------------------------------------
# Fraud Investigation Table
# ---------------------------------------------------

class FraudRecord(Base):

    __tablename__ = "fraud_records"

    id = Column(Integer, primary_key=True, index=True)

    sn = Column(Integer)

    district = Column(String)

    msme_name = Column(String)

    owner_name = Column(String)

    phone_no = Column(String)

    training_institute = Column(String)

    dpr_submitted = Column(String)

    business_running = Column(String)

    business_type = Column(String)

    not_running_reason = Column(String)

    loan_usage = Column(String)

    assistance_taken = Column(String)