from app.core.config import settings
import logging

logger = logging.getLogger(__name__)

async def send_sms(phone_number: str, message: str) -> bool:
    """
    Send SMS using Twilio (or print to console for development)
    """
    try:
        if settings.SMS_ENABLED:
            # TODO: Implement Twilio integration
            # from twilio.rest import Client
            # client = Client(settings.TWILIO_ACCOUNT_SID, settings.TWILIO_AUTH_TOKEN)
            # message = client.messages.create(
            #     body=message,
            #     from_=settings.TWILIO_PHONE_NUMBER,
            #     to=phone_number
            # )
            logger.info(f"SMS sent to {phone_number}")
            return True
        else:
            # Development mode - print OTP to console
            logger.info(f"📱 SMS to {phone_number}: {message}")
            print(f"\n{'='*50}")
            print(f"📱 DEV MODE - SMS to {phone_number}")
            print(f"📨 Message: {message}")
            print(f"{'='*50}\n")
            return True
    except Exception as e:
        logger.error(f"Failed to send SMS: {e}")
        return False

async def send_otp(phone_number: str, otp_code: str) -> bool:
    """Send OTP code via SMS"""
    message = f"Your verification code is: {otp_code}. Valid for {settings.OTP_EXPIRE_MINUTES} minutes."
    return await send_sms(phone_number, message)