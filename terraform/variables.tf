variable "hcloud_token" {
  description = "Hetzner Cloud API Token"
  type        = string
  sensitive   = true
}

variable "server_type" {
  description = "Hetzner server type (cpx31 recommended for 8GB RAM)"
  type        = string
  default     = "cpx31"
}

variable "location" {
  description = "Hetzner location code (e.g., fsn1, nbg1, hel1)"
  type        = string
  default     = "fsn1"
}

variable "ssh_public_key" {
  description = "SSH public key content for root access"
  type        = string
}
