import aws_cdk as core
import aws_cdk.assertions as assertions

from lambda_with_static_ip.lambda_with_static_ip_stack import LambdaWithStaticIpStack

# example tests. To run these tests, uncomment this file along with the example
# resource in lambda_with_static_ip/lambda_with_static_ip_stack.py
def test_sqs_queue_created():
    app = core.App()
    stack = LambdaWithStaticIpStack(app, "lambda-with-static-ip")
    template = assertions.Template.from_stack(stack)

#     template.has_resource_properties("AWS::SQS::Queue", {
#         "VisibilityTimeout": 300
#     })
