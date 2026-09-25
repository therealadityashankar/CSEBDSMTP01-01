output "server_ipv4" {
  description = "Public IPv4 address of the K3s server"
  value       = hcloud_server.k3s.ipv4_address
}

output "kubeconfig_fetch_cmd" {
  description = "Command to fetch kubeconfig from the server"
  value       = "ssh root@${hcloud_server.k3s.ipv4_address} 'cat /etc/rancher/k3s/k3s.yaml' | sed 's/127.0.0.1/${hcloud_server.k3s.ipv4_address}/g' > kubeconfig.yaml"
}
