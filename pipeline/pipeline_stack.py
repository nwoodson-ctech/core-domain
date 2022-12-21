from aws_cdk import (
    Stack,
    pipelines as pipelines,
    SecretValue
)
from constructs import Construct

from event_bridge.infrastructure.core_event_bridge_stage import CoreEventBridgeStage
from player.lambda_function.infrastructure.stream_add_player_stage import StreamAddPlayerStage


class PipelineStack(Stack):

    def __init__(self, scope: Construct, id: str, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)

        code_pipeline = pipelines.CodePipeline(
            self,
            'CoreDomain-Pipeline',
            docker_enabled_for_synth=True,
            synth=pipelines.ShellStep('Synth',
                                      input=pipelines.CodePipelineSource.git_hub(
                                          'nwoodson-ctech/core-domain',
                                          'main',
                                          authentication=SecretValue.secrets_manager(
                                              'exploration-token')
                                      ),
                                      env={'privileged': 'True'},
                                      commands=[
                                          "npm install -g aws-cdk",  # Installs the cdk cli on Codebuild
                                          # Instructs Codebuild to install required packages
                                          "pip3 install -r requirements.txt",
                                          "cdk synth"
                                      ]
                                      )
        )

        deploy_core_event_bridge = CoreEventBridgeStage(
            self, "DeployCoreEventBridge")
        code_pipeline.add_stage(
            deploy_core_event_bridge)

        deploy_stream_add_player = StreamAddPlayerStage(
            self, "DeployStreamAddPlayer")
        code_pipeline.add_stage(
            deploy_stream_add_player)
