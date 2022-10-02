import meraki
import config
import json

# Instantiate Dashboard API client
dashboard = meraki.DashboardAPI(config.api_key)
# Get organizations
orgs = dashboard.organizations.getOrganizations()
org_id = ""

# If an org_id is not provided in config.py, and an org_name is provided, find the org_id based on the org_name
if config.org_id == "":
    for org in orgs:
        if org['name']==config.org_name:
            org_id=org['id']

    if org_id != "":
        pass
    else:
        print("No organization found with the specified name. Enter a valid org_name or org_id in the config.py file and rerun.")
        exit()
# If an org_id is provided in config.py, assign to org_id
else:
    org_id = config.org_id

vmx_data = []
# For every region, instantiate a pair of vMX networks and configure them according to config.py
for i in range(2*config.num_regions):
    net = dashboard.organizations.createOrganizationNetwork(
        name=f"{config.region_name_prefixes[int(i/2)]}-vMX{i+1}",
        timeZone="America/New_York",
        tags=["vMXer",config.cloud_environment, f"vMX{i+1}", f"{config.regions[int(i/2)]}"],
        productTypes=["appliance"],
        organizationId=org_id
    )
    vmx = dashboard.networks.vmxNetworkDevicesClaim(networkId=net['id'], size=config.vmx_size)
    update_vmx = dashboard.devices.updateDevice(
        serial=vmx['serial'],
        name=f"{config.region_name_prefixes[int(i/2)]}-vMX{i+1}",
        tags=[f"vMX{i+1}"]
    )
    # Set up as Hub
    hub = dashboard.appliance.updateNetworkApplianceVpnSiteToSiteVpn(
        networkId=net['id'],
        mode=config.vpn_mode
    )
    
    # Obtain the authentication token for the vMX
    token = dashboard.appliance.createDeviceApplianceVmxAuthenticationToken(serial=vmx['serial'])
    passthrough = dashboard.appliance.updateNetworkApplianceSettings(
        networkId=net["id"],
        clientTrackingMethod="MAC address",
        deploymentMode="passthrough"
    )

    # Store data from each vMX in a json file for easy reference
    vmx_data.append(
        {
            "net_id": net['id'],
            "net_name": net['name'],
            "vmx_serial": vmx['serial'],
            "vmx_name": update_vmx["name"],
            "vmx_tags": update_vmx["tags"],
            "region": config.regions[int(i/2)],
            "vpc_subnet": config.vpc_summary_ranges[int(i/2)],
            "token": token["token"],
            "expiration": token["expiresAt"]
        }
    )

# Display vmx_data details
for vmx in vmx_data:
    print(vmx)

# Save json file with vmx_data
with open('vmx_data.json', 'w', encoding='utf-8') as f:
    json.dump(vmx_data, f, ensure_ascii=False, indent=4)
