enum ThingsDeviceProductType {
    CLOUD = 1;
    BLE = 2;
}

enum ThingsErrorCode {
    INTERNAL_SERVER_ERROR = 0;
    UNAUTHORIZED = 1;
    INVALID_REQUEST = 2;
    INVALID_STATE = 3;
}

struct ThingsDevice {
	1: string deviceId;
	2: string actionUri;
	3: string botMid;
	4: ThingsDeviceProductType productType;
	5: string providerName;
	6: string profileImageLocation;
	7: list<string> channelIdList;
}

struct BleProduct {
	1: string serviceUuid;
	2: string psdiServiceUuid;
	3: string psdiCharacteristicUuid;
	4: string name;
	5: string profileImageLocation;
}

struct UserDevice {
	1: ThingsDevice device;
	2: string deviceDisplayName;
}

struct GetBleDeviceRequest {
	1: string serviceUuid;
	2: string psdi;
}

struct DeviceLinkRequest {
	1: string deviceId;
}

struct DeviceUnlinkRequest {
	1: string deviceId;
}

exception ThingsException {
	1: ThingsErrorCode code;
	2: string reason;
}

service ThingsService {
	ThingsDevice getBleDevice(
		1: GetBleDeviceRequest request,
	) throws (1: ThingsException e),

	list<BleProduct> getBleProducts() throws (1: ThingsException e),

	list<UserDevice> getLinkedDevices() throws (1: ThingsException e),

	void linkDevice(
		1: DeviceLinkRequest request,
	) throws (1: ThingsException e),

	void unlinkDevice(
		1: DeviceUnlinkRequest request,
	) throws (1: ThingsException e),
}
