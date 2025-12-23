const string SQUARE_BOT = "/BP1"

struct SquareBot {
	1: string botMid;
	2: bool active;
	3: string displayName;
	4: string profileImageObsHash;
	5: i32 iconType;
	6: i64 lastModifiedAt;
	7: i64 expiredIn;
}

struct GetSquareBotResponse {
    1: SquareBot squareBot;
}

struct GetSquareBotRequest {
	1: string botMid;
}

enum BotErrorCode {
    UNKNOWN = 0;
    INTERNAL_ERROR = 500;
    ILLEGAL_ARGUMENT = 400;
    AUTHENTICATION_FAILED = 401;
    BOT_NOT_FOUND = 1;
    BOT_NOT_AVAILABLE = 2;
    NOT_A_MEMBER = 3;
}

exception BotException {
	1: BotErrorCode errorCode;
	2: string reason;
	3: map<string, string> parameterMap;
}

service SquareBotService {
    GetSquareBotResponse getSquareBot(
        1: GetSquareBotRequest req,
    ) throws (1: BotException e),
}
