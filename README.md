# Wazuh SOARCA integration

This module maps a Wazuh alerts to CACAO variable to trigger a playbook.

## Installation in Wazuh SIEM

Install Wazuh SIEM first! Use the  [installation](https://documentation.wazuh.com/current/quickstart.html) or use the Ansible script in this repo

```bash
cd ansible/wazuh-ansible-4.11.0
cp playbooks/vault.yml.example playbooks/vault.yml
nano playbooks/vault.yml
nano inventory
ansible-playbook -e @playbooks/vault.yml playbooks/wazuh-single-secure.yml -i inventory 
```

## Install the SOARCA Wazuh connector

```bash 
wget https://raw.githubusercontent.com/thecyberproject/SOARCA-wazuh-integration/refs/heads/main/custom_soarca.py
cp custom_soarca.py /var/ossec/integrations/custom-soarca.py
cd /var/ossec/integrations/
chown root:wazuh custom-soarca.py
chmod 750 custom-soarca.py
cp /var/ossec/integrations/slack /var/ossec/integrations/custom-soarca
chown root:wazuh custom-soarca
```

## Install SOARCA
On the SOARCA host execute the following

```bash
git clone https://github.com/COSSAS/SOARCA.git soarca
cd soarca/deployments/docker/soarca
# replace docker.io/cossas/soarca:latest with docker.io/cossas/soarca:development
sed -i 's/soarca:latest/soarca:development/' docker-compose.yml 
docker compose up -d --force-recreate
```

## Configure Wazuh
On the Wazuh host we need to add File Integrity Monitor (FIM)
This is based on the guide https://wazuh.com/blog/detecting-and-responding-to-malicious-files-using-cdb-lists-and-active-response/?highlight=fim%20detect%20hashes

```bash
touch /var/ossec/etc/lists/malware-hashes
echo -n 6297388ec99af270aca1b6d95c6879fe23015cecdbf6f9144aae5ae0892e25ee:soarca-logo > /var/ossec/etc/lists/malware-hashes
chown root:wazuh /var/ossec/etc/lists/malware-hashes

#Open the local rules
nano /var/ossec/etc/rules/local_rules.xml

#add the following
<group name="local,malware,">
  <rule id="100002" level="5">
    <if_sid>554</if_sid>
    <list field="sha256" lookup="match_key">etc/lists/malware-hashes</list>
    <description>A file - $(file) - in the malware blacklist was added to the system.</description>
  </rule>

  <rule id="100003" level="5">
    <if_sid>100002</if_sid>
    <field name="file" type="pcre2">(?i)[c-z]:</field>
    <description>A file - $(file) - in the malware blacklist was added to the system.</description>
  </rule>
</group>


# Add line to ossec conf
<list>etc/lists/malware-hashes</list>  

# Update wazuh soarca trigger
Add rule to the settings of the manager


# restart the wazuh manager
systemctl restart wazuh-manager

```

### Enrol agent via the agent page 
Download and install the agent on Windows to make sure the machine is monitored.

## Add playbook to SOARCA
```bash
# make sure an ssh server is running on adres 192.168.0.10

curl -X POST -H "Content-Type: application/json" -d @./playbook/starter-playbook.json localhost:8080/playbook/
```


## Test
- Trigger Windows agent by downloading the soarca logo from the GitHub

https://raw.githubusercontent.com/COSSAS/SOARCA/refs/heads/development/assets/soarca-logo.svg