"""
## 2. Config files parsing
Study Case: Multi environment Config manager
Konteks: ada beberapa environment, parsing config untuk masing2 environment, ambil dari .env.example dan masukin ke .env
Perintah:
- Baca example.config.yaml
- Baca secrets.json
- Tulis ke envvars ke config.yaml sesuai argument
"""

import pathlib
import yaml
from dotenv import dotenv_values
import sys
import json

# paths
SCRIPT_DIR = pathlib.Path(__file__).parent.resolve()
config_yaml = SCRIPT_DIR / "example.config.yaml"
prod_env = SCRIPT_DIR / ".env.prod"
dev_env = SCRIPT_DIR / ".env.dev"
secrets_json = SCRIPT_DIR / "secrets.json"



ENV_MAPPING = {
    "DATABASE_HOST": ["database", "host"],
    "DATABASE_PORT": ["database", "port"],
    "DATABASE_NAME": ["database", "name"],
    "LOGGING_LEVEL": ["logging", "level"],
    "FEATURES_RATE_LIMIT": ["features", "rate_limit"],
    "SERVER_WORKERS": ["server", "workers"],
}

def apply_env_to_config(config, env_vars, secrets):
    for env_key, path in ENV_MAPPING.items():
        if env_key in env_vars:
            target = config
            # navigasi ke path di config file (["database", "host"]-> database: {host:value})
            for key in path[:-1]:
                # ubah target jadi target[key], kalau key belum ada buat dict baru
                target = target.setdefault(key, {})
            target[path[-1]] = env_vars[env_key]
            
    # for secret_key, secret_value in secrets.items():
    #     print (secret_key, secret_value)
    #     target=config
    #     for key,val in secret_value.items():
    #         target=target.setdefault(val,{})
    #         target[val]=secret_value[key][val]

    return config


def main():
    # baca args dari command line untuk pilih environment
    env_args = "prod"
    if sys.argv[1:]:
        env_args = sys.argv[1]
    
    if env_args == "prod":
        env_vars = dotenv_values(prod_env)
    elif env_args == "dev":
        env_vars = dotenv_values(dev_env)
    
    with open(config_yaml) as f:
        config = yaml.safe_load(f)
    with open(secrets_json) as f:
        secrets = json.load(f)
        
    updated_config = apply_env_to_config(config, env_vars, secrets)
    with open(SCRIPT_DIR / "config.yaml", "w") as f:
        yaml.dump(updated_config, f)
    
if __name__ == "__main__":
    main()