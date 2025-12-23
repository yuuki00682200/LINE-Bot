const string LIFF = "/LIFF1"

enum LiffViewFeatures {
    ADVERTISING_ID = 2;
    BLUETOOTH_LE = 3;
    GEOLOCATION = 1;
}

enum LiffErrorCode {
	INVALID_REQUEST = 1;
	UNAUTHORIZED = 2;
	CONSENT_REQUIRED = 3;
	VERSION_UPDATE_REQUIRED = 4;
	SERVER_ERROR = 100;
}

struct LiffView {
	1: string type;
	2: string url;
	11: bool trustedDomain;
	6: string titleIconUrl;
	4: i32 titleTextColor;
	7: i32 titleSubtextColor;
	8: i32 titleButtonColor;
	5: i32 titleBackgroundColor;
	9: i32 progressBarColor;
	10: i32 progressBackgroundColor;
}

struct LiffNoneContext {}

struct LiffChatContext {
	1: string chatMid;
}

struct LiffSquareChatContext {
	1: string squareChatMid;
}

struct LiffContext {
	1: LiffNoneContext none;
	2: LiffChatContext chat;
	3: LiffSquareChatContext squareChat;
}

struct LiffErrorConsentRequired {
	1: string channelId;
	2: string consentUrl;
}

struct LiffErrorPayload {
	3: LiffErrorConsentRequired consentRequired;
}

struct LiffViewResponse {
	1: LiffView view;
	2: string contextToken;
	3: string accessToken;
	4: string featureToken;
	5: list<LiffViewFeatures> features;
	6: string channelId;
}

struct LiffViewRequest {
	1: string liffId;
	2: LiffContext context;
}

struct RevokeTokenRequest {
	1: string accessToken;
}

exception LiffException {
	1: LiffErrorCode code;
	2: string message;
	3: LiffErrorPayload payload;
}

service LiffService {
	LiffViewResponse issueLiffView(
		1: LiffViewRequest request,
	) throws (1: LiffException e),

	void revokeToken(
		1: RevokeTokenRequest request,
	) throws (1: LiffException e),
}
