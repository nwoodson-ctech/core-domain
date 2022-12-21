from aws_cdk import (
    Stack,
    aws_events as events,
    aws_events_targets as target,
    Duration
)
from constructs import Construct


class CoreEventBridgeStack(Stack):

    def __init__(self, scope: Construct, id: str, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)

        ### Create Core Event Bus ###
        core_event_bus = events.EventBus(self,
                                         id='core-event-bus',
                                         event_bus_name='CoreEventBus'
                                         )

        ### Create Core Event Bus Archive ###
        core_event_bus.archive('CoreEventBusArchive',
                               archive_name='CoreEventBusArchive',
                               description='CoreEventBus Archive',
                               event_pattern=events.EventPattern(
                                   account=[Stack.of(self).account]
                               ),
                               retention=Duration.days(1)
                               )

        add_player_rule = events.Rule(self, "add-player-rule",
                                      event_bus=core_event_bus,
                                      event_pattern=events.EventPattern(
                                          source=["ingest-api"],
                                          detail_type=["player"],
                                          detail={
                                              "eventName": ["AddPlayer"]
                                          }
                                      )
                                      )

        add_player_rule.add_target(target.EventBus(events.EventBus.from_event_bus_name(
            self, "add-player-event-bus", "PlayerEventBus")))

        save_player_rule = events.Rule(self, "save-player-rule",
                                      event_bus=core_event_bus,
                                      event_pattern=events.EventPattern(
                                          source=["ingest-api"],
                                          detail_type=["player"],
                                          detail={
                                              "eventName": ["SavePlayer"]
                                          }
                                      )
                                      )

        save_player_rule.add_target(target.EventBus(events.EventBus.from_event_bus_name(
            self, "save-player-event", "PlayerEventBus")))
