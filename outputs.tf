output "alb_dns_name" {
  value = aws_lb.alb.dns_name
}

output "ec2_private_ip" {
  value = aws_instance.app.private_ip
}
