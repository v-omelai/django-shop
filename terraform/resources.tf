resource "digitalocean_ssh_key" "public" {
  name       = "ssh"
  public_key = file(var.public)
}

resource "digitalocean_droplet" "web" {
  image    = var.image
  name     = var.name
  region   = var.region
  size     = var.size
  ssh_keys = [digitalocean_ssh_key.public.id]
}

resource "null_resource" "deploy" {
  connection {
    type        = "ssh"
    user        = "root"
    host        = digitalocean_droplet.web.ipv4_address
    private_key = file(var.private)
  }

  provisioner "file" {
    source      = "../.env.prod"
    destination = "/tmp/.env.prod"
  }

  provisioner "file" {
    source      = "deploy.sh"
    destination = "/tmp/deploy.sh"
  }

  provisioner "remote-exec" {
    inline = [
      "chmod +x /tmp/deploy.sh",
      "/tmp/deploy.sh",
    ]
  }
}
