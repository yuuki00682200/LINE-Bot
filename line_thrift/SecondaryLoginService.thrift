enum SecondaryQrCodeErrorCode {
	INTERNAL_ERROR = 0,
	ILLEGAL_ARGUMENT = 1,
	VERIFICATION_FAILED = 2,
	NOT_ALLOWED_QR_CODE_LOGIN = 3,
	VERIFICATION_NOTICE_FAILED = 4,
	RETRY_LATER = 5,
	INVALID_CONTEXT = 100,
	APP_UPGRADE_REQUIRED = 101
}

enum CallbackType {
    NOTIFY_SECONDARY_LOGIN_PIN = 3;
    NOTIFY_SECONDARY_LOGIN_QRCODE = 4;
    NOTIFY_SECONDARY_LOGIN_E2EE_PIN = 5;
    NOTIFY_SECONDARY_EMAIL_LOGIN_SUCCESS = 6;
}

struct CreateQrSessionRequest {

}

struct CreateQrSessionResponse {
    1: string authSessionId;
}

struct CreateQrCodeRequest {
    1: string authSessionId;
}

struct CreateQrCodeResponse {
    1: string callbackUrl;
}

struct CheckQrCodeVerifiedRequest {
    1: string authSessionId;
}

struct CheckQrCodeVerifiedResponse {

}

struct VerifyCertificateRequest {
	1: string authSessionId;
	2: string certificate;
}

struct VerifyCertificateResponse {

}

struct CreatePinCodeRequest {
    1: string authSessionId;
}

struct CreatePinCodeResponse {
    1: string pinCode;
}

struct CheckPinCodeVerifiedRequest {
    1: string authSessionId;
}

struct CheckPinCodeVerifiedResponse {

}

struct QrCodeLoginRequest {
    1: string authSessionId;
    2: string systemName;
    3: bool autoLoginIsRequired;
}

struct QrCodeLoginResponse {
    1: string certificate;
    2: string accessToken;
    3: i64 lastBindTimestamp;
    4: map<string, string> metaData;
}

exception SecondaryQrCodeException {
    1: SecondaryQrCodeErrorCode code;
    2: string alertMessage;
}

service SecondaryLoginService {

    CreateQrSessionResponse createSession(
        1: CreateQrSessionRequest req) throws(1: SecondaryQrCodeException e),

    CreateQrCodeResponse createQrCode(
        1: CreateQrCodeRequest req) throws(1: SecondaryQrCodeException e),

    CheckQrCodeVerifiedResponse checkQrCodeVerified(
        1: CheckQrCodeVerifiedRequest req) throws(1: SecondaryQrCodeException e),

    VerifyCertificateResponse verifyCertificate(
        1: VerifyCertificateRequest req) throws(1: SecondaryQrCodeException e),

    CreatePinCodeResponse createPinCode(
        1: CreatePinCodeRequest req) throws(1: SecondaryQrCodeException e),

    CheckPinCodeVerifiedResponse checkPinCodeVerified(
        1: CheckPinCodeVerifiedRequest req) throws(1: SecondaryQrCodeException e),

    QrCodeLoginResponse qrCodeLogin(
        1: QrCodeLoginRequest req) throws(1: SecondaryQrCodeException e),

}

