const string SEARCH = "/search/v1"

enum SearchErrorCode {
    UNKNOWN = 0;
    SUCCESS = 1;
    AUTHENTICATION_FAILURE = 2;
    TIMEOUT = 3;
    MAINTENANCE = 4;
    ILLEGAL_ARGUMENT = 5;
    INTERNAL_ERROR = 6;
}

enum SpotItemCategory {
    UNKNOWN = 0;
    GOURMET = 1;
    BEAUTY = 2;
    TRAVEL = 3;
    SHOPPING = 4;
    ENTERTAINMENT = 5;
    SPORTS = 6;
    TRANSPORT = 7;
    LIFE = 8;
    HOSPITAL = 9;
    FINANCE = 10;
    EDUCATION = 11;
    OTHER = 12;
    ALL = 0000;
}

enum ProductSearchSummaryType {
    STICKER = 1;
    THEME = 2;
    STICON = 3;
}

enum PromotionInfoType {
    NONE = 0;
    CARRIER = 1;
    BUDDY = 2;
    INSTALL = 3;
    MISSION = 4;
    MUSTBUY = 5;
}

enum StickerResourceType {
	STATIC = 1;
	ANIMATION = 2;
	SOUND = 3;
	ANIMATION_SOUND = 4;
	POPUP = 5;
	POPUP_SOUND = 6;
}

enum ThemeResourceType {
    STATIC = 1;
    ANIMATION = 2;
}

enum ProductSearchSummarySubType {
    GENERAL = 0;
    CREATORS = 1;
    STICON = 2;
}

enum PromotionMissionType {
    DEFAULT = 1;
    VIEW_VIDEO = 2;
}

enum BotType {
	RESERVED = 0;
	OFFICIAL = 1;
	LINE_AT_0 = 2;
	LINE_AT = 3;
}

enum SquareType {
	CLOSED = 0;
	OPEN = 1;
}


enum SquareChatState {
    ALIVE = 0;
    DELETED = 1;
    SUSPENDED = 2;
}

struct AutocompleteCandidate {
	1: string candidate;
}

struct AutocompleteResult {
	1: list<string> modifiedQueries;
	2: list<AutocompleteCandidate> candidates;
}

struct Notice {
	1: i32 type;
	2: string notice;
	3: i32 startTime;
	4: i32 endTime;
}

struct KeywordInfo {
	1: string keyword;
	2: string iconPath;
	3: string label;
	4: bool locationInfoAgreement;
}

struct SearchSection {
	1: i32 type;
	2: string title;
	3: KeywordInfo keywordInfos;
}

struct CategoryItem {
	1: i32 collection;
	2: i32 categoryId;
	3: string name;
}

struct SpotItem {
	2: string name;
	3: string phone;
	4: SpotItemCategory category;
	5: string mid;
	6: string countryAreaCode;
	10: bool freePhoneCallable;
}

struct StickerProperty {
	1: bool hasAnimation;
	2: bool hasSound;
	3: bool hasPopup;
	4: StickerResourceType stickerResourceType;
	5: string stickerOptions;
	6: i32 compactStickerOptions;
	7: string stickerHash;
	9: list<string> stickerIds;
}

struct ThemeProperty {
	1: string thumbnailUrl;
	2: ThemeResourceType themeResourceType;
}

struct SticonProperty {
	2: list<string> sticonIds;
}

struct ProductProperty {
	1: StickerProperty stickerProperty;
	2: ThemeProperty themeProperty;
	3: SticonProperty sticonProperty;
}

struct PromotionBuddyInfo {
	1: string buddyMid;
}

struct PromotionInstallInfo {
	1: string downloadUrl;
	2: string customUrlSchema;
}

struct PromotionMissionInfo {
	1: PromotionMissionType promotionMissionType;
	2: bool missionCompleted;
	3: string downloadUrl;
	4: string customUrlSchema;
}

struct PromotionDetail {
	1: PromotionBuddyInfo promotionBuddyInfo;
	2: PromotionInstallInfo promotionInstallInfo;
	3: PromotionMissionInfo promotionMissionInfo;
}

struct PromotionInfo {
	1: PromotionInfoType promotionType;
	51: PromotionBuddyInfo buddyInfo;
	2: PromotionDetail promotionDetail;
}

struct ProductSearchSummary {
	1: string id;
	2: ProductSearchSummaryType type;
	3: string name;
	4: string author;
	5: PromotionInfo promotionInfo;
	6: i64 version;
	7: bool newFlag;
	8: i32 priceTier;
	9: string priceInLineCoin;
	10: ProductProperty property;
	11: ProductSearchSummarySubType subType;
	12: bool onSale;
	13: bool availableForPresent;
	14: bool availableForPurchase;
	15: i32 validDays;
	16: string authorId;
	17: bool bargainFlag;
}

struct ServiceItem {
	1: string id;
	2: string title;
	3: i32 type;
	4: i32 subType;
	5: string appId;
	6: string channelId;
	7: string badge;
	8: string iconUrl;
	9: string downloadUrl;
	10: string launchScheme;
	11: bool iconTint;
}

struct AdditionalInfoItem {
	1: string id;
	2: i32 type;
	3: string title;
	4: string descr;
	5: string iconUrl;
	6: string link;
}

struct YellowpageItem {
	1: string id;
	2: string mid;
	3: string name;
	4: string address;
	5: double latitude;
	6: double longitude;
	7: double distance;
	8: bool canFreeCall;
	9: i32 countryCode;
	10: string phoneNumber;
	11: i32 categoryId;
	12: i32 categoryIcon;
	13: list<AdditionalInfoItem> additionalInfo;
}

struct BuddySearchResult {
	1: string mid;
	2: string displayName;
	3: string pictureStatus;
	4: string picturePath;
	5: string statusMessage;
	6: bool businessAccount;
	7: i32 iconType;
	8: BotType botType;
}

struct GeoAddressItem {
	1: double latitude;
	2: double longitude;
	3: string displayAddress;
}

struct AddFriendData {
	1: string mid;
}

struct InstallAppData {
	1: map<string, string> installData;
}

struct JumpUrlData {}

struct ButtonActionData {
	1: AddFriendData addFriendData;
	2: InstallAppData installAppData;
	3: JumpUrlData jumpUrlData;
}

struct ShortcutButtonAction {
	1: i32 actionType;
	2: ButtonActionData actionData;
}

struct ShortcutButton {
	1: string id;
	2: string title;
	3: string url;
	4: string iconPath;
	5: ShortcutButtonAction action;
}

struct ShortcutItem {
	1: string id;
	2: string title;
	3: string descr;
	4: string iconPath;
	5: string url;
	6: list<ShortcutButton> buttons;
	7: ShortcutButtonAction action;
}

struct Square {
	1: string mid;
	2: string name;
	3: string welcomeMessage;
	4: string profileImageObsHash;
	5: string desc;
	6: bool searchable;
	7: SquareType type;
	8: i32 categoryId;
	9: string invitationURL;
	10: i64 revision;
	11: bool ableToUseInvitationTicket;
	12: SquareChatState state;
}

struct SquareStatus {
	1: i32 memberCount;
	2: i32 joinRequestCount;
	3: i64 lastJoinRequestAt;
	4: i32 openChatCount;
}

struct NoteStatus {
	1: i32 noteCount;
	2: i64 latestCreatedAt;
}

struct SquareInfo {
	1: Square square;
	2: SquareStatus squareStatus;
	3: NoteStatus squareNoteStatus;
}

struct Category {
	1: i32 id;
	2: string name;
}

struct SearchItemUnion {
	1: CategoryItem categoryItem;
	2: SpotItem spotItem;
	3: ProductSearchSummary productItem;
	4: ServiceItem serviceItem;
	5: YellowpageItem yellowpageItem;
	6: BuddySearchResult oaItem;
	7: GeoAddressItem geoAddressItem;
	8: ShortcutItem shortcutItem;
	9: SquareInfo squareItem;
	10: Category squareCategoryItem;
}

struct SearchResultItem {
	1: string id;
	2: i32 type;
	3: SearchItemUnion item;
	4: string title;
	5: string sub1;
	6: string sub2;
	7: string iconUrl;
	8: string titleLink;
	9: string iconLink;
	10: string displayTemplate;
	11: list<AdditionalInfoItem> additionalInfo;
}

struct SearchResultCollection {
	1: i32 collection;
	2: string title;
	3: i32 rank;
	4: i32 hits;
	5: list<SearchResultItem> items;
	6: bool hasNext;
	7: list<i32> categoryId;
	8: string error;
	9: string tabTitle;
	10: i32 start;
	11: i32 length;
	12: i32 squareCategoryId;
}

struct SearchResult {
	1: string sid;
	2: list<SearchResultCollection> collections;
	3: i32 start;
	4: i32 length;
}

struct SearchCommonParameter {
	1: double latitude;
	2: double longitude;
	3: string source;
	4: string region;
	5: string sid;
	6: i32 queryType;
}

struct SearchPagingParameter {
	1: i32 collection;
	2: i32 start;
	3: i32 length;
	4: SearchCommonParameter commonParam;
}

struct AutocompleteRequest {
	1: string query;
	2: string region;
	3: i32 source;
	4: string sid;
}

exception SearchException {
	1: SearchErrorCode code;
	2: string reason;
	3: map<string, string> extra;
}

service SearchService {
	AutocompleteResult getAutocomplete(
		1: AutocompleteRequest request,
	) throws (1: SearchException e),

	map<i32, list<Notice>> getNotice(
		1: set<i32> noticeTypes,
		2: string region,
	) throws (1: SearchException e),

	map<i32, SearchSection> getSearchSection(
		1: set<i32> searchSectionTypes,
		2: string region,
	) throws (1: SearchException e),

	SearchResult searchAll(
		1: string query,
		2: SearchCommonParameter param,
		3: i32 currentCollection,
	) throws (1: SearchException e),

	SearchResult searchCollection(
		1: string query,
		2: SearchPagingParameter param,
	) throws (1: SearchException e),
}
