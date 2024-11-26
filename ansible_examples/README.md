# Ansible Examples

This repository contains various Ansible playbooks and roles used for automating tasks in the Photonic Lab NDFC Automation Webinar.

## Folder Structure
This folder structure contains the list of the files that you might need to consider if/when testing the playbooks in your own environment
### Warning!
Secrets for the additional services are stored inside the inventory/host_vars/ndfc01.yml file. Replace the values there

```
ansible_examples/
├── playbooks/
│   ├── playbook_1.yml
│   ├── playbook_2.yml
│   ├── playbook_3.yml
│   ├── playbook_4.yml
│   ├── mil-cml-wks-fabric-overlays.yml
├── inventory/
│   ├── host_vars/
│   │   └── ndfc01.yml
│   ├── group_vars/
│   │   └── ndfc.yml
│   └── hosts.yml
```

## Playbooks

- **playbook_1.yml**: Generate networks and VRF statically. No variables or loops used here
- **playbook_2.yml**: Generate networks and VRF with the help of an external variable file and a loop. The benefit here is the fact that there is no need to modify the playbook file itself
- **playbook_3.yml**: Read the data from an external Netbox and then create the objects in NDFC and the PortGroups in vCenter.
- **playbook_4.yml**: Contains a full example on how to create an external fabric and configure the 3 core routers interfaces, plus some protocols like OSPF and BGP 

## Inventory

- **hosts.yml**: Inventory file containing the IP address of NDFC. Replace it with your own
- 

## Usage

To run a playbook, use the following command:

```sh
ansible-playbook -i inventory/hosts playbook_1.yml --ask-vault-password
```

--ask-vault-password is only required if you keep the secrets inside inventory/host_vars/ndfc01.yml encrypted. If you type your secrets in plain, unencrypted text then it won't be necessaire.

Replace `playbook_1.yml` with the playbook you want to run.

