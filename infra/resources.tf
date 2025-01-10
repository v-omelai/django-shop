resource "digitalocean_ssh_key" "ssh" {
  name       = "ssh"
  public_key = file(var.ssh)
}

resource "digitalocean_droplet" "web" {
  image    = var.image
  name     = var.name
  region   = var.region
  size     = var.size
  ssh_keys = [digitalocean_ssh_key.ssh.id]
}
