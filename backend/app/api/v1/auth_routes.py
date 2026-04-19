import uuid
from fastapi import APIRouter, HTTPException
from twilio.base.exceptions import TwilioRestException
from app.models.auth_models import RequestOTPPayload, VerifyOTPPayload
from app.services.auth.auth_service import generate_otp, verify_otp, DatabaseUnavailableError, RateLimitExceededError

router = APIRouter()


@router.post("/request-otp")
def request_otp(payload: RequestOTPPayload):
    if not payload.phone_number:
        raise HTTPException(status_code=400, detail="Phone number is required")

    try:
        generate_otp(payload.phone_number)
        return {"message": "OTP sent successfully via SMS"}
    except RateLimitExceededError as e:
        raise HTTPException(status_code=429, detail=str(e))
    except DatabaseUnavailableError as e:
        raise HTTPException(status_code=503, detail=str(e))
    except ValueError as e:
        raise HTTPException(status_code=500, detail=str(e))
    except TwilioRestException as e:
        raise HTTPException(status_code=502, detail=f"SMS delivery failed: {e.msg}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Unexpected error sending OTP: {str(e)}")


@router.post("/verify-otp")
def verify_otp_endpoint(payload: VerifyOTPPayload):
    if not payload.phone_number or not payload.user_otp:
        raise HTTPException(status_code=400, detail="Phone number and OTP are required")

    try:
        is_valid = verify_otp(payload.phone_number, payload.user_otp)
    except DatabaseUnavailableError as e:
        raise HTTPException(status_code=503, detail=str(e))
    except ValueError as e:
        raise HTTPException(status_code=401, detail=str(e))

    if is_valid:
        session_token = str(uuid.uuid4())
        return {
            "message": "Authentication successful",
            "token": session_token,
            "phone_number": payload.phone_number,
        }
    else:
        raise HTTPException(status_code=401, detail="Incorrect OTP. Please try again.")
