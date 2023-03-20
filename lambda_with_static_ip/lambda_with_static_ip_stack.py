from aws_cdk import (
    # Duration,
    Stack,
    aws_ec2 as ec2,
    CfnOutput,
    aws_lambda
)
from constructs import Construct

class LambdaWithStaticIpStack(Stack):

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        requests_layer = aws_lambda.LayerVersion.from_layer_version_arn(
            scope=self,
            id='requests_layer',
            layer_version_arn='arn:aws:lambda:eu-central-1:770693421928:layer:Klayers-p39-requests:8'
        )

        private_subnet_config = ec2.SubnetConfiguration(
            name='private-subnet-1',
            subnet_type= ec2.SubnetType.PRIVATE_WITH_EGRESS,
            cidr_mask=24
        )

        public_subnet_config = ec2.SubnetConfiguration(
            name='public-subnet-1',
            subnet_type=ec2.SubnetType.PUBLIC,
            cidr_mask=24
        )

        vpc = ec2.Vpc(self, 'Vpc',
            vpc_name='vpc',
            nat_gateways=1,
            max_azs=1,
            subnet_configuration=[
                private_subnet_config,
                public_subnet_config
            ]   
        )

        function = aws_lambda.Function(
            scope=self,
            id="etl",
            runtime=aws_lambda.Runtime.PYTHON_3_9,
            handler="handler.main",
            code=aws_lambda.Code.from_asset("./lambda/src"),
            vpc=vpc,
            layers=[ requests_layer ]
        )

        vpcSecurityGroupOutputId = 'SgOutputId'
        vpcPrivateSubnetOutputId = 'VpcPvSubOutputId'

        private_subnets: ec2.SelectedSubnets = vpc.select_subnets(
            subnet_type=ec2.SubnetType.PRIVATE_WITH_NAT
        )
        privateSubnetId1 = private_subnets.subnet_ids[0]

        CfnOutput(
            scope=self,
            id=vpcSecurityGroupOutputId,
            value=vpc.vpc_default_security_group,
        )
        CfnOutput(
            scope=self,
            id=vpcPrivateSubnetOutputId,
            value=privateSubnetId1,
        )
