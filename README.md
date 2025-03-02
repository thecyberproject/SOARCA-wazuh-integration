# Wazuh SOARCA integration

This module maps a Wazuh alerts to CACAO variable to trigger a playbook.

## Installation in Wazuh SIEM

Install Wazuh SIEM first! [installation](https://documentation.wazuh.com/current/quickstart.html)

```bash 
wget https://raw.githubusercontent.com/thecyberproject/SOARCA-wazuh-integration/refs/heads/main/custom_soarca.py
cp custom_soarca.py file to /var/ossec/integrations/custom-soarca.py
chown root:wazuh custom-soarca
chmod 750 custom-soarca
cp /var/ossec/integrations/slack to /var/ossec/integrations/soarca
```
## Install SOARCA
```bash
wget https://raw.githubusercontent.com/COSSAS/SOARCA/refs/heads/development/deployments/docker/soarca/docker-compose.yml
replace docker.io/cossas/soarca:latest with docker.io/cossas/soarca:development
docker compose up -d --force-recreate

```
## Configure
- set central agent config
- setup FIM
- enrol agent (Windows)

- Add playbook to SOARCA
- Add trigger to FIM
- Link trigger to Playbook

## Test
- Trigger Windows agent by creating file 