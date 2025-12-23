const string CHANNEL = "/CH4"

enum ChannelErrorCode {
    ILLEGAL_ARGUMENT = 0;
    INTERNAL_ERROR = 1;
    CONNECTION_ERROR = 2;
    AUTHENTICATIONI_FAILED = 3;
    NEED_PERMISSION_APPROVAL = 4;
    COIN_NOT_USABLE = 5;
    WEBVIEW_NOT_ALLOWED = 6;
}

enum NotificationItemFetchMode {
    ALL = 0;
    APPEND = 1;
}

enum PublicType {
    HIDDEN = 0;
    PUBLIC = 1000;
}

enum ChannelConfiguration {
    MESSAGE = 0;
    MESSAGE_NOTIFICATION = 1;
    NOTIFICATION_CENTER = 2;
}

enum ChannelPermission {
    PROFILE = 0;
    FRIENDS = 1;
    GROUP = 2;
}

enum PaymentType {
    PAYMENT_APPLE = 1;
    PAYMENT_GOOGLE = 2;
}

struct OTPResult {
    1: string otpId;
    2: string otp;
}

struct ChannelToken {
    1: string token;
    2: string obsToken;
    3: i64 expiration;
    4: string refreshToken;
    5: string channelAccessToken;
}

struct NotificationItem {
    1: string id;
    2: string _from;
    3: string to;
    4: string fromChannel;
    5: string toChannel;
    7: i64 revision;
    8: i64 createdTime;
    9: map<string, string> content;
}

struct NotificationFetchResult {
    1: NotificationItemFetchMode fetchMode;
    2: list<NotificationItem> itemList;
}

struct ChannelProvider {
    1: string name;
}

struct ChannelDomain {
    1: string host;
    2: bool removed;
}

struct ChannelInfo {
    1: string channelId;
    3: string name;
    4: string entryPageUrl;
    5: string descriptionText;
    6: ChannelProvider provider;
    7: PublicType publicType;
    8: string iconImage;
    9: list<string> permissions;
    11: string iconThumbnailImage;
    12: list<ChannelConfiguration> channelConfigurations;
    13: bool lcsAllApiUsable;
    14: set<ChannelPermission> allowedPermissions;
    15: list<ChannelDomain> channelDomains;
    16: i64 updatedTimestamp;
}

struct ApprovedChannelInfo {
    1: ChannelInfo channelInfo;
    2: i64 approvedAt;
}

struct ApprovedChannelInfos {
    1: list<ApprovedChannelInfo> approvedChannelInfos;
    2: i64 revision;
}

struct ChannelNotificationSetting {
    1: string channelId;
    2: string name;
    3: bool notificationReceivable;
    4: bool messageReceivable;
    5: bool showDefault;
}

struct ChannelInfos {
    1: list<ChannelInfo> channelInfos;
    2: i64 revision;
}

struct ChannelDomains {
    1: list<ChannelDomain> channelDomains;
    2: i64 revision;
}

struct RequestTokenResponse {
    1: string requestToken;
    2: string returnUrl;
}

struct ChannelIdWithLastUpdated {
    1: string channelId;
    2: i64 lastUpdated;
}

struct CoinUseReservationItem {
    1: string itemId;
    2: string itemName;
    3: i32 amount;
}

struct CoinUseReservation {
    1: string channelId;
    2: string shopOrderId;
    3: PaymentType appStoreCode;
    4: list<CoinUseReservationItem> items;
    5: string country;
}

struct ChannelSyncDatas {
    1: list<ChannelInfo> channelInfos;
    2: list<ChannelDomain> channelDomains;
    3: i64 revision;
    4: i64 expires;
}

struct FriendChannelMatrix {
    1: string channelId;
    2: string representMid;
    3: i32 count;
    4: i32 point;
}

struct FriendChannelMatricesResponse {
    1: i64 expires;
    2: list<FriendChannelMatrix> matrices;
}

struct ChannelSettings {
    1: bool unapprovedMessageReceivable;
}

exception ChannelException {
    1: ChannelErrorCode code;
    2: string reason;
    3: map<string, string> parameterMap;
}

service ChannelService {

    OTPResult issueOTP(
        2: string channelId) throws (1: ChannelException e);

    ChannelToken approveChannelAndIssueChannelToken(
        1: string channelId) throws(1: ChannelException e);

    string approveChannelAndIssueRequestToken(
        1: string channelId,
        2: string otpId) throws(1: ChannelException e);

    NotificationFetchResult fetchNotificationItems(
        2: i64 localRev) throws(1: ChannelException e);

    ApprovedChannelInfos getApprovedChannels(
        2: i64 lastSynced,
        3: string locale) throws(1: ChannelException e);

    ChannelInfo getChannelInfo(
        2: string channelId,
        3: string locale) throws(1: ChannelException e);

    ChannelNotificationSetting getChannelNotificationSetting(
        1: string channelId,
        2: string locale) throws(1: ChannelException e);

    list<ChannelNotificationSetting> getChannelNotificationSettings(
        1: string locale) throws(1: ChannelException e);

    ChannelInfos getChannels(
        2: i64 lastSynced,
        3: string locale) throws(1: ChannelException e);

    ChannelDomains getDomains(
        2: i64 lastSynced) throws(1: ChannelException e);

    FriendChannelMatricesResponse getFriendChannelMatrices(
        1: list<string> channelIds) throws(1: ChannelException e);

    bool updateChannelSettings(
        1: ChannelSettings channelSettings) throws (1: ChannelException e)

    ChannelDomains getCommonDomains(
        1: i64 lastSynced) throws (1: ChannelException e);

    i32 getNotificationBadgeCount(
        2: i64 localRev) throws(1: ChannelException e);

    ChannelToken issueChannelToken(
        1: string channelId) throws(1: ChannelException e);

    string issueRequestToken(
        1: string channelId,
        2: string otpId) throws(1: ChannelException e);

    RequestTokenResponse issueRequestTokenWithAuthScheme(
        1: string channelId,
        2: string otpId,
        3: list<string> authScheme,
        4: string returnUrl) throws(1: ChannelException e);

    string issueRequestTokenForAutoLogin(
        2: string channelId,
        3: string otpId,
        4: string redirectUrl) throws (1: ChannelException e);

    list<string> getUpdatedChannelIds(
        1: list<ChannelIdWithLastUpdated> channelIds) throws (1: ChannelException e);

    string reserveCoinUse(
        2: CoinUseReservation request,
        3: string locale) throws(1: ChannelException e);

    void revokeChannel(
        1: string channelId) throws(1: ChannelException e);

    ChannelSyncDatas syncChannelData(
        2: i64 lastSynced,
        3: string locale) throws(1: ChannelException e);

    void updateChannelNotificationSetting(
        1: list<ChannelNotificationSetting> setting) throws(1: ChannelException e);

}
