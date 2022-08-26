const string CHAT_APP = "/CAPP1"

enum ChatappErrorCode {
    INVALID_REQUEST = 1;
    UNAUTHORIZED = 2;
    SERVER_ERROR = 100;
}

enum ChatappAvailableChatTypes {
	PERSONAL = 1;
	ROOM = 2;
	GROUP = 3;
	SQUARE_CHAT = 4;
}

enum MyChatappPriority {
	PRIORITY = 2;
	REGULAR = 1;
	MORE = 3;
}

struct Chatapp {
	1: string chatappId;
	2: string name;
	3: string icon;
	4: string url;
	5: ChatappAvailableChatTypes availableChatTypes;
}

struct MyChatapp {
	1: Chatapp app;
	2: MyChatappPriority category;
	3: i64 priority;
}

struct GetMyChatappsResponse {
	1: list<MyChatapp> apps;
	2: string continuationToken;
}

struct GetChatappRequest {
	1: string chatappId;
	2: string language;
}

struct GetMyChatappsRequest {
	1: string language;
	2: string continuationToken;
}

exception ChatappException {
	1: ChatappErrorCode code;
	2: string reason;
}

service ChatappService {
	GetMyChatappsResponse getChatapp(
		1: GetChatappRequest request,
	) throws (1: ChatappException e),

	GetMyChatappsResponse getMyChatapps(
		1: GetMyChatappsRequest request,
	) throws (1: ChatappException e),
}
