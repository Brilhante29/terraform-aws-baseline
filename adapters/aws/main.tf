resource "aws_vpc" "baseline" {
  cidr_block           = var.cidr_block
  enable_dns_hostnames = true
  enable_dns_support   = true

  tags = merge(var.tags, {
    Name = var.baseline_name
  })
}

resource "aws_internet_gateway" "baseline" {
  vpc_id = aws_vpc.baseline.id

  tags = merge(var.tags, {
    Name = "${var.baseline_name}-igw"
  })
}

resource "aws_subnet" "public" {
  for_each = toset(var.availability_zones)

  vpc_id                  = aws_vpc.baseline.id
  availability_zone       = each.key
  cidr_block              = cidrsubnet(var.cidr_block, 8, index(var.availability_zones, each.key))
  map_public_ip_on_launch = true

  tags = merge(var.tags, {
    Name = "${var.baseline_name}-${each.key}"
  })
}

resource "aws_route_table" "public" {
  vpc_id = aws_vpc.baseline.id

  route {
    cidr_block = "0.0.0.0/0"
    gateway_id = aws_internet_gateway.baseline.id
  }

  tags = merge(var.tags, {
    Name = "${var.baseline_name}-public"
  })
}

resource "aws_route_table_association" "public" {
  for_each = aws_subnet.public

  subnet_id      = each.value.id
  route_table_id = aws_route_table.public.id
}

resource "aws_security_group" "service" {
  name        = "${var.baseline_name}-service"
  description = "Egress-only security group for the baseline service."
  vpc_id      = aws_vpc.baseline.id

  egress {
    protocol    = "-1"
    from_port   = 0
    to_port     = 0
    cidr_blocks = ["0.0.0.0/0"]
  }

  tags = var.tags
}

resource "aws_ecs_cluster" "service" {
  name = "${var.baseline_name}-cluster"
  tags = var.tags
}

resource "aws_cloudwatch_log_group" "service" {
  name              = "/ecs/${var.baseline_name}"
  retention_in_days = var.log_retention_days
  tags              = var.tags
}

resource "aws_ecs_task_definition" "service" {
  family                   = var.baseline_name
  requires_compatibilities = ["FARGATE"]
  network_mode             = "awsvpc"
  cpu                      = "256"
  memory                   = "512"
  execution_role_arn       = var.execution_role_arn

  container_definitions = jsonencode([
    {
      name      = var.baseline_name
      image     = var.service_image
      essential = true
      cpu       = 256
      memory    = 512
      environment = [
        for name, value in var.service_environment : {
          name  = name
          value = value
        }
      ]
      logConfiguration = {
        logDriver = "awslogs"
        options = {
          awslogs-group         = aws_cloudwatch_log_group.service.name
          awslogs-region        = var.aws_region
          awslogs-stream-prefix = var.baseline_name
        }
      }
    }
  ])

  tags = var.tags
}

resource "aws_ecs_service" "service" {
  name            = var.baseline_name
  cluster         = aws_ecs_cluster.service.id
  task_definition = aws_ecs_task_definition.service.arn
  desired_count   = var.service_replicas
  launch_type     = "FARGATE"

  network_configuration {
    assign_public_ip = true
    subnets          = [for subnet in aws_subnet.public : subnet.id]
    security_groups  = [aws_security_group.service.id]
  }

  tags = var.tags
}
