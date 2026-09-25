# German Grammar Corrector (K3s on Hetzner)

Note a working deployment of this is present at the URL submitted along with the assignment. I am omitting mentioning the URL here due to concerns with regard to DDOSing via bots present in the wild. 

To test this on the live deployment do check out the "Testing the code" section, replacing it with the URL present in the assignment

## Installing required dependencies

macOS (via Homebrew):
```bash
brew tap hashicorp/tap
brew install hashicorp/tap/terraform
```


Ubuntu / Debian Linux:
```bash
sudo apt-get update && sudo apt-get install -y gnupg software-properties-common curl
curl -fsSL https://apt.releases.hashicorp.com/gpg | sudo gpg --dearmor -o /usr/share/keyrings/hashicorp-archive-keyring.gpg
echo "deb [signed-by=/usr/share/keyrings/hashicorp-archive-keyring.gpg] https://apt.releases.hashicorp.com $(lsb_release -cs) main" | sudo tee /etc/apt/sources.list.d/hashicorp.list
sudo apt update && sudo apt install terraform
```

## Terraform deployment instuctions

1. Copy the terraform.tfvars.example file into terraform.tfvars
2. Create an API key from hetzner by opening a project in Hetzner, then going to security, then to "API Tokens", copy this into the new terraform.tfvars file
3. Do copy your ssh key to the terraform.tfvars file, In a unix like machine (linux, macos, etc..) you can do:
    - If you don't already have an ssh key, you may create this from `ssh-keygen -t ed25519``
    - Run `cat ~/.ssh/id_ed25519.pub` to view your own SSH key
    - Do copy this file's contents into terraform.tfvars in the appropriate section

4. Initialize and provision the infrastructure

```bash
cd terraform
terraform init
terraform apply -auto-approve
````

5. You can build the container on the server with

```bash
# Get the server IP from terraform output
SERVER_IP=$(terraform output -raw server_ipv4)

# Copy application files to the server
cd ..
scp -r Dockerfile app k8s root@$SERVER_IP:/root/

# Build the container and import into K3s containerd
ssh root@$SERVER_IP "docker build -t grammar-corrector:latest /root && docker save grammar-corrector:latest | k3s ctr -n k8s.io images import -"
```

6. Deploy kubernetes

```bash
ssh root@$SERVER_IP "k3s kubectl apply -f /root/k8s/deployment.yaml"
````

7. Optionally, connect a custom domain

In your DNS provider, add the following details in a new record

```bash
Type: A
Name: grammer-correcter
Target / IP: <SERVER_IP>
```

you can get the server IP by doing `terraform output -raw server_ipv4`

## Testing the code

### Single request

The code can be tested using - for a single request

Note : The actual service url is present in the assignment, it is omitted here to prevent the server from being DDOSed

```bash
curl -X POST "https://(service url here, present in assignment submission)" \
  -H "Content-Type: application/json" \
  -d '{"text": "Ich gehe in die Schule jeden Tag mit der Bus."}'
```

### On a custom domain
`API_URL="(replace with the correct URL)" python3 test_server.py`