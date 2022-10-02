# credentials
# either org_id or org_name is needed, not both
api_key = "MERAKI_API_KEY"
org_id = ""
org_name = ""
# deployment_mode = passthrough or routed
# client_track = MAC address or IP address
deployment_mode = "passthrough"
client_track = "MAC address"
vpn_mode = "hub"
# Cloud Settings
num_regions = 2
regions = ['us-east-1', 'us-west-1']
vmx_size = "medium"
cloud_environment = "aws"
# don't exceed the number of regions set in num_regions
# no whitespaces in names
region_name_prefixes = ["us_east_1", "us_west_1"]
vpc_summary_ranges = ["10.210.0.0/16","10.211.0.0/16"]
vpc_transit_subnet = []
