variable "token" {
  description = "DigitalOcean API token"
  type        = string
}

variable "image" {
  description = "The base image for the Droplet"
  type        = string
}

variable "name" {
  description = "Name of the Droplet"
  type        = string
}

variable "region" {
  description = "Region to deploy the Droplet"
  type        = string
}

variable "size" {
  description = "Size of the Droplet"
  type        = string
}

variable "private" {
  description = "Path to your SSH private key"
  type        = string
}

variable "public" {
  description = "Path to your SSH public key"
  type        = string
}
