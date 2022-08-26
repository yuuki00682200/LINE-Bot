enum IdentityResponseType {
    UNKNOWN = 0;
    SUCCESS = 1;
    REQUIRE_SERVER_SIDE_EMAIL = 2;
    REQUIRE_CLIENT_SIDE_EMAIL = 3;
}

enum IdentityProvider {
    UNKNOWN = 0;
    LINE = 1;
    NAVER_KR = 2;
    LINE_PHONE = 3;
}

enum ErrorCode {
    ILLEGAL_ARGUMENT = 0;
    AUTHENTICATION_FAILED = 1;
    DB_FAILED = 2;
    INVALID_STATE = 3;
    EXCESSIVE_ACCESS = 4;
    NOT_FOUND = 5;
    INVALID_MID = 9;
    NOT_A_MEMBER = 10;
    INVALID_LENGTH = 6;
    NOT_AVAILABLE_USER = 7;
    NOT_AUTHORIZED_DEVICE = 8;
    NOT_AUTHORIZED_SESSION = 14;
    INCOMPATIBLE_APP_VERSION = 11;
    NOT_READY = 12;
    NOT_AVAILABLE_SESSION = 13;
    SYSTEM_ERROR = 15;
    NO_AVAILABLE_VERIFICATION_METHOD = 16;
    NOT_AUTHENTICATED = 17;
    INVALID_IDENTITY_CREDENTIAL = 18;
    NOT_AVAILABLE_IDENTITY_IDENTIFIER = 19;
    INTERNAL_ERROR = 20;
    NO_SUCH_IDENTITY_IDENFIER = 21;
    DEACTIVATED_ACCOUNT_BOUND_TO_THIS_IDENTITY = 22;
    ILLEGAL_IDENTITY_CREDENTIAL = 23;
    UNKNOWN_CHANNEL = 24;
    NO_SUCH_MESSAGE_BOX = 25;
    NOT_AVAILABLE_MESSAGE_BOX = 26;
    CHANNEL_DOES_NOT_MATCH = 27;
    NOT_YOUR_MESSAGE = 28;
    MESSAGE_DEFINED_ERROR = 29;
    USER_CANNOT_ACCEPT_PRESENTS = 30;
    USER_NOT_STICKER_OWNER = 32;
    MAINTENANCE_ERROR = 33;
    ACCOUNT_NOT_MATCHED = 34;
    ABUSE_BLOCK = 35;
    NOT_FRIEND = 36;
    NOT_ALLOWED_CALL = 37;
    BLOCK_FRIEND = 38;
    INCOMPATIBLE_VOIP_VERSION = 39;
    INVALID_SNS_ACCESS_TOKEN = 40;
    EXTERNAL_SERVICE_NOT_AVAILABLE = 41;
    NOT_ALLOWED_ADD_CONTACT = 42;
    NOT_CERTIFICATED = 43;
    NOT_ALLOWED_SECONDARY_DEVICE = 44;
    INVALID_PIN_CODE = 45;
    NOT_FOUND_IDENTITY_CREDENTIAL = 46;
    EXCEED_FILE_MAX_SIZE = 47;
    EXCEED_DAILY_QUOTA = 48;
    NOT_SUPPORT_SEND_FILE = 49;
    MUST_UPGRADE = 50;
    NOT_AVAILABLE_PIN_CODE_SESSION = 51;
    EXPIRED_REVISION = 52;
    NOT_YET_PHONE_NUMBER = 54;
    BAD_CALL_NUMBER = 55;
    UNAVAILABLE_CALL_NUMBER = 56;
    NOT_SUPPORT_CALL_SERVICE = 57;
    CONGESTION_CONTROL = 58;
    NO_BALANCE = 59;
    NOT_PERMITTED_CALLER_ID = 60;
    NO_CALLER_ID_LIMIT_EXCEEDED = 61;
    CALLER_ID_VERIFICATION_REQUIRED = 62;
    NO_CALLER_ID_LIMIT_EXCEEDED_AND_VERIFICATION_REQUIRED = 63;
    MESSAGE_NOT_FOUND = 64;
    INVALID_ACCOUNT_MIGRATION_PINCODE_FORMAT = 65;
    ACCOUNT_MIGRATION_PINCODE_NOT_MATCHED = 66;
    ACCOUNT_MIGRATION_PINCODE_BLOCKED = 67;
    INVALID_PASSWORD_FORMAT = 69;
    FEATURE_RESTRICTED = 70;
    MESSAGE_NOT_DESTRUCTIBLE = 71;
    PAID_CALL_REDEEM_FAILED = 72;
    PREVENTED_JOIN_BY_TICKET = 73;
    SEND_MESSAGE_NOT_PERMITTED_FROM_LINE_AT = 75;
    SEND_MESSAGE_NOT_PERMITTED_WHILE_AUTO_REPLY = 76;
    SECURITY_CENTER_NOT_VERIFIED = 77;
    SECURITY_CENTER_BLOCKED_BY_SETTING = 78;
    SECURITY_CENTER_BLOCKED = 79;
    TALK_PROXY_EXCEPTION = 80;
    E2EE_INVALID_PROTOCOL = 81;
    E2EE_RETRY_ENCRYPT = 82;
    E2EE_UPDATE_SENDER_KEY = 83;
    E2EE_UPDATE_RECEIVER_KEY = 84;
    E2EE_INVALID_ARGUMENT = 85;
    E2EE_INVALID_VERSION = 86;
    E2EE_SENDER_DISABLED = 87;
    E2EE_RECEIVER_DISABLED = 88;
    E2EE_SENDER_NOT_ALLOWED = 89;
    E2EE_RECEIVER_NOT_ALLOWED = 90;
    E2EE_RESEND_FAIL = 91;
    E2EE_RESEND_OK = 92;
    HITOKOTO_BACKUP_NO_AVAILABLE_DATA = 93;
    E2EE_UPDATE_PRIMARY_DEVICE = 94;
    SUCCESS = 95;
    CANCEL = 96;
    E2EE_PRIMARY_NOT_SUPPORT = 97;
    E2EE_RETRY_PLAIN = 98;
    E2EE_RECREATE_GROUP_KEY = 99;
    E2EE_GROUP_TOO_MANY_MEMBERS = 100;
    SERVER_BUSY = 101;
    NOT_ALLOWED_ADD_FOLLOW = 102;
    INCOMING_FRIEND_REQUEST_LIMIT = 103;
    OUTGOING_FRIEND_REQUEST_LIMIT = 104;
    OUTGOING_FRIEND_REQUEST_QUOTA = 105;
    DUPLICATED = 106;
    BANNED = 107;
}

enum LoginResultType {
    SUCCESS = 1;
    REQUIRE_QRCODE = 2;
    REQUIRE_DEVICE_CONFIRM = 3;
    REQUIRE_SMS_CONFIRM = 4;
}

enum VerificationMethod {
    NO_AVAILABLE = 0;
    PIN_VIA_SMS = 1;
    CALLERID_INDIGO = 2;
    PIN_VIA_TTS = 4;
    SKIP = 10;
}

enum LoginType {
    ID_CREDENTIAL = 0;
    QRCODE = 1;
    ID_CREDENTIAL_WITH_E2EE = 2;
}

struct IdentityCredentialResponse {
    1: map<string, string> metaData;
	2: IdentityResponseType responseType;
	3: string confirmationVerifier;
	4: i64 timeoutInSeconds;
}

struct IdentifierConfirmationRequest {
    1: map<string, string> metaData;
	2: bool forceRegistration;
	3: string verificationCode;
}
struct IdentityCredentialRequest {
    1: map<string, string> metaData;
	2: IdentityProvider identityProvider;
	3: string cipherKeyId;
	4: string cipherText;
	5: IdentifierConfirmationRequest confirmationRequest;
}

struct RSAKey {
    1: string keynm;
    2: string nvalue;
    3: string evalue;
    4: string sessionKey;
}

struct AuthSessionRequest {
    1: map<string, string> metaData;
}

struct E2EEPublicKey {
    1: i32 version;
    2: i32 keyId;
    4: binary keyData;
    5: i64 createdTime;
}

struct VerificationSessionData {
    1: string sessionId;
    2: VerificationMethod method;
    3: string callback;
    4: string normalizedPhone;
    5: string countryCode;
    6: string nationalSignificantNumber;
    7: list<VerificationMethod> availableVerificationMethods;
}

struct LoginResult {
    1: string authToken;
    2: string certificate;
    3: string verifier;
    4: string pinCode;
    5: LoginResultType type;
    6: i64 lastPrimaryBindTime;
    7: string displayMessage;
    8: VerificationSessionData sessionForSMSConfirm;
}

struct LoginRequest {
    1: i32 type;
    2: i32 identityProvider;
    3: string identifier;
    4: string password;
    5: bool keepLoggedIn;
    6: string accessLocation;
    7: string systemName;
    8: string certificate;
    9: string verifier;
    10: string secret;
    11: i32 e2eeVersion;
}

struct SecurityCenterResult {
    1: string uri;
    2: string token;
    3: string cookiePath;
    4: bool skip;
}

exception TalkException {
    1: ErrorCode code;
    2: string reason;
    3: map<string, string> parameterMap;
}

service AuthService {

    IdentityCredentialResponse updatePassword(
	    2: string authSessionId,
		3: IdentityCredentialRequest request) throws (1: TalkException e);

    RSAKey getAuthRSAKey(
	    2: string authSessionId,
		3: IdentityProvider identityProvider) throws (1: TalkException e);

    string openAuthSession(
	    2: AuthSessionRequest request) throws (1: TalkException e);

    string normalizePhoneNumber(
        2: string countryCode,
        3: string phoneNumber,
        4: string countryCodeHint) throws (1: TalkException e);

    void respondE2EELoginRequest(
        1: string verifier,
        2: E2EEPublicKey publicKey,
        3: binary encryptedKeyChain,
        4: binary hashKeyChain,
        5: ErrorCode errorCode) throws (1: TalkException e);

    string confirmE2EELogin(
        1: string verifier,
        2: binary deviceSecret) throws (1: TalkException e);

    void logoutZ() throws (1: TalkException e);

    LoginResult loginZ(
        2: LoginRequest loginRequest) throws (1: TalkException e);

    SecurityCenterResult issueTokenForAccountMigrationSettings(
        2: bool enforce) throws (1: TalkException e);

    SecurityCenterResult issueTokenForAccountMigration(
        2: string migrationSessionId) throws (1: TalkException e);

    string verifyQrcodeWithE2EE(
        2: string verifier,
        3: string pinCode,
        4: ErrorCode errorCode,
        5: E2EEPublicKey publicKey,
        6: binary encryptedKeyChain,
        7: binary hashKeyChain) throws (1: TalkException e);

}
