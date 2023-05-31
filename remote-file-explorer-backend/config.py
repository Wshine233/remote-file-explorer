session_expire_time = 3600000
use_ssl = False
ssl_context = ('remote-file-explorer-backend/cert/cert.crt', 'remote-file-explorer-backend/cert/ca/ca-key.pem')
host = '0.0.0.0'
port = 8512

mount_data_path = 'remote-file-explorer-backend/data/mounts'
perm_data_path = 'remote-file-explorer-backend/data/perms'
ignore_data_path = 'remote-file-explorer-backend/data/ignores'

share_data_path = 'remote-file-explorer-backend/data/shares'

user_data_path = 'remote-file-explorer-backend/data/users'
session_data_path = 'remote-file-explorer-backend/data/sessions'

permission_group_path = 'remote-file-explorer-backend/data/permission_groups'
default_group = 'restrict'